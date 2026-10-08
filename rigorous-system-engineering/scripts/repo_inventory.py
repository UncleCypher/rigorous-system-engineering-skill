#!/usr/bin/env python3
"""Produce a bounded, deterministic inventory for an unfamiliar repository."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


INDICATORS = {
    "manifests": {
        "package.json", "pnpm-workspace.yaml", "pyproject.toml", "requirements.txt",
        "go.mod", "Cargo.toml", "pom.xml", "build.gradle", "build.gradle.kts",
        "Gemfile", "composer.json", "*.sln", "*.csproj",
    },
    "locks": {
        "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "uv.lock",
        "poetry.lock", "Pipfile.lock", "Cargo.lock", "go.sum", "Gemfile.lock",
    },
    "ci": {".github/workflows", ".gitlab-ci.yml", "azure-pipelines.yml", "Jenkinsfile"},
    "containers": {"Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"},
    "docs": {"README*", "CONTRIBUTING*", "ARCHITECTURE*", "docs"},
    "tests": {"test", "tests", "spec", "__tests__", "e2e"},
    "migrations": {"migrations", "migration", "alembic", "prisma", "db/migrate"},
    "operations": {"terraform", "infra", "deploy", "helm", "k8s", "kubernetes"},
}

IGNORED_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "vendor", ".venv", "venv",
    "dist", "build", "target", ".next", ".cache", "coverage", "__pycache__",
}

SOURCE_EXTENSIONS = {
    ".py": "Python", ".js": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust",
    ".java": "Java", ".kt": "Kotlin", ".cs": "C#", ".rb": "Ruby",
    ".php": "PHP", ".swift": "Swift", ".scala": "Scala", ".ex": "Elixir",
    ".exs": "Elixir", ".c": "C", ".h": "C/C++", ".cc": "C++", ".cpp": "C++",
}


def matches(relative: Path, pattern: str) -> bool:
    normalized = relative.as_posix()
    if "*" in pattern:
        return relative.match(pattern) or relative.name.startswith(pattern.rstrip("*"))
    return normalized == pattern or relative.name == pattern or normalized.startswith(pattern + "/")


def inventory(root: Path, max_files: int) -> dict[str, object]:
    categories: dict[str, list[str]] = {key: [] for key in INDICATORS}
    languages: dict[str, int] = {}
    scanned = 0
    truncated = False

    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        relative = path.relative_to(root)
        if any(part in IGNORED_DIRS for part in relative.parts):
            continue
        if path.is_dir():
            for category, patterns in INDICATORS.items():
                if any(matches(relative, pattern) for pattern in patterns):
                    categories[category].append(relative.as_posix() + "/")
            continue
        scanned += 1
        if scanned > max_files:
            truncated = True
            break
        language = SOURCE_EXTENSIONS.get(path.suffix.lower())
        if language:
            languages[language] = languages.get(language, 0) + 1
        for category, patterns in INDICATORS.items():
            if any(matches(relative, pattern) for pattern in patterns):
                categories[category].append(relative.as_posix())

    return {
        "root": str(root),
        "files_scanned": min(scanned, max_files),
        "truncated": truncated,
        "language_file_counts": dict(sorted(languages.items(), key=lambda item: (-item[1], item[0]))),
        "indicators": {key: sorted(set(values))[:100] for key, values in categories.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", default=".", help="repository root (default: current directory)")
    parser.add_argument("--max-files", type=int, default=20000, help="maximum files to inspect")
    args = parser.parse_args()
    root = Path(args.repository).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    if args.max_files < 1:
        parser.error("--max-files must be positive")
    print(json.dumps(inventory(root, args.max_files), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
