"""IoT Project Builder Profile - Main CLI entry point."""

from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalysis, DBusAnalyzer
from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalysis, ESPHomeAnalyzer
from iot_profile_builder.generator.profile_generator import (
    ProfileGenerator,
    generate_heuristic_profile,
)
from iot_profile_builder.models import RepositoryMetrics, ScanConfig
from iot_profile_builder.output.renderer import generate_profile_outputs
from iot_profile_builder.scanner.github_scanner import GitHubScanner, ScanResult

console = Console()
logger = logging.getLogger(__name__)


class IoTProfileBuilder:
    """Main orchestrator for IoT developer profile generation."""

    def __init__(self, config: ScanConfig):
        self.config = config
        self.scanner = GitHubScanner(config)
        self.esphome_analyzer = ESPHomeAnalyzer()
        self.dbus_analyzer = DBusAnalyzer()
        self.generator = ProfileGenerator(config)

    async def run(self, output_dir: Path, use_llm: bool = True) -> Path:
        """Run the complete profile generation pipeline."""
        console.print(
            Panel.fit(
                f"IoT Profile Builder for [bold cyan]{self.config.username}[/bold cyan]",
                title="Starting",
                border_style="blue",
            )
        )

        # Step 1: Scan GitHub repositories
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            scan_task = progress.add_task("Scanning GitHub repositories...", total=None)
            scan_result = await self.scanner.scan()
            progress.update(
                scan_task,
                completed=True,
                description=(
                    f"Scanned {scan_result.total_scanned} repos, "
                    f"found {scan_result.iot_repos} IoT-related"
                ),
            )

        _print_scan_summary(scan_result)

        # Step 2: Analyze ESPHome configs
        esphome_analyses = []
        if self.config.analyze_esphome:
            esphome_analyses = await self._analyze_esphome(scan_result.repositories)
            console.print(
                f"[green]✓[/green] Analyzed {len(esphome_analyses)} ESPHome configurations"
            )

        # Step 3: Analyze D-Bus services
        dbus_analyses = []
        if self.config.analyze_dbus:
            dbus_analyses = await self._analyze_dbus(scan_result.repositories)
            console.print(f"[green]✓[/green] Analyzed {len(dbus_analyses)} D-Bus services")

        # Step 4: Get GitHub stats
        github_stats = {
            "total_repos": scan_result.total_scanned,
            "iot_repos": scan_result.iot_repos,
            "errors": scan_result.errors,
            "scanned_at": datetime.now().isoformat(),
        }

        # Step 5: Generate profile
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            gen_task = progress.add_task("Generating engineering profile...", total=None)

            if use_llm:
                profile = self.generator.generate(
                    scan_result.repositories,
                    esphome_analyses,
                    dbus_analyses,
                    github_stats,
                )
            else:
                profile = generate_heuristic_profile(
                    scan_result.repositories,
                    esphome_analyses,
                    dbus_analyses,
                    github_stats,
                    self.config.username,
                )

            progress.update(gen_task, completed=True, description="Profile generated")

        # Step 6: Render outputs
        console.print("[blue]Rendering outputs...[/blue]")
        formats = ["markdown", "html", "json", "charts"]
        output_paths = generate_profile_outputs(profile, output_dir, formats)

        _print_output_summary(output_paths)

        return output_dir / f"{self.config.username}_profile.md"

    @staticmethod
    def _repo_ref(repo: RepositoryMetrics) -> str:
        """Prefer owner/name so org repos resolve correctly."""
        return repo.full_name or repo.name

    @staticmethod
    def _prioritize_repos(
        repos: list[RepositoryMetrics], needles: tuple[str, ...]
    ) -> list[RepositoryMetrics]:
        """Prefer name/topic matches, then IoT score — do not drop relevant repos via [:10]."""

        def rank(r: RepositoryMetrics) -> tuple[int, float]:
            blob = " ".join([r.name, r.full_name or "", *(r.topics or [])]).lower()
            matched = 1 if any(n in blob for n in needles) else 0
            return (matched, r.iot_score)

        return sorted(repos, key=rank, reverse=True)

    async def _analyze_esphome(self, repos: list[RepositoryMetrics]) -> list[ESPHomeAnalysis]:
        """Analyze ESPHome configurations in repositories (recursive file discovery)."""
        analyses: list[ESPHomeAnalysis] = []
        candidates = self._prioritize_repos(repos, ("esphome", "esp32", "esp8266", "ble"))

        for repo in candidates[:25]:
            ref = self._repo_ref(repo)
            try:
                yaml_files = await self.scanner.list_repo_files(
                    ref, suffixes=(".yaml", ".yml"), max_files=80
                )
                # Prefer likely ESPHome configs over CI/pre-commit yaml
                yaml_files = sorted(
                    yaml_files,
                    key=lambda c: (
                        0
                        if any(
                            p in c["path"].lower()
                            for p in ("pattern", "esphome", "esp32", "sensor", "device")
                        )
                        else 1,
                        0 if "/.github/" not in c["path"] else 1,
                    ),
                )
                per_repo = 0
                for yaml_file in yaml_files:
                    if per_repo >= 15:
                        break
                    if yaml_file.get("type") != "file":
                        continue
                    if "/.github/" in yaml_file["path"] or yaml_file["path"].startswith(".github/"):
                        continue
                    if "secrets.example" in yaml_file["path"]:
                        continue
                    content = await self.scanner.get_file_content(ref, yaml_file["path"])
                    if not content:
                        continue
                    lower = content.lower()
                    is_esphome = "esphome:" in lower or (
                        ("esp32:" in lower or "esp8266:" in lower or "rp2040:" in lower)
                        and ("sensor:" in lower or "mqtt:" in lower or "api:" in lower)
                    )
                    if not is_esphome:
                        continue
                    analysis = self.esphome_analyzer.analyze_content(
                        content,
                        f"{ref}/{yaml_file['path']}",
                    )
                    # Keep clearly matching configs even if component parse is sparse
                    if analysis.components or analysis.devices or is_esphome:
                        if not analysis.devices and ("esp32" in lower or "esp8266" in lower):
                            analysis.devices = [
                                d for d in ("esp32", "esp8266", "rp2040") if f"{d}:" in lower
                            ] or analysis.devices
                        analyses.append(analysis)
                        per_repo += 1
            except Exception as e:
                logger.warning(f"Failed to analyze ESPHome in {ref}: {e}")

        return analyses

    async def _analyze_dbus(self, repos: list[RepositoryMetrics]) -> list[DBusAnalysis]:
        """Analyze D-Bus services in repositories (recursive; includes .py.j2 templates)."""
        analyses: list[DBusAnalysis] = []
        candidates = self._prioritize_repos(repos, ("dbus", "vedbus", "victron", "venus"))

        for repo in candidates[:25]:
            ref = self._repo_ref(repo)
            try:
                py_files = await self.scanner.list_repo_files(ref, suffixes=(".py",), max_files=80)
                py_files = sorted(
                    py_files,
                    key=lambda c: (
                        0
                        if any(
                            n in c["path"].lower() for n in ("dbus", "service", "vedbus", "bridge")
                        )
                        else 1,
                        0 if "/test" not in c["path"].lower() else 1,
                    ),
                )
                per_repo = 0
                for py_file in py_files:
                    if per_repo >= 10:
                        break
                    if py_file.get("type") != "file":
                        continue
                    path_l = py_file["path"].lower()
                    if "/tests/" in path_l or path_l.startswith("tests/"):
                        continue
                    content = await self.scanner.get_file_content(ref, py_file["path"])
                    if not content:
                        continue
                    dbus_keywords = [
                        "dbus",
                        "pydbus",
                        "gi.repository",
                        "com.victronenergy",
                        "vedbus",
                        "vedbusservice",
                    ]
                    if not any(kw in content.lower() for kw in dbus_keywords):
                        continue
                    analysis = self.dbus_analyzer.analyze_content(
                        content, f"{ref}/{py_file['path']}"
                    )
                    has_signal = any(
                        i.methods or i.signals or i.properties for i in analysis.interfaces
                    )
                    if analysis.object_paths or has_signal:
                        analyses.append(analysis)
                        per_repo += 1
            except Exception as e:
                logger.warning(f"Failed to analyze D-Bus in {ref}: {e}")

        return analyses


