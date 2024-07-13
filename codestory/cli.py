import click
import logging
import sys
from .git_utils import get_git_diff
from .llm_utils import generate_commit_message
from .config import config

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format='%(message)s')
logger = logging.getLogger(__name__)

# set httpx logging to WARNING to suppress INFO messages --> for claude api calls
logging.getLogger("httpx").setLevel(logging.WARNING)


@click.group()
def main():
    pass


@main.command()
@click.option('--model', default=None,
              help="Name of the model to use (e.g., openai/gpt-3.5-turbo, gemini/gemini-pro, claude/claude-3-sonnet-20240320, groq/llama3-8b, ollama/llama2)")
@click.option('--emoji/--no-emoji', default=None, help="Use emoji in commit message")
@click.option('--repo-path', default='.', help="Path to the Git repository")
@click.option('--include-description/--exclude-description', default=None, help="Include commit description")
@click.option('--description-length', default=None, type=int, help="Maximum length of commit description")
@click.option('--verbose', is_flag=True, help="Show verbose output")
@click.option('--debug', is_flag=True, help="Show debug information")
def generate(model, emoji, repo_path, include_description, description_length, verbose, debug):
    """Generate a commit message based on the current git diff."""
    if verbose or debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    logger.debug("Starting commit message generation...")

    diff = get_git_diff(repo_path)
    if diff is None:
        click.echo("Error: Not a valid git repository or no changes detected.", err=True)
        return
    elif diff == "":
        click.echo(
            "No changes detected in the repository. Make some changes and stage them before generating a commit message.",
            err=True)
        return

    logger.debug(f"Generated diff (first 100 chars): {diff[:100]}...")

    model_name = model or config.DEFAULT_MODEL
    use_emoji = emoji if emoji is not None else config.USE_EMOJI
    include_desc = include_description if include_description is not None else config.INCLUDE_DESCRIPTION
    desc_length = description_length or config.DESCRIPTION_LENGTH

    logger.debug(
        f"Configuration: model={model_name}, emoji={use_emoji}, include_description={include_desc}, description_length={desc_length}")

    try:
        commit_message = generate_commit_message(
            diff,
            model_name,
            use_emoji=use_emoji,
            include_description=include_desc,
            description_length=desc_length,
            debug=debug
        )
        click.echo(commit_message)
    except Exception as e:
        click.echo(f"Error generating commit message: {str(e)}", err=True)
        if debug:
            logger.exception("Detailed error information:")


if __name__ == "__main__":
    main()