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
