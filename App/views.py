from flask import render_template, redirect, url_for, request, flash, send_from_directory
from daoMySQL import Estoque_Tabela, Vendas_Tabela, Historico_Tabela, Produtos_Tabela
from app import app, db
from models import Produto_Estoque, Produto, Produto_Model
from pprint import pprint
from helpers import verifica_form, recupera_imagem, deleta_arquivo
from time import time

estoque_tabela = Estoque_Tabela(db)
vendas_tabela = Vendas_Tabela(db)
historico_tabela = Historico_Tabela(db)
produtos_tabela = Produtos_Tabela(db)



@app.route('/')
def index():
    return render_template('index.html', titulo = 'Pagina Inicial')

@app.route('/controle_estoque')
def controle_estoque():
    itens = estoque_tabela.listar()
    itens_venda = vendas_tabela.listar()
    historico = historico_tabela.listar()
    return render_template('controle_estoque.html'
                           ,itens=itens
                           ,itens_vendas=itens_venda
                           ,historico=historico
                           ,titulo="Controle Estoque")


#Pega o parametro chamado nome_arquivo via GET
#  e aramazena em uma variavel de mesmo nome 
@app.route('/uploads/<nome_arquivo>')
#Passa o parametro recebido via GET 
# como argumento para a função
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

@app.route('/adicionar_produto')
def adicionar_produto():
    return render_template('adicionar_produto.html')

@app.route('/novo_produto', methods=['POST', 'GET'])
def novo_produto():
    vazio = False
    formularios_cria_jogo = ["nome", "categoria"]
    
    # Validação formulario
    for i in formularios_cria_jogo:
        formulario = request.form[i]
        if(not formulario):
            vazio = True
            break
    
    if(not vazio):
        # Armazena produto em um objeto produto
        novo_produto = Produto_Model(request.form["nome"], request.form["categoria"])
        error = False
        #Salva o produto na tabela enviando o objeto para o método
        retorno = produtos_tabela.salvar(novo_produto)
        print(">>>>>>>>>>>>>>>>>>>>>>>",retorno)
        if(retorno):
            produto = Produto_Model(retorno[1], retorno[2], id=retorno[0])
            flash("Produto {} salvo com sucesso".format(novo_produto.nome))
            #Pega o arquivo enviado e salva no servidor
            if('arquivo' in request.files.keys()):
                arquivo = request.files["arquivo"]                                      #Pega arquivos do request
                arquivo.save('{}/capa{}-{}.jpg'.format(app.config['UPLOAD_PATH'],produto.id, time())) #Diz aonde o arquivo será salvo e o nome do arquivo
            return redirect(url_for('produtos'))
        flash("Não é possivel registrar um produto duas vezes")
        return redirect(url_for('produtos'))
    else:
        error = True
        flash("Existem campos não preenchidos")
    return redirect(url_for('produto'))

#Pega o parametro passado pela URI, diz o tipo e já o 
# passa para a função como parametro
@app.route('/editar/<int:id>')
def editar(id):
    produto = produtos_tabela.busca_por_id(id)
    print(produto)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html'
                           ,titulo='Editando Produto' 
                           ,produto=produto
                           ,img_produto=nome_imagem
                           )

@app.route('/atualizar', methods=['POST', ])
def atualizar():
    print(request)
    produto = Produto_Model(request.form['nome']
                            ,request.form['categoria']
                            , id=request.form['id'])
    produtos_tabela.salvar(produto)
    print('>>>>>>>>>>>>>','arquivo' in request.files.keys())
    if('arquivo' in request.files.keys()):
        deleta_arquivo(produto.id)
        request.files["arquivo"].save("{}/capa{}-{}.jpg".format(app.config["UPLOAD_PATH"], produto.id, time()))
    return redirect(url_for('produtos'))
   

@app.route('/estoque')
def estoque():
    itens = estoque_tabela.listar()
    return render_template('estoque_geral.html', itens=itens)
@app.route('/atualiza_estoque', methods=['POST',])
def atualiza_estoque():
    # ADICIONAR AO ESTOQUE
    if(verifica_form(request.form)):
        if('add_est' in request.form.keys()):
            # Envia uma lista, com ID do item e quantidade
            # Função adicionar produtos a um estoque de um produto já existente
            estoque_tabela.insere_estoque(
                [request.form['id_item'], request.form['quantidade']])
        # ADICIONAR ITEM
        elif('novo_est' in request.form.keys()):
            item = Produto_Estoque((request.form['item'],
                                    request.form['quantidade'],
                                    request.form['categoria'],
                                    request.form['custo'],
                                    request.form['preco']))
            estoque_tabela.insere_estoque(item, quantidade=request.form['quantidade'])
        #VENDER ITENS
        elif('rm_est' in request.form.keys()):
            if(estoque_tabela.verifica_estoque(request.form['id_item'], request.form['quantidade'])):
                estoque_tabela.adiciona_venda(
                    request.form['id_item'], request.form['quantidade'])
            else:
                flash('Não há itens suficientes no estoque para serem vendidos!')
        else:
            flash('Não foi possivel realizar a requisição!')  
    else:
        flash("Favor, preencher todos os parametros!")
    return redirect(url_for('index'))


@app.route('/produtos')
def produtos():
    estoque = estoque_tabela.listar()
    produtos = produtos_tabela.listar()
    vendas = vendas_tabela.listar()
    historico = historico_tabela.listar()
    print(produtos)
    return render_template('produtos.html'
                           ,produtos = produtos
                           ,itens=estoque
                           ,historico=historico
                           ,itens_vendas= vendas
                           )