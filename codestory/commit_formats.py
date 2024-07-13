from enum import Enum
from pydantic import BaseModel, Field


class CommitType(str, Enum):
    feat = "feat"
    fix = "fix"
    docs = "docs"
    style = "style"
    refactor = "refactor"
    perf = "perf"
    test = "test"
    build = "build"
    ci = "ci"
    chore = "chore"
    revert = "revert"


class ConventionalCommit(BaseModel):
    type: CommitType
    scope: str = Field(default="", max_length=50)
    description: str = Field(default="")


EMOJI_MAP = {
    "feat": "✨",
    "fix": "🐛",
    "docs": "📚",
    "style": "💎",
    "refactor": "📦",
    "perf": "🚀",
    "test": "🚨",
    "build": "🛠️",
    "ci": "⚙️",
    "chore": "♻️",
    "revert": "⏪"
}


def format_conventional_commit(commit: ConventionalCommit, use_emoji: bool = False, include_description: bool = True,
                               description_length: int = 100) -> str:
    emoji = EMOJI_MAP[commit.type.value] + " " if use_emoji else ""
    scope = f"({commit.scope})" if commit.scope else ""

    if include_description and commit.description:
        description = commit.description[:description_length] + "..." if len(
            commit.description) > description_length else commit.description
        return f"{emoji}{commit.type.value}{scope}: {description}"
    else:
        return f"{emoji}{commit.type.value}{scope}"