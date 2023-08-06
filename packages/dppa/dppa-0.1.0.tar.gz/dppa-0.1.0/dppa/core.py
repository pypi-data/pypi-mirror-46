### Deep Protein Polarity Analyser (DPPA)
### Copyright (c) 2019 Jan Marans Agnella Justi & Mariana de França Costa

from ._src import _core_methods

_cmh = _core_methods.CoreMethods()

def _main():
    _cmh.start_main()

def run(target_fn):
    return _cmh.start_run(target_fn)

def export(report_name, report_type, results_df_list):
    _cmh.start_export(report_name, report_type, results_df_list)

def set_debug_mode(isActive):
    _cmh.set_debug_mode(isActive)