def _print_scan_summary(result: ScanResult) -> None:
    """Print scan summary table."""
    table = Table(title="Scan Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Total Scanned", str(result.total_scanned))
    table.add_row("IoT Repositories", str(result.iot_repos))
    table.add_row("Errors", str(len(result.errors)))

    console.print(table)

    if result.repositories:
        repo_table = Table(title="Top IoT Repositories")
        repo_table.add_column("Repository", style="cyan")
        repo_table.add_column("Language", style="yellow")
        repo_table.add_column("Stars", justify="right")
        repo_table.add_column("IoT Score", justify="right")
        repo_table.add_column("Complexity")

        for repo in sorted(result.repositories, key=lambda r: r.iot_score, reverse=True)[:10]:
            repo_table.add_row(
                repo.name,
                repo.language or "N/A",
                str(repo.stars),
                f"{repo.iot_score:.2f}",
                repo.complexity.value,
            )
        console.print(repo_table)


def _print_output_summary(paths: dict[str, Path]) -> None:
    """Print output file summary."""
    table = Table(title="Generated Outputs")
    table.add_column("Format", style="cyan")
    table.add_column("Path", style="green")

    for fmt, path in paths.items():
        table.add_row(fmt, str(path))

    console.print(table)


async def main(
    username: str,
    token: str | None = None,
    output_dir: Path = Path("."),
    max_repos: int = 100,
    use_llm: bool = True,
    model: str | None = None,
    include_orgs: list[str] | None = None,
) -> int:
    """Main entry point."""
    config_kwargs: dict[str, Any] = {
        "username": username,
        "token": token,
        "max_repos": max_repos,
        "include_orgs": (
            include_orgs
            if include_orgs is not None
            else ["victron-venus", "ha-homelab", "open-ott-play"]
        ),
    }
    if model:
        config_kwargs["llm_model"] = model

    config = ScanConfig(**config_kwargs)

    builder = IoTProfileBuilder(config)
    output_path = await builder.run(output_dir, use_llm)

    console.print(
        Panel.fit(
            f"Profile generated: [bold green]{output_path}[/bold green]",
            title="Complete",
            border_style="green",
        )
    )

    return 0


def cli() -> int:
    """Synchronous CLI wrapper."""
    import argparse

    parser = argparse.ArgumentParser(description="IoT Developer Profile Generator")
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--token", "-t", help="GitHub personal access token")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--max-repos", "-m", type=int, default=100, help="Max repositories to scan")
    parser.add_argument(
        "--no-llm", action="store_true", help="Disable LLM analysis (heuristic only)"
    )
    parser.add_argument(
        "--model",
        "-M",
        default=None,
        help="LLM model id (default: claude-3-5-sonnet-20241022; any id exposed by the gateway works)",
    )
    parser.add_argument(
        "--orgs",
        default="",
        help="Comma-separated GitHub orgs to include (default: victron-venus,ha-homelab,open-ott-play)",
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.WARNING)

    try:
        return asyncio.run(
            main(
                username=args.username,
                token=args.token,
                output_dir=Path(args.output),
                max_repos=args.max_repos,
                use_llm=not args.no_llm,
                model=args.model,
                include_orgs=[o.strip() for o in args.orgs.split(",") if o.strip()] or None,
            )
        )
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted[/red]")
        return 1
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        logger.exception("Fatal error")
        return 1


if __name__ == "__main__":
    sys.exit(cli())
