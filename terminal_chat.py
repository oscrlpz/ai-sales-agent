from uuid import uuid4

from api.services.sales_agent import run_chat

def main():
    print("🤖 AI Sales Agent (Terminal Mode)\nEscribe '\\salir' para terminar.\n")

    # Usa un identificador fijo de sesión (puedes hacer esto dinámico si quieres simular varios usuarios)
    session_id = str(uuid4())
    print(f"ID de sesión: {session_id}\n")

    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["\\salir", "\\exit", "\\quit"]:
            print("👋 ¡Hasta luego!")
            break

        reply = run_chat(user_input=user_input, session_id=session_id, verbose=False)
        print(f"🤖: {reply}\n")


if __name__ == "__main__":
    main()
