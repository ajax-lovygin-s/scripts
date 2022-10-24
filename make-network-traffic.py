from pathlib import Path
from random import choice
from string import ascii_uppercase, digits

from pexpect import spawn, EOF


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


def generate_content_file(filename: Path) -> None:
    """Generate small file (~5Mb) with trash content."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    if filename.exists():
        print(f'file ({filename}) is already exist and will be truncated')

    file_size = 5*1024*1024
    generate_file(path=filename, size=file_size, line_length=120)
    print(f'file ({filename}) generated: size = {filename.stat().st_size}')


def send_file(source: Path, user: str, host: str, destination: Path, password: str) -> None:
    """Send <source> file to <host>/<destination> by using scp command."""
    command = f'scp {source} {user}@{host}:{destination}'
    print(command)

    command = f'/bin/bash -c "{command}"'
    with spawn(command) as task:
        task.expect(f"{user}@{host}'s password:")
        task.sendline(password)
        task.expect(EOF)


def main() -> None:
    source = Path(__file__).parent / '.cache' / 'to-device'
    generate_content_file(source)

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
