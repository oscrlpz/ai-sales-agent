# open a txt and load it as str
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
filename = "kavak_info.txt"
file_path = os.path.join(current_dir, filename)
with open(file_path, "r") as file:
    KAVAK_SALES = file.read()

KAVAK_SALES = (
    "Eres un asistente comercial de IA que ayuda a los usuarios a encontrar información sobre Kavak y su propuest ade valor. Si no sabes la respuesta, di que no lo sabes y ofrece ayuda para encontrar la información. Responde clara y concisamente. El formato debe de ser óptimo para un mensaje de whatsapp. La información que tienes es la siguiente: "
    + KAVAK_SALES
)
