import datetime
import sys

import stumpy
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as dates
from matplotlib.patches import Rectangle
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


if __name__ == "__main__":
    date_time, mag = read_lc("result_21798_20241110_UT175605.phV")

    # plt.suptitle('Steamgen Dataset', fontsize='30')
    # plt.xlabel('Time', fontsize='20')
    # plt.ylabel('Steam Flow', fontsize='20')
    # plt.plot(date_time, mag)
    # plt.show()

    # sys.exit()
    date_time = [x.timestamp() for x in date_time]
    # time_series = z = np.column_stack((date_time, mag))

    d = {'time': date_time, 'mag': mag}
    df = pd.DataFrame(data=d)

    # your_time_series = np.random.rand(3, 1000)  # Each row represents data from a different dimension while each column represents data from the same dimension
    window_size = 50  # Approximately, how many data points might be found in a pattern
    m = window_size


    # print(type(time_series))
    # mp, mp_indices = stumpy.mstump([df["time"].values, df["mag"].values], m=window_size)

    mp = stumpy.stump(df["mag"].values, m=window_size)

    # TODO: what next ?
    # https://stumpy.readthedocs.io/en/latest/Tutorial_STUMPY_Basics.html

    motif_idx = np.argsort(mp[:, 0])[0]
    print(f"The motif is located at index {motif_idx}")

    nearest_neighbor_idx = mp[motif_idx, 1]
    print(f"The nearest neighbor is located at index {nearest_neighbor_idx}")

    fig, axs = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0})
    plt.suptitle('Motif (Pattern) Discovery', fontsize='30')

    axs[0].plot(df['mag'].values)
    # axs[0].plot(date_time, mag)
    axs[0].set_ylabel('Steam Flow', fontsize='20')
    rect = Rectangle((motif_idx, 0), m, 10, facecolor='lightgrey')
    axs[0].add_patch(rect)
    rect = Rectangle((nearest_neighbor_idx, 0), m, 10, facecolor='lightgrey')
    axs[0].add_patch(rect)
    axs[1].set_xlabel('Time', fontsize='20')
    axs[1].set_ylabel('Matrix Profile', fontsize='20')
    axs[1].axvline(x=motif_idx, linestyle="dashed")
    axs[1].axvline(x=nearest_neighbor_idx, linestyle="dashed")
    axs[1].plot(mp[:, 0])
    plt.show()


    # https://stumpy.readthedocs.io/en/latest/Tutorial_Time_Series_Chains.html
