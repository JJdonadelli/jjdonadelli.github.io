def data_pascoa(ano: int) -> tuple[int, int]:
    """
    Calcula a data da Páscoa para um dado ano, usando o algoritmo
    do calendário Gregoriano (Meeus/Jones/Butcher).

    Parâmetros
    ----------
    ano : int
        Ano (calendário gregoriano) para o qual se deseja calcular a Páscoa.

    Retorna
    -------
    (dia, mes) : tuple[int, int]
        Dia e mês da Páscoa naquele ano.
    """
    a = ano % 19
    b = ano // 100
    c = ano % 100
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

    return dia, mes


def data_carnaval(ano: int):
    """
    Calcula a data da terça-feira de Carnaval de um ano, que ocorre
    47 dias antes do Domingo de Páscoa.
    """
    from datetime import date, timedelta

    dia, mes = data_pascoa(ano)
    pascoa = date(ano, mes, dia)
    carnaval = pascoa - timedelta(days=47)
    return carnaval.day, carnaval.month


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        ano = int(sys.argv[1])
    else:
        ano = int(input("Digite o ano: "))

    dia, mes = data_pascoa(ano)
    dia_c, mes_c = data_carnaval(ano)

    meses = ["", "janeiro", "fevereiro", "março", "abril", "maio"]
    print(f"Em {ano}, a Páscoa cai em {dia} de {meses[mes]}.")
    print(f"Em {ano}, o Carnaval (terça-feira) cai em {dia_c} de {meses[mes_c]}.")
