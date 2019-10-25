#!/usr/bin/python
"""Processing of the simulation data"""
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

from scipy.stats import invgamma

def load_data(filename, burnin=50):
    s2x = []
    s2y = []
    with open(filename, 'r') as f:
        data = json.load(f)
        a = 0
        for i, d in enumerate(data[burnin:-1]):
            if i == 0:
                prev = np.array([x["x"] for x in d["x"]])
            else:
                curr = np.array([x["x"] for x in d["x"]])
                a += prev == curr
                prev = curr
            if isinstance(d["θ"]["sigma_x"], dict):
                sigma2x = d["θ"]["sigma_x"]
                sigma2y = d["θ"]["sigma_y"]
                s2x.append(invgamma.rvs(sigma2x["α"], scale=sigma2x["β"]))
                s2y.append(invgamma.rvs(sigma2y["α"], scale=sigma2y["β"]))
            else:
                s2x.append(d["θ"]["sigma_x"])
                s2y.append(d["θ"]["sigma_y"])
        updatefreq = 1 - a/(len(data) - burnin)
    return s2x, s2y, updatefreq


def corr(x, n_lags):
    N = len(x)
    autocorr = np.zeros(n_lags)

    mu = np.mean(x)

    for k in range(n_lags):
        autocorr[k] = np.dot(x[k:] - mu, x[:N-k] - mu)/(N-k)
    autocorr /= autocorr[0]
    return autocorr

import multiprocessing as mp

if __name__ == "__main__":

    input_folder = "output/"
    file_mpg_50 = input_folder + "toy_simulation_50_mpg.json"
    file_pg_50 = input_folder + "toy_simulation_50_pg.json"
    file_mpg_500 = input_folder + "toy_simulation_50_mpgas.json"
    file_pg_500 = input_folder + "toy_simulation_50_pgas.json"

    files = [file_mpg_50, file_pg_50, file_mpg_500, file_pg_500]

    with mp.Pool(mp.cpu_count()) as pool:
        mpg_50, pg_50, mpg_500, pg_500 = pool.map(load_data, files)

    fig, axes = plt.subplots(1,4)
    for data, label, ax in zip([mpg_50, pg_50, mpg_500, pg_500], ['mPG 50', 'PG 50', 'mPGAS 50', 'PGAS 50'], axes):
        ax.hist(data[0], alpha=0.5, density=True, label=label)
        ax.hist(data[1], alpha=0.5, density=True, label=label)
        ax.plot([10.0, 10.0], [0.0, 1.0])
        ax.plot([1.0, 1.0], [0.0, 1.0])
        ax.legend()
    plt.savefig('histograms_toy_simulation.png')
    plt.show()

    fig, axes = plt.subplots(4,1)
    for data, label, ax in zip([mpg_50, pg_50, mpg_500, pg_500], ['mPG 50', 'PG 50', 'mPGAS 50', 'PG 50'], axes):
        ax.plot(data[0], label=label)
        ax.plot(data[1], label=label)
        ax.plot([0.0, 10000.0], [10.0, 10.0])
        ax.plot([0.0, 10000.0], [1.0, 1.0] )
        ax.legend()
    plt.savefig('traces_toy_simulation.png')
    plt.show()

    fig, axes = plt.subplots(4,1)
    for data, label, ax in zip([mpg_50, pg_50, mpg_500, pg_500], ['mPG 50', 'PG 50', 'mPGAS 50', 'PGAS 50'], axes):
        corrx = corr(data[0], 40)
        corry = corr(data[1], 40)
        ax.plot(corrx, label=label)
        ax.plot(corry, label=label)
        ax.legend()
    plt.savefig('autocorr_toy_simulations.png')
    plt.show()
