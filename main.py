import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")
args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

CATEGORIES = {
    "Audio": [".mp3"],
    "Video": [".mp4"],
    "Fotos": [".jpg"],
    "Docs": [".rtf", ".txt", ".bmp", ".pdf"],
    "Archives": [".zip", ".tar"]
}

def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            grabs_folder(el)

def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix.lower()
            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    dest_folder = output / category
                    try:
                        dest_folder.mkdir(exist_ok=True, parents=True)
                        copyfile(el, dest_folder / el.name)
                    except OSError as err:
                        logging.error(err)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    
    grabs_folder(source)

    threads = []
    for folder in [source] + list(output / category for category in CATEGORIES.keys()):
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"Можна видалять {source}")

