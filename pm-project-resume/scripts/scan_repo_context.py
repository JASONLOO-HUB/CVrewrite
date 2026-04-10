#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from pathlib import Path


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".agents",
    ".claude",
    ".codex",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    "vendor",
    "target",
    "__pycache__",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "tmp",
    "out",
    "skills",
    ".DS_Store",
}

DOC_EXTS = {".md", ".mdx", ".txt", ".rst"}
CODE_EXTS = {
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".go",
    ".rs",
    ".java",
    ".kt",
    ".swift",
    ".dart",
    ".vue",
    ".svelte",
    ".rb",
    ".php",
    ".cs",
    ".lua",
    ".wxml",
    ".wxss",
}

DOC_HINTS = {
    "prd": 10,
    "spec": 9,
    "design": 9,
    "requirement": 9,
    "roadmap": 8,
    "plan": 8,
    "architecture": 8,
    "doc": 5,
    "notes": 4,
}

EXTERNAL_CONTEXT_HINTS = {
    "jd",
    "resume",
    "cv",
    "简历",
}

MANIFEST_NAMES = {
    "package.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "package-lock.json",
    "pyproject.toml",
    "requirements.txt",
    "poetry.lock",
    "cargo.toml",
    "go.mod",
    "gemfile",
    "pubspec.yaml",
    "pom.xml",
    "build.gradle",
    "app.json",
    "game.json",
    "project.config.json",
    "tsconfig.json",
}

CODE_HINTS = {
    "pages": 7,
    "routes": 7,
    "screens": 7,
    "views": 6,
    "features": 6,
    "feature": 6,
    "engines": 7,
    "engine": 7,
    "core": 6,
    "domain": 6,
    "modules": 5,
    "store": 5,
    "services": 5,
    "service": 5,
    "components": 4,
    "scenes": 6,
    "models": 5,
    "config": 4,
}

ENTRY_NAMES = {
    "app",
    "main",
    "index",
    "game",
    "server",
    "client",
}


def normalize_excludes(repo: Path, raw_excludes: list[str]) -> list[Path]:
    excludes: list[Path] = []
    for raw in raw_excludes:
        candidate = Path(raw).expanduser()
        if not candidate.is_absolute():
            candidate = (repo / candidate).resolve()
        else:
            candidate = candidate.resolve()
        excludes.append(candidate)
    return excludes


def is_excluded(path: Path, excludes: list[Path]) -> bool:
    for exclude in excludes:
        if path == exclude or exclude in path.parents:
            return True
    return False


def should_skip(path: Path, excludes: list[Path]) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts) or is_excluded(path, excludes)


