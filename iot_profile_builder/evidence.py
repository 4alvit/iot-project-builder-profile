"""Bounded, public-metadata-only checkpoints for retrying profile generation.

Checkpoints contain analyzer summaries, never source files, component configuration,
credentials or arbitrary analyzer dictionaries. They are evidence, not publications.
"""

from __future__ import annotations

import json
import os
import stat
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError

from .models import (
    ComplexityLevel,
    DBusAnalysis,
    DBusInterface,
    ESPHomeAnalysis,
    ESPHomeComponent,
    FocusArea,
    RepositoryMetrics,
    ScanConfig,
)

MAX_BYTES = 8 * 1024 * 1024
MAX_AGE = timedelta(hours=24)


class EvidenceError(ValueError):
    """A checkpoint cannot safely serve as this run's evidence."""


class _Record(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)


class _Repository(_Record):
    name: str = Field(min_length=1, max_length=100)
    full_name: str = Field(pattern=r"^[A-Za-z0-9-]+/[A-Za-z0-9_.-]+$")
    description: str | None = Field(max_length=10000)
    stars: int = Field(ge=0)
    forks: int = Field(ge=0)
    language: str | None
    topics: list[str]
    is_fork: bool
    created_at: datetime
    updated_at: datetime
    size_kb: int = Field(ge=0)
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]
    iot_score: float = Field(ge=0, le=1)


class _Component(_Record):
    type: str
    platform: str | None
    name: str
    integrations: list[str]


class _ESPHome(_Record):
    file_path: str
    devices: list[str]
    components: list[_Component]
    custom_components: list[str]
    external_libs: list[str]
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]


class _Member(_Record):
    name: str
    type: str


class _Interface(_Record):
    name: str
    path: str
    methods: list[_Member]
    signals: list[_Member]
    properties: list[_Member]


class _DBus(_Record):
    service_name: str
    interfaces: list[_Interface]
    object_paths: list[str]
    complexity: ComplexityLevel
    focus_areas: list[FocusArea]


class _Options(_Record):
    max_repos: int = Field(gt=0)
    include_forks: bool
    min_iot_score: float = Field(ge=0, le=1)
    analyze_esphome: bool
    analyze_dbus: bool
    include_orgs: list[str]


class _Scope(_Record):
    max_repositories_per_owner: int = Field(gt=0)
    max_repositories_per_analyzer: int = Field(gt=0)
    max_files_per_repository_per_analyzer: int = Field(gt=0)
    max_esphome_matches_per_repository: int = Field(gt=0)
    max_dbus_matches_per_repository: int = Field(gt=0)


class _Stats(_Record):
    total_repos: int = Field(gt=0)
    iot_repos: int = Field(gt=0)
    errors: list[str] = Field(max_length=0)
    scanned_at: datetime
    analysis_scope: _Scope


