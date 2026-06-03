import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


episodes = pd.read_csv(
    "tv_episodes.tsv",
    sep="\t"
)

ratings = pd.read_csv(
    "title.ratings.tsv",
    sep="\t"
)

# merge e limpeza

df = pd.merge(
    episodes,
    ratings,
    on="tconst",
    how="inner"
)


df = df[df["startYear"].notna()]
df = df[df["averageRating"].notna()]

df["startYear"] = pd.to_numeric(
    df["startYear"],
    errors="coerce"
)

df = df[df["startYear"].notna()]

df["startYear"] = df["startYear"].astype(int)

# remover episódios com poucas avaliações
df = df[df["numVotes"] >= 100]


STREAMING_YEAR = 2010

before = df[df["startYear"] < STREAMING_YEAR]
after = df[df["startYear"] >= STREAMING_YEAR]

# médias

mean_before = before["averageRating"].mean()
mean_after = after["averageRating"].mean()

print("\n=== MÉDIAS ===\n")

print(f"Antes de 2010 : {mean_before:.3f}")
print(f"Após 2010     : {mean_after:.3f}")

# normalizar histogramas para que não haja viés relacionado ao valor absoluto

bins = np.arange(0, 10.5, 0.5)

before_counts, _ = np.histogram(
    before["averageRating"],
    bins=bins
)

after_counts, _ = np.histogram(
    after["averageRating"],
    bins=bins
)

# normalização
before_counts = (
    before_counts / before_counts.sum()
)

after_counts = (
    after_counts / after_counts.sum()
)


x = bins[:-1]

width = 0.2

# plotando

plt.figure(figsize=(12, 6))

# barras antes
plt.bar(
    x - width/2,
    before_counts,
    width=width,
    color="skyblue",
    alpha=0.9,
    label="Antes de 2010"
)

# barras depois
plt.bar(
    x + width/2,
    after_counts,
    width=width,
    color="salmon",
    alpha=0.9,
    label="Após 2010"
)

# linhas das médias
plt.axvline(
    mean_before,
    color="blue",
    linestyle="--",
    linewidth=3,
    label=f"Média antes ({mean_before:.2f})"
)

plt.axvline(
    mean_after,
    color="darkred",
    linestyle="--",
    linewidth=3,
    label=f"Média após ({mean_after:.2f})"
)


plt.xlabel("Nota IMDB")
plt.ylabel("Frequência Normalizada")

plt.title(
    "Distribuição das Notas de Episódios\n"
    "Antes e Após os Streamings"
)

plt.xlim(0, 10)

plt.legend()

plt.tight_layout()


plt.savefig(
    "histograma_episodios.png",
    dpi=300
)

print(
    "\nGráfico salvo como:"
    "\nhistograma_episodios.png"
)