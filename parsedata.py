import json
import pandas
import matplotlib.pyplot as plt

import numpy as np

from scipy.special import logsumexp
from scipy.stats import invgamma


with open("output/toy_pf.json") as f:
    data_pf = json.load(f)

with open("output/toy_pgibbs.json") as f:
    data_pgibbs = json.load(f)

# with open("output/toy_pgas.json") as f:
#     data_pgas = json.load(f)

with open("output/toy_csmc.json") as f:
    data_csmc = json.load(f)

with open("output/toy_pmmh.json") as f:
    data_pmmh = json.load(f)

# Each entry is a Dict with
# - "lweight" : weights
# - "x" : states (a dict with "t" and "x")
# - "θ" : parameters (a dict with "sigma_x" and "sigma_y")
#         each parameter is a dict with "class", "α", and "β"
# - "y" : output

# Returns the mixture of Gamma distributions in the given dataset
def plot_inverse_gamma(json_dataset, x):

  weights = np.asarray([data["lweight"] for data in json_dataset]) # Extract weight vector
  weights = np.exp(weights - logsumexp(weights))

  s2x = np.zeros(x.size)
  s2y = np.zeros(x.size)

  for (i,w) in enumerate(weights):

    sigma2x = json_dataset[i]["θ"]["sigma_x"]
    alphax = sigma2x["α"]
    betax = sigma2x["β"]

    sigma2y = json_dataset[i]["θ"]["sigma_y"]
    alphay = sigma2y["α"]
    betay = sigma2y["β"]

    s2x += w*invgamma.pdf(x, alphax, scale=betax)
    s2y += w*invgamma.pdf(x, alphay, scale=betay)

  return s2x, s2y

# Get all the posteriors as mixtures of Gammas
s2 = np.linspace(2.0, 25.0, 200) # variance

s2x_pf, s2y_pf = plot_inverse_gamma(data_pf, s2)
s2x_csmc, s2y_csmc = plot_inverse_gamma(data_csmc, s2)


# Load the data for the Birch PG
s2x_pg = [data["θ"]["sigma_x"] for data in data_pgibbs[2:-1]]
s2y_pg = [data["θ"]["sigma_y"] for data in data_pgibbs[2:-1]]

# Load the data for the Birch PG
s2x_pg = [data["θ"]["sigma_x"] for data in data_pmmh[2:-1]]
s2y_pg = [data["θ"]["sigma_y"] for data in data_pmmh[2:-1]]

# Load the data for the Birch PG
#s2x_pgas = [data["θ"]["sigma_x"] for data in data_pgas[2:-1]]
#s2y_pgas = [data["θ"]["sigma_y"] for data in data_pgas[2:-1]]

(figure, axes) = plt.subplots(2, 1)

axes[0].plot(s2, s2x_pf)
axes[0].hist(s2x_pg, bins=20, density=1)
#axes[0].hist(s2x_pgas, bins=20, density=1)
axes[1].plot(s2, s2y_pf)
axes[1].hist(s2y_pg, bins=20, density=1)
#axes[1].hist(s2y_pgas, bins=20, density=1)

plt.show()