class _Checkpoint(_Record):
    schema_version: Literal[1]
    mode: Literal["evidence_only"]
    source_visibility: Literal["public"]
    username: str = Field(pattern=r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
    captured_at: datetime
    scan_options: _Options
    github_stats: _Stats
    repositories: list[_Repository] = Field(min_length=1)
    esphome_analyses: list[_ESPHome]
    dbus_analyses: list[_DBus]


@dataclass
class EvidenceSnapshot:
    """Safe analyzer objects and original scan provenance for the generator."""

    repositories: list[RepositoryMetrics]
    esphome_analyses: list[ESPHomeAnalysis]
    dbus_analyses: list[DBusAnalysis]
    github_stats: dict[str, Any]
    captured_at: datetime


def _options(config: ScanConfig) -> dict[str, Any]:
    return {name: getattr(config, name) for name in _Options.model_fields}


def _iso(value: datetime) -> str:
    return (value.replace(tzinfo=UTC) if value.tzinfo is None else value).isoformat()


def _projection(
    config: ScanConfig,
    repositories: list[RepositoryMetrics],
    esphome: list[ESPHomeAnalysis],
    dbus: list[DBusAnalysis],
    stats: dict[str, Any],
) -> dict[str, Any]:
    """Select named fields; adding an analyzer attribute cannot expose it here."""
    return {
        "schema_version": 1,
        "mode": "evidence_only",
        "source_visibility": "public",
        "username": config.username,
        "captured_at": datetime.now(UTC).isoformat(),
        "scan_options": _options(config),
        "github_stats": {name: stats[name] for name in _Stats.model_fields},
        "repositories": [
            {
                **{name: getattr(repo, name) for name in _Repository.model_fields},
                "created_at": _iso(repo.created_at),
                "updated_at": _iso(repo.updated_at),
            }
            for repo in repositories
        ],
        "esphome_analyses": [
            {
                **{name: getattr(item, name) for name in _ESPHome.model_fields},
                "components": [
                    {name: getattr(component, name) for name in _Component.model_fields}
                    for component in item.components
                ],
            }
            for item in esphome
        ],
        "dbus_analyses": [
            {
                **{name: getattr(item, name) for name in _DBus.model_fields},
                "interfaces": [
                    {
                        "name": interface.name,
                        "path": interface.path,
                        **{
                            group: [
                                {name: member[name] for name in _Member.model_fields}
                                for member in getattr(interface, group)
                            ]
                            for group in ("methods", "signals", "properties")
                        },
                    }
                    for interface in item.interfaces
                ],
            }
            for item in dbus
        ],
    }


def _validate(data: bytes, config: ScanConfig) -> _Checkpoint:
    if not config.strict_scan:
        raise EvidenceError("Evidence checkpoints require --strict-scan")
    if len(data) > MAX_BYTES:
        raise EvidenceError("Evidence checkpoint exceeds the size limit")
    try:
        evidence = _Checkpoint.model_validate_json(data)
    except ValidationError:
        # ValidationError contains rejected input; never log it or raw evidence.
        raise EvidenceError("Invalid evidence checkpoint schema") from None
    if evidence.username != config.username or evidence.scan_options.model_dump() != _options(
        config
    ):
        raise EvidenceError("Evidence username or scan options do not match this run")
    scanned = evidence.github_stats.scanned_at
    captured = evidence.captured_at
    now = datetime.now(UTC)
    if (
        scanned.tzinfo is None
        or captured.tzinfo is None
        or not now - MAX_AGE <= scanned <= captured <= now + timedelta(minutes=5)
    ):
        raise EvidenceError("Evidence must be timezone-aware and no older than 24 hours")
    repos = evidence.repositories
    names = [repo.full_name.casefold() for repo in repos]
    owners = {owner.casefold() for owner in [config.username, *config.include_orgs]}
    if (
        len(set(names)) != len(names)
        or any(name.split("/", 1)[0] not in owners for name in names)
        or any(repo.name != repo.full_name.split("/", 1)[1] for repo in repos)
        or evidence.github_stats.iot_repos != len(repos)
        or evidence.github_stats.total_repos < len(repos)
        or evidence.github_stats.analysis_scope.max_repositories_per_owner != config.max_repos
        or (not config.include_forks and any(repo.is_fork for repo in repos))
        or (not config.analyze_esphome and evidence.esphome_analyses)
        or (not config.analyze_dbus and evidence.dbus_analyses)
    ):
        raise EvidenceError("Evidence repository counts or scan scope are inconsistent")
    if any(
        not any(item.file_path.startswith(f"{repo.full_name}/") for repo in repos)
        for item in evidence.esphome_analyses
    ):
        raise EvidenceError("ESPHome evidence must belong to a scanned repository")
    return evidence


def _snapshot(evidence: _Checkpoint) -> EvidenceSnapshot:
    stats = evidence.github_stats.model_dump(mode="json")
    # Match the scanner's ISO representation so the model sees the same context.
    stats["scanned_at"] = evidence.github_stats.scanned_at.isoformat()
    return EvidenceSnapshot(
        repositories=[RepositoryMetrics(**repo.model_dump()) for repo in evidence.repositories],
        esphome_analyses=[
            ESPHomeAnalysis(
                **item.model_dump(exclude={"components"}),
                components=[
                    ESPHomeComponent(**part.model_dump(), config={}) for part in item.components
                ],
            )
            for item in evidence.esphome_analyses
        ],
        dbus_analyses=[
            DBusAnalysis(
                **item.model_dump(exclude={"interfaces"}),
                interfaces=[DBusInterface(**part.model_dump()) for part in item.interfaces],
            )
            for item in evidence.dbus_analyses
        ],
        github_stats=stats,
        captured_at=evidence.captured_at,
    )


def write_evidence(
    path: Path,
    config: ScanConfig,
    repositories: list[RepositoryMetrics],
    esphome: list[ESPHomeAnalysis],
    dbus: list[DBusAnalysis],
    stats: dict[str, Any],
) -> EvidenceSnapshot:
    """Atomically save validated summaries before a model request can fail."""
    try:
        data = json.dumps(_projection(config, repositories, esphome, dbus, stats)).encode()
    except (KeyError, TypeError, ValueError):
        raise EvidenceError("Cannot create evidence from incomplete analyzer summaries") from None
    evidence = _validate(data, config)
    if path.is_symlink() or (path.exists() and not path.is_file()) or path.parent.is_symlink():
        raise EvidenceError("Evidence destination must be a regular file")
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as staged:
        temporary = Path(staged.name)
        # Persist the exact bytes checked against MAX_BYTES; pretty-printing
        # here could create a checkpoint that its own reader refuses.
        staged.write(data)
        staged.flush()
        os.fsync(staged.fileno())
    try:
        temporary.chmod(0o600)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)
    return _snapshot(evidence)


def load_evidence(path: Path, config: ScanConfig) -> EvidenceSnapshot:
    """Load only a recent, matching checkpoint; no network or source-code reads."""
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode):
            raise EvidenceError("Evidence source must be a regular file")
        flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_BINARY", 0)
        flags |= getattr(os, "O_NONBLOCK", 0)
        with os.fdopen(os.open(path, flags), "rb") as source:
            opened = os.fstat(source.fileno())
            if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (
                before.st_dev,
                before.st_ino,
            ):
                raise EvidenceError("Evidence source must be a regular file")
            data = source.read(MAX_BYTES + 1)
    except OSError:
        raise EvidenceError("Cannot read a regular evidence checkpoint") from None
    return _snapshot(_validate(data, config))
