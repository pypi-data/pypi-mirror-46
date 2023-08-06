from tkinter import Frame

from bets.ui.matches_tab.manual_match_input_frame import ManualMatchInputFrame
from bets.ui.matches_tab.matches_table_frame import MatchesTableFrame
from bets.ui.matches_tab.pasted_matches_input import PastedMatchesInput


class MatchesTabFrame(Frame):
    matches_table: MatchesTableFrame
    single_match_input: ManualMatchInputFrame
    pasted_matches_input: PastedMatchesInput

    def __init__(self, win, tabs, matches):
        super().__init__(tabs)
        self.win = win
        self.tabs = tabs
        self.matches = matches
        self.tabs.add(self, text="Matches")
        self.create_widgets()

    def create_widgets(self):
        self.pasted_matches_input = PastedMatchesInput(self, self.matches, column=0, row=0)
        self.single_match_input = ManualMatchInputFrame(self, self.matches, column=1, row=0)
        self.matches_table = MatchesTableFrame(self, self.matches, column=0, row=2)
