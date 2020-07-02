"""Create a subcorpus:
* based on filenames that match a regex pattern
* based on metadata criteria
"""

import csv
import os
import re
import shutil

def create_subcorpus_based_on_fn(folder, outfolder, fn_pattern):
    """Create a subcorpus in `outfolder` of files from `folders` \
    of which the file names match the `fn_pattern`

    Args:
        folder (str): path to the i.stylo folder
        outfolder (str): path to the folder where the files should be copied to
        fn_pattern (str): a regex pattern that filenames should match
            to become part of the subcorpus
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    for root, dirs, files in os.walk(folder):
        for fn in files:
            if re.findall(fn_pattern, fn):
            #if fn_pattern in fn:
                fp = os.path.join(root, fn)
                outfp = os.path.join(outfolder, fn)
                shutil.copyfile(fp, outfp)
    print("Created subcorpus in", outfolder)


def create_subcorpus_based_on_metadata(meta, folder, outfolder, criteria={},
                                       silent=False, class_prefix=None):
    """
    Create a subcorpus based on metadata criteria.
    (texts need to match all criteria in order to be included in the subcorpus)
    
    criteria examples:
        {"tags": "CENTURY01|SHICR"}
        {"tags": "CENTURY01|SHICR", "title": "ديوان"}
        {"date": "< 100 & >50", "status": "pri"}

    Args:
        meta (dict): metadata dictionary
            (k: url, v: dictionary containing all metadata for that text)
        folder (str): path to the i.stylo folder
        outfolder (str): path to the folder where the files should be copied to
        criteria (dict): only texts that match all criteria in the `criteria`
            dictionary will be copied into the subcorpus.
            The keys in the dictionary are the column titles of the metadata csv
            NB: make sure you don't have the same key twice in the dictionary!
        silent (bool): if False, the script will first print the files
            it would copy, before giving the user the choice
            whether or not to execute the proposed actions.
        class_prefix (str): if not None, the `class_prefix` string will be
            prepended to every filename
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    sel = []
    for url, d in meta.items():
        select = []
        for k,v in criteria.items():
            #print(v)
            if ">" in v or "<" in v:
                for el in v.split("&"):
                    if not eval(str(int(d[k]))+el):
                        select.append(False)
                        break
            else:
                if not re.findall(v, d[k]):
                    select.append(False)
                    break
        if not False in select:
            #sel[url.split("/")[-1]] = uri2fn(d["versionUri"])
            sel.append(uri2fn(d["versionUri"]))
    copy_to_folder(sel, folder, outfolder, silent, class_prefix)


def uri2fn(uri):
    """Make the stylo-style fn out of the uri."""
    fn = uri.split("-")[0]
    fn = "{}_{}-{}".format(*fn.split("."))
    return fn


def load_metadata(meta_fp):
    """Load metadata csv into a dictionary \
    (k: url, v: dictionary containing all metadata for that text)"""
    with open(meta_fp, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")
        meta = {row["url"]: row  for row in reader}
        for k in meta:
            meta[k]["stylo_fn"] = uri2fn(meta[k]["versionUri"])
    return meta


def copy_to_folder(sel, folder, outfolder, silent, class_prefix):
    """Copy the selected files to another folder.

    Args:
        sel (list): list of filenames to be copied
        silent (bool): if False, the script will first print the files
            it would copy, before giving the user the choice
            whether or not to execute the proposed actions.
        class_prefix (str): if not None, the `class_prefix` string will be
            prepended to every filename
    """
    #for fn, outfn in fn_dict.items():
    for fn in sel:
        fp = os.path.join(folder, fn)
        if class_prefix:
            outfn = class_prefix + "_" + fn
        outfp = os.path.join(outfolder, outfn)
        if silent:
            shutil.copyfile(fp, outfp)
        else:
            print(fp, ">", outfp)        
    if silent:
        print("Copied {} texts to folder {}".format(len(sel), outfolder))
    else:
        msg = "Do you want to copy these {} texts to folder {}? Y/N "
        msg = msg.format(len(sel), outfolder)
        resp = input(msg)
        if resp in "yY":
            copy_to_folder(sel, folder, outfolder, True, class_prefix)




if __name__ == "__main__":
    folder = "data"
    outfolder = "../Tabari2/corpus"
    fn_pattern = "0310Tabari"
    #create_subcorpus_based_on_fn(folder, outfolder, fn_pattern)
    meta_fp = "OpenITI_metadata_light.csv"
    meta = load_metadata(meta_fp)
    criteria = {"tags": "SHICR", "title": "ديوان"}
    criteria = {"url": "0310Tabari", "status": "pri"}
    create_subcorpus_based_on_metadata(meta, folder, outfolder, criteria,
                                       silent=False, class_prefix="test")
    
