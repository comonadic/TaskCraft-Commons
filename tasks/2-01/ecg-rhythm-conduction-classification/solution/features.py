import numpy as np
from scipy.signal import welch
import wfdb
def features(path):
    x=wfdb.rdrecord(str(path)).p_signal
    f,p=welch(x,fs=100,nperseg=256,axis=0)
    bands=[]
    for lo,hi in [(0,.5),(.5,2),(2,5),(5,10),(10,20),(20,40)]:bands.extend(np.log1p(p[(f>=lo)&(f<hi)].sum(axis=0)).tolist())
    return np.r_[np.quantile(x,[.01,.1,.25,.5,.75,.9,.99],axis=0).ravel(),x.std(axis=0),np.mean(np.abs(np.diff(x,axis=0)),axis=0),bands]
