"""Create a subcorpus of filenames that match a regex pattern"""

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
            
if __name__ == "__main__":
    folder = "."
    outfolder = "../GRAR/Galen/corpus"
    fn_pattern = "Jalinus"
    create_subcorpus(folder, outfolder, fn_pattern)
    
