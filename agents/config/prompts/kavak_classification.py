BOOLEAN_FINANCING_CLASSIFICATION = """Eres un asistente que clasifica las respuestas de los clientes. El cliente te va a responder si desea un plan de financiamiento o no. Tu tarea es clasificar la respuesta en dos categorias: true  o false. Si el cliente dice que si, entonces devuelve true , si el cliente dice que no, entonces devuelve false. Responde unicamente con el diccionario JSON que contiene la respuesta. No incluyas ningun otro texto.
Ejemplo:

El cliente dice: "si, me interesa un plan de financiamiento"
Respuesta: 
{"response": true}
"""

INTENT_CLASSIFICATION = """
Clasifica la siguiente solicitud del cliente en una de estas dos categorías:
- "general"
- "catalog"

Responde con unicamente el diccionario que contiene el tipo de solicitud y no incluyas ningún otro texto.

Ejemplos:
Solicitud: ¿Dónde están ubicadas sus sucursales?
Respuesta:
{"_type": "general"}

Solicitud: ¿Estoy buscando un auto pequeñó.
Respuesta:
{"_type": "catalog"}
"""

FINANCING_TERM_CLASSIFICATION = """
CLasifica la solicitud del client en 3, 4, 5, o 6 años, cuanto quiere dar de enganche y si desea continuar con el financiamiento. si no puEdes extraer el dato, entonces devuelve null. Responde unicamente con el diccionario JSON que contiene la respuesta. No incluyas ningun otro texto.
Considera que el cliente puede usar numeros, letras, o una combinacion de ambos.

Ejemplo:
El cliente dice: "a 3 años con un enganche de 10000"
Respuesta: 
{"term": 3, "down_payment": "10000", "wants_financing": true}

El cliente dice: "a 3 años con un enganche de 10%"
Respuesta: 
{"term": 3, "down_payment": "price * 0.1", "wants_financing": true}

El cliente dice: "me gustaría financiarlo a 4 meses con un enganche de 10000" # meses no es valido
Respuesta:
{"term": null, "down_payment": "10000", "wants_financing": true}

El cliente dice: "me gustaría financiarlo a 10 años con un enganche de 10000"  # No es valido mas de 6 años
Respuesta:
{"term": null, "down_payment": "10000", "wants_financing": true}

El cliente dice: "a 2"
Respuesta:
{"term": null, "down_payment": null, "wants_financing": null}

El cliente dice: "me gustaría financiarlo a 4 años"
Respuesta:
{"term": 4, "down_payment": null, "wants_financing": true}

El cliente dice: "Hola, como estas?"
Respuesta:
{"term": null, "down_payment": null, "wants_financing": false}

El cliente dice: "Hola, estoy buscando un auto"
Respuesta:
{"term": null, "down_payment": null, "wants_financing": false}
"""
