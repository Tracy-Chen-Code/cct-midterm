# debug with help of chatgpt o4-mini-high

import numpy as np, pandas as pd, pymc as pm, arviz as az
import matplotlib.pyplot as plt

# 1. setup data
def load_csv(path):
    df = pd.read_csv(path)
    return df.iloc[:, 1:].astype(int).values     

X = load_csv("/home/jovyan/project/cct-midterm/data/plant_knowledge.csv")
N, M = X.shape

# 2. PyMC model
with pm.Model() as model:
    D = pm.Uniform("D", 0.5, 1, shape=N)
    Z = pm.Bernoulli("Z", 0.5, shape=M)
    p = Z * D[:, None] + (1 - Z) * (1 - D[:, None])
    pm.Bernoulli("X", p=p, observed=X)
    trace = pm.sample(2000, chains=4, tune=1000, target_accept=0.9)

# 3. result
pd.set_option('display.max_rows', None, 'display.max_columns', None,
                  'display.width', None, 'display.max_colwidth', None)
np.set_printoptions(threshold=np.inf, linewidth=200)
print(az.summary(trace, var_names=["D", "Z"]))
az.plot_posterior(trace, var_names=["D"])
plt.tight_layout()
plt.savefig("/home/jovyan/project/cct-midterm/code/competence_posterior.png")  
plt.close()
az.plot_posterior(trace, var_names=["Z"])
plt.tight_layout()
plt.savefig("/home/jovyan/project/cct-midterm/code/consensus_posterior.png")
plt.close()
D_mean = trace.posterior["D"].mean(("chain", "draw")).values
Z_mean = trace.posterior["Z"].mean(("chain", "draw")).values
Z_key  = (Z_mean >= 0.5).astype(int)
majority = (X.mean(axis=0) >= 0.5).astype(int)
print("CCT key:", Z_key)
print("Majority:", majority)
