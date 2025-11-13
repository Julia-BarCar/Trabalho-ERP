import sqlite3

# Cria uma conexão do código  com um banco de dadoss
conn = sqlite3.connect('banco_de_dados.db')
cursor  = conn.cursor()
# Cursor = interpretador dos comandos sql do sistema
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estoque (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        quantidade INTEGER,
        preco REAL,
        estoquemin INTEGER
    )
''')

def validar_nome():
    while True:
# Faz repetir o símbolo do igual 100 vezes
        print("\n" + "="*100)
#.title bota a inicial das palavras em maiúsculo
        name = input("Nome do produto: ").title()
        if name:
            return name
        print("Nome inválido. Digite um produto válido!")
def validar_quantidade():
    while True:
        try:
            quant = int(input("Quantidade: "))
            if quant:
                return quant
        except ValueError:
            print("Quantidade inválida. Digite um valor válido!")
def validar_preco():
    while True:
        try:
            valor = float(input("Preço unitário: "))
            if valor:
                return valor
        except ValueError:
            print("Preço inválido. Digite um valor válido!")
def validar_estoquemin():
    while True:
        try:
            estomin = int(input("Estoque mínimo: "))
            if estomin:
                return estomin
        except ValueError:
            print("Quantidade inválida. Digite um estoque válido!")
def cadastrar_produto():
    nome = validar_nome()
    quantidade = validar_quantidade()
    preco = validar_preco()
    estoquemin = validar_estoquemin()
# Insere nas colunas os valores das variáveis ditas anteriormente
    cursor.execute('''
        INSERT INTO estoque (nome, quantidade, preco, estoquemin)
        VALUES (?, ?, ?, ?)
    ''', (nome, quantidade, preco, estoquemin))
# .commit é para salvar as mudanças feitas na Database
    conn.commit()
# .lastrowid fornece o id da última linha inserida com sucesso
    id = cursor.lastrowid
    print(f"Produto cadastrado com sucesso! ID: {id}")

def listar_estoque():
    print("\n" + "-" * 60, "LISTAR ESTOQUE", "-" * 60)
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

# Executa a consulta para todas as linhas da tabela estoque
    cursor.execute("SELECT COUNT(*) FROM estoque")
# .fetchone é para recuperar uma única linha da tabela
    qtd = cursor.fetchone()[0]
    print(f"Quantidade de produtos no estoque: {qtd}")

    cursor.execute("SELECT * FROM estoque ORDER BY id")
# .fetchall é para recuperar todas as linhas de tuplas de uma só vez
    produtos = cursor.fetchall()

    conn.close()

    if not produtos:
        print("-" * 10, "Estoque vazio!", "-" * 10)
        return

# Os números são para formatar o print numa saída bonita
    print(f"\n{'ID':<10} {'Nome':<25} {'Qtd':<8} {'Preço':<12} {'Total':<12}")
    print("-" * 70)

    for produto in produtos:
        id, nome, quantidade, preco, estomin = produto
        total = quantidade * preco
        alerta = "⚠" if quantidade <= estomin else " "
        print(f"{id:<10} {nome:<25} {quantidade:<8} {preco:<12.2f} {total:<12.2f} {alerta}")

def atualizar_qtd():
    print("\n", "-"*60,"ATUALIZAR QUANTIDADE","-"*60)
    try: 
        codigo = int(input("Digite o ID do produto desejado: ").strip())
    except ValueError:
        print("Digite um código válido!")
        return
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nome, quantidade FROM estoque WHERE id = ?", (codigo,))
    produto = cursor.fetchone()

    if not produto:
        print(f"Produto com código '{codigo}' não encontrado.")
        conn.close()
        return

    nome, qtd_atual = produto
    print(f"Produto: {nome}")
    print(f"Quantidade atual: {qtd_atual}")
    
    try:
        opcao = int(input("\n1 - Adicionar Quantidade\n2 - Subtrair Quantidade\nDigite qual a opção escolhida: ").strip())
    except ValueError:
        print("Erro: Digite um número válido para a opção!")
        conn.close()
        return

    try:
        match opcao:
            case 1:
                qtd_atualizada = int(input("Quantidade a ser adicionada: ").strip())
                if qtd_atualizada <= 0:
                    print("Quantidade a ser adicionada tem que ser positiva!")
                    return
                nova_qtd = qtd_atual + qtd_atualizada
                cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (nova_qtd, codigo))
                conn.commit()
                print(f"\n{qtd_atualizada} unidades adicionadas!\nNova quantidade: {nova_qtd}")
            case 2:
                qtd_atualizada = int(input("Quantidade a ser subtraída: ").strip())
                if qtd_atualizada <= 0:
                    print("Quantidade a ser subtraída deve ser maior que zero!")
                    return
                if qtd_atualizada > qtd_atual:
                    print(f"Não há estoque suficiente para retirar {qtd_atualizada} unidades.")
                    return
                nova_qtd = qtd_atual - qtd_atualizada
                cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (nova_qtd, codigo))
                conn.commit()
                print(f"\n{qtd_atualizada} unidades removidas!\nNova quantidade: {nova_qtd}")
            case _:
                print("Digite uma opção válida!")
    except ValueError:
        print("Erro: Digite um número válido para a quantidade!")
# O próximo bloco vai rodar independentemente de ter ocorrido uma exeção do try ou não
    finally:
        conn.close()

def remover_produto():
    print("\n", "-"*60,"REMOVER PRODUTO","-"*60)
    try:
        codigo = int(input("Digite o ID do produto: "))
    except ValueError:
        print("Produto não encontrado! Digite um ID válido.")
        return
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT nome FROM estoque WHERE id = ?',(codigo,))
    produto = cursor.fetchone()

    if produto:
        nome = produto [0]
# .strip é para remover caracteres de espaço branco que houver antes e depois do input
        confirmacao = input(f"Deseja realmente remover '{nome}' (ID: {codigo})? (S/N)\n").strip().upper()
        if confirmacao == 'S':
            cursor.execute('DELETE FROM estoque WHERE id = ?',(codigo,))
            conn.commit()
            print("Produto removido com sucesso!")
        elif confirmacao == 'N':
            print("Operação cancelada!")
        else:
            print("Digite uma operação  válida.")
            return
    
    conn.close()

def consultar_produto():
    print("\n", "-"*60,"CONSULTAR PRODUTO","-"*60)
    try:
        codigo = int(input("Digite o ID do produto: "))
    except ValueError:
        print("Produto não encontrado! Digite um ID válido.")
        return
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM estoque WHERE id = ?',(codigo,))
    produto = cursor.fetchone()
    conn.close()

    if produto:
        codigo, nome, quantidade, preco, estoquemin = produto
        print(f"\nID: {codigo}")
        print(f"Produto: {nome}")
        print(f"Quantidade: {quantidade} unidades")
        print(f"Estoque Mínimo: {estoquemin} unidades")
        print(f"Preço Unitário: R${preco:.2f}")
        print(f"Preço total: R${quantidade*preco:.2f}")
        if quantidade <= estoquemin:
            print(f"⚠ Estoque de {nome} baixo! ⚠")
    else:
        print(f"Produto com ID {codigo} não encontrado.")

def estoque_baixo():
    print("\n", "-"*50,"PRODUTOS EM ESTOQUE BAIXO","-"*50)
    
    conn = sqlite3.connect('banco_de_dados.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, nome, quantidade, estoquemin
        FROM estoque
        WHERE quantidade <= estoquemin
        ORDER BY id
    ''')
    produtos_baixo = cursor.fetchall()
    conn.close()

    if not produtos_baixo:
        print("Não há produtos abaixo do limite no estoque!")
        return
    
    print(f"\n{'ID':<10} {'Nome':<25} {'Qnt Atual':<12} {'Mínimo':<10}")
    print("-"*60)

    for produtos in produtos_baixo:
        codigo, nome, quantidade,  estoquemin = produtos
        print(f"\n{codigo:<10} {nome:<25} {quantidade:<12} {estoquemin:<10}")
    
    print("-"*60)
    print("⚠ Produtos com Estoque Baixo! ⚠")


def menu():
    while True:
        try:
            print ("\n" + "="*50,"SELECIONE UMA OPÇÃO","="*50)
            print ("\n1 - Adicionar Produto\n2 - Listar Estoque\n3 - Atualizar Estoque\n4 - Remover Produto",
            "\n5 - Consultar Produto\n6 - Consultar Estoque Baixo\n0 - Sair")
            acao = int(input("Escolha a opção: "))
            match acao:
                case 1:
                    cadastrar_produto()
                case 2:
                    listar_estoque()
                case 3:
                    atualizar_qtd()
                case 4:
                    remover_produto()
                case 5:
                    consultar_produto()
                case 6:
                    estoque_baixo()
                case 0:
                    print("."*60,"SAINDO","."*60)
                    break
                case _ :
                    print("Ação não possível. Digite uma opção válida!")
        except ValueError:
            print("Ação não possível! Tente digitar uma opção válida!")

menu()