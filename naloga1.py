import pandas as pd
import math
import matplotlib.pyplot as plt

# Preberemo podatke in jih shranimo v X
X = pd.read_csv("Kibergrad.csv")
X.columns = X.columns.str.strip("'")

# Definiramo nov stolpec "brez_ss":
# 1 - nima niti srednjesolske izobrazbe,
# 0 - ima vsaj srednjesolsko izobrazbo
X['brez_ss'] = X['IZOBRAZBA'].apply(lambda x: 1 if x < 39 else 0)

N = len(X)  # Velikost populacije
n = 200  # Velikost vzorca
sample = X.sample(n)  # Vzamemo vzorec velikosti n

# a)
# Izbrana cenilka za delež je delež na vzorcu
mi = sample['brez_ss'].mean()
print(f"Ocena za delež je {mi:0.3f}.")

# b)
# Standardna napaka cenilke iz naloge a)
# Pomagaj si s primerom C na strani 209
SE = math.sqrt((N - n) * mi * (1 - mi) / ((n - 1) * N))

# https://stackoverflow.com/questions/53519823/confidence-interval-in-python-dataframe
CI = (mi - 1.96 * SE, mi + 1.96 * SE)
print(f"Interval zaupanja je {CI}.")

# c)
# pop_mi = X['brez_ss'].mean()
# pop_sigma = X['brez_ss'].std(ddof=0)
# pop_SE = ((N - n) / (N - 1) * (pop_sigma**2) / n)**(1 / 2)
# pop_ci = (pop_mi - 1.96 * pop_sigma / math.sqrt(N),
#           pop_mi + 1.96 * pop_sigma / math.sqrt(N))
# print(pop_ci)

pop_mi = X['brez_ss'].mean()
pop_SE = X['brez_ss'].sem()

if CI[0] < pop_mi < CI[1]:
    print(f"Da, interval zaupanja pokrije populacijski delež: {pop_mi}")
else:
    print(f"Ne, interval zaupanja ne pokrije populacijskega deleža: {pop_mi}")

# d)
tests = 99
count = 0
samples = pd.DataFrame(columns=['low', 'high', 'mi', 'SE'])
ci_df = pd.DataFrame([[CI[0], CI[1], mi, SE]],
                     columns=['low', 'high', 'mi', 'SE'])
samples = pd.concat([samples, ci_df], ignore_index=True)

if CI[0] < pop_mi < CI[1]:
    count += 1

for i in range(tests):
    sample = X.sample(n)
    mi = sample['brez_ss'].mean()
    SE = math.sqrt((N - n) * mi * (1 - mi) / ((n - 1) * N))
    CI = (mi - 1.96 * SE, mi + 1.96 * SE)
    ci_df = pd.DataFrame([[CI[0], CI[1], mi, SE]],
                         columns=['low', 'high', 'mi', 'SE'])
    samples = pd.concat([samples, ci_df], ignore_index=True)
    if CI[0] < pop_mi < CI[1]:
        count += 1

print(
    f"Pri n={n} {100*count/(tests+1)}% intervalov zaupanja pokrije populacijski delež."
)
# print(samples)

for i, low, high, _, _ in samples.to_records():
    plt.plot((low, high), (i, i), color='blue')
plt.plot((pop_mi, pop_mi), (0, tests), color='red')
plt.savefig("1d.png")

plt.clf()

# e)
# Standardni odklon vzorčnih deležev za 100 prej dobljenih vzorcev
# std_mi_samples = samples['mi'].std(ddof=0)
# print(pop_SE)

# f)
n = 800
tests = 100
count = 0
samples = pd.DataFrame(columns=['low', 'high', 'mi', 'SE'])

for _ in range(tests):
    sample = X.sample(n)
    mi = sample['brez_ss'].mean()
    SE = math.sqrt((N - n) * mi * (1 - mi) / (N * (n - 1)))
    CI = (mi - 1.96 * SE, mi + 1.96 * SE)

    ci_df = pd.DataFrame([[CI[0], CI[1], mi, SE]],
                         columns=['low', 'high', 'mi', 'SE'])
    samples = pd.concat([samples, ci_df], ignore_index=True)

    if CI[0] < pop_mi < CI[1]:
        count += 1

for i, low, high, _, _ in samples.to_records():
    plt.plot((low, high), (i, i), color='blue')
plt.plot((pop_mi, pop_mi), (0, tests), color='red')
plt.savefig("1f.png")

plt.clf()

print(
    f"Pri n={n} {100*count/tests}% intervalov zaupanja pokrije populacijski delež."
)

# pop_SE = ((N - n) / (N - 1) * (pop_sigma**2) / n)**(1 / 2)
# STD_mi_samples2 = samples['mi'].std(ddof=0)
# print(STD_mi_samples2)
# print(pop_SE)
#

# n = 1600
# tests = 100
# count = 0
# samples = pd.DataFrame(columns=['low', 'high', 'mi', 'SE'])
#
# for _ in range(tests):
#     sample = X.sample(n)
#     mi = sample['brez_ss'].mean()
#     SE = math.sqrt((N - n) / (N * n) * sample['brez_ss'].var())
#     CI = (mi - 1.96 * SE, mi + 1.96 * SE)
#
#     ci_df = pd.DataFrame([[CI[0], CI[1], mi, SE]],
#                          columns=['low', 'high', 'mi', 'SE'])
#     samples = pd.concat([samples, ci_df], ignore_index=True)
#
#     if CI[0] < pop_mi < CI[1]:
#         count += 1
#
# for i, low, high, _, _ in samples.to_records():
#     plt.plot((low, high), (i, i), color='blue')
# plt.plot((pop_mi, pop_mi), (0, tests-1), color='red')
# plt.savefig("1z.png")
#
# plt.clf()
#
# print(
#     f"Pri n={n} {100*count/tests}% intervalov zaupanja pokrije populacijski delež."
# )

# n = 3200
# tests = 100
# count = 0
# samples = pd.DataFrame(columns=['low', 'high', 'mi', 'SE'])
#
# for _ in range(tests):
#     sample = X.sample(n)
#     mi = sample['brez_ss'].mean()
#     SE = math.sqrt((N - n) / (N * n) * sample['brez_ss'].var())
#     CI = (mi - 1.96 * SE, mi + 1.96 * SE)
#
#     ci_df = pd.DataFrame([[CI[0], CI[1], mi, SE]],
#                          columns=['low', 'high', 'mi', 'SE'])
#     samples = pd.concat([samples, ci_df], ignore_index=True)
#
#     if CI[0] < pop_mi < CI[1]:
#         count += 1
#
# for i, low, high, _, _ in samples.to_records():
#     plt.plot((low, high), (i, i), color='blue')
# plt.plot((pop_mi, pop_mi), (0, tests-1), color='red')
# plt.savefig("1ž.png")
#
# print(
#     f"Pri n={n} {100*count/tests}% intervalov zaupanja pokrije populacijski delež."
# )
