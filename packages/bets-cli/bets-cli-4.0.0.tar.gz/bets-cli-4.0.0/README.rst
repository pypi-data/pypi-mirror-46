========
bets-cli
========


CLI to assist football bets


Description
===========

Reads a list of matches from a text file and outputs all possible scenarios

Installation
============

``pip install bets-cli``


Usage
=====

``bets -a ACTION --in-file=IN_FILE [---in-fmt=INT_FMT] --out-dest=OUT_DEST --out-fmt=OUT_FMT``

ACTIONS:

- matches - read the matches file and output to console. ( Use this to check if the file can be loaded properly )
    - ``--in-fmt`` currently supports ``[ lines | efbet ]``
    - ``--out-dest`` defaults to console, but will write to file if passed
    - ``--out-fmt`` supported formats ``[ plain | fancy_grid | csv ]``

- scenarios - reads the matches file, then generates all the possible scenarios and outputs them to a file.
    - ``--in-file`` used as matches source file
    - ``--out-dest`` behave same as with matches


Note
====

Due to memory issues, 13 matches is the current limit when having 16GB RAM.
