import tkinter as tk
from functools import partial
from multiprocessing import Process
from subprocess import call
from tkinter import Canvas, Frame, Label, LabelFrame, Scrollbar
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showwarning, showerror, askyesno
from typing import List

from tabulate import tabulate

from bets.model.matches import Matches
from bets.model.scenarios import Scenarios
from bets.utils import log


def _setup_canvas(table_frame, data: List[List[str]], column_widths: List[int] = None, height=200, width=None):
    if not column_widths:
        column_widths = _get_columns_widths(data)

    if not width:
        cells_width = sum(column_widths) * 8  # text len * char size
        cells_ipadx = len(column_widths) * 8  # inner padding
        # borders_width = len(column_widths)
        width = (cells_width + cells_ipadx)
        log.debug(f"got canvas width: {width}")
    canvas = Canvas(table_frame, borderwidth=0)
    canvas_frame = Frame(canvas)
    vsb = Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set, width=width, heigh=height)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4, 4), window=canvas_frame, anchor="nw", tags="frame")
    # be sure that we call OnFrameConfigure on the right canvas
    canvas_frame.bind("<Configure>", lambda event, canvas=canvas: _OnFrameConfigure(canvas))

    _fill_data(canvas_frame, data, column_widths)


def _fill_data(frame,
               data: List[List[str]],
               column_widths: List[int] = None,
               font=("Consolas", 10, "normal")
               ):
    column_widths = column_widths or _get_columns_widths(data)

    for row_idx, row in enumerate(data):
        for col_idx, cell_text in enumerate(row):
            cell_label = Label(frame,
                               text=cell_text, width=column_widths[col_idx], borderwidth="1", relief="solid", font=font)
            cell_label.grid(column=col_idx, row=row_idx, ipadx=4, ipady=2, sticky="W")
        if row_idx % 15 == 0:
            frame.update()


def _get_columns_widths(data: List[List[str]]) -> List[int]:
    widths = [len(cell) for cell in data[0]]
    for row in data:
        for idx, cell in enumerate(row):
            widths[idx] = max(len(cell), widths[idx])
    log.debug(f"columns widths: {widths}")
    return widths


def _OnFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))


def _create_table_frame(parent,
                        columns: List[str],
                        rows: List[List[str]],
                        height=200,
                        width: int = None):
    columns_widths = _get_columns_widths([columns] + rows)

    header_frame = LabelFrame(parent, text=" Columns ")
    header_frame.grid(column=0, row=0, sticky="WE", padx=4, ipady=2)
    _fill_data(header_frame, [columns], columns_widths)

    body_frame = LabelFrame(parent, text=" Data ")
    body_frame.grid(column=0, row=1, sticky="WE", ipadx=4, ipady=2)

    _setup_canvas(body_frame, rows, columns_widths, height, width)

    footer_frame = LabelFrame(parent, text=" Actions ")
    footer_frame.grid(column=0, row=2, sticky="WE", ipadx=4, ipady=2)

    return header_frame, body_frame, footer_frame


class TableFrame:
    def __init__(self, title: str, columns: List[str], rows: List[List[str]], height=200, width: int = None):
        self.win = tk.Tk()
        self.win.title(title)
        self.parent = tk.Frame(self.win)
        self.parent.grid(column=0, row=0, padx=8, pady=4)
        self.columns = ["ID"] + columns
        self.rows = [[str(i + 1)] + row for i, row in enumerate(rows)]
        self.header, self.body, self.footer = _create_table_frame(self.parent, self.columns, self.rows, height, width)
        export_frame = tk.LabelFrame(self.footer, text=" Save As ")
        export_frame.pack(fill=tk.X, side=tk.LEFT, anchor="e", padx=8, pady=4)
        tk.Button(export_frame, text="CSV", command=partial(self._save_as, "csv")).pack(side=tk.LEFT, padx=8, pady=4)
        tk.Button(export_frame, text="TXT", command=partial(self._save_as, "txt")).pack(side=tk.LEFT, padx=8, pady=4)
        tk.Button(self.footer, text="Close", command=self._close).pack(side=tk.RIGHT, anchor="se", padx=8, pady=10)
        self.win.mainloop()

    @property
    def table_text(self) -> str:
        return tabulate(tabular_data=self.rows, headers=self.columns, tablefmt="fancy_grid", stralign="center")

    @property
    def csv_text(self) -> str:
        all_rows = [self.columns] + self.rows
        return "\n".join(row_csv for row_csv in [",".join(row) for row in all_rows])

    def _close(self):
        self.win.quit()
        self.win.destroy()
        self.header = None
        self.body = None
        self.footer = None
        self.parent = None
        self.columns = None
        self.rows = None

    def _save_as(self, file_ext: str):
        file_path = asksaveasfilename(filetypes=(f"Text .{file_ext}",))

        if not file_path:
            showwarning("", "Save canceled!")
            return
        if not file_path.endswith(f".{file_ext}"):
            file_path = f"{file_path}.{file_ext}"

        if askyesno("Confirm destination", f"Write data to:\n{file_path}"):
            try:
                with open(file_path, "wb") as file:
                    file.write((self.csv_text if file_ext == "csv" else self.table_text).encode("utf-8"))
                if askyesno("Save success!", f"Do you want to open the file?\n{file_path}"):
                    Process(target=partial(call, ["cmd", "/c", file_path]), daemon=True).start()
            except Exception as err:
                showerror("Save failed!", f"Error occurred while saving:\n{str(err)}")


def main():
    matches = Matches.random(4)
    scenarios = Scenarios.from_matches(matches)
    columns = scenarios.columns
    rows = [s.values for s in scenarios]
    TableFrame("Scenarios", columns, rows)


if __name__ == '__main__':
    main()
