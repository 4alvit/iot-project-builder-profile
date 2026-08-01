# IoT Project Builder Profile

> Automated engineering profile generator for IoT developers based on GitHub activity

Analyzes a developer's GitHub repositories, ESPHome configurations, and D-Bus services to generate a comprehensive engineering profile with skill assessments, focus areas, and interactive visualizations.

![Profile Generation Pipeline](docs/pipeline.svg)

## Features

- **GitHub Scanner** - Identifies IoT-related repositories using keyword matching, language detection, and activity scoring
- **ESPHome Analyzer** - Parses YAML configurations to extract devices, components, integrations, and custom components
- **D-Bus Analyzer** - Extracts interfaces, methods, signals, and properties from Python D-Bus services
- **LLM-Generated Profile** - Uses Anthropic Claude to create evidence-based skill assessments and narrative summaries
- **Multi-Format Output** - Markdown, HTML (with embedded Plotly charts), JSON, and static chart images
- **GitHub Action** - Automated weekly profile updates

## Architecture

```mermaid
graph TD
    A[GitHub API] --> B[Repository Scanner]
    B --> C{IoT Score ≥ 0.3?}
    C -->|Yes| D[Collect Metrics]
    C -->|No| E[Skip]
    D --> F[ESPHome Analyzer]
    D --> G[D-Bus Analyzer]
    F --> H[Profile Generator]
    G --> H
    H --> I{LLM Available?}
    I -->|Yes| J[LLM Analysis]
    I -->|No| K[Heuristic Analysis]
    J --> L[Render Outputs]
    K --> L
    L --> M[Markdown]
    L --> N[HTML + Charts]
    L --> O[JSON]
    L --> P[Chart Images]
```

## Quick Start

```bash
# Install with pipx (recommended)
pipx install git+https://github.com/4alvit/iot-project-builder-profile.git

# Or install in development mode
git clone https://github.com/4alvit/iot-project-builder-profile.git
cd iot-project-builder-profile
pip install -e ".[dev]"

# Generate profile (with LLM)
iot-profile-builder 4alvit --token $GITHUB_TOKEN --output ./profile

# Generate profile (heuristic only, no API key needed)
iot-profile-builder 4alvit --no-llm --output ./profile
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token (public_repo scope) | Yes |
| `ANTHROPIC_API_KEY` | Anthropic API key for LLM analysis | No (falls back to heuristic) |

### CLI Options

```bash
iot-profile-builder USERNAME [OPTIONS]

Options:
  -t, --token TEXT       GitHub personal access token
  -o, --output PATH      Output directory (default: .)
  -m, --max-repos INT    Max repositories to scan (default: 100)
  --no-llm               Disable LLM analysis (heuristic only)
  -h, --help             Show help message
```

## Output Formats

| Format | Description | File |
|--------|-------------|------|
| Markdown | Human-readable profile with tables | `username_profile.md` |
| HTML | Interactive dashboard with Plotly charts | `username_profile.html` |
| JSON | Machine-readable structured data | `username_profile.json` |
| Charts | Static PNG charts (radar, pie, bar) | `charts/*.png` |

## Sample Output

### Focus Areas Radar Chart
![Focus Areas](docs/focus-radar.png)

### Complexity Distribution
![Complexity](docs/complexity-pie.png)

### Skills Assessment
![Skills](docs/skills-bar.png)

## GitHub Action

The included workflow (`.github/workflows/update-profile.yml`) runs weekly to keep your profile current.

### Setup

1. Add `ANTHROPIC_API_KEY` to repository secrets (optional)
2. Enable GitHub Actions on your fork
3. Trigger manually via "Actions" tab or wait for Monday 6 AM UTC run

### Customization

```yaml
# In workflow_dispatch inputs
username: "your-github-username"  # Target user to analyze
use-llm: true                     # Enable/disable LLM analysis
```

## Project Structure

```
iot-project-builder-profile/
├── .github/workflows/     # GitHub Actions
├── src/
│   ├── cli.py             # Main CLI entry point
│   ├── models.py          # Core data models (Pydantic-free)
│   ├── scanner/
│   │   └── github_scanner.py  # GitHub API scanner
│   ├── analyzers/
│   │   ├── esphome_analyzer.py  # ESPHome YAML parser
│   │   └── dbus_analyzer.py     # D-Bus service analyzer
│   ├── generator/
│   │   └── profile_generator.py # LLM + heuristic profile gen
│   └── output/
│       └── renderer.py    # Markdown/HTML/JSON/Charts
├── tests/                 # Pytest test suite
├── pyproject.toml         # Project config
└── README.md              # This file
```

## Data Models

```mermaid
classDiagram
    class EngineeringProfile {
        +username: str
        +skills: List[SkillAssessment]
        +focus_areas: Dict[FocusArea, float]
        +complexity_distribution: Dict[ComplexityLevel, int]
        +top_repositories: List[RepositoryMetrics]
        +esphome_analyses: List[ESPHomeAnalysis]
        +dbus_analyses: List[DBusAnalysis]
        +narrative_summary: str
        +key_strengths: List[str]
        +growth_areas: List[str]
    }
    class SkillAssessment {
        +name: str
        +category: str
        +proficiency: int
        +evidence: List[str]
        +confidence: float
    }
    class RepositoryMetrics {
        +name: str
        +stars: int
        +language: str
        +iot_score: float
        +complexity: ComplexityLevel
        +focus_areas: List[FocusArea]
    }
    class ESPHomeAnalysis {
        +devices: List[str]
        +components: List[ESPHomeComponent]
        +custom_components: List[str]
        +complexity: ComplexityLevel
    }
    class DBusAnalysis {
        +service_name: str
        +interfaces: List[DBusInterface]
        +complexity: ComplexityLevel
    }
    EngineeringProfile "1" *-- "*" SkillAssessment
    EngineeringProfile "1" *-- "*" RepositoryMetrics
    EngineeringProfile "1" *-- "*" ESPHomeAnalysis
    EngineeringProfile "1" *-- "*" DBusAnalysis
```

## Development

```bash
# Run tests
pytest -v --cov=src

# Type checking
mypy src/

# Linting
ruff check src/

# Format
ruff format src/
```

## Tech Stack

- **Python 3.11+**
- **GitHub API** via PyGithub
- **YAML Parsing** via PyYAML
- **Templating** via Jinja2
- **Charts** via Plotly
- **LLM** via Anthropic SDK (optional)
- **CLI** via Rich

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [esphome](https://github.com/esphome/esphome) - ESPHome firmware framework
- [dbus-python](https://github.com/freedesktop/dbus-python) - Python D-Bus bindings
- [Victron Energy](https://www.victronenergy.com/) - Energy management systems