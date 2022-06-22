import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("Temp_LJ.csv")
data.columns = data.columns.str.strip("'")

Y = data['TEMPERATURA'].to_numpy()
Y = Y - Y.mean()

n = Y.shape[0]

Y = Y.reshape([n, 1])

X_A = np.arange(n).reshape([n, 1])
sin = np.sin(math.pi * np.arange(n) / 6)
cos = np.cos(math.pi * np.arange(n) / 6)
sin = sin.reshape([n, 1])
cos = cos.reshape([n, 1])
X_A = np.concatenate((X_A, sin, cos), axis=1)

# Po metodi največjega verjetja je cenilka za vektor b rešitev predoločenega
# sistema
beta_A = np.dot(np.dot(np.linalg.inv(np.dot(X_A.T, X_A)), X_A.T), Y)

print("Vektor ocen za parametre modela A je: ",
      list(np.around(beta_A[:, 0], 3)))

# Narišemo graf
f = plt.figure()
f.set_figwidth(8)
f.set_figheight(3)
plt.plot(np.dot(X_A, beta_A)[300:] + data['TEMPERATURA'].mean(), linewidth=1.5)
plt.plot(Y[300:] + data['TEMPERATURA'].mean(), linewidth=1.5)
plt.xlabel("Meseci od januarja 2011")
plt.ylabel("Temperatura v stopinjah celzija")
plt.tight_layout()
plt.savefig("3a.png")
plt.clf()

RSS_A = np.linalg.norm(Y - np.dot(X_A, beta_A))

AIC_A = 2 * 4 + n * np.log(RSS_A)
print(f"Akaikejeva informacija za model A: {AIC_A:0.5f}")

X_B = np.arange(n).reshape([n, 1])
for i in range(12):
    tmp = (np.arange(n) % 12) == i
    tmp = tmp.astype(int)
    tmp = tmp.reshape([n, 1])
    X_B = np.concatenate((X_B, tmp), axis=1)

# Po metodi največjega verjetja je cenilka za vektor b rešitev predoločenega
# sistema
beta_B = np.dot(np.dot(np.linalg.inv(np.dot(X_B.T, X_B)), X_B.T), Y)

print("Vektor ocen za parametre modela B je: ",
      list(np.around(beta_B[:, 0], 3)))

# Narišemo graf
f = plt.figure()
f.set_figwidth(8)
f.set_figheight(3)
plt.plot(np.dot(X_B, beta_B)[300:] + data['TEMPERATURA'].mean(), linewidth=1.5)
plt.plot(Y[300:] + data['TEMPERATURA'].mean(), linewidth=1.5)
plt.xlabel("Meseci od januarja 2011")
plt.ylabel("Temperatura v stopinjah celzija")
plt.tight_layout()
plt.savefig("3b.png")
plt.clf()

RSS_B = np.linalg.norm(Y - np.dot(X_B, beta_B))

AIC_B = 2 * (1 + 12) + n * np.log(RSS_B)
print(f"Akaikejeva informacija za model B: {AIC_B:0.5f}")
