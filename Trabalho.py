import sqlite3
conn = sqlite3.connect('repositorio.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reservatorio (
        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        categoria TEXT,
        preco REAL, 
        quantidade INTEGER,
        estoqueminimo INTEGER
    )
''')

def validar_nome():
    while True:
        nome = input("Produto: ").title()
        if nome:
            return nome
        else:
            print("Não pode deixar esse espaço em branco!")
def validar_categoria():
    while True:
        tipo = input("Categoria: ").title()
        if tipo:
            return tipo
        else:
            print("Não pode deixar esse espaço em branco!")
def validar_preco():
    while True:
        try:
            valor = float(input("Preço Unitário: "))
            if valor <= 0:
                print("O preço tem que ser um número real positivo!")
            else:
                return valor
        except ValueError:
            print("O preço tem que ser um número real positivo!")
def validar_quantidade():
    while True:
        try:
            qtd = int(input("Quantidade: "))
            if qtd <= 0:
                print("A quantidade tem que ser um número inteiro positivo!")
            else:
                return qtd
        except ValueError:
            print("A quantidade tem que ser um número inteiro positivo!")
def validar_minimo():
    while True:
        try:
            estomin = int(input("Estoque Mínimo: "))
            if estomin <= 0:
                print("O estoque mínimo tem que ser um número inteiro positivo!")
            else:
                return estomin
        except ValueError:
            print("O estoque mínimo tem que ser um número inteiro positivo!")
def cadastro_produto():
    print("\n","-"*5,"CADASTRO DE PRODUTO","-"*5)
    nome = validar_nome()
    tipo = validar_categoria()
    valor = validar_preco()
    qtd = validar_quantidade()
    min = validar_minimo()

    cursor.execute('''
                   INSERT INTO reservatorio (nome,categoria,preco,quantidade,estoqueminimo) 
                   VALUES (?,?,?,?,?)
                   ''', (nome,tipo,valor,qtd,min))
    conn.commit()
    id_produto = cursor.lastrowid
    print(f"ID DO PRODUTO {nome}: {id_produto}")

def excluir_produto():
    print("\n", "-"*5, "EXCLUIR PRODUTO", "-"*5)
    try:
        id_produto = int(input("Digite o ID do produto a ser excluído: "))
    except ValueError:
        print("Digite um ID válido!")
        return
    cursor.execute('SELECT nome FROM reservatorio WHERE id_produto = ?', (id_produto,))
    item = cursor.fetchone()
    if item:
        nome = item[0]
        confirmacao = input(f"Deseja realmente remover '{nome}' (ID: {id_produto})? (S/N)\n").strip().upper()
        if confirmacao == 'S':
            cursor.execute('DELETE FROM reservatorio WHERE id_produto = ?', (id_produto,))
            conn.commit()
            print("Produto removido com sucesso!")
        elif confirmacao == 'N':
            print("Operação cancelada!")
        else:
            print("Digite uma operação válida.")
    else:
        print("Produto não encontrado!")

def menu():
    while True:
        print("\n", "="*50, "SELECIONE UMA AÇÃO", "="*50, "\n")
        print("1 - Cadastrar Produto\n2 - Excluir Produto\n0 - Sair do Sistema")
        try:
            acao = int(input("Escolha uma ação: "))
            match acao:
                case 1:
                    cadastro_produto()
                case 2:
                    excluir_produto()
                case 0:
                    print("-"*55, "SAINDO", "-"*55)
                    break
                case _:
                    print("Opção inválida! Digite uma ação válida.")
        except ValueError:
            print("Caractere inválido! Tente novamente.")


menu()