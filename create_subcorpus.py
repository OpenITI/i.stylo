"""Create a subcorpus:
* based on filenames that match a regex pattern
* based on metadata criteria
"""

import csv
import os
import re
import shutil

def create_subcorpus(folder, outfolder, fn_pattern):
    """Create a subcorpus in `outfolder` of files from `folders` \
    that match the `fn_pattern`

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


def uri2fn(uri):
    """Make the stylo-style fn out of the uri."""
    fn = uri.split("-")[0]
    fn = "{}_{}-{}".format(*fn.split("."))
    return fn


def create_subcorpus_based_on_metadata(meta_fp, folder, outfolder, criteria={}, execute=False):
    """
    Create a subcorpus based on metadata criteria.
    (texts need to match all criteria in order to be included in the subcorpus)
    
    criteria examples:
        {"tags": "CENTURY01|SHICR"}
        {"tags": "CENTURY01|SHICR", "title": "ديوان"}
        {"date": "< 100 & >50"}
    """
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    with open(meta_fp, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter="\t")
        meta = {row["url"]: row  for row in reader}
        for k in meta:
            meta[k]["stylo_fn"] = uri2fn(meta[k]["versionUri"])
    sel = dict()
    for url, d in meta.items():
        select = []
        for k,v in criteria.items():
            #print(v)
            if ">" in v or "<" in v:
                for el in v.split("&"):
                    #print(str(int(d[k]))+el, eval(str(int(d[k]))+el))
                    if not eval(str(int(d[k]))+el):
                        select.append(False)
                        break
            else:
                if not re.findall(v, d[k]):
                    select.append(False)
                    break
        if not False in select:
            sel[url.split("/")[-1]] = uri2fn(d["versionUri"])
    for fn, outfn in sel.items():
        fp = os.path.join(folder, outfn)
        outfp = os.path.join(outfolder, outfn)
        if execute:
            shutil.copyfile(fp, outfp)
        else:
            print(fp, ">", outfp)
        

if __name__ == "__main__":
    folder = "data"
    outfolder = "../GRAR/Galen2/corpus"
    fn_pattern = "Jalinus"
    #create_subcorpus(folder, outfolder, fn_pattern)
    meta_fp = "OpenITI_metadata_light.csv"
    criteria = {"tags": "SHICR", "title": "ديوان"}
    criteria = {"date": "< 100 & > 50"}
    create_subcorpus_based_on_metadata(meta_fp, folder, outfolder, criteria)
    
