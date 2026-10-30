"""Installed packages and user templates are read-only inputs to the renderer."""

import base64
import hashlib
import json
import re
from copy import deepcopy
from datetime import datetime
from html import unescape
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from iot_profile_builder.models import EngineeringProfile, FocusArea
from iot_profile_builder.output import renderer

ROOT = Path(__file__).resolve().parents[1]


class RendererTemplateTests(TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.profile = EngineeringProfile(
            username="fixture",
            generated_at=datetime(2026, 1, 1),
            total_repos_analyzed=0,
            iot_repos_count=0,
            narrative_summary="<script>untrusted metadata</script>",
        )

    def test_default_templates_render_from_read_only_package(self) -> None:
        package = self.root / "installed-package"
        package.mkdir()
        package.chmod(0o555)
        self.addCleanup(package.chmod, 0o755)
        with patch.object(renderer, "__file__", str(package / "renderer.py")):
            subject = renderer.ProfileRenderer()
            subject.render_markdown(self.profile, self.root / "profile.md")
            subject.render_html(self.profile, self.root / "profile.html")
        self.assertEqual(list(package.iterdir()), [])
        self.assertIn("fixture", (self.root / "profile.md").read_text())
        html = (self.root / "profile.html").read_text()
        self.assertIn("&lt;script&gt;untrusted metadata&lt;/script&gt;", html)
        self.assertNotIn("<script>untrusted metadata</script>", html)

    def test_markdown_focus_scores_do_not_depend_on_unpublished_images(self) -> None:
        self.profile.focus_areas = {FocusArea.ENERGY_MANAGEMENT: 0.75}
        output = self.root / "profile.md"
        renderer.ProfileRenderer().render_markdown(self.profile, output)
        markdown = output.read_text()
        self.assertIn("Energy Management: 75.0%", markdown)
        self.assertNotIn("![", markdown)
        self.assertEqual(list(self.root.iterdir()), [output])

    def test_missing_custom_directory_uses_defaults_without_creating_it(self) -> None:
        templates = self.root / "missing-templates"
        subject = renderer.ProfileRenderer(templates)
        subject.render_markdown(self.profile, self.root / "profile.md")
        subject.render_html(self.profile, self.root / "profile.html")
        self.assertFalse(templates.exists())
        self.assertIn("IoT Engineering Profile", (self.root / "profile.md").read_text())
        self.assertIn("fixture", (self.root / "profile.html").read_text())

    def test_custom_template_overrides_default_without_materializing_fallback(self) -> None:
        templates = self.root / "custom-templates"
        templates.mkdir()
        custom = templates / "profile.html.j2"
        text = "<main>{{ profile.username }}: {{ profile.narrative_summary }}</main>"
        custom.write_text(text)
        subject = renderer.ProfileRenderer(templates)
        subject.render_html(self.profile, self.root / "profile.html")
        subject.render_markdown(self.profile, self.root / "profile.md")
        self.assertEqual(custom.read_text(), text)
        self.assertEqual(list(templates.iterdir()), [custom])
        self.assertTrue((self.root / "profile.html").read_text().startswith("<main>fixture:"))
        self.assertIn("IoT Engineering Profile", (self.root / "profile.md").read_text())

    def test_existing_package_templates_keep_precedence(self) -> None:
        package = self.root / "installed-package"
        templates = package / "templates"
        templates.mkdir(parents=True)
        (templates / "profile.md.j2").write_text("Custom {{ profile.username }}")
        with patch.object(renderer, "__file__", str(package / "renderer.py")):
            subject = renderer.ProfileRenderer()
            subject.render_markdown(self.profile, self.root / "profile.md")
        self.assertEqual((self.root / "profile.md").read_text(), "Custom fixture")

    def test_custom_templates_keep_the_trusted_plotly_context(self) -> None:
        templates = self.root / "plotly-template"
        templates.mkdir()
        (templates / "profile.html.j2").write_text("<script>{{ plotly_js|safe }}</script>")
        with patch.object(renderer, "get_plotlyjs", return_value="/* trusted installed chart */"):
            renderer.ProfileRenderer(templates).render_html(self.profile, self.root / "chart.html")
        self.assertEqual(
            (self.root / "chart.html").read_text(), "<script>/* trusted installed chart */</script>"
        )

    def test_html_generation_emits_three_distinct_portable_pages(self) -> None:
        outputs = renderer.generate_profile_outputs(self.profile, self.root, formats=["html"])
        self.assertEqual(set(outputs), {"html", "repositories", "evidence"})
        for key, kind, name in (
            ("html", "overview", "fixture_profile.html"),
            ("repositories", "repositories", "repositories.html"),
            ("evidence", "evidence", "evidence.html"),
        ):
            self.assertEqual(outputs[key], self.root / name)
            html = outputs[key].read_text()
            self.assertIn(f'data-profile-page="{kind}"', html)
            self.assertIn('data-profile-version="2"', html)
            self.assertIn('data-profile-user="fixture"', html)
            self.assertIn('data-profile-generated="2026-01-01T00:00:00"', html)
            self.assertIn('href="fixture_profile.html"', html)

    def test_html_is_optional_and_unknown_page_kinds_fail_without_writes(self) -> None:
        outputs = renderer.generate_profile_outputs(self.profile, self.root, formats=["json"])
        self.assertEqual(set(outputs), {"json"})
        self.assertEqual({path.name for path in self.root.iterdir()}, {"fixture_profile.json"})
        with self.assertRaises(ValueError):
            renderer.ProfileRenderer().render_html(
                self.profile, self.root / "unknown.html", page_kind="unknown"
            )
        self.assertFalse((self.root / "unknown.html").exists())

    def test_csp_hash_matches_the_only_emitted_inline_script(self) -> None:
        output = self.root / "profile.html"
        renderer.ProfileRenderer().render_html(self.profile, output)
        html = output.read_text()
        scripts = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
        self.assertEqual(len(scripts), 1)
        digest = base64.b64encode(hashlib.sha256(scripts[0].encode()).digest()).decode()
        policy = re.search(r'http-equiv="Content-Security-Policy" content="([^"]+)"', html)
        self.assertIsNotNone(policy)
        assert policy is not None
        content = unescape(policy[1])
        self.assertIn(f"script-src 'sha256-{digest}'", content)
        self.assertNotIn("script-src 'unsafe-inline'", content)
        self.assertIn("connect-src 'self' https://api.github.com", content)

    def test_published_profile_roundtrip_preserves_all_json_and_metadata(self) -> None:
        payload = json.loads((ROOT / "docs/4alvit_profile.json").read_text())
        restored = renderer.profile_from_dict(payload)
        self.assertEqual(renderer._profile_to_dict(restored), payload)
        self.assertEqual(restored.generated_at.isoformat(), payload["generated_at"])
        restored.github_stats["generation"]["mode"] = "changed-copy"
        self.assertNotEqual(payload["github_stats"]["generation"]["mode"], "changed-copy")

    def test_snapshot_reconstruction_rejects_invalid_schema_and_numbers(self) -> None:
        original = renderer._profile_to_dict(self.profile)
        for key, value in (
            ("unknown", "would silently disappear"),
            ("generated_at", "not-a-date"),
            ("username", 42),
            ("total_repos_analyzed", True),
            ("iot_repos_count", -1),
            ("focus_areas", {"not-an-enum": 0.5}),
            ("focus_areas", {"energy_management": float("nan")}),
            ("complexity_distribution", {"expert": -1}),
            ("github_stats", {"not-finite": float("inf")}),
            ("skills", [{"name": "missing-fields"}]),
        ):
            with self.subTest(key=key, value=value):
                payload = deepcopy(original)
                payload[key] = value
                with self.assertRaises(ValueError):
                    renderer.profile_from_dict(payload)
        del original["generated_at"]
        with self.assertRaises(ValueError):
            renderer.profile_from_dict(original)

    def test_snapshot_reconstruction_validates_nested_fields(self) -> None:
        original = json.loads((ROOT / "docs/4alvit_profile.json").read_text())
        for collection, key, value in (
            ("top_repositories", "complexity", "unknown"),
            ("top_repositories", "is_fork", 1),
            ("top_repositories", "iot_score", 1.1),
            ("top_repositories", "updated_at", "not-a-date"),
            ("skills", "proficiency", 11),
            ("skills", "confidence", -1),
        ):
            with self.subTest(collection=collection, key=key):
                payload = deepcopy(original)
                payload[collection][0][key] = value
                with self.assertRaises(ValueError):
                    renderer.profile_from_dict(payload)
