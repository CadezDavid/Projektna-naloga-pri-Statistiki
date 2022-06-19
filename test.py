import pandas as pd
import random
from math import sqrt

N = 1000
n = 100

random.seed(3.14159)
mi = 0
sigma = 1
seznam = [random.normalvariate(mi, sigma) for _ in range(N)]

X = pd.DataFrame(seznam, columns=['val'])
sample = X.sample(n)

sample_crta = sample['val'].mean()
moj_se = sqrt((N - n) / (N * n) * sample['val'].var())

se = X['val'].sem()

print("moj: ", moj_se)
print("pravi: ", se)

# var = (sum_{i=1}^{n} (x_i - x_crta) ** 2) / (n - 1)
# std = sqrt(var)
# sem = std / sqrt(N - 1)
