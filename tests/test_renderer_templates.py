"""Installed packages and user templates are read-only inputs to the renderer."""

from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import patch

from iot_profile_builder.models import EngineeringProfile
from iot_profile_builder.output import renderer


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
