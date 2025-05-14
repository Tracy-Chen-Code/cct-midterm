# cct-midterm
# This is the midterm project of COGS 107.

Report





Requirements

Objective
Implement the basic Cultural Consensus Theory (CCT) model using PyMC to analyze a small (fake) dataset concerning local plant knowledge. Estimate the consensus answers to the questions and the competence level of each informant.

Background
Cultural Consensus Theory (Romney, Weller & Batchelder, 1986) provides a framework for evaluating the extent to which cultural beliefs are shared within a group and for estimating individual differences in knowledge (competence). The core idea is that agreement between informants is proportional to their knowledge of a shared cultural consensus.

The Model
Let:

N be the number of informants.
M be the number of items (questions).
Xij be the response of informant i to item j (0 or 1).
Zj be the latent "consensus" or "correct" answer for item j (0 or 1).
Di be the latent "competence" of informant i (probability of knowing the correct answer), where 0.5 ≤ Di ≤ 1.
The model assumes that an informant's response Xij depends on their competence Di and the consensus answer Zj. Specifically, the probability that informant i gives the answer Zj for item j is Di. The probability they give the incorrect answer is 1 − Di.

This can be formulated as a Bernoulli likelihood: Xij∼ Bernoulli(pij)

Where the probability pij of informant i answering '1' for item j is: pij = Di if Zj = 1 pij = 1 − Di if Zj = 0

This can be written more compactly as: pij = Zj × Di + (1 − Zj) × (1 − Di)

Requirements
Load the Data
Load the "plant knowledgeLinks to an external site." dataset. Represent it appropriately (e.g., as a NumPy array or Pandas DataFrame, excluding the Informant ID column).
Write a custom function to load the data and return it.
Define Priors
For each informant's competence Di, choose a suitable prior distribution. Justify your choice in the report.
For each consensus answer Zj, choose a suitable prior. Since it's a binary value (0 or 1), a Bernoulli distribution is appropriate. A common choice reflecting minimal prior assumption is Bernoulli(0.5).
Implement the Model in PyMC
Create a PyMC model context (pm.Model()).
Define the priors for D (vector of size N) and Z (vector of size M).
Define the probability pij using the formula above.
You might need to reshape or broadcast D and Z appropriately to calculate p for all i and j.
For example, in my solution, the PyMC model had lines like this:
               D = pm.Uniform(...)
               Z = pm.Bernoulli(...)
               D_reshaped = D[:, None] 
               p = Z * D_reshaped + (1 - Z) * (1 - D_reshaped) 
Define the likelihood using pm.Bernoulli, linking the observed data X to the calculated probability p. Ensure the observed argument points to your data matrix.
Perform Inference
Use PyMC's MCMC sampler (e.g., pm.sample()) to draw samples from the posterior distribution. Use a reasonable number of draws and chains (e.g., 2000 draws per chain, 4 chains, potentially with tuning steps).
Analyze Results
Examine the convergence diagnostics (e.g., R-hat values from az.summary(trace) and the pair plot).
Did the model converge?
Estimate Informant Competence
Calculate and report the posterior mean competence Di for each informant.
Visualize the posterior distributions for competence (e.g., using az.plot_posterior(trace, var_names=['D']).
Identify the most and least competent informants based on your model.
Estimate Consensus Answers
Calculate and report the posterior mean probability for each consensus answer Zj.
Determine the most likely consensus answer key (e.g., by taking the mode or rounding the posterior mean for each Zj).
Visualize the posterior probabilities for Z (e.g., using az.plot_posterior(trace, var_names=['Z']).
Compare with Naive Aggregation
Calculate the simple majority vote answer for each question based on the raw data. How does this compare to the consensus answer key estimated by your CCT model? Discuss any differences -- why do they occur?
