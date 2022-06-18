import math
import statsmodels.api as sm
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

data = pd.read_csv("Mangan.csv")
data.columns = data.columns.str.strip("'")
data = data.drop('DAN', axis=1)

fig, plot = plt.subplots(1, 3, figsize=(12, 5))

all_measurements = pd.DataFrame(pd.concat([
    data['ODLITEK1'], data['ODLITEK2'], data['ODLITEK3'], data['ODLITEK4'],
    data['ODLITEK5']
],
                                          ignore_index=True),
                                columns=['value'])

# a)

n = len(all_measurements)
[q1, q3] = all_measurements['value'].quantile([.25, .75])
IQR = q3 - q1
width = 2.6 * IQR / (n**(1 / 3))
bins = int(
    math.ceil(
        (all_measurements['value'].max() - all_measurements['value'].min()) /
        width))
all_measurements['value'].plot.kde(ax=plot[0])
mi = all_measurements['value'].mean()
sigma = all_measurements['value'].std()
# all_measurements.plot()

# Create bar plot
# plt.bar(df['class_marks_marsk'],
#         df['Frec_abs'],
#         color='blue',
#         ec='black',
#         alpha=0.5)
# Add labels and modify size
# plt.ylabel('Absolute Frequency',fontsize=14)
# plt.xlabel('Weight (Kg)',fontsize=14)
# plt.xticks(fontsize=14)
# plt.yticks(fontsize=14)
# Add title
# plt.title('ABSOLUTE FREQUENCY HISTOGRAM',fontsize=16);


def phi(variable):
    return 1 - norm.sf(variable)


def aux(x, mi, sigma):
    return phi((x + width - mi) / sigma) - phi((x - mi) / sigma)


all_measurements['value'].hist(bins=bins, density=True, ax=plot[0])

# b)
freq = pd.DataFrame()
freq = round(((all_measurements['value'] // width) * width + width / 2.), 2)
freq = pd.DataFrame(freq.value_counts())
freq['obs_count'] = freq / freq.sum()
freq['exp_count'] = aux(freq.index, mi, sigma)
freq['diffs'] = freq['obs_count'] - freq['exp_count']

freq['diffs'].plot.bar(ax=plot[1])

# plt.plot(freq['diffs'])
# plot[1].bar(freq['diffs'].to_list())

# c)
sm.qqplot(all_measurements['value'], ax=plot[2])

plt.savefig("output_3.png")
