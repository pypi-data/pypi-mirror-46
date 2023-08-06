from tkinter import Button, Frame, IntVar, Label, LabelFrame, EW
from typing import List

from bets.model.matches import Matches
from bets.model.scenarios import Scenarios
from bets.ui.constants import PAD_X, PAD_Y
from bets.ui.scenarios_tab.scenarios_data_row import ScenariosDataRow


class ScenariosTabFrame(Frame):
    scenarios: Scenarios

    def __init__(self, win, tabs, matches: Matches):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.matches = matches
        self.scenarios = None
        self.tabs.add(self, text="Scenarios")
        self.var_scenarios_count = IntVar()
        self.var_scenarios_count.set(0)
        self.gen_frame = LabelFrame(self, text=" Initial data ")
        self.gen_frame.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y)
        self.create_widgets()
        self.scenarios_rows: List[ScenariosDataRow] = []

    def _clear_views(self):
        for row in self.scenarios_rows:
            row.destroy()

        self.scenarios_rows.clear()

    def _generate_scenarios(self):
        self._clear_views()
        self.scenarios = Scenarios.from_matches(self.matches)
        self.var_scenarios_count.set(len(self.scenarios))
        self.add_scenarios_row(" Initial ", self.scenarios)

    def add_scenarios_row(self, title: str, scenarios: Scenarios):
        row = ScenariosDataRow(self, title, scenarios)
        row.grid(column=0, row=(len(self.scenarios_rows) + 1), padx=PAD_X, pady=PAD_Y, sticky=EW)
        self.scenarios_rows.append(row)

    def create_widgets(self):
        gen_btn = Button(self.gen_frame, text="(Re)Generate Scenarios", command=self._generate_scenarios)
        gen_btn.grid(column=0, row=0, sticky=EW, padx=PAD_X, pady=PAD_Y)
        Label(self.gen_frame, text="Total scenarios count:").grid(column=1, row=0, padx=10, pady=5)
        Label(self.gen_frame, textvariable=self.var_scenarios_count).grid(column=2, row=0, padx=10, pady=5)
