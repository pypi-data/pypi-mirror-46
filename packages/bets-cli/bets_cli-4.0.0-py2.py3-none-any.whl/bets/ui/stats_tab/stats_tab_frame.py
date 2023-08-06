from tkinter import Frame, Label
from tkinter import EW, W, E, RAISED
from tkinter.filedialog import askopenfilename, asksaveasfilename

from tkinter.ttk import Button, Combobox, Entry, LabelFrame

from pathlib import Path
from typing import Dict

from bets.model.stats import reports
from bets.model.stats.stats_collection import StatsCollection
from bets.ui.constants import PAD_X, PAD_Y
from bets.utils import log, file_sys

ALL = "All"


class LoadStatsFrame(LabelFrame):

    def __init__(self, parent, set_stats):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text="  Load Stats  ")

        self.parent = parent
        self.set_stats = set_stats

        Label(self, text="Pick stats file: ").grid(row=0, column=0, sticky=W)

        self.file_input = Entry(self, width=60, text="Not set!", state="readonly")
        self.file_input.grid(row=0, column=1, sticky=EW)

        Button(self, text="Browse", command=self._browse_for_stats).grid(row=0, column=2, sticky=E)
        Button(self, text="Use Bundled", command=self._use_bundled_stats).grid(row=0, column=3, sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=PAD_Y, sticky=EW)

    def load_stats(self, file: str):
        self.file_input.configure(text=file)
        stats = StatsCollection.read_json(file)
        self.set_stats(stats)

    def _browse_for_stats(self):
        self.load_stats(askopenfilename())

    def _use_bundled_stats(self):
        self.load_stats(str(Path(__file__).parent.joinpath("matches.json")))


class CountersFrame(LabelFrame):
    def __init__(self, parent, text):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text=text)

    def set_stats(self, counters: Dict[str, int]):
        for child in self.winfo_children():
            child.destroy()

        col_idx = 0
        for name, count in counters.items():
            Label(self, text=f"{name}: ").grid(row=0, column=col_idx)
            col_idx += 1
            Label(self, text=str(count), relief=RAISED).grid(row=0, column=col_idx)
            col_idx += 1

        for child in self.winfo_children():
            child.grid_configure(padx=PAD_X, pady=2 * PAD_Y)


class FilterSelectionFrame(LabelFrame):
    def __init__(self, parent, get_all, get_selection, set_selection):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text="  Filters  ")

        self.parent = parent
        self.get_all = get_all
        self.get_selection = get_selection
        self.set_selection = set_selection

        Label(self, text="Country: ").grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky=EW)

        self.cb_country = Combobox(self, state="readonly", values=("All",), width=30)
        self.cb_country.bind("<<ComboboxSelected>>", self.apply_country_filter)
        self.cb_country.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y, sticky=EW)
        self.cb_country.current(0)

        Label(self, text="Tournament: ").grid(row=0, column=2, padx=PAD_X, pady=PAD_Y, sticky=EW)

        self.cb_tournament = Combobox(self, state="readonly", values=("All",), width=50)
        self.cb_tournament.bind("<<ComboboxSelected>>", self.apply_tournament_filter)
        self.cb_tournament.current(0)
        self.cb_tournament.grid(row=0, column=3, padx=PAD_X, pady=PAD_Y, sticky=EW)

        Button(self, text="Reset", command=self.reset_filters).grid(row=0, column=4)

    def set_countries(self, countries):
        values = (ALL,)
        if countries:
            values += tuple(countries)

        self.cb_country.configure(values=values)

    def set_tournaments(self, tournaments):
        values = (ALL,)
        if tournaments:
            values += tuple(tournaments)

        self.cb_tournament.configure(values=values)

    def apply_country_filter(self, _):
        country = self.cb_country.get()
        selection = self.get_all() if country == ALL else self.get_selection().with_country(country)
        self.set_selection(selection)

    def apply_tournament_filter(self, _):
        tournament = self.cb_tournament.get()
        selection = self.get_all() if tournament == ALL else self.get_selection().with_tournament(tournament)
        self.set_selection(selection)

    def reset_filters(self):
        self.set_selection(self.get_all())
        self.cb_country.current(0)
        self.cb_tournament.current(0)


