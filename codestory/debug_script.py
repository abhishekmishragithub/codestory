import sys
import os

# adding the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codestory.llm_utils import generate_commit_message
from codestory.git_utils import get_git_diff
from codestory.config import config


def main():
    print("Starting debug script...")
    diff = get_git_diff('.')
    print(f"Git diff (first 100 characters): {diff[:100]}...")

    if not diff:
        print("No changes detected in the repository.")
        return

    # generating commit messages with different models
    models = [
        "groq/llama3-8b-8192",
        "ollama/llama3",
        "openai/gpt-3.5-turbo"  # make sure you have an OpenAI API key set up for this
    ]

    for model in models:
        print(f"\nTrying model: {model}")
        try:
            commit_message = generate_commit_message(
                diff,
                model,
                use_emoji=False,
                include_description=True,
                description_length=100,
                debug=True
            )
            print(f"Generated commit message: {commit_message}")
        except Exception as e:
            print(f"Error with {model}: {str(e)}")


if __name__ == "__main__":
    main()