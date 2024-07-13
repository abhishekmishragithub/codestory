import git
import logging

logger = logging.getLogger(__name__)


def get_git_diff(repo_path='.'):
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)

        # diff of staged changes
        staged_diff = repo.git.diff("--staged")

        # if no staged changes, get the diff of unstaged changes
        if not staged_diff:
            unstaged_diff = repo.git.diff()
            logger.debug(f"Unstaged diff found: {unstaged_diff[:100]}...")
            return unstaged_diff.strip()

        logger.debug(f"Staged diff found: {staged_diff[:100]}...")
        return staged_diff.strip()
    except git.InvalidGitRepositoryError:
        logger.error(f"Error: {repo_path} is not a valid git repository.")
        return None
    except git.GitCommandError as e:
        logger.error(f"Error executing git command: {e}")
        return None