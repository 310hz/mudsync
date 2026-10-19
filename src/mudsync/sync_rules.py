import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


DEFAULT_GLOBAL_EXCLUDES = [
    ".git/",
    "__pycache__/",
    ".venv/",
    "node_modules/",
    ".ipynb_checkpoints/",
    ".DS_Store",
    "*.pyc",
    "*.pyo",
    "msync.json",
]


@dataclass
class ProjectConfig:
    server: str
    remote_path: str
    excludes: list[str] = field(default_factory=list)
    data_dir: str | None = None
    data_includes: list[str] = field(default_factory=list)
    auto_excluded: list[str] = field(default_factory=list)


def _msync_json_path(project_root: Path) -> Path:
    return project_root / "msync.json"


def load_project_config(project_root: Path) -> Optional[ProjectConfig]:
    path = _msync_json_path(project_root)
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    data.setdefault("data_dir", None)
    data.setdefault("data_includes", [])
    data.setdefault("auto_excluded", [])
    return ProjectConfig(**data)


def save_project_config(project_root: Path, config: ProjectConfig) -> None:
    path = _msync_json_path(project_root)
    path.write_text(
        json.dumps(
            {
                "server": config.server,
                "remote_path": config.remote_path,
                "excludes": config.excludes,
                "data_dir": config.data_dir,
                "data_includes": config.data_includes,
                "auto_excluded": config.auto_excluded,
            },
            indent=2,
        )
        + "\n"
    )


def require_project_config(project_root: Path) -> ProjectConfig:
    config = load_project_config(project_root)
    if config is None:
        raise SystemExit("Error: msync.json not found. Run 'msync set' first.")
    return config


def anchor_rule(pattern: str) -> str:
    return "/" + pattern.lstrip("/")


def get_exclude_rules(config: ProjectConfig) -> list[str]:
    # Project rules are paths from the project root, but unanchored rsync patterns
    # match at any depth ("data/" would also exclude "src/pkg/data/").
    # Global excludes are meant to match at any depth, so they stay unanchored.
    rules = [anchor_rule(p) for p in [*config.excludes, *config.data_includes]]
    return [*rules, *DEFAULT_GLOBAL_EXCLUDES]
