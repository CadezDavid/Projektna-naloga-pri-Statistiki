import math
import statsmodels.api as sm
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

X = pd.read_csv("Temp_LJ.csv")
X.columns = X.columns.str.strip("'")

# model A
# linearen trend in sinusno nihanje s periodo eno leto
Y = a + b * X["LETO"] + A * math.sin((2*math.pi/12) * (X["MESEC"] - 1) + omega)
