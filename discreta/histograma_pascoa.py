"""
Gera o histograma de frequências relativas da data da Páscoa,
reproduzindo o gráfico "Distribution of the Date of Easter"
https://upload.wikimedia.org/wikipedia/commons/3/3b/Easter_Distribution.png

"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta

# ------------------------------------------------------------------
# 1) Calcula (mes, dia) da Páscoa para um array de anos, de forma
#    vetorizada com numpy (equivalente ao algoritmo de pascoa.py).
# ------------------------------------------------------------------
def datas_pascoa_vetorizado(anos: np.ndarray):
    a = anos % 19
    b = anos // 100
    c = anos % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    L = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * L) // 451

    mes = (h + L - 7 * m + 114) // 31
    dia = ((h + L - 7 * m + 114) % 31) + 1

    return mes, dia


# ------------------------------------------------------------------
# 2) Percorre um ciclo completo de 5.700.000 anos (período de
#    repetição do calendário gregoriano para a data da Páscoa).
# ------------------------------------------------------------------
CICLO = 5_700_000
ANO_INICIAL = 1583  # ano seguinte à adoção do calendário gregoriano

anos = np.arange(ANO_INICIAL, ANO_INICIAL + CICLO, dtype=np.int64)
meses, dias = datas_pascoa_vetorizado(anos)

# ------------------------------------------------------------------
# 3) Conta a frequência de cada data (a Páscoa só cai entre
#    22/mar e 25/abr) e converte para percentual.
# ------------------------------------------------------------------
datas_possiveis = []
d0 = date(2001, 3, 22)  # ano não-bissexto qualquer, só para gerar a sequência
for n in range(35):  # 22/mar até 25/abr = 35 datas possíveis
    d = d0 + timedelta(days=n)
    datas_possiveis.append((d.month, d.day))

contagem = {dm: 0 for dm in datas_possiveis}
for mm, dd in zip(meses, dias):
    contagem[(int(mm), int(dd))] += 1

total = CICLO
percentuais = [100 * contagem[dm] / total for dm in datas_possiveis]

# ------------------------------------------------------------------
# 4) Plota o histograma, no mesmo estilo da imagem de referência.
# ------------------------------------------------------------------
rotulos = []
for mm, dd in datas_possiveis:
    rotulos.append(str(dd))

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(range(35), percentuais, color="green", edgecolor="black", width=0.9)

ax.set_xticks(range(35))
ax.set_xticklabels(rotulos)
ax.set_ylabel("Pfrequência dos dias de Páscoa")
ax.set_title("Distribuição das datas da Páscoa \n A sequência dos dias tem ciclos de período 5.700.000 anos aproximadamente.")
ax.set_ylim(0, 4.0)
ax.yaxis.set_major_formatter(lambda y, _: f"{y:.2f}%")
ax.grid(axis="y", linestyle="--", alpha=0.6)

# Anotações "March" e "April" abaixo do eixo x, como na imagem original
idx_abril = [n for n, (mm, dd) in enumerate(datas_possiveis) if mm == 4][0]
ax.annotate("Março", xy=(0, -0.14), xycoords=("data", "axes fraction"),
            ha="left", fontsize=12, fontweight="bold")
ax.annotate("Abril", xy=(idx_abril, -0.14), xycoords=("data", "axes fraction"),
            ha="left", fontsize=12, fontweight="bold")
ax.annotate("", xy=(idx_abril - 0.5, -0.10), xytext=(2.5, -0.10),
            xycoords=("data", "axes fraction"),
            arrowprops=dict(arrowstyle="->"))

plt.tight_layout()
# plt.savefig("histograma_pascoa.png", dpi=150)

plt.show()

# Mostra alguns valores para conferência
for dm, p in zip(datas_possiveis[:5], percentuais[:5]):
    print(dm, f"{p:.2f}%")
