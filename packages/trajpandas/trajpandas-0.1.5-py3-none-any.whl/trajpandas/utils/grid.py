
import numpy as np

def normalize_vec(vals, minval=None, maxval=None):
    """Normalize values in vec to 0-1 range"""
    minval = vals.min()   if minval is None else minval
    maxval = vals.max()+1 if maxval is None else maxval
    return (vals-minval) / (maxval-minval)
    
def general_heatmat(xvec, yvec, xsize=100, ysize=100,
            xmin=None, xmax=None, ymin=None, ymax=None):
    """Create a 2D heatmap showing densities of x-y combinations""" 
    mask = np.isfinite(xvec) & np.isfinite(yvec)
    xvec = xvec[mask]
    yvec = yvec[mask]
    xint = normalize_vec(xvec, xmin, xmax)
    yint = normalize_vec(yvec, ymin, ymax)
    mask = (xint>=0) & (xint<=1) & (yint>=0) & (yint<=1)
    xint = (xint[mask] * (xsize-1)).astype(int)
    yint = (yint[mask] * (ysize-1)).astype(int)
    ijvec = np.ravel_multi_index((xint,yint),(xsize,ysize))
    return np.bincount(ijvec, minlength=xsize*ysize).reshape(xsize,ysize).T


def heatmat(df, imax=None, jmax=None):
    """Create a 2D heatmap showing densities of x-y combinations"""
    xint = df.xpos.astype(np.int32)
    yint = df.ypos.astype(np.int32)
    if imax is None:
        if hasattr(df, "imax"):
            imax = df.imax
        else:
            imax = xint.max()+1
    if jmax is None:
        if hasattr(df, "jmax"):
            jmax = df.jmax
        else:
            jmax = yint.max()+1
    ijvec = np.ravel_multi_index((xint,yint),(imax,jmax))
    return np.bincount(ijvec, minlength=imax*jmax).reshape(imax,jmax).T
