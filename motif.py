from matplotlib import pyplot as plt
import numpy as np
import matrixprofile as mp
from datetime import datetime


def read_lc(lc_filename):
    date_time = []
    flux, f_err, mR, m_err, Az, El = np.genfromtxt(lc_filename, skip_header=True, usecols=(6, 7, 8, 9, 10, 11),
                                                   unpack=True)
    date, time = np.genfromtxt(lc_filename, unpack=True, skip_header=True, usecols=(0, 1), dtype=None,
                               encoding="utf-8")

    for i in range(0, len(date)):
        date_time.append(datetime.strptime(date[i] + ' ' + time[i] + "000", "%Y-%m-%d %H:%M:%S.%f"))

    # z = np.vstack((date_time, mR)).T
    # z = np.column_stack((date_time, mR))

    return date_time, mR


# https://matrixprofile.docs.matrixprofile.org/index.html
