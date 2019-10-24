#!/usr/bin/python
"""Processing of the simulation data"""
import json
import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

from scipy.stats import invgamma


# Parameters
burnin = 100
input_folder = "output/"
file_mpgas = input_folder + "toy_mpgas.json"
file_pgas = input_folder + "toy_pgas.json"
file_mpg = input_folder + "toy_mpg.json"
#file_mpg = input_folder + "toy_simulation_50_mpg.json"
file_pg = input_folder + "toy_pg.json"
#file_pg = input_folder + "toy_simulation_50_pg.json"
autocorr_file = "data/autocorr_toy_model.csv"


# Load pgibbs data
s2x_pg = []
s2y_pg = []
with open(file_pg, "r") as f:
    data = json.load(f)
    a = 0
    for i, d in enumerate(data[burnin:-1]):
        if i == 0:
            prev = np.array([x["x"] for x in d["x"]])
        else:
            curr = np.array([x["x"] for x in d["x"]])
            a += prev == curr
            prev = curr
        s2x_pg.append(d["θ"]["sigma_x"])
        s2y_pg.append(d["θ"]["sigma_y"])
    updatefreq_pg = 1 - a/(len(data) - burnin)

s2x_pgas = []
s2y_pgas = []
with open(file_pgas, "r") as f:
    data = json.load(f)
    a = 0
    for i,d in enumerate(data[burnin:-1]):
        if i == 0:
            prev = np.array([x["x"] for x in d["x"]])
        else:
            curr = np.array([x["x"] for x in d["x"]])
            a += prev == curr
            prev = curr
        s2x_pgas.append(d["θ"]["sigma_x"])
        s2y_pgas.append(d["θ"]["sigma_y"])
    updatefreq_pgas = 1 - a/(len(data) - burnin)

# Load mpgibbs data
s2x_mpg = []
s2y_mpg = []
with open(file_mpg, "r") as f:
    data = json.load(f)
    a = 0
    for i,d in enumerate(data[burnin:-1]):
        if i == 0:
            prev = np.array([x["x"] for x in d["x"]])
        else:
            curr = np.array([x["x"] for x in d["x"]])
            a += prev == curr
            prev = curr
        sigma2x = d["θ"]["sigma_x"]  # Careful!
        sigma2y = d["θ"]["sigma_y"]  # Careful!
        s2x_mpg.append(invgamma.rvs(sigma2x["α"], scale=sigma2x["β"]))
        s2y_mpg.append(invgamma.rvs(sigma2y["α"], scale=sigma2y["β"]))
    updatefreq_mpg = 1 - a/(len(data) - burnin)

s2x_mpgas = []
s2y_mpgas = []
with open(file_mpgas, "r") as f:
    data = json.load(f)
    a = 0
    for i,d in enumerate(data[burnin:-1]):
        if i == 0:
            prev = np.array([x["x"] for x in d["x"]])
        else:
            curr = np.array([x["x"] for x in d["x"]])
            a += prev == curr
            prev = curr
        sigma2x = d["θ"]["sigma_x"]  # Careful!
        sigma2y = d["θ"]["sigma_y"]  # Careful!
        s2x_mpgas.append(invgamma.rvs(sigma2x["α"], scale=sigma2x["β"]))
        s2y_mpgas.append(invgamma.rvs(sigma2y["α"], scale=sigma2y["β"]))
    updatefreq_mpgas = 1 - a/(len(data) - burnin)


def corr(x, n_lags):
    N = len(x)
    autocorr = np.zeros(n_lags)

    mu = np.mean(x)

    for k in range(n_lags):
        autocorr[k] = np.dot(x[k:] - mu, x[:N-k] - mu)/(N-k)
    autocorr /= autocorr[0]
    return autocorr


print(len(s2x_pg))
print(len(s2x_pgas))
print(len(s2x_mpgas))
print(len(s2x_mpg))

n_lags = 100
corr_s2x_pg = corr(s2x_pg, n_lags)
corr_s2x_pgas = corr(s2x_pgas, n_lags)
corr_s2x_mpg = corr(s2x_mpg, n_lags)
corr_s2x_mpgas = corr(s2x_mpgas, n_lags)
corr_s2y_pg = corr(s2y_pg, n_lags)
corr_s2y_pgas = corr(s2y_pgas, n_lags)
corr_s2y_mpg = corr(s2y_mpg, n_lags)
corr_s2y_mpgas = corr(s2y_mpgas, n_lags)



