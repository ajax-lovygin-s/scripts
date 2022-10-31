from pathlib import Path
from random import choice
from string import ascii_uppercase, digits

from click import command, option
from pexpect import spawn, EOF

DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024


def generate_random_string(size: int = 1024, allowed_chars: str = ascii_uppercase + digits) -> str:
    return ''.join(choice(allowed_chars) for _ in range(size))


def generate_file(path: Path, size: int, line_length: int = 1024) -> None:
    with open(path, 'w') as file:
        lines_count, extra_line_size = divmod(size, line_length)
        for _ in range(lines_count):
            generated_line = generate_random_string(line_length) + "\n"
            file.write(generated_line)

        if extra_line_size:
            generated_line = generate_random_string(extra_line_size) + "\n"
            file.write(generated_line)


def generate_content_file(filename: Path, file_size: int = DEFAULT_CHUNK_SIZE) -> None:
    """Generate small file (~<file_size>) with trash content."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    if filename.exists():
        print(f'file ({filename}) is already exist and will be truncated')

    generate_file(path=filename, size=file_size, line_length=120)
    print(f'file ({filename}) generated: size = {filename.stat().st_size}')


def send_file(source: Path, user: str, host: str, destination: Path, password: str) -> None:
    """Send <source> file to <host>/<destination> by using scp command."""
    cmd_line = f'scp {source} {user}@{host}:{destination}'
    print(cmd_line)

    cmd_line = f'/bin/bash -c "{cmd_line}"'
    with spawn(cmd_line) as task:
        task.expect(f"{user}@{host}'s password:")
        task.sendline(password)
        task.expect(EOF)


@command()
@option("--chunk-size", default=DEFAULT_CHUNK_SIZE, help='network transaction size', show_default=True)
def main(chunk_size: int) -> None:
    source = Path(__file__).parent / '.cache' / 'to-device'
    generate_content_file(source, file_size=chunk_size)

    print('starting do network activity')
    try:
        while True:
            send_file(
                source=source,
                host='192.168.0.248', destination=Path('/tmp'),
                user='root', password='welcome-to-ajax'
            )
    except KeyboardInterrupt:
        print('stop network activity')


if __name__ == '__main__':
    main()
