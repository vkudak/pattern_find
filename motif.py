from matplotlib import pyplot as plt
import numpy as np
import matrixprofile as mp
from datetime import datetime

# Need python 3.9 !!!!!!!!!!!!!!!!!!


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


dataset = mp.datasets.load('motifs-discords-small')
ts = dataset['data']

date_time, mag = read_lc("result_22076_20240730_UT212240.phV")
# date_time = [x.timestamp() for x in date_time]
# d = {'time': date_time, 'mag': mag * -1}
# ts = pd.DataFrame(data=mag*-1)
ts = mag

# plt.figure(figsize=(18, 5))
# plt.plot(np.arange(len(ts)), ts)
# plt.title('Synthetic Time Series')
# plt.show()


profile, figures = mp.analyze(ts, windows=70, n_jobs=5, threshold=0.75)

plt.show()
