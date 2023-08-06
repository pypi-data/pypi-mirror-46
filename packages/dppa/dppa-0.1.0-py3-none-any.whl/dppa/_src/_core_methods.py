import argparse
import logging
from pathlib import PurePath
from pandas import DataFrame, read_csv
from tqdm import tqdm
from .helpers.auxfunc import AuxFuncPack
from .conv.export_dfs import DfExporter

logging.basicConfig(level=logging.INFO, format='%(message)s')

class CoreMethods:
    def start_main(self):
        # get options from user
        parser = argparse.ArgumentParser(description='Analyse all protein alignment .fasta files from a target.')
        parser.add_argument(
            'target', help='Target .fasta file to be analysed.', type=str,
            metavar='TARGET'
        )
        parser.add_argument(
            'reportType', help='Output report file type.', type=str,
            choices=['csv', 'xls', 'all'], metavar='REPORTTYPE'
        )
        parser.add_argument(
            '--reportName', help='Output report file name.'
        )
        parser.add_argument(
            '--debug', help='Turn debug messages on.', action='store_true'
        )
        args = vars(parser.parse_args())
        # config logging
        self.set_debug_mode(args['debug'])
        # run
        results_df_list = self.start_run(args['target'])
        # export dfs
        report_name = args['reportName'] if (args['reportName'] is not None) else args['target']
        self.start_export(
            report_name, args['reportType'], results_df_list
        )
        logging.debug('Done.')
    
    def start_run(self, target_fn):
        # run analyser
        logging.debug(f'Starting analysis for {target_fn}')
        # create handler of custom functions
        auxf_handler = AuxFuncPack()
        # create list from .fasta target file
        target_list = auxf_handler.fasta_to_list(target_fn)
        # create dfs
        df_pol_results = DataFrame(columns=['ColNum', 'PossibleAminos', 'PossiblePols', 'PolScore'])
        df_alert_results = DataFrame(columns=['SeqName', 'ColNum', 'AlertType'])
        csv_path = PurePath(__file__).parent.parent / 'data' / 'pols.csv'
        df_pols = read_csv(csv_path)
        # get list of unknown and known aminos
        [unknown_aminos, known_aminos] = auxf_handler.get_lists_aminos(df_pols)
        # execute deep searcher
        number_columns = len(target_list[0][1]) # number of chars on sequence
        # on each column from .fasta target file
        isDebugModeNotActive = not logging.getLogger().isEnabledFor(logging.DEBUG)
        for current_col in tqdm(range(0, number_columns), disable=isDebugModeNotActive):
            root, df_alert_results = auxf_handler.deep_searcher(
                target_list, current_col, df_alert_results, unknown_aminos
            )
            # get root list of elements
            amino_leaves = []
            for leaf in root.leaves:
                if leaf.amino in known_aminos or leaf.amino in unknown_aminos:
                    amino_leaves.append(leaf.amino)
                else:
                    # invalid char, increment on df_alert_results
                    df_alert_results = auxf_handler.add_alert_on_df(
                        df_alert_results,
                        leaf.name,
                        current_col,
                        'Unlisted Char ' + leaf.amino
                    )
            # remove still unknown aminos
            amino_leaves = [x for x in amino_leaves if x not in unknown_aminos]
            # unify list
            unified_list = list(set(amino_leaves))
            # check length
            if len(unified_list) > 1:
                # get aminos percentages dict
                aminos_dict = auxf_handler.get_aminos_perc_dict(root, unified_list, unknown_aminos)
                # get polarities percentages dict
                pols_dict = auxf_handler.get_polarities_perc_dict(aminos_dict, df_pols)
                # get polarity score
                curr_pol_score = auxf_handler.get_pol_score(pols_dict, df_pols)
                # increment on df_pol_results
                df_pol_results = df_pol_results.append(
                    {
                        'ColNum': current_col+1,
                        'PossibleAminos': aminos_dict,
                        'PossiblePols': pols_dict,
                        'PolScore': curr_pol_score
                    }, ignore_index=True)
        results_df_list = [df_pol_results, df_alert_results]
        return results_df_list

    def start_export(self, report_name, report_type, results_df_list):
        # export dfs
        DfExporter().export_dfs(
            report_name, report_type, results_df_list
        )
    
    def set_debug_mode(self, isActive):
        curr_level = logging.DEBUG if isActive else logging.INFO
        logging.getLogger().setLevel(curr_level)