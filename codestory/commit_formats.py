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
    description: str = Field(..., max_length=100)
    long_description: str = Field(default="", max_length=1000)


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

    formatted_commit = f"{emoji}{commit.type.value}{scope}: {commit.description}"

    if include_description and commit.long_description:
        formatted_commit += f"\n\n{commit.long_description[:description_length]}"

    return formatted_commit