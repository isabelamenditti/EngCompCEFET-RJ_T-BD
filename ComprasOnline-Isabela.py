# Trabalho Banco de Dados - Sistema de Gerenciamento de Compras Online - Isabela Alves
# Por Organização, todas as interfaces foram colocadas dentro de uma pasta chamada (Interface)
from datetime import date

import mysql.connector
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> VARIÁVEIS GLOBAIS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
global x #será uma variável auxiliar para verificar de qual opção o cadastro de CPF está vindo
global cpf_cliente # armazena o valor do CPF do cliente


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CONECTANDO O BANCO DE DADOS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
BD = mysql.connector.connect(
    host='localhost',
    database='sistema_compras',
    user='root',
    password='#######')

cursor = BD.cursor()

'''if BD.is_connected(): # testando a conexão do banco de dados
    print("BD conectado!")'''

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FUNÇÕES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def Resetar_Dados(): # função para limpar as caixas de texto das telas
    tela5.cpf.setText("")
    tela3.nome.setText("")
    tela3.telefone.setText("")
    tela4.nomeUsuario.setText("")
    tela4.email.setText("")
    tela4.senha.setText("")
    tela6.sku.setText("")
    tela6.qtdAdc.setText("")
    tela7.tipo.setText("")
    tela7.qtd.setText("")
    tela7.preco.setText("")
    tela8.sku.setText("")
    tela8.qtdAdc.setText("")
    tela9.sku.setText("")
    tela9.qtdAtualizar.setText("")
    tela17.sku.setText("")
    tela10.cupom.setText("")
    tela23.local.setText("")

def Inicio():
    Resetar_Dados()
    tela1.show()

def Excluir_Produto():
    tela17.close()
    # recebendo os dados do produto a ser excluido. Lembrando que:
    # tela17.sku.text() recebe o sku do produto

    # a exclusão não poderá ser efetivamente concluída, devido ao fato das vendas necessitarem armazenar ainda esse conteúdo
    cursor.execute("UPDATE produto SET quantidade = -1 WHERE sku_produto = {};".format(tela17.sku.text()))
    BD.commit()

    Inicio()

def Atualizar_Preco():
    tela18.close()
    # recebendo os dados de atualização do produto. Lembrando que:
    # tela18.sku.text() recebe o sku do produto
    # tela18.preco.text() recebe o preço do produto que será modificado

    # atualizando o preço
    cursor.execute("UPDATE produto SET preco_produto = {} WHERE sku_produto = {};".format(tela18.preco.text(), tela18.sku.text()))
    BD.commit()

    Inicio()

def Atualizar_Quantidade():
    tela8.close()
    # recebendo os dados de atualização do produto. Lembrando que:
    # tela8.sku.text() recebe o sku do produto
    # tela8.qtdAdc.text() recebe a quantidade de produto que será inserida a mais no estoque

    # atualizando a quantidade
    cursor.execute("UPDATE produto SET quantidade = quantidade + {} WHERE sku_produto = {};".format(tela8.qtdAdc.text(), tela8.sku.text()))
    BD.commit()

    Inicio()

def Cadastrar_Produto():
    tela7.close()
    # recebendo os dados do cadastro do produto. Lembrando que:
    # tela7.tipo.text() armazena o tipo de produto. Ex: caneta azul compactor/caneta preta bic/ borracha branca pentel
    # tela7.qtd.text() armazena a quantidade de produto que será inserida
    # tela7.preco.text() armazena o preco do produto

    Query = "INSERT INTO produto (tipo_produto, quantidade, preco_produto) VALUES (%s, %s, %s);"  # inserindo os valores no BD
    info = (tela7.tipo.text(), tela7.qtd.text(), tela7.preco.text())
    cursor.execute(Query, info)
    BD.commit()

    Inicio() # retorna a tela principal

def Alteracoes_Estoque():
    tela2.close()

    # opcao1: produto novo
    if tela2.op1.isChecked():
        tela7.show()

    # opcao2: repor estoque = adicionar mais quantidade de produto
    elif tela2.op2.isChecked():
        tela8.show()

    # opcao2: atualizar preço de produto
    elif tela2.op3.isChecked():
        tela18.show()

    # opcao4: excluir produto
    elif tela2.op4.isChecked():
        tela17.show()

