def calc_down_from_str(down_str, total_price):
    _expr = down_str.replace("precio", str(total_price))
    return eval(_expr)


def calc_financing(total_price, down_payment, term):
    down = calc_down_from_str(down_payment, total_price)
    if term < 3 or term > 6:
        raise ValueError("El plazo debe ser entre 3 y 6 años")

    monto_financiar = total_price - down
    tasa_anual = 0.10
    tasa_mensual = tasa_anual / 12
    meses = term * 12

    mensualidad = (
        monto_financiar
        * (tasa_mensual * (1 + tasa_mensual) ** meses)
        / ((1 + tasa_mensual) ** meses - 1)
    )
    total_pagado = mensualidad * meses
    intereses_totales = total_pagado - monto_financiar

    return {
        "precio": total_price,
        "enganche": down,
        "años": term,
        "mensualidad": round(mensualidad, 2),
        "total_pagado": round(total_pagado, 2),
        "intereses_totales": round(intereses_totales, 2),
        "monto_financiar": monto_financiar,
    }
