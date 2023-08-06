from pathlib import Path
from Bio.SeqIO import FastaIO
from anytree import AnyNode, LevelOrderGroupIter
import string
import logging

class AuxFuncPack:
    # package of custom functions

    def fasta_to_list(self, fasta_fn):
        ### convert .fasta file into a list
        # list format: [(name, seq)]
        filepath = Path.cwd() / fasta_fn
        fasta_list = list(FastaIO.SimpleFastaParser(open(filepath)))
        # check if all sequences have the same size
        sizes_list = []
        for fasta_idx in range(0, len(fasta_list)):
            sizes_list.append(len(fasta_list[fasta_idx][1]))
        if not all(x == sizes_list[0] for x in sizes_list):
            logging.getLogger().info(f'WARNING: .fasta file has inconsistency: {fasta_fn}')

        return fasta_list

    def add_alert_on_df(self, df_alert, seq_name, col_num, alert_type_str):
        df_alert = df_alert.append(
            {
                'SeqName': seq_name.replace('_', ' '),
                'ColNum': col_num+1,
                'AlertType': alert_type_str
            }
        , ignore_index=True)

        return df_alert
    
    def get_lists_aminos(self, df_pols):
        ### get list of unknown aminos, based on df_pols
        # get alphabet list
        unknown_aminos = list(string.ascii_uppercase)
        # add '?' and '-' char
        unknown_aminos.extend(['?', '-'])
        # start known aminos list
        known_aminos = []
        # remove all pol-defined letters
        for curr_pol in range(0, df_pols.shape[0]):
            list_curr_pol = list(df_pols.Amino.at[curr_pol])
            known_aminos.extend(list_curr_pol)
            unknown_aminos = [x for x in unknown_aminos if x not in list_curr_pol]

        return unknown_aminos, known_aminos

    def deep_searcher(self, fasta_list, col_num, df_alert, unknown_aminos):
        # create local root
        loc_root = AnyNode(name='LocRoot', amino='LocRootAmino')
        # create nodes from column number
        for row in range(0, len(fasta_list)):
            AnyNode(
                name=fasta_list[row][0], 
                amino=fasta_list[row][1][col_num], 
                parent=loc_root
            )
        # run through nodes
        for node in loc_root.children:
            # check if amino is possibly deepable
            if node.amino in unknown_aminos:
                if 'consensus_sequence' in node.name and node.amino not in ['-', '?']: 
                    # non-gap deepable char
                    fasta_dict = dict(fasta_list)
                    # check previous number of gaps from sequence
                    num_gaps = fasta_dict[node.name][:col_num].count('-')
                    # shift column number to the correct one
                    shifted_col_num = col_num-num_gaps
                    # get fasta_list of this node's original sequence
                    deeper_fn = node.name.replace('_', ' ') 
                    deeper_fn = deeper_fn.replace(' consensus sequence','') + '.fasta'
                    deeper_list = self.fasta_to_list(deeper_fn)
                    # go deeper
                    deeper_result = self.deep_searcher(deeper_list, shifted_col_num, df_alert, unknown_aminos)
                    deeper_result[0].parent = node
                    df_alert = deeper_result[1]
                else:
                    # non-deepable char, increment on df_ale
                    df_alert = self.add_alert_on_df(
                        df_alert, 
                        node.name,
                        col_num, 
                        'Pure ' + node.amino
                    )

        return loc_root, df_alert

    def get_aminos_perc_dict(self, root, aminos_list, unknown_aminos):
        ### convert list of aminos to dict (amino -> its perc)
        # get list of aminos levels
        aminos_levels = [[node.amino for node in children] for children in LevelOrderGroupIter(
            root,
            filter_=lambda n: n.amino != 'LocRootAmino'
        )]
        # clear any empty lists (parent roots)
        aminos_levels = [x for x in aminos_levels if x]
        # run through levels
        deepables = [*unknown_aminos]
        deepables.remove('?') # '?' is not deepable
        deepables.remove('-') # '-' is not deepable
        aminos_dict = {}
        for target_amino in aminos_list:
            total_perc = 0
            deepness_perc = 1
            for level in aminos_levels:
                amino_perc_on_lvl = (level.count(target_amino)/len(level))
                total_perc = total_perc + (amino_perc_on_lvl)*deepness_perc
                num_of_deepables = sum(level.count(x) for x in deepables)
                deepables_perc_on_lvl = (num_of_deepables/len(level))
                deepness_perc = deepness_perc * deepables_perc_on_lvl
            aminos_dict[target_amino] = round(100*total_perc,3)

        return aminos_dict
    
    def get_polarities_perc_dict(self, aminos_dict, df_pols):
        ### get dict of polarities within aminos list
        # get list of tuples (pol_type -> perc)
        list_percs = []
        for curr_pol in range(0, df_pols.shape[0]):
            pol_amino_list = list(df_pols.Amino.at[curr_pol])
            for curr_amino in list(aminos_dict.items()):
                if curr_amino[0] in pol_amino_list:
                    list_percs.append((df_pols.Type.at[curr_pol], curr_amino[1]))
        # convert into unified dict
        pols_dict = {}
        for key, value in list_percs:
            pols_dict[key] = round(pols_dict.get(key, 0) + value, 2)

        return pols_dict

    def get_pol_score(self, pols_dict, df_pols):
        ### calculate polarity score
        # convert dict into list of tuples
        pols_percs = list(pols_dict.items())
        # get sum of current scores
        sum_scores = 0
        for curr_pol in pols_percs:
            sum_scores += df_pols.loc[df_pols['Type'] == curr_pol[0], 'Score'].values[0]
        # calculate
        pol_list_size = len(pols_percs)
        if pol_list_size is 1:
            pol_score = 0
        else:
            # get minimal value of perc
            min_pols = min(pols_percs, key = lambda t: t[1])[1]
            pol_score = round(sum_scores*3 + pol_list_size*0.6 + min_pols*0.01, 5)

        return pol_score