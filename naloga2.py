import math
import statsmodels.api as sm
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

X = pd.read_csv("Mangan.csv")
X.columns = X.columns.str.strip("'")
X = X.drop('DAN', axis=1)

fig, plots = plt.subplots(1, 3, figsize=(10, 5), constrained_layout=True)

#fig.tight_layout()

plots[0].title.set_text('Histogram')
plots[1].title.set_text('Viseči histogram')
plots[2].title.set_text('Primerjalni kvantilni (Q-Q) grafikon')

all_measurements = pd.DataFrame(pd.concat([
    X['ODLITEK1'], X['ODLITEK2'], X['ODLITEK3'], X['ODLITEK4'], X['ODLITEK5']
],
                                          ignore_index=True),
                                columns=['value'])

# a)
n = len(all_measurements)

[q1, q3] = all_measurements['value'].quantile([.25, .75])
IQR = q3 - q1

# Using Freedman-Diaconis rule
width = 2.6 * IQR / (n**(1 / 3))

# Define bins
bins = int(
    math.ceil(
        (all_measurements['value'].max() - all_measurements['value'].min()) /
        width))

# all_measurements['value'].plot.kde(ax=plots[0])
mi = all_measurements['value'].mean()
sigma = all_measurements['value'].std()

mu, std = norm.fit(X)
x = np.linspace(all_measurements['value'].min(),
                all_measurements['value'].max(), 100)
p = norm.pdf(x, mu, std)
plots[0].plot(x, p, 'k', linewidth=2)


def phi(variable):
    return 1 - norm.sf(variable)


def aux(x, mi, sigma):
    return phi((x + width - mi) / sigma) - phi((x - mi) / sigma)


all_measurements['value'].hist(bins=bins, density=True, ax=plots[0])

# b)
freq = pd.DataFrame()
freq = round(((all_measurements['value'] // width) * width + width / 2.), 2)
freq = pd.DataFrame(freq.value_counts())
freq['obs_count'] = 24 * 5 * freq / freq.sum()
freq['exp_count'] = 24 * 5 * aux(freq.index, mi, sigma)
freq['diffs'] = freq['obs_count'] - freq['exp_count']

freq['diffs'].plot.bar(ax=plots[1])

# c)
sm.qqplot(all_measurements['value'],
          xlabel="Normalna porazdelitev",
          ylabel="Porazdelitev meritev",
          ax=plots[2])

plt.savefig("2.png")
