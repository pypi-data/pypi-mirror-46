# This file is part of wildboar
#
# wildboar is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wildboar is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

# Authors: Isak Karlsson
import numpy as np
import scipy.fftpack as fftpack


def average_distance_peak(i, k, t):
    before = t[max(0, i - k):i]
    after = t[i + 1:i + k + 1]
    max_before = np.max(t[i] - before) if before.size > 0 else t[i]
    max_after = np.max(t[i] - after) if after.size > 0 else t[i]
    return (max_before + max_after) / 2


def remove_random_frequencies(x, n=400, min_remove=1, max_remove=10):
    x_freq = fftpack.rfft(x)
    freqs = fftpack.rfftfreq(x.shape[0])
    X = np.empty((n, x_freq.shape[0]), dtype=np.float32)
    X_indicator = np.zeros((n, x_freq.shape[0] // 2))
    for i in range(n):
        size = np.random.randint(min_remove, max_remove)
        order = np.arange(x_freq.shape[0] // 2)
        np.random.shuffle(order)
        remove = order[:size]
        X[i, :] = x_freq
        X[i, remove] *= 1 * np.random.randn()
        X_indicator[i, remove] = 1

    print(freqs.shape)
    print(x_freq.shape)
    return fftpack.irfft(X, axis=1), X_indicator, freqs[:x_freq.shape[0] // 2]


if __name__ == "__main__":
    import matplotlib.pylab as plt
    print("Running tests")

    Fs = 128  # Sampling rate.
    Ts = 1 / Fs  # Sampling interval.
    Time = np.arange(0, 10, Ts)  # Time vector.
    signal = np.cos(4 * np.pi * Time) + np.cos(6 * np.pi * Time) + np.cos(
        8 * np.pi * Time)

    def spectrum(sig, t):
        """
        Represent given signal in frequency domain.
        :param sig: signal.
        :param t: time scale.
        :return:
        """
        print(t[1] - t[0])
        f = fftpack.rfftfreq(sig.size, d=t[1] - t[0])
        y = fftpack.rfft(sig)
        return f, np.abs(y)

    def bandpass(f, sig, min_freq, max_freq):
        """
        Bandpass signal in a specified by min_freq and max_freq frequency range.
        :param f: frequency.
        :param sig: signal.
        :param min_freq: minimum frequency.
        :param max_freq: maximum frequency.
        :return:
        """
        return np.where(np.logical_or(f < min_freq, f > max_freq), sig, 0)

    freq, spec = spectrum(signal, Time)
    print(freq)
    signal_filtered = fftpack.irfft(bandpass(freq, spec, 5, 7))

    print(signal_filtered)

    x = np.sin(np.linspace(0, 10, 100))

    freq, spec = spectrum(x, [0, 1])
    print(freq.shape, spec.shape)
    plt.plot(x)
    plt.show()
    X, X_ind, freqs = remove_random_frequencies(
        x, min_remove=95, max_remove=100)
    plt.plot(freqs)
    plt.plot(X[0])
    plt.show()
    diff = 3
    epsilon = 1
    x = np.array([-10, 0, 10, 1, -1, -1, -1, 5, 1, 1, -10])
    a = []
    for i in range(len(x)):
        a.append(average_distance_peak(i, diff, x))
    print(a)
    mean = np.mean(a)
    std = np.std(a)

    peak = []
    vale = []
    for i in range(len(x)):
        if a[i] > 0 and a[i] - mean > epsilon * std:
            peak.append(i)
        elif a[i] < 0 and a[i] - mean < epsilon * std:
            vale.append(i)

    ret = []
    k = 0
    while k < len(peak):
        if k == len(peak) - 1:
            ret.append(peak[k])
            break

        i = peak[k]
        j = peak[k + 1]
        print(i, j, abs(j - i), abs(j - i) <= diff)
        if abs(j - i) <= diff:
            ret.append(max(i, j))
            k += 2
        else:
            ret.append(i)
            k += 1

    print("peak", peak)
    print("vale", vale)
    print(ret)