def Cadastro_Web():
    tela4.close()
    # recebendo os dados do cadastro Web. Lembrando que:
    # tela4.nomeUsuario.text() armazena o user do cliente
    # tela4.email.text() armazena o email do cliente
    # tela4.senha.text() armazena a senha do cliente

    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text())) # captando o ID ligado ao CPF
    res = cursor.fetchall() # recebendo o resultado
    id_cliente = res[0][0]

    Query = "INSERT INTO usuarioWeb (nome_login, id_cliente, status_conta, email_cliente, senha) VALUES (%s, %s, %s, %s, %s);" # inserindo os valores no BD
    info = (tela4.nomeUsuario.text(), id_cliente, 'novo', tela4.email.text(), tela4.senha.text())
    cursor.execute(Query, info)
    BD.commit()

    Inicio() # retorna ao menu principal

def Cadastro_Cliente():
    tela3.close()
    # recebendo os dados do cadastro do cliente. Lembrando que:
    # tela5.cpf.text() armazena o cpf do cliente
    # tela3.nome.text() armazena o nome do cliente
    # tela3.telefone.text() armazena o telefone do cliente

    # verificando se o cadastro será também como usuário Web
    if tela3.opcaoSim.isChecked(): # Será cadastrado como usuario Web
        web_cliente = 'S'
        tela4.show()

    else: # NÂO é usuário Web
        web_cliente = 'N'

    Query = "INSERT INTO conta_cliente (CPF, nome, telefone, usuario_web) VALUES (%s, %s, %s, %s);" # inserindo os valores no BD
    info = (tela5.cpf.text(), tela3.nome.text(), tela3.telefone.text(), web_cliente)
    cursor.execute(Query, info)
    BD.commit()

    if web_cliente == 'N':
        Inicio() # retorna ao menu principal

def Inserir_Cupom():
    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]

    if tela10.cupom.text() != '': # inserindo cupom de desconto
        cursor.execute("SELECT desconto FROM cupom WHERE cupom_desconto = '{}';".format(tela10.cupom.text()))
        desc = cursor.fetchall()  # recebendo o valor do desconto
        Desconto = desc[0][0]
        ValorTotal = float(ValorTotal) * float(Desconto)
        cursor.execute("UPDATE pedidos SET valor_total = {} WHERE id_carrinho = {};".format(ValorTotal, IDcarrinho))

    tela10.listWidget.clear()  # printando o valor total do pedido na tela
    tela10.listWidget.addItem(str(ValorTotal))

def Forma_Pagamento():
    tela10.close()

    # boleto
    if tela10.boleto.isChecked():
        tipo_pgto = 'boleto'

    # pix
    elif tela10.pix.isChecked():
        tipo_pgto = 'pix'

    # Cartão de crédito
    elif tela10.cartao.isChecked():
        tipo_pgto = 'cartao de credito'

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]

    # alterando a quantidade de produtos no estoque
    cursor.execute("SELECT sku_produto, qtd_carrinho FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    produtos = cursor.fetchall()  # recebendo o resultado
    NumProdutos = len(produtos)

    for i in range(0, NumProdutos):
        cursor.execute("UPDATE produto SET quantidade = quantidade - {} WHERE sku_produto = {};".format(produtos[i][1], produtos[i][0]))

    cursor.execute("UPDATE pedidos SET tipo_pgto = '{}' WHERE id_carrinho = {};".format(tipo_pgto, IDcarrinho))

    BD.commit()

    Inicio()

def Endereco_Entrega():
    tela19.close()
    # recebendo os dados do endereço de entrega. Lembrando que:
    # tela19.rua.text() armazena a rua
    # tela19.num.text() armazena o numero
    # tela19.bairro.text() armazena o bairro
    # tela19.cidade.text() armazena a cidade
    # tela19.estado.text() armazena o estado
    # tela19.cep.text() armazena o cep

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # inserindo o endereço no BD
    Query = "INSERT INTO enderecos(rua, numero, bairro, cidade, estado, cep, id_cliente) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    info = (tela19.rua.text(), tela19.num.text(), tela19.bairro.text(), tela19.cidade.text(), tela19.estado.text(), tela19.cep.text(), IDcliente)
    cursor.execute(Query, info)

    BD.commit()

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]

    # captando o endereço ligado ao cliente
    cursor.execute("SELECT MAX(id_endereco) FROM enderecos WHERE id_cliente = {};".format(IDcliente))
    end = cursor.fetchall()  # recebendo o resultado
    IDendereco = end[0][0]

    data = date.today()

    # inserindo o pedido no BD
    Query = "INSERT INTO pedidos(id_endereco, status_pedido, data_pedido, id_carrinho, valor_total) VALUES (%s, %s, %s, %s, %s);"
    info = (IDendereco, 'confirmado', data, IDcarrinho, ValorTotal)
    cursor.execute(Query, info)

    BD.commit()

    tela10.listWidget.addItem(str(ValorTotal))  # imprimindo o valor total do carrinho na tela
    tela10.show()

