import stumpy
import numpy as np

def read_lc(lc_filename):
    date_time = []
    flux, f_err, mR, m_err, Az, El = np.genfromtxt(filename, skip_header=True, usecols=(6, 7, 8, 9, 10, 11),
                                                   unpack=True)
    date, time = np.genfromtxt(filename, unpack=True, skip_header=True, usecols=(0, 1), dtype=None,
                               encoding="utf-8")

    for i in range(0, len(date)):
        date_time.append(datetime.strptime(date[i] + ' ' + time[i] + "000", "%Y-%m-%d %H:%M:%S.%f"))

    # z = np.vstack((date_time, mR)).T
    z = np.column_stack((date_time, mR))

    return z



if __name__ == "__main__":
    your_time_series = read_lc("result_21798_20241110_UT175605.phV")
    # your_time_series = np.random.rand(3, 1000)  # Each row represents data from a different dimension while each column represents data from the same dimension
    window_size = 50  # Approximately, how many data points might be found in a pattern

    matrix_profile, matrix_profile_indices = stumpy.mstump(your_time_series, m=window_size)

    # TODO: what next ?
    # https://stumpy.readthedocs.io/en/latest/Tutorial_STUMPY_Basics.html
