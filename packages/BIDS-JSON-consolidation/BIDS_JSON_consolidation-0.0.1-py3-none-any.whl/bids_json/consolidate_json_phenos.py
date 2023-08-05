#!/usr/bin/env python

import sys, os
import os.path
import csv
import json
import glob

from datetime import datetime
from datetime import date

import argparse

import pdb

today = date.today().isoformat()


def common_mrigenie_phenotypes():
    """Return the set of phenotypes that are requested with the '-c,--common'
    parameter
    """
    phenotypes = [
        "Site_id", # TODO should be ID not id
        "Age",
        "Sex",
        "HTN",
        "AF",
        "CAD",
        "DM",
        "Smoking_status",
        "First_stroke",
        "Ethnicity",
        "Race",
        "WMH_volume",
        "Brain_volume",
        "No_csf_brain_vol",
        "Ventricle_volume",
        "Ventricle_volume_manual",
        "TOAST",
        "NIHSS",
        "MRS"
    ]
    return phenotypes


# TODO could be cleaner
def get_pheno(_dict, _item):
    # handle phenotypes with only 1 common name
    if type(_item) is not tuple:
        if _item in _dict.keys() and 'volume' not in _item:
            return str(_dict[_item])
        elif 'volume' in _item and 'cc' not in _item:
            return get_pheno_volume(_dict, _item)
        else:
            return 'NA'

    # handle phenotypes with multiple 'synonyms'
    vals = [None] * len(_item)
    for idx, synonym in enumerate(_item):
        if synonym not in _dict.keys():
            vals[idx] = 'NA'
            continue

        if 'volume' in synonym: #if synonym.split('_')[1].lower() == 'volume':
            vals[idx] = get_pheno_volume(_dict, synonym)
        else:
            vals[idx] = _dict[synonym]
    return first_not_missing(vals)


def get_pheno_volume(_dict, _synonym):
    """Get the volume for a given phenotype"""
    # current setup, return the manual volume if we are asking for DWI volume or a manual volume,
    # e.g. Brain_volume_manual or DWI_volume
    #if _synonym.split('_')[0] == 'DWI' or _synonym.split('_')[-1].lower() == 'manual':
    if 'manual' in _synonym:
        #set_trace()
        _synonym = '_'.join(_synonym.split('_')[:-1]) # everything except last item after last _
        # set_trace()
        _value = _dict[_synonym]['Manual']['Volume']
    else:
        _value = _dict[_synonym]['Automated']['Volume']
    return _value


def first_not_missing(val_set):
    """Return the first value in a list that is not 'NA', otherwise return 'NA'"""
    found = 'NA'
    for val in val_set:
        if val != 'NA' and val != '' and val != ' ' and val is not None:
            found = val
            break
    return found


def format_data(val):
    try:
        return(float(val))
    except:
        return(val)


def main(args=None, parser=None):
    if args is None and parser is None:
        phenotype_list = input('Enter phenotypes for dict: ')
        json_base = input('Enter file path base for JSON files: ')
        output = input('Enter output file name: ')
        subject_list = False
        common_phenotypes = False

        phenotype_list = phenotype_list.split()
        args = argparse.Namespace(
            common_phenotypes=common_phenotypes, json_base=json_base, subject_list=subject_list, phenotype_list=phenotype_list, output=output
        )

    if args.common_phenotypes:
        phenotypes = common_mrigenie_phenotypes()
    elif args.phenotype_list:
        phenotypes = args.phenotype_list
    else:
        print("\nPlease specify phenotypes with '-a/--all' or '-p/--phenotypes-list'\n")
        print(parser.print_help())
        sys.exit(1)

    # image base
    if args.json_base:
        json_base = args.json_base
    else:  # default
        json_base = "/data/triangulum/Data/MRIGenie_bids/nifti"

    # subject list
    if args.subject_list:
        with open(args.subject_list) as subf:
            sub_list = [line.rstrip() for line in subf]
    else:
        sub_list = None

    # output csv file
    if args.output is not None:
        output = args.output

    print(f"phenotypes: %s"%phenotypes)
    print(f"output: %s"%output)

    header = ["Subject_ID"]
    header.extend(phenotypes)

    all_sub_phenos = []
    all_subs_dict = {}

    for subject in glob.glob(f"%s/*"%json_base):
        sub_id = os.path.basename(subject)

        # skip if we only want specific subjects
        if sub_list and sub_id not in sub_list:
            continue

        print(f"processing %s ..."%sub_id)
        with open(f"%s/%s.json"%(subject,sub_id)) as jsonf:
            subdict = json.load(jsonf)

        phenos = [get_pheno(subdict, pheno) for pheno in phenotypes]

        # for dict format
        sub_pheno_dict = {pheno:format_data(value) for pheno,value in zip(phenotypes,phenos)}
        all_subs_dict[int(sub_id)] = sub_pheno_dict

        if output:
            # for csv
            phenos.insert(0, sub_id) # add subject ID to beginning of list
            all_sub_phenos.append(phenos)

    # TODO implement this and previous better
    if output:
        with open(output, "w") as outf:
            str_header = ",".join(header)
            outf.write(f"%s\n"%str_header)
            for line in all_sub_phenos:
                str_line = ",".join(line)
                outf.write("%s\n"%str_line)

    return all_subs_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--common-phenotypes", action="store_true", help="add all common phenotypes to your csv"
    )
    parser.add_argument(
        "-j", "--json-base",
        help="the deepest location of commonality of the json files just before the subject ids: \
                default: /data/triangulum/Data/MRIGenie_bids/nifti"
    )
    parser.add_argument(
        "-s", "--subject-list",
        help="optional: the ids of the subjects to extract data from, default: all MRI-GENIE subjects' data. \
                argument is a csv with one column of each subject to be included in the final csv output"
    )
    parser.add_argument(
        "-p", "--phenotype-list", nargs="+", help="a white space separated list of the phenotypes you want in your csv. If a phenotype contains white space, enclose it in quotations"
    )
    parser.add_argument(
        "-o", "--output", help="the name of your csv output file"
    )
    args = parser.parse_args()
    main(args, parser)
