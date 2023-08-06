from functools import partial
from multiprocessing import Process
from subprocess import call
from tempfile import gettempdir
from pathlib import Path
from shutil import copyfile, copytree
from random import choice
from string import ascii_letters

from bets.utils import log


def get_temp_location(path: str) -> str:
    log.debug(f"getting temp location for: [{path}]")

    path = Path(path).absolute()
    log.debug(f"got absolute path: [{str(path)}]")

    tmp_name = "tmp_" + "".join([choice(ascii_letters) for _ in range(8)]) + "_" + path.name
    tmp_path = str(Path(gettempdir()).absolute().joinpath(tmp_name))
    log.debug(f"got temp location: [{tmp_path}]")

    return tmp_path


def delete(path: str):
    path = Path(path)

    if not path.exists():  # pragma: no cover
        raise FileNotFoundError(str(path))

    if path.is_file():
        log.debug(f"deleting file at: [{str(path)}]")
        path.unlink()
        return

    if path.is_dir():
        log.debug(f"deleting dir contents: [{str(path)}]")

        for child_path in path.iterdir():
            delete(str(child_path))

        log.debug(f"deleting dir at: [{str(path)}]")
        path.rmdir()


def copy(src_path: str, dst_path: str, exists_ok=False) -> str:
    log.debug(f"copying file or dir from [{src_path}] to [{dst_path}]")
    src_path = Path(src_path).absolute()
    if not src_path.exists():  # pragma: no cover
        raise FileNotFoundError(str(src_path))

    dst_path = Path(dst_path).absolute()

    if dst_path.exists():  # pragma: no cover
        if exists_ok:
            delete(str(dst_path))
        else:
            raise FileExistsError(str(dst_path))

    if src_path.is_file():
        log.debug(f"copying file from: [{str(src_path)}] to: [{str(dst_path)}]")
        return copyfile(str(src_path), str(dst_path))

    if src_path.is_dir():  # pragma: no cover
        log.debug(f"copying dir from: [{str(src_path)}] to: [{str(dst_path)}]")
        return copytree(str(src_path), str(dst_path))


def copy_to_temp_location(path: str) -> str:
    src_path = Path(path).absolute()
    dst_path = Path(get_temp_location(path))

    log.debug(f"copying [{str(src_path)}] to temp location: [{str(dst_path)}]...")
    return copy(str(src_path), str(dst_path), exists_ok=True)


def open_file(file_path: str, safe=True):  # pragma: no cover
    """Makes a temp copy of a file and opens it with the system default handler"""

    if safe:
        file_path = copy_to_temp_location(file_path)

    process = Process(target=partial(call, ["cmd", "/c", file_path]), daemon=True)
    process.start()
    process.join(timeout=2)


def write_text(text: str, file: str):
    path = Path(file).absolute()
    log.debug(f"writing text to: [{str(path)}] ({len(text)} chars)")
    with path.open("wb") as out:
        out.write(text.encode("utf-8"))


def view_text(text: str):
    dst_file = get_temp_location("text_view.txt")
    write_text(text, dst_file)
    open_file(dst_file, False)


def main():  # pragma: no cover
    log.init()
    file = r"D:\PROJECT_HOME\f_stats\src\f_stats\storage\matches.json"
    open_file(file)


if __name__ == '__main__':  # pragma: no cover
    main()
