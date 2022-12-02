from pathlib import Path
from click import command, argument


@command()
@argument('json-file', type=Path)
@argument('out-file', type=Path)
def main(json_file: Path, out_file: Path) -> None:
    with open(json_file, 'r', encoding='utf-8') as in_file, open(out_file, 'w', encoding='utf-8') as result_file:
        for line in in_file:
            line = line.strip()

            content = None
            if line.startswith('"rtsp.length'):
                _, _, content = line.partition(': ')
                content = content.strip('",')

            elif line.startswith('"rtsp.data'):
                _, _, payload = line.partition(': ')
                payload = payload.strip('",')
                content = '0x' + payload.replace(':', '\n0x')

            if content:
                result_file.write(content)
                result_file.write('\n')


if __name__ == '__main__':
    main()
