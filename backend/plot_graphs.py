import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results.csv")

avg = df[["sha256_time", "md5_time", "blake2_time"]].mean()

plt.bar(avg.index, avg.values)
plt.title("Hash Algorithm Time Comparison")
plt.xlabel("Algorithm")
plt.ylabel("Time (seconds)")
plt.show()