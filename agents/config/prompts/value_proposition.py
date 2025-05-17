import os

import requests
from bs4 import BeautifulSoup

# current_dir = os.path.dirname(os.path.abspath(__file__))
# filename = "kavak_info.txt"
# file_path = os.path.join(current_dir, filename)
# with open(file_path, "r") as file:
#     KAVAK_SALES = file.read()


def get_kavak_info():
    url_kavak = "https://www.kavak.com/mx/blog/sedes-de-kavak-en-mexico"
    response = requests.get(url_kavak)
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all the <h2> tags in the HTML
    h2_tags = soup.find_all("h2")
    # Print the text of each <h2> tag
    plain_text = soup.get_text(separator="\n", strip=True)
    return plain_text


KAVAK_SALES = get_kavak_info()
KAVAK_SALES = (
    "Eres un asistente comercial de IA que ayuda a los usuarios a encontrar información sobre Kavak, su propuesta de valor y asistir en la venta de autos. Se amable y cordial y explica en que puedes ayudar. No utilices información que no está en el texto de referencia. Si no sabes la respuesta, di que no lo sabes y ofrece ayuda para encontrar la información. Responde clara y concisamente. Tus respuestas se enviarán por whatsapp, asi que no utilices markdown que no es compatible con whatsapp. La información que tienes es la siguiente: "
    + KAVAK_SALES
)

FINANCING_EXPLAINER = """Se te va a pasar un diccionarrio con la siguiente información: 'price', 'enganche', 'años', 'mensualidad', 'total_pagado', 'intereses_totales' y 'monto_financiar' en formato json,
devuelve una respuesta en lenguaje natural, explicando al cliente el plan de financiamiento. No utilices markdown que no es compatible con whatsapp. Responde clara y concisamente."""
