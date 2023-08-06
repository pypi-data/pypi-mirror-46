from pathlib import Path
from tempfile import gettempdir

from bets.utils import file_sys
from bets.utils import log

log.init()

FILE_PATH = Path(__file__).absolute()
FILE_NAME = FILE_PATH.name


def test_get_temp_location():
    temp_file = Path(file_sys.get_temp_location(str(FILE_PATH)))
    assert temp_file.parent == Path(gettempdir())
    assert temp_file.name.startswith("tmp_")
    assert temp_file.name.endswith(FILE_NAME)


def test_delete():
    tmp_dir = Path(gettempdir()).absolute().joinpath("tmp_dir_for_deletion")
    tmp_dir.mkdir()

    inner_dirs = ["d1",
                  "d2",
                  "d3"]
    inner_paths = [tmp_dir.joinpath(d) for d in inner_dirs]
    for ip in inner_paths:
        ip.mkdir(parents=True, exist_ok=True)
        inner_file = ip.joinpath("file.txt")
        log.debug(f'writing text to: {str(inner_file)}')
        inner_file.write_text("msome_Text", encoding="utf-8")

    log.debug(f"created temp dir structure at: {tmp_dir}")
    file_sys.delete(str(tmp_dir))

    assert not tmp_dir.exists()


def test_copy_to_tmp_location_file():
    src_file = Path(__file__).absolute()
    dst_file = Path(file_sys.copy_to_temp_location(str(src_file)))
    src_bytes = src_file.read_bytes()
    dst_bytes = dst_file.read_bytes()
    assert dst_bytes == src_bytes
