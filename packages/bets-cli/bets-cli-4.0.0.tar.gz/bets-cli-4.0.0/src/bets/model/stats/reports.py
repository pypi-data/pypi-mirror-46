from typing import List

from tabulate import tabulate

from bets.model.stats.stats_collection import StatsCollection
from bets.utils import file_sys, excel_util

TABLE_FMT = {True: "simple", False: "fancy_grid", None: "fancy_grid", }


def _fmt_table(table: List[dict], simple=True, showindex=False):
    return tabulate(
        tabular_data=table,
        headers="keys",
        tablefmt=TABLE_FMT[simple],
        floatfmt=".02f",
        stralign="right",
        showindex=showindex
    )


def prepare_daily_report(stats: StatsCollection, simple=True) -> str:
    summary = _fmt_table(stats.summary_by_date(), simple)
    daily = "\n\n".join([f"{date}:\n{_fmt_table(date_stats, simple)}"
                         for date, date_stats
                         in stats.agg_date().items()])

    return f"Summary:\n{summary}\n\n\n{daily}"


def save_daily_report_simple(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_daily_report(stats, simple=True), file)


def save_daily_report_fancy(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_daily_report(stats, simple=False), file)


def save_daily_report_excel(stats: StatsCollection, file: str):
    data = dict(summary=stats.summary_by_date(), **stats.agg_date())
    excel_util.write_sheets(data, file)


def prepare_ranks_report(stats: StatsCollection, simple=True) -> str:
    summary = _fmt_table(stats.summary_by_rank(), simple)
    ranked = "\n\n".join([f"{rank}:\n{_fmt_table(rank_stats, simple)}"
                          for rank, rank_stats
                          in stats.agg_rank().items()])

    return f"Summary:\n{summary}\n\n{ranked}"


def save_ranks_report_simple(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_ranks_report(stats, simple=True), file)


def save_ranks_report_fancy(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_ranks_report(stats, simple=False), file)


def save_ranks_report_excel(stats: StatsCollection, file: str):
    data = dict(summary=stats.summary_by_rank(), **stats.agg_rank())
    excel_util.write_sheets(data, file)


def prepare_ratios_report(stats: StatsCollection, simple=True) -> str:
    summary_table = _fmt_table(stats.summary_by_ratio(), simple)

    ratios_tables = "\n\n\n".join([f"[{ratio}]\n{_fmt_table(ratio_stats, simple)}"
                                   for ratio, ratio_stats
                                   in stats.agg_ratio().items()])

    return f"Summary:\n{summary_table}\n\n{ratios_tables}"


def save_ratios_report_simple(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_ratios_report(stats, simple=True), file)


def save_ratios_report_fancy(stats: StatsCollection, file: str):
    file_sys.write_text(prepare_ratios_report(stats, simple=False), file)


def save_ratios_report_excel(stats: StatsCollection, file: str):
    data = dict(summary=stats.summary_by_ratio(), **stats.agg_ratio())
    excel_util.write_sheets(data, file)
