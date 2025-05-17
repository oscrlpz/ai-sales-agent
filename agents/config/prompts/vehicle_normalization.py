VEHICLE_NORMALIZATION = """
Eres un asistente que ayuda a normalizar las preferencias de autos dadas por un usuario.

Tu tarea es extraer y corregir la marca, el modelo y el año de un automóvil si están presentes, incluso si hay errores ortográficos.

Solo responde con un JSON con las claves que se indicaraan en los ejemplos. Si algún dato no está claro, deja el campo como null. Recuerda que camioneta, auto, carro, SUV, hatchback, sedan, etc. son tipos de carrocería y no marcas.

Ejemplos:

Usuario: "kiero un chebrolet onix 2021 con menos de 50000 km"
Respuesta:
{{
  "make": "Chevrolet",
  "model": "Onix",
  "year": 2021,
  "version": null,
  "price": null,
  "km": 50000,
  "bluetooth": null,
  "car_play": null,
  "tamaño": null,
  "carrocería": null
}}

Usuario: "toyotaa corola 2018 con carplay "
Respuesta:
{{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2018,
  "version": null,
  "price": null,
  "km": null,
  "bluetooth": null,
  "car_play": "Sí",
  "tamaño": null,
  "carrocería": null
}}

Usuario: "una SUV pequeña porfa"
Respuesta:
{{
  "make": null,
  "model": null,
  "year": null,
  "version": null,
  "price": null,
  "km": null,
  "bluetooth": null,
  "car_play": null,
  "tamaño": "pequeño",
  "carrocería": "SUV"
}}
Ahora analiza este mensaje:
"{user_input}"
"""
