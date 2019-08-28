import re
import django
from itertools import combinations, chain
import pickle
from decimal import *
from pathlib import Path

from IPython.display import display
import pandas as pd

from protein.models import Protein, ProteinSegment, ProteinFamily, ProteinGProteinPair

def get_receptor_classes():
    return ProteinFamily.objects.filter(parent=1).exclude(slug=100)


def get_gprot_classes():
    return ProteinFamily.objects.filter(parent=533)


def get_receptor_segments():
    return ProteinSegment.objects.filter(proteinfamily="GPCR")


def get_gprot_segments():
    return ProteinSegment.objects.filter(proteinfamily="Alpha")


def extract_per_attr(data, attr, name):
    """Return elements of data for which attr is equal to name"""
    return [elem for elem in data if name in elem[attr]]


def calc_consensus_from_signature(signature_dict):
    from signprot.interactions import get_generic_numbers, get_signature_consensus
    
    signature = signature_dict["signature"]

    sig_data = signature.prepare_display_data()
    gn = get_generic_numbers(sig_data)
    gn_flat = list(chain.from_iterable(gn))

    signature_dict["consensus"] = get_signature_consensus(sig_data, gn_flat)
    return signature_dict


def aggregate_consensus_data(entry, origin=None):
    data = []
    consensus = entry["consensus"]
    rec_class = entry["rec_class"]
    gprot = entry["gprot"]
    while len(consensus) > 0:
        a = consensus.pop()
        a["gprot"] = gprot
        a["rec_class"] = rec_class
        a["origin"] = origin
        data.append(a)
    return data


def summarize_df(df):
    print("Dataframe description:")
    display(df.describe())
    print("\n")

    print("Dataframe size:")
    print(df.shape)
    print("\n")

    display(df.head())


def show_group_top_n(df, group='feature', n=5):
    count_col = "{}_count".format(group)
    print(count_col)
    d1 = df.groupby(group)[group].agg(
        {count_col: len}).sort_values(
        count_col, ascending=False).head(n).reset_index()

    display(d1)


def compare_sets(
    df1, df2, method=set.intersection, drop_list=["origin", "key", "score", "cons"]
):
    v_ds1 = df1.drop(drop_list, 1)
    v_ds2 = df2.drop(drop_list, 1)
    colnames = v_ds1.columns

    summarize_df(v_ds1)
    summarize_df(v_ds2)

    ds1 = set([tuple(line) for line in v_ds1.values])
    ds2 = set([tuple(line) for line in v_ds2.values])

    comp = pd.DataFrame(list(method(ds1, ds2)))
    try:
        comp.columns = colnames
        return comp
    except ValueError as e:
        print("Value Error\n{}:\nNo entries overlap between the two sets.".format(e))


# import cPickle as pickle
def pickle_signature(data, path, filename):


    with open(path+filename, 'wb+') as out_file:

        p = pickle.Pickler(out_file)
        p.fast = True
        p.dump(data) # d is your dictionary
        p.clear_memo()

        # pickle.dump(data, out_file)


def load_pickle_signature(path, result_file, which, with_type):
    if with_type == 0:
        wt = 'file_with'
    elif with_type == 1:
        wt = 'file_wo'
    else:
        print('Pick either 0 for "file_with" or 1 for "file_wo" column')
        return

    file_path = Path(path + result_file.iloc[which][wt])
    with file_path.open('rb') as f:
        obj = pickle.load(f)

    return obj


def consensus_to_dataframe(entry):
    data = []
    consensus = entry['consensus']
    rec_class = entry['rec_class']
    gprot = entry['gprot']
    while len(consensus) > 0:
        a = consensus.pop()
        a['gprot'] = gprot
        a['rec_class'] = rec_class
        data.append(a)

    ds1 = pd.DataFrame(data)
    return ds1


