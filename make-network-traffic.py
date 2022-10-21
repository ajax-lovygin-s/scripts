from pathlib import Path

from pexpect import spawn, EOF


def generate_file(filename: Path) -> None:
    filename.parent.mkdir(parents=True, exist_ok=True)
    if filename.exists():
        print(f"file is already exist and will be truncated")

    with open(filename, "w") as file:
        file.write('test')


def send_file(source: Path, user: str, host: str, destination: Path, password: str) -> None:
    """Send <source> file to <host>/<destination> by using scp command."""
    command = f'scp {source} {user}@{host}:{destination}'
    print(command)

    command = f'/bin/bash -c "{command}"'
    with spawn(command) as task:
        task.expect(f'{user}@{host} password:')
        task.sendline(password)
        task.expect(EOF)


def main() -> None:
    source = Path(__file__).parent / 'cache' / 'to-device'
    generate_file(source)

    print('starting do network activity')
    try:
        while True:
            send_file(
                source=source,
                destination=Path('/tmp'),
                user='root',
                password='welcome-to-ajax',
                host='192.168.0.248'
            )
    except KeyboardInterrupt:
        print('stop network activity')


if __name__ == '__main__':
    main()
