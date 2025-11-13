import sqlite3


def inicializar_banco():
    conn = sqlite3.connect('repositorio.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservatorio (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            categoria TEXT,
            preco REAL, 
            quantidade INTEGER,
            estoqueminimo INTEGER
        )
    ''')

    conn.commit()
    conn.close()

def menu():
    inicializar_banco()
    while True:
        print("\n", "="*50, "SELECIONE UMA AÇÃO", "="*50, "\n")
        print("0 - Sair do Sistema")
        try:
            acao = int(input("Escolha uma ação: "))
            match acao:
                case 0:
                    print("-"*55, "SAINDO", "-"*55)
                    break
                case _:
                    print("Opção inválida! Digite uma ação válida.")
        except ValueError:
            print("Caractere inválido! Tente novamente.")


validar_preco()