def Ir_Carrinho():
    tela9.close()
    tela19.show()

def Atualizar_Carrinho():
    # recebendo os dados dos produto que estão no carrinho. Lembrando que:
    # tela9.sku.text() possui o sku do produto
    # tela9.qtdAtualizar.text() armazena a quantidade que será atualizada no carrinho
    # tela9.cupom.text() retorna o cupom de desconto

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    if int(tela9.qtdAtualizar.text()) > 0: # atualizando itens no carrinho
        cursor.execute("UPDATE itens_carrinho SET qtd_carrinho = {} WHERE id_carrinho = {} AND sku_produto = {};".format(tela9.qtdAtualizar.text(), IDcarrinho, tela9.sku.text()))  # atualizando a qtd no BD

    else: # caso a quantidade seja menor que 0, exclui item do carrinho
        cursor.execute("DELETE FROM itens_carrinho WHERE id_carrinho = {} AND sku_produto = {};".format(IDcarrinho, tela9.sku.text()))  # excluindo o item no BD

    BD.commit()

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]

    tela9.listWidget.clear() # printando o valor total do carrinho na tela
    tela9.listWidget.addItem(str(ValorTotal))

    cursor.execute("SELECT sku_produto, preco_compra, qtd_carrinho FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))  # obtendo os dados dos produtos contidos no carrinho da pessoa
    itens = cursor.fetchall()

    tela9.tableWidget.clearContents()

    # captando o numero de linhas e colunas de produtos para imprimir na tela
    linhas = len(itens)
    colunas = 3

    tela9.tableWidget.setRowCount(linhas)
    tela9.tableWidget.setColumnCount(colunas)

    for i in range(0, linhas):  # imprimindo os dados dos produtos na tela
        for j in range(0, colunas):
            tela9.tableWidget.setItem(i, j, QTableWidgetItem(str(itens[i][j])))

def Finalizar_Depois():
    tela9.close()

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]

    # inserindo o pedido no BD
    Query = "INSERT INTO pedidos(status_pedido, id_carrinho, valor_total) VALUES (%s, %s, %s);"
    info = ('não finalizado', IDcarrinho, ValorTotal)
    cursor.execute(Query, info)

    BD.commit()

    Inicio()

