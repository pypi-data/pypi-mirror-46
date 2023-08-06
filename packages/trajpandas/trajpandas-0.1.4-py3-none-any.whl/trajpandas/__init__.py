__version__ = "0.1.1"

import os
import glob
from collections import OrderedDict as odict
import warnings

import numpy as np
import pandas as pd
from scipy.interpolate import interpn

from trajpandas.io.trm import read_bin as read_trm
from trajpandas.utils.grid import heatmat

from pandas import *




@pd.api.extensions.register_dataframe_accessor("traj")
class TrajAccessor(object):
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        if len(pandas_obj) == 0:
            raise pd.errors.EmptyDataError("No Trajectory data")
        for key in ["id", "xpos", "ypos"]:
            if not key in self._obj:
                raise KeyError(f"The row '{key}' is missing.")

    def setup_grid(self,latmat, lonmat):
        """Provide infomation about the GCM grid used to advect particles"""
        self.jmt,self.imt = latmat.shape
        self.latmat = latmat
        self.lonmat = lonmat

    def add_latlon(self, latmat=None, lonmat=None):
        if latmat is None:
            latmat = self.latmat
        if lonmat is None:
            lonmat = self.lonmat
        ijtup = (np.arange(lonmat.shape[0]),np.arange(lonmat.shape[1]))
        xyarr = self._obj[["ypos","xpos"]].values
        xyarr[xyarr<0] = 0
        self._obj["lon"] = interpn(ijtup, lonmat, xyarr).astype(np.float32)
        self._obj["lat"] = interpn(ijtup, latmat, xyarr).astype(np.float32)

    def add_age(self):
        """Calculate the age since release for all postions in trdf"""
        age = lambda jd: jd - jd.iloc[0]
        self._obj["_index_time"] = self._obj.index
        self._obj["age"] = self._obj.groupby("id")["_index_time"].transform(age)
        del self._obj["_index_time"]

    def add_delta(self, rowname=None, Dxy=False):
        """Calculate DChl from traj dataframe"""
        #if rowname not in self._obj.keys():
        #    raise KeyError(f"The row '{rowname}' is not in the Dataframe")
        if type(rowname)==str:
            rowlist = ["time", rowname]
        elif type(rowname) is None:
            rowlist = ["time",]
        else:
            rowlist = ["time",]+rowname
        self._obj["time"] = self._obj.index
        if Dxy:
            rowlist += ["xpos", "ypos"]
        self._objd = self._obj[["id",] + rowlist].groupby("id").transform(
            lambda x: x.diff())
        for fn in rowlist:
            self._obj[f"D{fn}"] = self._objd[fn]

    #@need_grid_info
    def add_dist(self, cummulative=False):
        """Calculate distances along all positions along all trajs."""
        if not hasattr(self._obj, 'lon'):
            self.add_latlon()
        
        ll2 = self._obj
        dll = ll2.groupby("id")[["lat","lon"]].transform(lambda x: x.diff())
        ll1 = ll2.groupby("id")[["lat","lon"]].transform(
            lambda x: np.append(np.zeros(1), x[:-1]) )
        radius = 6371 * 1000  # m
        a = (np.sin(np.deg2rad(dll["lat"])/2)**2 +
             np.cos(np.deg2rad(ll1["lat"])) * np.cos(np.deg2rad(ll2["lat"])) *
             np.sin(np.deg2rad(dll["lon"])/2)**2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        self._obj["dist"] = radius * c

        
    def add_speed(self, t2=False):
        """Calculate the speed in m/s of the particle. 

        Values are added to t=1 by default set t2 to True for t=2
        
        Examples:
        t2=False:
        time xpos ypos speed
        0    1.1  1.1  4.0
        1
        """
        if not hasattr(self._obj, "dist"):
            self.add_dist()
        if not hasattr(self._obj, "Dtime"):
            self._obj["time"] = self._obj.index
            Dtime = self._obj[["id","time"]].groupby("id").transform(
                lambda x: x.diff()).squeeze()
        else:
            Dtime = self._obj["Dtime"]
        self._obj["speed"] = (self._obj["dist"].values /
                              (Dtime.values.astype(int)/1e9))
        if not t2:
            self._obj["speed"] = (self._obj[["id","speed"]].
                                  groupby("id").
                                  transform(lambda x: np.roll(x,-1)))

    def need_grid_info(aFunc):
        """Check if grid inof is loaded."
        def bFunc( *args, **kw ):
            if not "x" in dir(args[0]):
                raise NameError, "Trajectory data not loaded."
            if len(args[0].x) == 0:
                raise ValueError, "Trajectory data empty."
            return aFunc( *args, **kw )
        bFunc.__name__ = aFunc.__name__
        bFunc.__doc__ = aFunc.__doc__
        return bFunc
    """

def piecewise_distance(latvec, lonvec):
    """Calculate the Haversine distance.
    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)
    Returns
    -------
    distance_in_km : float
    Examples
    --------
    >>> munich = (48.1372, 11.5756)
    >>> berlin = (52.5186, 13.4083)
    >>> round(haversine_distance(munich, berlin), 1)
    504.2
    >>> new_york_city = (40.712777777778, -74.005833333333)  # NYC
    >>> round(haversine_distance(berlin, new_york_city), 1)
    6385.3
    """
    radius = 6371  # km
    lat = np.deg2rad(latvec)
    lon = np.deg2rad(lonvec)
    dlat = lat[1:] - lat[:-1]
    dlon = lon[1:] - lon[:-1]
    dist = latvec * 0
    a = np.sin(dlat/2)**2 + np.cos(lat[:-1])*np.cos(lat[1:])*np.sin(dlon/2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    dist[1:] = radius * c
    return dist

def filter_by_len(df, traj_minlen=-np.inf, traj_maxlen=np.inf):
    """Remove trajectories longer and shorter limits"""    
    gr = df.groupby("id").filter(lambda x: len(x) >= traj_minlen)
    gr = gr.groupby("id").filter(lambda x: len(x) <= traj_maxlen)
    return gr

def interpolate(df, dt="1h", method="cubic", traj_minlen=7, limit=12):
    """Interpolate each trajectory to dt distances"""
    gr = filter_by_len(df, traj_minlen=traj_minlen)
    dd = gr.groupby("id").apply(
        lambda grp: grp.resample(dt).interpolate(method=method, limit=limit))
    if hasattr(dd, "id"):
        del dd["id"] 
    return dd.reset_index(level=0)

