from flask import render_template, redirect, url_for, request, flash
from daoMySQL import Estoque_Tabela, Vendas_Tabela, Historico_Tabela
from app import app, db
from models import Produto_Estoque
from pprint import pprint
from helpers import verifica_form
estoque_tabela = Estoque_Tabela(db)
vendas_tabela = Vendas_Tabela(db)
historico_tabela = Historico_Tabela(db)

@app.route('/')
def index():
    itens = estoque_tabela.listar()
    itens_venda = vendas_tabela.listar()
    historico = historico_tabela.listar()
    return render_template('index.html', itens=itens, itens_vendas=itens_venda, historico=historico)

@app.route('/estoque')
def estoque():
    itens = estoque_tabela.listar()
    return render_template('estoque_geral.html', itens=itens)
@app.route('/atualiza_estoque', methods=['POST',])
def atualiza_estoque():
    # ADICIONAR AO ESTOQUE
    if(verifica_form(request.form)):
        if('add_est' in request.form.keys()):
            estoque_tabela.insere_estoque(
                [request.form['id_item'], request.form['quantidade']])
        # ADICIONAR ITEM
        elif('novo_est' in request.form.keys()):
            item = Produto_Estoque((request.form['item'],request.form['quantidade'],request.form['categoria'],request.form['custo'],request.form['preco']))
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
