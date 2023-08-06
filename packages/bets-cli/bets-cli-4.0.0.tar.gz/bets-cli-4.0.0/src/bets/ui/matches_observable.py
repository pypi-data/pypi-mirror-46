from abc import ABC, abstractmethod
from typing import List, Iterable

from bets.model.matches import Match, Matches


class MatchesObserver(ABC):

    @abstractmethod
    def matches_changed(self, matches_observable: "MatchesObservable"):
        pass


class MatchesObservable(Matches):

    def __init__(self):
        super().__init__()
        self._observers: List[MatchesObserver] = []

    def notify_observers(self):
        for o in self._observers:
            o.matches_changed(self)

    def add_observer(self, observer: MatchesObserver):
        self._observers.append(observer)

    def append(self, match: Match):
        super().append(match)
        self.notify_observers()

    def clear(self):
        super().clear()
        self.notify_observers()

    def extend(self, matches: Iterable[Match]):
        super().extend(matches)
        self.notify_observers()
