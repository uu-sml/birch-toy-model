using JSON
using CSV
using StatsFuns
using Plots
using Distributions
pyplot()


data_pf = JSON.parsefile("output/toy_pf.json")
data_pgibbs = JSON.parsefile("output/toy_pgibbs.json")
data_csmc = JSON.parsefile("output/toy_csmc.json")
# Each entry is a Dict with
# - "lweight" : weights
# - "x" : states (a dict with "t" and "x")
# - "θ" : parameters (a dict with "sigma_x" and "sigma_y")
#         each parameter is a dict with "class", "α", and "β"
# - "y" : output



# Returns the mixture of Gamma distributions in the given dataset
function plot_inverse_gamma(json_dataset, x)

  weights = [data["lweight"] for data in json_dataset] # Extract weight vector
  weights = exp.(weights .- logsumexp(weights))

  s2x = zeros(length(x))
  s2y = zeros(length(x))

  for (i,w) in enumerate(weights);

    σ2x = json_dataset[i]["θ"]["sigma_x"]
    αx = σ2x["α"]
    βx = σ2x["β"]
    s2x += w.*pdf.(Distributions.InverseGamma(αx,βx), x)

    σ2y = json_dataset[i]["θ"]["sigma_y"]
    αy = σ2y["α"]
    βy = σ2y["β"]

    s2y += w.*pdf.(Distributions.InverseGamma(αy,βy), x)
  end

  return s2x, s2y
end


# Get all the posteriors as mixtures of Gammas
s2 = range(2.0, stop=100.0, length=200); # variance

s2x_pf, s2y_pf = plot_inverse_gamma(data_pf, s2);
s2x_csmc, s2y_csmc = plot_inverse_gamma(data_csmc, s2);

# Load the data from the simulation
data_cpp = CSV.read("data/data_cpp.csv"); # Contains standard deviations!
s2x_cpp = data_cpp[:sx_pg].^2
s2y_cpp = data_cpp[:sy_pg].^2

px = plot([2.3^2, 2.3^2], [0.0, 1.0], label="True")
plot!(px, s2, s2x_pf, label="PF")
plot!(px, s2, s2x_csmc, label="cSMC")
histogram!(px, s2x_cpp, normalize=:pdf, label="C++")
ylabel!("p(σ2x)")
xlabel!("σ2x")

py = plot([3.3^2, 3.3^2], [0.0, 1.0], label="True")
plot!(py, s2, s2y_pf, label="PF")
plot!(py, s2, s2y_csmc, label="cSMC")
histogram!(py, s2y_cpp, normalize=:pdf, label="C++")
ylabel!("p(σ2y)")
xlabel!("σ2y")

plot(px, py, layout=(2,1))
