from tkinter import END, NSEW
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Button, Combobox, Label, LabelFrame
from typing import Optional

from bets.model.matches import Matches
from bets.ui import constants
from bets.ui.constants import PAD_X, PAD_Y
from bets.utils import log


class PastedMatchesInput(LabelFrame):
    paste_input: ScrolledText
    paste_fmt_combo: Combobox

    def __init__(self, parent, matches: Matches, column=0, row=1):
        super().__init__(parent, text=" Pasted input ")
        self.parent = parent
        self.matches = matches
        self.grid(column=column, row=row, sticky=NSEW, padx=PAD_X, pady=PAD_Y)
        self.create_widgets()

    def create_widgets(self):
        self.paste_input = ScrolledText(self, width=2 * constants.W_MATCH_TITLE, height=4)
        self.paste_input.grid(column=0, row=0, rowspan=4)

        Label(self, text="Paste format:").grid(column=1, row=0)
        self.paste_fmt_combo = Combobox(self, values=("efbet", "lines"), state="readonly")
        self.paste_fmt_combo.grid(column=1, row=1)
        self.paste_fmt_combo.current(0)

        Button(self, text="Add", command=self._add_pasted_matches).grid(column=1, row=2)
        Button(self, text="Clear", command=self._clear_paste_input).grid(column=1, row=3)

        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=PAD_Y, sticky=NSEW)

    def _clear_paste_input(self):
        self.paste_input.delete("1.0", END)

    def _get_pasted_text(self) -> str:
        pasted_text = self.paste_input.get("1.0", END).strip()
        return pasted_text

    def _get_pasted_text_fmt(self) -> str:
        paste_fmt = self.paste_fmt_combo.get()
        return paste_fmt

    def _get_pasted_matches(self) -> Optional[Matches]:
        try:
            log.debug("parsing pasted matches...")
            matches = Matches.PARSERS[self._get_pasted_text_fmt()](self._get_pasted_text())
            if matches:
                log.debug(f" got [{len(matches)}] new matches!\n{matches.table}")
                return matches
        except Exception as ex:
            log.exception("Error while parsing pasted matches!")
            messagebox.showerror("Error while parsing pasted text!", f" Exception: {str(ex)}, args:{ex.args}")

        return None

    def _add_pasted_matches(self):
        matches = self._get_pasted_matches()
        if matches:
            self.matches.extend(matches)
            self._clear_paste_input()
