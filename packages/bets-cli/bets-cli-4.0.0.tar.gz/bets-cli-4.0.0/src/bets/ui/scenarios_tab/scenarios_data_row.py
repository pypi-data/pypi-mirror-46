from tkinter import BOTH, LEFT, RIGHT, W, X, SE
from tkinter import LabelFrame
from tkinter import filedialog, messagebox
from tkinter.ttk import Button
from tkinter.ttk import LabelFrame as TtkLabelFrame

from bets.model.scenarios import Scenarios
from bets.ui.constants import PAD_X, PAD_Y
from bets.ui.scenarios_tab.filter_frames import TotalOccurrencesFilterFrame, SequentialOccurrencesFilterFrame
from bets.utils import log
from bets.utils.file_sys import open_file


def _get_from_to_values(text: str, max_value: int):
    try:
        values = tuple(int(value) for value in text.strip().split(" "))
        if len(values) == 1:
            values = (values[0], values[0])
    except ValueError:
        values = 0, max_value

    log.debug("got from-to values:", str(values))
    return values


class ScenariosDataRow(TtkLabelFrame):

    def __init__(self, parent, title, scenarios: Scenarios):
        self.title = f"{title} Scenarios ({len(scenarios)}) "
        super().__init__(parent, text=self.title)
        self.parent = parent
        self.scenarios = scenarios
        self.create_widgets()

    def create_widgets(self):
        self._create_filters()
        self._create_actions()

    def _create_filters(self):
        filter_frame = LabelFrame(self)
        filter_frame.pack(side=LEFT, anchor=W, fill=X)
        self._create_range_filter(filter_frame)
        self._create_occurrence_filter(filter_frame)

        for child in filter_frame.winfo_children():
            child.grid_configure(padx=PAD_X, pady=PAD_Y, sticky=W)

    def _create_actions(self):
        actions_frame = LabelFrame(self)
        actions_frame.pack(side=RIGHT, anchor=W, fill=BOTH)
        save_frame = LabelFrame(actions_frame, text=" Save as ")
        save_frame.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
        Button(save_frame, text="CSV", command=self.export_as_csv).grid(column=0, row=0, padx=PAD_X // 2, pady=PAD_Y)
        Button(save_frame, text="TXT", command=self.export_as_grid).grid(column=1, row=0, padx=PAD_X // 2, pady=PAD_Y)
        Button(actions_frame,
               text="Delete", command=self.destroy).grid(column=2, row=0, padx=PAD_X, pady=PAD_Y, sticky=SE)

    def _create_range_filter(self, filter_frame):
        range_filter_frame = TotalOccurrencesFilterFrame(filter_frame, max_value=len(self.scenarios.matches))
        range_filter_frame.grid(column=0, row=0)

        def _apply_filter():
            target, count_from, count_to = range_filter_frame.get_values()
            scenarios = self.scenarios.filter_by_total_occurrences(target, count_from, count_to)
            self.parent.add_scenarios_row(title=f"Range({target})[{count_from} - {count_to}]", scenarios=scenarios)

        range_filter_frame.apply_button["command"] = _apply_filter

    def _create_occurrence_filter(self, filter_frame):
        occurrence_filter_frame = SequentialOccurrencesFilterFrame(filter_frame, max_value=len(self.scenarios.matches))
        occurrence_filter_frame.grid(column=1, row=0)

        def _apply_filter():
            target, count = occurrence_filter_frame.get_values()
            scenarios = self.scenarios.filter_by_sequential_occurrences(target, count)
            self.parent.add_scenarios_row(title=f"Seq({target})[up to {count} in a row]", scenarios=scenarios)

        occurrence_filter_frame.apply_button["command"] = _apply_filter

    def _export_scenarios(self, file_ext):
        target_file = filedialog.asksaveasfilename(filetypes=(f"Text .{file_ext}",))

        if not target_file:
            messagebox.showinfo("", "Export canceled")
            return

        if not target_file.lower().endswith(file_ext):
            target_file = f"{target_file}.{file_ext}"

        if messagebox.askyesno("Confirm export", f"Target file:\n{target_file}"):
            self.scenarios.write_to_file(target_file)
            if messagebox.askyesno("Export success!", f"Open output file?\n{target_file}"):
                open_file(target_file)

        else:
            messagebox.showinfo("", "Export canceled")

    def export_as_grid(self):
        self._export_scenarios("txt")

    def export_as_csv(self):
        self._export_scenarios("csv")
