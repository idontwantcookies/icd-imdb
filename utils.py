from typing import Callable

import numpy as np

rng = np.random.default_rng()

Estimador = Callable[[np.ndarray], np.number]


def normalizar(x: np.ndarray) -> np.ndarray:
    return (x - np.mean(x)) / np.std(x)


def ic_pela_formula(x: np.ndarray, z=2.58):
    μ = x.mean()
    σ = x.std()
    li = μ - z * σ / np.sqrt(len(x))
    ls = μ + z * σ / np.sqrt(len(x))
    return li, ls


def ic(x: np.ndarray, alfa=0.05) -> tuple[np.number, np.number]:
    """Retorna o Intervalo de Confiança da variável aleatória x, dado alfa.
    Presume-se que x seja o resultado de um bootstrap iterado sobre um estimador,
    que deve ser feito por fora dessa função (usando, por exemplo, a função 
    bootstrap.)
    Alfa deve ser um valor entre 0 e 1, e representa a probabilidade de erro
    do tipo 1.

    Retorna uma tupla com o limite inferior e o limite superior.
    """

    li = np.percentile(x, alfa / 2 * 100)
    ls = np.percentile(x, 100 - alfa / 2 * 100)

    return li, ls


def bootstrap(x: np.ndarray, estimador: Estimador = np.mean, n_subamostras=5000) -> np.ndarray:
    """Retorna um vetor com estimativas feitas sob subamostras das observações x
    em x. estimador é uma função que recebe um array e retorna um número escalar.
    Seu valor padrão é a função np.mean().
    """
    n = len(x)
    estimativas = np.zeros(n_subamostras)

    for i in range(n_subamostras):
        estimativas[i] = estimador(rng.choice(x, n, replace=True))

    return estimativas


def bootstrap_diffs(x: np.ndarray, y: np.ndarray, estimador: Estimador = np.mean, n_subamostras=5000) -> np.ndarray:
    """Retorna um vetor com diferenças entre as estimativas de subamostragens de
    dois grupos, x e y, baseado na função estimador. 
    estimador é a função np.mean(), por padrão.
    """
    n = len(x)
    diffs = np.zeros(n_subamostras)

    for i in range(n_subamostras):
        x_estim = estimador(rng.choice(x, n, replace=True))
        y_estim = estimador(rng.choice(y, n, replace=True))
        diffs[i] = np.mean(x_estim - y_estim)

    return diffs


def teste_permutacao(x: np.ndarray, y: np.ndarray, estimador: Estimador = np.mean, n_permut=5000) -> np.ndarray:
    k = len(x)

    dados = np.concat([x, y])
    diffs = np.zeros(n_permut)

    for i in range(n_permut):
        rng.shuffle(dados)
        x_amostra = estimador(dados[:k])
        y_amostra = estimador(dados[k:])
        diffs[i] = x_amostra - y_amostra

    return diffs


def valor_p