def Finalizar_Carrinho():
    tela6.close()

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    IDcliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(IDcliente))
    res = cursor.fetchall()  # recebendo o resultado
    IDcarrinho = res[0][0]

    cursor.execute("SELECT sku_produto, preco_compra, qtd_carrinho FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho)) # obtendo os dados dos produtos no carrinho
    itens = cursor.fetchall()

    # calculando o valor total do carrinho
    cursor.execute("SELECT SUM(preco_compra*qtd_carrinho) FROM itens_carrinho WHERE id_carrinho = {};".format(IDcarrinho))
    valor = cursor.fetchall()  # recebendo o resultado
    ValorTotal = valor[0][0]
    tela9.listWidget.addItem(str(ValorTotal)) # imprimindo o valor total do carrinho na tela

    # captando o numero de linhas e colunas de produtos para imprimir na tela
    linhas = len(itens)
    colunas = 3

    tela9.tableWidget.setRowCount(linhas)
    tela9.tableWidget.setColumnCount(colunas)

    for i in range(0, linhas):  # imprimindo os dados dos produtos na tela
        for j in range(0, colunas):
            tela9.tableWidget.setItem(i, j, QTableWidgetItem(str(itens[i][j])))

    tela9.show()

def Inserir_Carrinho():
    # recebendo os dados do produto que será adicionado ao carrinho. Lembrando que:
    # tela6.sku.text() possui o sku do produto
    # tela6.qtdAdc.text() armazena a quantidade adicionada ao carrinho

    # captando o preço relacionado ao sku
    cursor.execute("SELECT preco_produto FROM produto WHERE sku_produto = {};".format(tela6.sku.text()))
    p = cursor.fetchall()  # recebendo o resultado
    preco = p[0][0]

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    id_cliente = id[0][0]

    # captando o id do carrinho atual ligado àquele cliente
    cursor.execute("SELECT MAX(id_carrinho) FROM carrinho WHERE id_cliente = {};".format(id_cliente))
    res = cursor.fetchall()  # recebendo o resultado
    id_carrinho = res[0][0]

    # inserindo itens no carrinho
    Query = "INSERT INTO itens_carrinho (sku_produto, preco_compra, id_carrinho, qtd_carrinho) VALUES (%s, %s, %s, %s);"  # criando o carrinho no BD
    info = (tela6.sku.text(), preco, id_carrinho, tela6.qtdAdc.text())  # inicialmente nenhum carrinho tem cupom na criação
    cursor.execute(Query, info)

    cursor.execute("SELECT usuario_web FROM conta_cliente WHERE id_cliente = {};".format(id_cliente))
    w = cursor.fetchall()  # recebendo o resultado
    web = p[0][0]

    if web == 'S':
        cursor.execute("UPDATE usuarioWeb SET status_conta = 'ativo' WHERE id_cliente = {};".format(id_cliente)) # atualizando status do usuario

    BD.commit()

def Atualizar_ClienteWeb():
    tela13.close()
    # tela13.nome.text() capta o nome a ser atualizado
    # tela13.telefone.text() capta o telefone a ser atualizado
    # tela13.nomeUsuario.text() capta o user a ser atualizado
    # tela13.email.text() capta o email a ser atualizado
    # tela13.senha.text() capta o email a ser atualizado

    # captando o ID ligado ao CPF
    cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
    id = cursor.fetchall()  # recebendo o resultado
    id_cliente = id[0][0]

    cursor.execute("UPDATE conta_cliente SET nome = '{}', telefone = {} WHERE CPF = {};".format(tela13.nome.text(), tela13.telefone.text(), tela5.cpf.text()))
    cursor.execute("UPDATE usuarioWeb SET nome_login = '{}', status_conta = '{}', email_cliente = '{}', senha = '{}' WHERE id_cliente = {};".format(tela13.nomeUsuario.text(), tela13.status.text(), tela13.email.text(), tela13.senha.text(), id_cliente))

    BD.commit()

    Inicio()

def Atualizar_Cliente():
    tela12.close()
    # tela12.nome.text() capta o nome a ser atualizado
    # tela12.telefone.text() capta o telefone a ser atualizado

    cursor.execute("UPDATE conta_cliente SET nome = '{}', telefone = {} WHERE CPF = {};".format(tela12.nome.text(), tela12.telefone.text(), tela5.cpf.text()))

    BD.commit()
    Inicio()

def Excluir_conta():
    tela14.close()

    if tela14.sim.isChecked():
        # verificando se é usuário web
        cursor.execute("SELECT id_cliente, usuario_web FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
        p = cursor.fetchall()  # recebendo o resultado
        Web = p[0][1]

        if Web == 'S':
            cursor.execute("UPDATE usuarioWeb SET nome_login = 'EXCLUIDO', status_conta = 'EXCLUIDO', email_cliente = 'EXCLUIDO', senha = '0' WHERE id_cliente = {};".format(p[0][0]))

        # limpando dados da conta
        cursor.execute("UPDATE conta_cliente SET CPF = 0, nome = 'EXCLUIDO', telefone = 0 WHERE CPF = {};".format(tela5.cpf.text()))

        BD.commit()
        Inicio()

    elif tela14.nao.isChecked():
        Inicio()

def Exibir_Pedidos():
    tela15.close()
    Inicio()

def Usuario_Opcoes():
    tela11.close()

    # opcao1: atualizar dados
    if tela11.op1.isChecked():
        cursor.execute("SELECT id_cliente, nome, telefone, usuario_web FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))
        p = cursor.fetchall()  # recebendo o resultado
        Web = p[0][3]

        if Web == 'S': # buscando os dados do usuário
            cursor.execute("SELECT nome_login, status_conta, email_cliente, senha FROM usuarioWeb WHERE id_cliente = '{}';".format(p[0][0]))
            q = cursor.fetchall()  # recebendo o resultado do usuario web

            tela13.nome.setText(str(p[0][1])) # mostrando os dados atuais para modificação
            tela13.status.setText(str(q[0][1]))
            tela13.telefone.setText(str(p[0][2]))
            tela13.nomeUsuario.setText(str(q[0][0]))
            tela13.email.setText(str(q[0][2]))
            tela13.senha.setText(str(q[0][3]))

            tela13.show()

        else:
            tela12.nome.setText(str(p[0][1]))  # mostrando os dados atuais para modificação
            tela12.telefone.setText(str(p[0][2]))

            tela12.show()

    # opcao2: excluir conta
    elif tela11.op2.isChecked():
        tela14.show()

    # opcao3: exibir pedidos
    elif tela11.op3.isChecked():
        cursor.execute("SELECT id_cliente FROM conta_cliente WHERE CPF = {};".format(tela5.cpf.text()))  # buscando o id do cliente
        idCliente = cursor.fetchall()

        cursor.execute("SELECT id_pedido, status_pedido, valor_total FROM pedidos WHERE EXISTS (SELECT id_carrinho FROM carrinho WHERE id_cliente = {});".format(idCliente[0][0]))
        pedidos = cursor.fetchall()  # obtendo os dados dos pedidos

        # captando o numero de linhas e colunas de pedidos para imprimir na tela
        linhas = len(pedidos)
        colunas = 3

        tela15.tableWidget.setRowCount(linhas)
        tela15.tableWidget.setColumnCount(colunas)

        for i in range(0, linhas):  # imprimindo os dados dos produtos na tela
            for j in range(0, colunas):
                tela15.tableWidget.setItem(i, j, QTableWidgetItem(str(pedidos[i][j])))

        tela15.show()

def Status_Error():
    tela20.close()
    Inicio()

def Verifica_CPF():
    tela5.close()

    cpf_cliente = tela5.cpf.text()

    # opcao1: cadastrar cliente
    if tela1.op1.isChecked():
        tela3.show()

    #opcao3: realizar pedido
    elif tela1.op3.isChecked():
        cursor.execute("SELECT id_cliente, usuario_web FROM conta_cliente WHERE CPF = {};".format(cpf_cliente))  # captando o ID ligado ao CPF
        res = cursor.fetchall()  # recebendo o resultado
        id_cliente = res[0][0]
        Web = res[0][1]

        if Web == 'S': # buscando os dados do usuário
            cursor.execute("SELECT status_conta FROM usuarioWeb WHERE id_cliente = '{}';".format(id_cliente))
            s = cursor.fetchall()  # recebendo o resultado do usuario web
            status = s[0][0]

            if status == 'bloqueado' or status == 'banido':
                tela20.listWidget.addItem(str(status))  # imprimindo o status atual do cliente
                tela20.show()
                return

        tela6.show()

        cursor.execute("SELECT * FROM produto WHERE quantidade <> -1;")  # obtendo os dados dos produtos
        produtos = cursor.fetchall()

        # captando o numero de linhas e colunas de produtos para imprimir na tela
        linhas = len(produtos)
        colunas = 4

        tela6.tableWidget.setRowCount(linhas)
        tela6.tableWidget.setColumnCount(colunas)

        for i in range(0, linhas): #imprimindo os dados dos produtos na tela
            for j in range(0, colunas):
                tela6.tableWidget.setItem(i, j, QTableWidgetItem(str(produtos[i][j])))

            # criação do carrinho de compras
            Query = "INSERT INTO carrinho (id_cliente, cupom_desconto) VALUES (%s, %s);"  # criando o carrinho no BD
            info = (id_cliente, 'NONE') # inicialmente nenhum carrinho tem cupom na criação
            cursor.execute(Query, info)
            BD.commit()

    # opcao4: dados de cliente
    elif tela1.op4.isChecked():
        tela11.show()

def Usuarios_Cadastrados():
    tela21.close()
    Inicio()

def PgtoMais_Utilizado():
    tela22.close()
    Inicio()

def Usuarios_Local():
    tela24.close()
    Inicio()

def Filtrar_Local():
    tela23.close()

    if tela23.op1.isChecked():
        # calculando o numero total de clientes por bairro
        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE id_cliente = (SELECT MAX(id_cliente) FROM enderecos WHERE bairro = '{}') AND CPF <> 0;".format(tela23.local.text()))
        Clientes = cursor.fetchall()  # obtendo os ids dos clientes naquele bairro

    elif tela23.op2.isChecked():
        # calculando o numero total de clientes por cidade
        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE id_cliente = (SELECT MAX(id_cliente) FROM enderecos WHERE cidade = '{}') AND CPF <> 0;".format(tela23.local.text()))
        Clientes = cursor.fetchall()  # obtendo os ids dos clientes naquela cidade

    elif tela23.op3.isChecked():
        # calculando o numero total de clientes por estado
        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE id_cliente = (SELECT MAX(id_cliente) FROM enderecos WHERE estado = '{}') AND CPF <> 0;".format(tela23.local.text()))
        Clientes = cursor.fetchall()  # obtendo os ids dos clientes naquele estado

    # captando o numero de linhas e colunas de pedidos para imprimir na tela
    linhas = len(Clientes)
    colunas = 2

    tela24.tableWidget.setRowCount(linhas)
    tela24.tableWidget.setColumnCount(colunas)

    for i in range(0, linhas):  # imprimindo os dados dos clientes na tela
        for j in range(0, colunas):
            tela24.tableWidget.setItem(i, j, QTableWidgetItem(str(Clientes[i][j])))

    tela24.show()

def Estado_MaxVendas():
    tela25.close()
    Inicio()

def Media_Anual():
    tela26.close()
    Inicio()

def Maiores_Vendas():
    tela27.close()
    Inicio()

def Carrinhos_NaoFinalizados():
    tela28.close()
    Inicio()

def Clientes_Fidelidade():
    tela29.close()
    Inicio()

def Estatistica_Empresa():
    tela16.close()

    # opcao1: usuários cadastrados
    if tela16.op1.isChecked():

        # calculando o numero total de clientes
        cursor.execute("SELECT COUNT(id_cliente) FROM conta_cliente WHERE CPF <> 0;")
        cont = cursor.fetchall()  # recebendo o resultado

        contador = cont[0][0] # contando o numero de clientes com conta ativa

        tela21.listWidget.addItem(str(contador))  # imprimindo o valor total de clientes na tela

        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE CPF <> 0;")
        usuarios = cursor.fetchall()  # obtendo os dados dos pedidos

        # captando o numero de linhas e colunas de pedidos para imprimir na tela
        linhas = len(usuarios)
        colunas = 2

        tela21.tableWidget.setRowCount(linhas)
        tela21.tableWidget.setColumnCount(colunas)

        for i in range(0, linhas):  # imprimindo os dados dos clientes na tela
            for j in range(0, colunas):
                tela21.tableWidget.setItem(i, j, QTableWidgetItem(str(usuarios[i][j])))

        tela21.show()

    # opcao2: Forma de pagamento mais utilizada
    elif tela16.op2.isChecked():

        cursor.execute("SELECT tipo_pgto, COUNT(tipo_pgto) FROM pedidos GROUP BY tipo_pgto HAVING MAX(tipo_pgto) > 0 ORDER BY count(tipo_pgto) DESC;")
        cont = cursor.fetchall()  # recebendo o resultado

        contador = cont[0][0]

        tela22.listWidget.addItem(str(contador))  # imprimindo o maior tipo de pgto utilizado na tela

        tela22.show()

    # opcao3: Filtro de usuários por localidade
    elif tela16.op3.isChecked():
        tela23.show()

    # opcao4: Estado Campeão de Vendas
    elif tela16.op4.isChecked():

        cursor.execute("SELECT estado, COUNT(estado) FROM enderecos GROUP BY estado HAVING MAX(estado) >= 0 ORDER BY count(estado) DESC;")
        cont = cursor.fetchall()  # recebendo o resultado

        contador = cont[0][0]

        tela25.listWidget.addItem(str(contador))  # imprimindo o estado com maior numero de vendas
        tela25.show()

    # opcao5: Média Anual de Vendas
    elif tela16.op5.isChecked():

        cursor.execute("SELECT SUM(valor_total) FROM pedidos WHERE status_pedido = 'confirmado';") # somando todos os pedidos
        t = cursor.fetchall()  # recebendo o resultado
        Total = t[0][0]

        cursor.execute("SELECT MIN(Year(data_pedido)) FROM pedidos WHERE status_pedido = 'confirmado';") # data primeiro pedido confirmado
        diaInicio = cursor.fetchall()  # recebendo o resultado
        anoInicio = diaInicio[0][0]

        cursor.execute("SELECT MAX(Year(data_pedido)) FROM pedidos WHERE status_pedido = 'confirmado';") # data ultimo pedido confirmado
        diaFim = cursor.fetchall()  # recebendo o resultado
        anoFim = diaFim[0][0]

        anos = anoFim - anoInicio + 1 # calculando a diferença de anos existente
        Media = Total/anos

        tela26.listWidget.addItem(str(Media))  # imprimindo a media anual de vendas

        tela26.show()

    # opcao6: Mês e ano com Maior Venda
    elif tela16.op6.isChecked():

        # ano com maior venda
        cursor.execute("SELECT Year(data_pedido), SUM(valor_total) FROM pedidos WHERE status_pedido <> 'não finalizado' GROUP BY Year(data_pedido) HAVING SUM(valor_total) >= 0 ORDER BY SUM(valor_total) DESC;")
        ano = cursor.fetchall()  # recebendo o resultado
        anoMaior = ano[0][0]

        tela27.listWidget.addItem(str(anoMaior))  # imprimindo o ano com maior venda

        # mês com maior venda naquele ano
        cursor.execute("SELECT Month(data_pedido), SUM(valor_total) FROM pedidos WHERE status_pedido <> 'não finalizado' AND Year(data_pedido) = {} GROUP BY Month(data_pedido) HAVING SUM(valor_total) >= 0 ORDER BY SUM(valor_total) DESC;".format(anoMaior))
        mes = cursor.fetchall()  # recebendo o resultado
        mesMaior = mes[0][0]

        tela27.listWidget_2.addItem(str(mesMaior))  # imprimindo o ano com maior venda

        tela27.show()

    # opcao7: Clientes fidelidade
    elif tela16.op7.isChecked():

        # captando o nome e o cpf dos usuarios que compraram todos os meses do ano
        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE id_cliente = (SELECT id_cliente FROM carrinho WHERE id_carrinho = (SELECT id_carrinho FROM pedidos WHERE EXISTS(SELECT num_mes FROM meses WHERE num_mes NOT IN (SELECT month(data_pedido) FROM pedidos))));")
        resultado = cursor.fetchall()  # recebendo o resultado

        linhas = len(resultado)
        colunas = 2

        tela29.tableWidget.setRowCount(linhas)
        tela29.tableWidget.setColumnCount(colunas)

        for i in range(0, linhas):  # imprimindo os dados dos produtos na tela
            for j in range(0, colunas):
                tela29.tableWidget.setItem(i, j, QTableWidgetItem(str(resultado[i][j])))

        tela29.show()

    # opcao8: Usuários que nao finalizaram a compra
    elif tela16.op8.isChecked():

        # captando os os usuários com pedidos não finalizados
        cursor.execute("SELECT CPF, nome FROM conta_cliente WHERE id_cliente = (SELECT id_cliente FROM carrinho WHERE id_carrinho = (SELECT id_carrinho FROM pedidos WHERE status_pedido = 'não finalizado')) AND CPF <> 0;")
        pedidosNAO = cursor.fetchall()

        # captando o numero de linhas e colunas de clientes para imprimir na tela
        linhas = len(pedidosNAO)
        colunas = 2

        tela28.tableWidget.setRowCount(linhas)
        tela28.tableWidget.setColumnCount(colunas)

        for i in range(0, linhas):  # imprimindo os dados dos clientes na tela
            for j in range(0, colunas):
                tela28.tableWidget.setItem(i, j, QTableWidgetItem(str(pedidosNAO[i][j])))

        tela28.show()

def Menu_Principal():
    tela1.close()

    #opcao1: cadastrar cliente
    if tela1.op1.isChecked():
        tela5.show()

    # opcao2: alterar estoque
    elif tela1.op2.isChecked():
        tela2.show()

    #opcao3: realizar pedido
    elif tela1.op3.isChecked():
        tela5.show()

    #opcao4: dados de cliente
    elif tela1.op4.isChecked():
        tela5.show()

    #opcao5: estatisticas da empresa
    elif tela1.op5.isChecked():
        tela16.show()


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MAIN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#>>>>>>>>>>>>>>>>>>>>>>>>> DECLARANDO AS INTERFACES <<<<<<<<<<<<<<<<<<<<<<
app = QtWidgets.QApplication([])

# declarando as telas das interfaces gráficas
tela1 = uic.loadUi("Interface/tela1.ui")
tela1.pushButton.clicked.connect(Menu_Principal)

tela5 = uic.loadUi("Interface/tela5.ui")
tela5.pushButton.clicked.connect(Verifica_CPF)

tela3 = uic.loadUi("Interface/tela3.ui")
tela3.pushButton.clicked.connect(Cadastro_Cliente)

tela4 = uic.loadUi("Interface/tela4.ui")
tela4.pushButton.clicked.connect(Cadastro_Web)

tela2 = uic.loadUi("Interface/tela2.ui")
tela2.pushButton.clicked.connect(Alteracoes_Estoque)

tela7 = uic.loadUi("Interface/tela7.ui")
tela7.pushButton_2.clicked.connect(Cadastrar_Produto)

tela8 = uic.loadUi("Interface/tela8.ui")
tela8.pushButton.clicked.connect(Atualizar_Quantidade)

tela18 = uic.loadUi("Interface/tela18.ui")
tela18.pushButton.clicked.connect(Atualizar_Preco)

tela17 = uic.loadUi("Interface/tela17.ui")
tela17.pushButton.clicked.connect(Excluir_Produto)

tela6 = uic.loadUi("Interface/tela6.ui")
tela6.pushButton.clicked.connect(Inserir_Carrinho)
tela6.pushButton_2.clicked.connect(Finalizar_Carrinho)

tela9 = uic.loadUi("Interface/tela9.ui")
tela9.pushButton.clicked.connect(Atualizar_Carrinho)
tela9.pushButton_2.clicked.connect(Ir_Carrinho)
tela9.pushButton_3.clicked.connect(Finalizar_Depois)

tela19 = uic.loadUi("Interface/tela19.ui")
tela19.pushButton.clicked.connect(Endereco_Entrega)

tela10 = uic.loadUi("Interface/tela10.ui")
tela10.pushButton.clicked.connect(Forma_Pagamento)
tela10.pushButton_2.clicked.connect(Inserir_Cupom)

tela11 = uic.loadUi("Interface/tela11.ui")
tela11.pushButton.clicked.connect(Usuario_Opcoes)

tela12 = uic.loadUi("Interface/tela12.ui")
tela12.pushButton.clicked.connect(Atualizar_Cliente)

tela13 = uic.loadUi("Interface/tela13.ui")
tela13.pushButton.clicked.connect(Atualizar_ClienteWeb)

tela14 = uic.loadUi("Interface/tela14.ui")
tela14.pushButton.clicked.connect(Excluir_conta)

tela20 = uic.loadUi("Interface/tela20.ui")
tela20.pushButton.clicked.connect(Status_Error)

tela15 = uic.loadUi("Interface/tela15.ui")
tela15.pushButton.clicked.connect(Exibir_Pedidos)

tela16 = uic.loadUi("Interface/tela16.ui")
tela16.pushButton.clicked.connect(Estatistica_Empresa)

tela21 = uic.loadUi("Interface/tela21.ui")
tela21.pushButton.clicked.connect(Usuarios_Cadastrados)

tela22 = uic.loadUi("Interface/tela22.ui")
tela22.pushButton.clicked.connect(PgtoMais_Utilizado)

tela23 = uic.loadUi("Interface/tela23.ui")
tela23.pushButton.clicked.connect(Filtrar_Local)

tela24 = uic.loadUi("Interface/tela24.ui")
tela24.pushButton.clicked.connect(Usuarios_Local)

tela25 = uic.loadUi("Interface/tela25.ui")
tela25.pushButton.clicked.connect(Estado_MaxVendas)

tela26 = uic.loadUi("Interface/tela26.ui")
tela26.pushButton.clicked.connect(Media_Anual)

tela27 = uic.loadUi("Interface/tela27.ui")
tela27.pushButton.clicked.connect(Maiores_Vendas)

tela28 = uic.loadUi("Interface/tela28.ui")
tela28.pushButton.clicked.connect(Carrinhos_NaoFinalizados)

tela29 = uic.loadUi("Interface/tela29.ui")
tela29.pushButton.clicked.connect(Clientes_Fidelidade)

#>>>>>>>>>>>>>>>>>>>>>>>>> INICIALIZANDO O PROGRAMA <<<<<<<<<<<<<<<<<<<<<<
tela1.show()  # iniciando a interface gráfica, chamando a Tela Principal
app.exec()