def walk_files(repo: Path, excludes: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in repo.rglob("*"):
        if path.is_file() and not should_skip(path, excludes):
            files.append(path)
    return files


def score_doc(rel: Path) -> int:
    score = 0
    name = rel.name.lower()
    rel_text = rel.as_posix().lower()

    if rel.suffix.lower() in DOC_EXTS:
        score += 4
    if "docs/" in rel_text or rel.parts[:1] == ("docs",):
        score += 3
    for hint, weight in DOC_HINTS.items():
        if hint in name or hint in rel_text:
            score += weight
    return score


def score_code(rel: Path) -> int:
    score = 0
    rel_text = rel.as_posix().lower()
    stem = rel.stem.lower()

    if rel.suffix.lower() in CODE_EXTS:
        score += 3
    if stem in ENTRY_NAMES:
        score += 6
    for part in rel.parts:
        key = part.lower()
        score += CODE_HINTS.get(key, 0)
    if rel.parent == Path("."):
        score += 2
    if rel_text.count("/") <= 2:
        score += 1
    return score


def top_items(items: list[tuple[int, Path]], limit: int) -> list[Path]:
    items = sorted(items, key=lambda item: (-item[0], item[1].as_posix()))
    return [path for _, path in items[:limit]]


def is_external_context(rel: Path) -> bool:
    rel_text = rel.as_posix().lower()
    name = rel.name.lower()
    return any(hint in rel_text or hint in name for hint in EXTERNAL_CONTEXT_HINTS)


def detect_code_roots(files: list[Path], repo: Path) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for path in files:
        rel = path.relative_to(repo)
        if rel.suffix.lower() not in CODE_EXTS:
            continue
        root = rel.parts[0] if rel.parts else "."
        counts[root] += 1
    return counts.most_common(10)


def detect_doc_roots(files: list[Path], repo: Path) -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    for path in files:
        rel = path.relative_to(repo)
        if rel.suffix.lower() not in DOC_EXTS:
            continue
        root = rel.parts[0] if rel.parts else "."
        counts[root] += 1
    return counts.most_common(10)


def classify(files: list[Path], repo: Path, limit: int) -> dict[str, list[Path] | list[tuple[str, int]]]:
    doc_candidates: list[tuple[int, Path]] = []
    external_context_candidates: list[tuple[int, Path]] = []
    manifest_candidates: list[Path] = []
    code_candidates: list[tuple[int, Path]] = []
    extension_counts: Counter[str] = Counter()

    for path in files:
        rel = path.relative_to(repo)
        extension_counts[rel.suffix.lower() or "[no_ext]"] += 1

        if rel.name.lower() in MANIFEST_NAMES:
            manifest_candidates.append(rel)

        doc_score = score_doc(rel)
        if doc_score > 0:
            if is_external_context(rel):
                external_context_candidates.append((doc_score, rel))
            else:
                doc_candidates.append((doc_score, rel))

        code_score = score_code(rel)
        if code_score > 0 and rel.suffix.lower() in CODE_EXTS:
            code_candidates.append((code_score, rel))

    return {
        "docs": top_items(doc_candidates, limit),
        "external_context": top_items(external_context_candidates, limit),
        "manifests": sorted(manifest_candidates)[:limit],
        "code": top_items(code_candidates, limit),
        "code_roots": detect_code_roots(files, repo),
        "doc_roots": detect_doc_roots(files, repo),
        "extensions": extension_counts.most_common(12),
    }


def print_section(title: str, lines: list[str]) -> None:
    print(f"## {title}")
    if not lines:
        print("- 无")
    else:
        for line in lines:
            print(f"- {line}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan a repository and produce a high-signal context index for PM resume writing."
    )
    parser.add_argument("repo", help="Repository root path")
    parser.add_argument("--limit", type=int, default=15, help="Max items per file section")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="File or directory to exclude from scanning; can be repeated.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists() or not repo.is_dir():
        raise SystemExit(f"Repository not found: {repo}")

    excludes = normalize_excludes(repo, args.exclude)
    files = walk_files(repo, excludes)
    data = classify(files, repo, args.limit)

    print(f"# 仓库上下文索引：{repo}")
    print()
    print(f"- 文件总数：{len(files)}")
    if excludes:
        print(f"- 已排除路径：{', '.join(str(path) for path in excludes)}")
    print(f"- 代码根目录候选：{', '.join(f'{name}({count})' for name, count in data['code_roots']) or '无'}")
    print(f"- 文档根目录候选：{', '.join(f'{name}({count})' for name, count in data['doc_roots']) or '无'}")
    print()

    print_section("优先阅读的文档 / 计划 / 设计材料", [path.as_posix() for path in data["docs"]])  # type: ignore[arg-type]
    print_section("仓库中发现的外部上下文文件", [path.as_posix() for path in data["external_context"]])  # type: ignore[arg-type]
    print_section("优先阅读的 manifest / 入口配置", [path.as_posix() for path in data["manifests"]])  # type: ignore[arg-type]
    print_section("优先阅读的代码文件", [path.as_posix() for path in data["code"]])  # type: ignore[arg-type]
    print_section(
        "文件类型分布（Top 12）",
        [f"{suffix}: {count}" for suffix, count in data["extensions"]],  # type: ignore[arg-type]
    )

    print("## 建议阅读顺序")
    print("- 先读文档 / 设计 / 计划类材料，提炼项目原始意图")
    print("- 再读 manifest 和入口文件，判断产品形态和主路径")
    print("- 再读核心代码目录，补足关键路径、系统抽象和业务闭环")
    print("- 最后再结合原简历和 JD，决定只包装哪 1-2 个岗位点")


if __name__ == "__main__":
    main()
