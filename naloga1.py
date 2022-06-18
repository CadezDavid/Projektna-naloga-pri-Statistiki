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
sigma = sample['brez_ss'].std(ddof=0)

SE = sample['brez_ss'].sem(ddof=0)
print(SE)
SE_plus = sample['brez_ss'].sem()
print(SE_plus)

# https://stackoverflow.com/questions/53519823/confidence-interval-in-python-dataframe
ci = (mi - 1.96 * sigma / math.sqrt(n), mi + 1.96 * sigma / math.sqrt(n))
print(ci)

# c)
pop_mi = X['brez_ss'].mean()
pop_sigma = X['brez_ss'].std(ddof=0)
pop_SE = ((N - n) / (N - 1) * (pop_sigma**2) / n)**(1 / 2)
pop_ci = (pop_mi - 1.96 * pop_sigma / math.sqrt(N),
          pop_mi + 1.96 * pop_sigma / math.sqrt(N))
print(pop_ci)
if ci[0] < pop_mi < ci[1]:
    print("Da, interval zaupanja pokrije populacijski delež: ", pop_mi)
else:
    print("Ne, interval zaupanja ne pokrije populacijskega deleža: ", pop_mi)

# d)
n_tests = 99
count = 0
samples = pd.DataFrame(columns=['low', 'high', 'mi', 'sigma'])
ci_df = pd.DataFrame([[ci[0], ci[1], mi, sigma]],
                     columns=['low', 'high', 'mi', 'sigma'])
samples = pd.concat([samples, ci_df], ignore_index=True)
if ci[0] < pop_mi < ci[1]:
    count += 1
for i in range(n_tests):
    sample = X.sample(n)
    mi = sample['brez_ss'].mean()
    sigma = sample['brez_ss'].std(ddof=0)
    ci = (mi - 1.96 * sigma / math.sqrt(n), mi + 1.96 * sigma / math.sqrt(n))
    ci_df = pd.DataFrame([[ci[0], ci[1], mi, sigma]],
                         columns=['low', 'high', 'mi', 'sigma'])
    samples = pd.concat([samples, ci_df], ignore_index=True)
    if ci[0] < pop_mi < ci[1]:
        count += 1
print(f"{count} od {n_tests+1} jih pokrije populacijski delež.")
print(samples)

for i, low, high, _, _ in samples.to_records():
    plt.plot((low, high), (i, i), color='blue')
plt.plot((pop_mi, pop_mi), (0, 99), color='red')
plt.savefig("output_1.png")

# e)
STD_mi_samples = samples['mi'].std(ddof=0)
print(STD_mi_samples)
print(pop_SE)

# f)
n = 800
n_samples = 100
count2 = 0
samples2 = pd.DataFrame(columns=['low', 'high', 'mi', 'sigma'])
for _ in range(n_samples):
    sample = X.sample(n)
    mi = sample['brez_ss'].mean()
    sigma = sample['brez_ss'].std(ddof=0)
    ci = (mi - 1.96 * sigma / math.sqrt(n), mi + 1.96 * sigma / math.sqrt(n))

    ci_df = pd.DataFrame([[ci[0], ci[1], mi, sigma]],
                         columns=['low', 'high', 'mi', 'sigma'])
    samples2 = pd.concat([samples2, ci_df], ignore_index=True)

    if ci[0] < pop_mi < ci[1]:
        count2 += 1

for i, low, high, _, _ in samples2.to_records():
    plt.plot((low, high), (i, i), color='blue')
plt.plot((pop_mi, pop_mi), (0, 99), color='red')
plt.savefig("output_2.png")

print(samples2)

print(
    f"Pri n={n} {count2} od {n_samples} vzorcev pokrije populacijsko povprečje."
)

pop_SE = ((N - n) / (N - 1) * (pop_sigma**2) / n)**(1 / 2)
STD_mi_samples2 = samples2['mi'].std(ddof=0)
print(STD_mi_samples2)
print(pop_SE)
