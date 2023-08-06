
import numpy as np
import pandas as pd

import trajpandas


def loops():
    index = pd.date_range(start="2018-01-01", end="2018-01-10",freq="4h")
    dflist = []
    for num in range(1,8):
        tpos = np.linspace(0, np.pi*5, len(index))
        xpos = (np.sin(tpos) + tpos*0.1*num)
        ypos = (np.cos(tpos) * 3) +8
        trid = (xpos * 0 + num).astype(int)
        df = pd.DataFrame(index=index, data={"id":trid,"xpos":xpos,"ypos":ypos})
        dflist.append(df)
    df = pd.concat(dflist)
    df.sort_index(inplace=True)

    llat,llon = np.mgrid[35:35.05:0.001, -55:-54.95:0.001]
    df.traj.setup_grid(llat, llon)
    df.traj.add_latlon()
    return df

def straight_line():
    index = pd.date_range(start="2018-01-01", end="2018-01-02",freq="1h")
    lon  = np.arange(-20,-20+(1/60)*25,1/60)[:25]
    xpos = np.arange(1,26)
    def dfline(trid, ypos, lat):
        return pd.DataFrame({"id":trid,
            "xpos":xpos, "ypos":ypos, "lon":lon, "lat":lat}, index=index)

    df1 = dfline(1, np.arange(60,60+25), 60)
    df2 = dfline(2, np.arange(45,45+25), 45)
    df3 = dfline(3, np.arange(30,30+25), 30)
    return pd.concat([df1,df2,df3]).sort_index()

def one_mile():
     index = pd.date_range(start="2018-01-01", end="2018-01-02",freq="1h")[:2]
     xpos = [1,1]
     ypos = [1,2]
     lat  = [30,30+1/60]
     lon  = [0,0]
     return pd.DataFrame(
         {"id":1, "xpos":xpos, "ypos":ypos, "lon":lon, "lat":lat}, index=index)