# PLOTTING
def updatefreqplot():
    plt.plot(updatefreq_pg)
    plt.plot(updatefreq_pgas)
    plt.plot(updatefreq_mpg)
    plt.plot(updatefreq_mpgas)
    plt.legend(["PG","PGAS","mPG","mPGAS"])
    #plt.legend(["PG","mPG"])
    plt.savefig('updatefreq_toy_model.png')
    plt.show()

def autocorrplot():

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.plot(corr_s2x_pg)
    ax1.plot(corr_s2x_pgas)
    ax1.plot(corr_s2x_mpg)
    ax1.plot(corr_s2x_mpgas)
    ax1.set_xlabel("Lag")
    ax1.set_ylabel("Sigma2 x")
    ax1.legend(["PG", "mPG", "PGAS", "mPGAS"])
    #ax1.legend(["PG", "mPG"])

    ax2.plot(corr_s2y_pg)
    ax2.plot(corr_s2y_pgas)
    ax2.plot(corr_s2y_mpg)
    ax2.plot(corr_s2y_mpgas)
    ax2.set_xlabel("Lag")
    ax2.set_ylabel("Sigma2 y")
    ax2.legend(["PG", "mPG", "PGAS", "mPGAS"])
    #ax2.legend(["PG", "mPG"])
    plt.title("Toy model")

    plt.savefig("autocorr_toy_model.png")

    plt.show()


def traceplot():
    fig , (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(s2x_pg)
    ax1.plot(s2x_mpg)
    ax1.plot(s2x_pgas)
    ax1.plot(s2x_mpgas)
    ax1.legend(["PG","mPG", "PGAS", "mPGAS"])

    ax2.plot(s2y_pg)
    ax2.plot(s2y_mpg)
    ax2.plot(s2y_pgas)
    ax2.plot(s2y_mpgas)
    ax2.legend(["PG","mPG", "PGAS", "mPGAS"])

    plt.savefig("traces_toy_model.png")
    plt.show()


def histogramplot():
    #fig, (ax1, ax2, ax3, ax4) = plt.subplots(4,2)

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.hist(s2x_pg, alpha=0.5)
    ax1.hist(s2x_mpg, alpha=0.5)
    ax1.hist(s2x_pgas, alpha=0.5)
    ax1.hist(s2x_mpgas, alpha=0.5)
    ax1.legend(["PG","mPG", "PGAS", "mPGAS"])

    ax2.hist(s2y_pg, alpha=0.5)
    ax2.hist(s2y_mpg, alpha=0.5)
    ax2.hist(s2y_pgas, alpha=0.5)
    ax2.hist(s2y_mpgas, alpha=0.5)
    ax2.legend(["PG","mPG", "PGAS", "mPGAS"])
    #plt.hist(s2x_mpgas, alpha=0.5)
    # ax2.hist(s2y_pg)
    # ax2.hist(s2y_mpg)
    # ax2.legend(["PG","mPG"])
    # ax2.sel_xlabel("s2y")
    # ax2.hist(s2y_pg)
    # ax3.hist(s2x_pgas)
    # ax3.hist(s2x_mpgas)
    # ax3.legend(["PGAS","mPGAS"])
    # ax3.sel_xlabel("s2x")
    # ax4.hist(s2y_pgas)
    # ax4.hist(s2y_mpgas)
    # ax4.sel_xlabel("s2y")
    # ax4.legend(["PGAS","mPGAS"])
    plt.savefig("histograms_toy_model.png")
    plt.show()


def save():

    with open(autocorr_file, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["lag",
                         "s2x_PG",
                         "s2x_PGAS",
                         "s2x_mPG",
                         "s2x_mPGAS",
                         "s2y_PG",
                         "s2y_mPG",
                         "s2y_PGAS",
                         "s2y_mPGAS"])
        writer.writerows(zip(range(n_lags),
                             corr_s2x_pg,
                             corr_s2x_pgas,
                             corr_s2x_mpg,
                             corr_s2x_mpgas,
                             corr_s2y_pg,
                             corr_s2y_pgas,
                             corr_s2y_mpg,
                             corr_s2y_mpgas))


if __name__ == "__main__":
    updatefreqplot()
    histogramplot()
    traceplot()
    autocorrplot()
