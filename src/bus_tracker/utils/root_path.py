import subprocess
from pathlib import Path


def get_git_root() -> Path:
    try:
        git_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            stdout=subprocess.PIPE,
            check=True,
            text=True,
        ).stdout.strip()

        return Path(git_root)
    except subprocess.CalledProcessError:
        raise RuntimeError("Not in a Git repository")


BASE_DIR = get_git_root()

DATABASE_PATH = BASE_DIR / "data" / "logs.db"
