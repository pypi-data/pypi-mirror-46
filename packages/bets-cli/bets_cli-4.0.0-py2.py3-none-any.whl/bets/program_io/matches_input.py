import logging

from pathlib import Path
from typing import List

from bets.model.match import Match

_log = logging.getLogger(__name__)


class EfbetParser:
    def __init__(self, lines: List[str]):
        self.lines = lines.copy()
        self.idx_first_title = self._get_title_idx(start_line=0)
        self.idx_first_ratio_1 = self.idx_first_title + 1
        self.idx_first_ratio_x = self.idx_first_ratio_1 + 1
        self.idx_first_ratio_2 = self.idx_first_ratio_x + 1
        self.idx_second_title = self._get_title_idx(self.idx_first_ratio_2)
        self.step_size = self.idx_second_title - self.idx_first_title

    def _get_title_idx(self, start_line=0) -> int:
        for i, line in enumerate(self.lines):
            if i < start_line:
                continue
            if "vs" in line:
                return i
        raise ValueError("lines don't contain efbet match title (no 'vs')!")

    def parse(self) -> List[Match]:
        titles = self.lines[self.idx_first_title::self.step_size]
        ratios_1 = self.lines[self.idx_first_ratio_1::self.step_size]
        ratios_x = self.lines[self.idx_first_ratio_x::self.step_size]
        ratios_2 = self.lines[self.idx_first_ratio_2::self.step_size]

        return [Match(title, r1, rx, r2)
                for title, r1, rx, r2
                in zip(titles, ratios_1, ratios_x, ratios_2)]

    @classmethod
    def parse_text(cls, text) -> List[Match]:
        return EfbetParser([line.strip()
                            for line
                            in text.strip().split("\n")
                            if line.strip()]).parse()


class LinesParser:
    def __init__(self, lines: List[str]):
        self.lines = lines

    @classmethod
    def parse_line(cls, line: str) -> Match:
        """Parses a string to a Match"""

        if not isinstance(line, str):
            raise TypeError("Expected string but got {}!".format(type(line).__name__))

        if not line:
            raise ValueError("Expected non-empty string!")

        line_parts = line.strip().split(" ")
        if len(line_parts) < 4:
            raise ValueError("Line should contain at least 4 space-separated parts!")

        title = " ".join(line_parts[:-3])
        r1, rx, r2 = line_parts[-3:]

        return Match(title, r1, rx, r2)

    @classmethod
    def parse_text(cls, text: str) -> List[Match]:
        return LinesParser([line.strip()
                            for line
                            in text.split("\n")
                            if line.strip()]).parse()

    def parse(self) -> List[Match]:

        matches = []

        for line in self.lines:
            try:
                matches.append(self.parse_line(line))
            except (ValueError, TypeError):
                continue

        if not matches:
            raise ValueError("The lines did not contain any matches!", self.lines)

        return matches


class MatchesInput:
    PARSERS = {
        "efbet": EfbetParser,
        "lines": LinesParser
    }

    def __init__(self, file: str, fmt: str, encoding="utf-8"):
        _log.debug("creating MatchesReader (file_fmt={}), pointing to [{}]...".format(fmt, file))

        if not isinstance(file, str):
            raise TypeError("Expected string")
        if not file:
            raise ValueError("Expected non-empty string")
        if fmt not in self.PARSERS:
            raise ValueError("Unknown fmt [{}]".format(fmt))

        self.encoding = encoding
        self.fmt = fmt
        self.file_path = Path(file).absolute()
        self._assert_path()

    def __repr__(self):
        return "MatchesReader(file={}, fmt={}, encoding={})".format(self.file_path,
                                                                    self.fmt,
                                                                    self.encoding)

    def _assert_path(self):
        if not self.file_path.exists():
            raise FileNotFoundError(str(self.file_path))
        if self.file_path.is_dir():
            raise IsADirectoryError(str(self.file_path))

    def _get_lines(self) -> List[str]:
        _log.debug("reading lines from file...")
        return [line.strip()
                for line
                in self.file_path.read_text(encoding=self.encoding).strip().split("\n")
                if line.strip()]

    def read(self) -> List[Match]:
        lines = self._get_lines()
        _log.debug("parsing lines (fmt={}): \n{}".format(self.fmt, "\n".join(lines)))
        return self.PARSERS[self.fmt](lines).parse()

    @classmethod
    def read_file(cls, file, fmt="lines", encoding="utf-8") -> List[Match]:
        try:
            return MatchesInput(file, fmt, encoding).read()
        except ValueError:
            # attempt with non-default format (will raise if fail)
            return MatchesInput(file, "efbet", encoding="utf=8").read()
