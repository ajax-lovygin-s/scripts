"""Update recursively all repos."""
from pathlib import Path
from subprocess import Popen, PIPE
from typing import List, Tuple

from click import command, option


def gather_repos(root_dir: Path) -> Tuple[Path, ...]:
    return tuple(folder.parent for folder in root_dir.glob(r'*/.git'))


def update_repo(repo: Path) -> List[str]:
    process = Popen(['git', '-C', str(repo), 'pull'], stdout=PIPE)
    stdout, _ = process.communicate()
    output = stdout.decode("utf-8").strip().split("\n")

    process = Popen(['git', '-C', str(repo), 'submodule', 'update', '--init', '--recursive'], stdout=PIPE)
    stdout, _ = process.communicate()
    output += stdout.decode("utf-8").strip().split('\n')

    return output


def default_repos_dir() -> Path:
    return Path.home() / 'work' / 'projects'


@command()
@option('--root-dir', type=Path, default=default_repos_dir(), help='repos root dir', show_default=True)
def main(root_dir: Path) -> None:
    repos = gather_repos(root_dir)
    for repo in repos:
        update_repo(repo)
        print(f"{repo.relative_to(root_dir)} was synced")
        print()

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
