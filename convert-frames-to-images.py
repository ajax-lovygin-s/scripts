from pathlib import Path

from subprocess import call


def main() -> None:
    images_dir = Path('data') / 'images'
    if images_dir.exists():
        for file in images_dir.iterdir():
            file.unlink()
    images_dir.mkdir(parents=True, exist_ok=True)

    frames_dir = Path('data') / 'frames'
    for frame_file in frames_dir.glob('*.raw'):
        image_file = images_dir / f'{frame_file.stem}.png'
        call(['ffmpeg', '-i', str(frame_file), str(image_file)])


if __name__ == '__main__':
    main()
