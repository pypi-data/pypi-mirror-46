from tkinter import StringVar, NSEW
from tkinter.ttk import Label, LabelFrame

from bets.ui.constants import PAD_X, PAD_Y
from bets.ui.matches_observable import MatchesObserver, MatchesObservable


class MatchesTableFrame(LabelFrame, MatchesObserver):

    def __init__(self, parent, matches: MatchesObservable, column=0, row=2):
        super().__init__(parent, text=" Matches ")
        self.grid(column=column, row=row, columnspan=2, padx=PAD_X, pady=PAD_Y, sticky=NSEW)
        self.var_table = StringVar()
        self.table_label = Label(self, textvariable=self.var_table, font="Consolas")
        self.table_label.grid(column=0, row=0, padx=PAD_X, pady=PAD_Y, sticky=NSEW)
        matches.add_observer(self)

    def matches_changed(self, matches_observable: MatchesObservable):
        self.var_table.set(matches_observable.table if matches_observable else "")