class ReportsFrame(LabelFrame):
    REPORTS = (
        "Daily - Simple",
        "Daily - Fancy",
        "Daily - Excel",
        "Ranks - Simple",
        "Ranks - Fancy",
        "Ranks - Excel",
        "Ratios - Simple",
        "Ratios - Fancy",
        "Ratios - Excel",
    )

    def __init__(self, parent, get_stats):
        log.debug(f"creating {type(self).__name__}...")
        super().__init__(parent, text="  Reports  ")
        self.get_stats = get_stats

        Label(self, text="Report type: ").grid(row=0, column=0)
        self.combo_report = Combobox(self, values=self.REPORTS, state="readonly")
        self.combo_report.current(0)
        self.combo_report.grid(row=0, column=1, padx=PAD_X, pady=PAD_Y)
        Button(self, text="View", command=self.view_report).grid(row=0, column=2)
        Button(self, text="Save", command=self.save_report).grid(row=0, column=3)

    def _get_save_report_func(self):
        aggregation, fmt = [word.strip().lower() for word in self.combo_report.get().split("-")]
        return getattr(reports, f"save_{aggregation}_report_{fmt}")

    def view_report(self):
        save_report = self._get_save_report_func()
        file_ext = "xlsx" if save_report.__name__.lower().endswith("excel") else "txt"
        out_file = file_sys.get_temp_location(f"report.{file_ext}")
        save_report(self.get_stats(), out_file)
        file_sys.open_file(out_file, safe=False)

    def save_report(self):
        save_report = self._get_save_report_func()
        file_ext = "xlsx" if save_report.__name__.lower().endswith("excel") else "txt"
        file_type = ("Text" if file_ext == "txt" else "Excel") + f" .{file_ext}"
        out_file = asksaveasfilename(filetypes=(file_type,))
        save_report(self.get_stats(), out_file)
        file_sys.open_file(out_file, safe=False)


class StatsTabFrame(Frame):

    def __init__(self, win, tabs):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.tabs.add(self, text="Stats")

        self.stats: StatsCollection = None
        self.selection: StatsCollection = None

        self._body = Frame(self)
        self._body.grid(row=0, column=0, sticky=EW, padx=PAD_X, pady=PAD_Y)

        # Load
        self._load_stats = LoadStatsFrame(self._body, self.set_stats)
        self._load_stats.grid(row=0, column=0, padx=PAD_X, pady=PAD_Y, sticky=EW)

        # Summary
        self._summary = LabelFrame(self._body, text="  Records  ")
        self._summary.grid(row=1, column=0, sticky=EW)

        self._all_counters = CountersFrame(self._summary, text="  All  ")
        self._all_counters.grid(row=0, column=0, padx=2 * PAD_X, pady=2 * PAD_Y, sticky=EW)

        self._selection_counters = CountersFrame(self._summary, text="  Selection  ")
        self._selection_counters.grid(column=1, row=0, padx=2 * PAD_X, pady=2 * PAD_Y, sticky=EW)

        # Filter
        self._filters = FilterSelectionFrame(self._body, self.get_all, self.get_selection, self.set_selection)
        self._filters.grid(row=2, column=0, sticky=EW)

        # Reports
        self._reports = ReportsFrame(self._body, self.get_selection)
        self._reports.grid(row=3, column=0, sticky=EW)

    def get_all(self) -> StatsCollection:
        return self.stats

    def get_selection(self) -> StatsCollection:
        return self.selection

    def set_stats(self, stats: StatsCollection):
        self.stats = stats
        self._all_counters.set_stats(stats.get_counters())
        self._filters.set_countries(stats.unique_countries)
        self.set_selection(stats)

    def set_selection(self, stats: StatsCollection):
        self.selection = stats
        self._selection_counters.set_stats(stats.get_counters())
        self._filters.set_tournaments(stats.unique_tournaments)
