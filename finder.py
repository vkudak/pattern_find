import sys
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import stumpy
from matplotlib import rcParams
from matplotlib.patches import Rectangle
from numba import cuda


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
    rcParams["figure.figsize"] = [18, 6]
    rcParams["xtick.direction"] = "in"
    # plt.style.use('https://raw.githubusercontent.com/TDAmeritrade/stumpy/main/docs/stumpy.mplstyle')

    # date_time, mag = read_lc("result_21798_20241110_UT175605.phV")
    # date_time, mag = read_lc("result_6275_20241110_UT170831.phB")
    date_time, mag = read_lc("result_22076_20240730_UT212240.phV")

    # plt.suptitle('Steamgen Dataset', fontsize='30')
    # plt.xlabel('Time', fontsize='20')
    # plt.ylabel('Steam Flow', fontsize='20')
    # plt.plot(date_time, mag)
    # plt.show()

    # sys.exit()
    date_time = [x.timestamp() for x in date_time]
    # time_series = z = np.column_stack((date_time, mag))

    d = {'time': date_time, 'mag': mag * -1}
    df = pd.DataFrame(data=d)

    # your_time_series = np.random.rand(3, 1000)  # Each row represents data from a different dimension while each column represents data from the same dimension
    window_size = 40  # Approximately, how many data points might be found in a pattern
    m = window_size


    # print(type(time_series))
    # mp, mp_indices = stumpy.mstump([df["time"].values, df["mag"].values], m=window_size)

    mp = stumpy.stump(df["mag"].values, m=window_size, k=50)

    # GPU
    # all_gpu_devices = [device.id for device in cuda.list_devices()]  # Get a list of all available GPU devices
    # mp = stumpy.gpu_stump(df["mag"].values, m=window_size, device_id=all_gpu_devices)

    # TODO: what next ?
    # https://stumpy.readthedocs.io/en/latest/Tutorial_STUMPY_Basics.html

    print(np.argsort(mp[:, 0]))
    print(mp[:, 0])

    # sys.exit()

    for motif_idx in np.argsort(mp[:, 0])[:3]:

        # motif_idx = np.argsort(mp[:, 0])[0]
        print(f"The motif is located at index {motif_idx}")

        # nearest_neighbor_idx = mp[motif_idx, 1]
        # print(f"XXX {mp[motif_idx]}")
        # print(f"The nearest neighbor is located at index {nearest_neighbor_idx}")
        # print(f"Second nearest neighbor is located at index {mp[motif_idx, 3]}")

        fig, axs = plt.subplots(2, sharex=True, gridspec_kw={'hspace': 0})
        plt.suptitle('Motif (Pattern) Discovery', fontsize='30')

        min_y = min(df["mag"].values)
        max_y = max(df["mag"].values)
        hy = max_y - min_y

        axs[0].plot(df['mag'].values)
        # axs[0].plot(date_time, mag)
        axs[0].set_ylabel('Steam Flow', fontsize='20')

        rect = Rectangle((motif_idx, min_y), m, height=hy, facecolor='lightgrey')
        axs[0].add_patch(rect)

        # for x in mp[motif_idx][1:]:
        for x in mp[motif_idx]:
            rect = Rectangle((x, min_y), m, height=hy, facecolor='lightgrey')
            axs[0].add_patch(rect)
            axs[1].axvline(x=x, linestyle="dashed")
        # rect = Rectangle((nearest_neighbor_idx, 0), m, 10, facecolor='lightgrey')
        # axs[0].add_patch(rect)

        axs[1].set_xlabel('Time', fontsize='20')
        axs[1].set_ylabel('Matrix Profile', fontsize='20')
        # axs[1].axvline(x=motif_idx, linestyle="dashed")
        # axs[1].axvline(x=nearest_neighbor_idx, linestyle="dashed")
        axs[1].plot(mp[:, 0])

        plt.tight_layout()
        plt.show()

        # https://stumpy.readthedocs.io/en/latest/Tutorial_Time_Series_Chains.html

        # plt.clf()
        plt.close()
