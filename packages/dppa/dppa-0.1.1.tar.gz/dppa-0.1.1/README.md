DPPA (Deep Protein Polarity Analyser)
=====================================

Installation
------------
```bash
pip install dppa --user
```

Usage
-----
CLI:

```bash
usage: run-dppa [-h] [--reportName REPORTNAME] [--reportPath REPORTPATH]
                [--debug]
                TARGET REPORTTYPE

Analyse all protein alignment .fasta files from a target.

positional arguments:
  TARGET                Target .fasta file to be analysed.
  REPORTTYPE            Output report file type.

optional arguments:
  -h, --help            show this help message and exit
  --reportName REPORTNAME
                        Output report custom file name.
  --reportPath REPORTPATH
                        Output report custom file path.
  --debug               Turn debug messages on.
```

Python:

```python
import dppa.core as pol_solver

target_path = 'example.fasta'
report_name = 'myrep'
report_type = 'xls'
report_path = 'results-folder' # optional

pol_solver.set_debug_mode(True) # optional

# results[0] -> polarity results dataframe
# results[1] -> alerts dataframe
results = pol_solver.run(target_path)

# option 1: export to the current folder
pol_solver.export(results, report_type, report_name)
# option 2: export to custom folder
pol_solver.export(results, report_type, report_name, report_path)
```