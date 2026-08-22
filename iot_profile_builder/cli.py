"""IoT Project Builder Profile - Main CLI entry point."""

from __future__ import annotations

import asyncio
import logging
import sys
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from iot_profile_builder.analyzers.dbus_analyzer import DBusAnalyzer
from iot_profile_builder.analyzers.esphome_analyzer import ESPHomeAnalyzer
from iot_profile_builder.generator.profile_generator import (
    ProfileGenerator,
    generate_heuristic_profile,
)
from iot_profile_builder.models import ScanConfig
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

    async def _analyze_esphome(self, repos) -> list:
        """Analyze ESPHome configurations in repositories."""
        analyses = []
        local_cache = Path.home() / ".cache" / "iot-profile-builder" / "repos"
        local_cache.mkdir(parents=True, exist_ok=True)

        for repo in repos[:10]:  # Limit to top 10 repos
            try:
                # Look for YAML files in the repo
                contents = await self.scanner.get_repo_contents(repo.name)
                yaml_files = [c for c in contents if c["path"].endswith((".yaml", ".yml"))]

                for yaml_file in yaml_files[:5]:  # Max 5 YAML files per repo
                    if yaml_file["type"] == "file":
                        content = await self.scanner.get_file_content(repo.name, yaml_file["path"])
                        is_esphome = content and (
                            "esphome" in content or "esp32" in content or "esp8266" in content
                        )
                        if is_esphome:
                            analysis = self.esphome_analyzer.analyze_content(
                                content, f"{repo.name}/{yaml_file['path']}"
                            )
                            if analysis.components:
                                analyses.append(analysis)
            except Exception as e:
                logger.warning(f"Failed to analyze ESPHome in {repo.name}: {e}")

        return analyses

    async def _analyze_dbus(self, repos) -> list:
        """Analyze D-Bus services in repositories."""
        analyses = []

        for repo in repos[:10]:  # Limit to top 10 repos
            try:
                contents = await self.scanner.get_repo_contents(repo.name)
                py_files = [c for c in contents if c["path"].endswith(".py")]

                for py_file in py_files[:5]:
                    if py_file["type"] == "file":
                        content = await self.scanner.get_file_content(repo.name, py_file["path"])
                        dbus_keywords = ["dbus", "pydbus", "gi.repository", "com.victronenergy"]
                        if content and any(kw in content.lower() for kw in dbus_keywords):
                            analysis = self.dbus_analyzer.analyze_content(
                                content, f"{repo.name}/{py_file['path']}"
                            )
                            if analysis.interfaces:
                                analyses.append(analysis)
            except Exception as e:
                logger.warning(f"Failed to analyze D-Bus in {repo.name}: {e}")

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


def _print_output_summary(paths: dict) -> None:
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
) -> int:
    """Main entry point."""
    config = ScanConfig(
        username=username,
        token=token,
        max_repos=max_repos,
    )

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


def cli():
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
