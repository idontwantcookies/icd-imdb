import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


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

# ==========================
# TESTE DE HIPÓTESE
# ==========================
# H0: a distribuição de averageRating dos episódios é a mesma antes e depois de 2010

print("\n" + "="*60)
print("TESTE DE HIPÓTESE - QUALIDADE DOS EPISÓDIOS (ANTES x APÓS 2010)")
print("="*60)

# Mann-Whitney U: não-paramétrico, não exige normalidade
u_stat, p_mw = mannwhitneyu(
    before["averageRating"],
    after["averageRating"],
    alternative="two-sided"
)

print(f"\nMann-Whitney U: p = {p_mw:.5f}")

if p_mw < 0.05:
    print("Conclusão: Existe diferença estatisticamente significativa "
          "na qualidade dos episódios antes x após o streaming.")
else:
    print("Conclusão: Não foi encontrada diferença significativa "
          "na qualidade dos episódios antes x após o streaming.")


# Teste de permutação: confirma o resultado sem assumir distribuição teórica
def permutation_test_diff_means(a, b, n_perm=10_000, seed=42):
    rng = np.random.default_rng(seed)

    a = np.asarray(a)
    b = np.asarray(b)

    observed_diff = a.mean() - b.mean()

    pooled = np.concatenate([a, b])
    n_a = len(a)

    perm_diffs = np.empty(n_perm)

    for i in range(n_perm):
        shuffled = rng.permutation(pooled)
        perm_diffs[i] = shuffled[:n_a].mean() - shuffled[n_a:].mean()

    p_value = np.mean(np.abs(perm_diffs) >= np.abs(observed_diff))

    return observed_diff, p_value


diff_obs, p_perm = permutation_test_diff_means(
    before["averageRating"],
    after["averageRating"]
)

print(f"\nDiferença observada (Antes - Após): {diff_obs:.3f}")
print(f"Permutação (10.000): p = {p_perm:.5f}")

if p_perm < 0.05:
    print("Conclusão: O teste de permutação confirma diferença "
          "estatisticamente significativa.")
else:
    print("Conclusão: O teste de permutação não encontrou diferença "
          "significativa.")
