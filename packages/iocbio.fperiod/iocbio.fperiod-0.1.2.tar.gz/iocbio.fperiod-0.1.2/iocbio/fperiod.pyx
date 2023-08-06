import numpy as np
cimport numpy as np
cimport cython

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

cdef extern from "libfperiod.h":
    double iocbio_fperiod(double *f, int n, int m, double initial_period, int detrend, int method)

cdef double fperiod_worker(np.ndarray[DTYPE_t, ndim=2, mode="c"] data, double initial_period, int detrend, int method):
    return iocbio_fperiod(&data[0,0], data.shape[1], data.shape[0], initial_period, detrend, method)

def fperiod(data, initial_period, detrend, method):
    return fperiod_worker(data.astype(np.float64), initial_period, detrend, method)
        
