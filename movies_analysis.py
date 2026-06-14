import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu


ratings = pd.read_parquet("ratings.parquet")
movies = pd.read_parquet("movies.parquet")

# tratamento de colunas

ratings = ratings[["tconst", "averageRating", "numVotes"]]

movies = movies[[
    "tconst",
    "primaryTitle",
    "startYear",
    "genres"
]]

df = pd.merge(movies, ratings, on="tconst")

# limpando dados

# remover anos inválidos
df = df[df["startYear"].notna()]

# converter para inteiro
df["startYear"] = df["startYear"].astype(int)

# remover filmes com poucas avaliações
df = df[df["numVotes"] >= 1000]

# remover ratings nulos
df = df[df["averageRating"].notna()]

# dividindo antes e depois de 2010 (começo da era dos streamings)

STREAMING_YEAR = 2010

before_streaming = df[df["startYear"] < STREAMING_YEAR]
after_streaming = df[df["startYear"] >= STREAMING_YEAR]

mean_before = before_streaming["averageRating"].mean()
mean_after = after_streaming["averageRating"].mean()

# histograma comparativo

plt.figure(figsize=(10, 6))

# bins das notas
bins = np.arange(0, 10.5, 0.5)

# frequências
before_counts, _ = np.histogram(
    before_streaming["averageRating"],
    bins=bins
)

after_counts, _ = np.histogram(
    after_streaming["averageRating"],
    bins=bins
)

# normalização pra evitar viés
before_counts = (
    before_counts / before_counts.sum()
)

after_counts = (
    after_counts / after_counts.sum()
)

# posições das barras
x = bins[:-1]

# largura das barras
width = 0.2

plt.bar(
    x - width/2,
    before_counts,
    width=width,
    color="skyblue",
    alpha=0.9,
    label="Antes do streaming"
)

plt.bar(
    x + width/2,
    after_counts,
    width=width,
    color="salmon",
    alpha=0.9,
    label="Após streaming"
)

# linhas verticais das médias

plt.axvline(
    mean_before,
    color="blue",
    linestyle="--",
    linewidth=2,
    label=f"Média antes ({mean_before:.2f})"
)

plt.axvline(
    mean_after,
    color="red",
    linestyle="--",
    linewidth=2,
    label=f"Média após ({mean_after:.2f})"
)


plt.xlabel("Nota IMDB")
plt.ylabel("Frequência Normalizada")

plt.title(
    "Distribuição das Notas IMDB\nAntes e Após os Streamings"
)

plt.xlim(0, 10)

plt.legend()

plt.tight_layout()

plt.savefig(
    "histograma_ratings.png",
    dpi=300
)

print(
    "Histograma salvo em histograma_ratings.png"
)

# ==========================
# TESTE DE HIPÓTESE
# ==========================
# H0: a distribuição de averageRating é a mesma antes e depois de 2010

print("\n" + "="*60)
print("TESTE DE HIPÓTESE - QUALIDADE DOS FILMES (ANTES x APÓS 2010)")
print("="*60)

print(f"\nMédia antes de {STREAMING_YEAR}: {mean_before:.3f}")
print(f"Média após {STREAMING_YEAR}    : {mean_after:.3f}")

# Mann-Whitney U: não-paramétrico, não exige normalidade
u_stat, p_mw = mannwhitneyu(
    before_streaming["averageRating"],
    after_streaming["averageRating"],
    alternative="two-sided"
)

print(f"\nMann-Whitney U: p = {p_mw:.5f}")

if p_mw < 0.05:
    print("Conclusão: Existe diferença estatisticamente significativa "
          "na qualidade dos filmes antes x após o streaming.")
else:
    print("Conclusão: Não foi encontrada diferença significativa "
          "na qualidade dos filmes antes x após o streaming.")


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
    before_streaming["averageRating"],
    after_streaming["averageRating"]
)

print(f"\nDiferença observada (Antes - Após): {diff_obs:.3f}")
print(f"Permutação (10.000): p = {p_perm:.5f}")

if p_perm < 0.05:
    print("Conclusão: O teste de permutação confirma diferença "
          "estatisticamente significativa.")
else:
    print("Conclusão: O teste de permutação não encontrou diferença "
          "significativa.")
