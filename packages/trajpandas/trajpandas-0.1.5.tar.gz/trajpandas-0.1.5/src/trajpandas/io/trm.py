
import os
import glob
from collections import OrderedDict as odict

import numpy as np
import pandas as pd

def read_bin(filename, count=-1, keep_2D_zpos=False):
    """Read TRACMASS binary file"""
    dtype = np.dtype([('id',  'i4'), ('jd',  'f8'),
		      ('xpos','f4'), ('ypos','f4'),
		      ('zpos','f4')])
    runtraj = np.fromfile(open(filename), dtype, count=count)
    dt64 = ((runtraj["jd"])*24*60*60-62135683200).astype("datetime64[s]")
    df = pd.DataFrame(data={"id":runtraj["id"],
                            "xpos":runtraj["xpos"]-1,
                            "ypos":runtraj["ypos"]-1,
                            "zpos":runtraj["zpos"]-1},
                      index=pd.Series(dt64))
    if (not keep_2D_zpos) and (len(df["zpos"].unique())==1):
        del df["zpos"]
    df.sort_index(inplace=True)
    return df
   
