def vehicle_size_classifier(largo_cm: float, ancho_cm: float, alto_cm: float) -> dict:
    """
    Classifies the size and type of a vehicle based on its dimensions.

    Args:
        largo_cm (float): Length of the vehicle in centimeters.
        ancho_cm (float): Width of the vehicle in centimeters.
        alto_cm (float): Height of the vehicle in centimeters.

    Returns:
        dict: A dictionary containing the classification of the vehicle.
    """
    resultado = {}
    largo_m = largo_cm / 1000
    ancho_m = ancho_cm / 1000
    alto_m = alto_cm / 1000

    # Clasificación por tamaño
    if largo_m < 3.7:
        resultado["tamaño"] = "Auto pequeño / urbano"
    elif 3.7 <= largo_m < 4.1:
        resultado["tamaño"] = "Auto compacto"
    elif 4.1 <= largo_m < 4.5:
        resultado["tamaño"] = "Auto mediano"
    elif 4.5 <= largo_m < 4.85:
        resultado["tamaño"] = "Auto grande / familiar"
    else:
        resultado["tamaño"] = "Vehículo muy grande / ejecutivo o de carga"

    # Estimar tipo de carrocería
    if alto_m >= 1.65 and ancho_m >= 1.75:
        if largo_m > 4.8:
            resultado["carrocería"] = "SUV grande o camioneta"
        elif largo_m > 4.3:
            resultado["carrocería"] = "SUV mediano o crossover"
        else:
            resultado["carrocería"] = "Mini SUV / crossover compacto"
    elif alto_m < 1.45:
        if largo_m > 4.2 and ancho_m > 1.75:
            resultado["carrocería"] = "Coupé o sedán deportivo"
        else:
            resultado["carrocería"] = "Hatchback o compacto bajo"
    else:
        resultado["carrocería"] = "Sedán o auto tradicional"

    # # Estimar uso típico
    # if resultado["carrocería"] in ["SUV grande o camioneta", "SUV mediano o crossover"]:
    #     resultado["uso_típico"] = "Familiar, caminos difíciles o viajes largos"
    # elif resultado["carrocería"] in ["Hatchback o compacto bajo", "Auto pequeño / urbano"]:
    #     resultado["uso_típico"] = "Uso urbano, económico y fácil de estacionar"
    # elif "sedán" in resultado["carrocería"].lower():
    #     resultado["uso_típico"] = "Uso mixto: ciudad y carretera"
    # elif "coupé" in resultado["carrocería"].lower():
    #     resultado["uso_típico"] = "Deportivo o recreativo"
    # else:
    #     resultado["uso_típico"] = "Versátil / depende del equipamiento"

    return resultado
