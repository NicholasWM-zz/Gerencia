
from flask_mysqldb import MySQL
from datetime import datetime
from app import db
from models import ItemEstoque



class Produtos():
    def __init__(self):
        ...
    def lista(self)->tuple:
        return Loja.lista()

    def cria_novo_produto(self):
        

    def adiciona_estoque(self, id_produto, quantidade, usuario):
        '''
            Modifico Estoque(Adicionar)
            Modifico Historico()
            Atualiza Loja
        '''
        item_estoque = ItemEstoque(id_produto)
        Estoque.adiciona(item_estoque, quantidade)
        Historico.adiciona_registro(item_estoque, 'adiciona estoque', quantidade, usuario)
        Loja.atualiza(ItemEstoque(id_produto), item_estoque)

        
    def adiciona_venda(self, id, valor):
        '''
            Adiciona itens vendidos a tabela vendas. 
            Remove itens vendidos da tabela estoque
            Atualiza a Loja
            Atualiza o Caixa
            Atualiza o Histórico
        '''
        Loja.modifica_numero_itens(id, 'vendidos', valor)
        Loja.modifica_numero_itens(id, 'estoque', valor, somar=False)

    def verifica_estoque(self, id, valor)->bool:
        '''
            Verifica se existem itens o suficiente no estoque.
        '''
        return Loja.verifica_estoque(id, valor)

    
class Loja:
    '''
        Isola todas as responsabilidades da tabela Loja.
        Não pode ser instânciada.
    '''
    def __init__(self):
        raise RuntimeError('Essa classe não pode ser instanciada!!!!')

    
    @staticmethod
    def atualiza(item_antigo, item_atual):
        if(item_antigo.custo_unidade == item_atual.custo_unidade and item_antigo.preco_unidade == item_atual.preco_unidade):
            ...
        


    @staticmethod
    def modifica_numero_itens(id_item: int, coluna: str, valor: int, somar=True):
        """
            Modifica o numero de itens de respectivas colunas na tabela loja
            Metodos Usando: adiciona_estoque, adiciona_venda
        """
        print('UPDATE loja set {}={}{}{} where id={}'.format(
            coluna, coluna, '+' if somar else '-', valor, id_item))
        cursor = db.connection.cursor()
        cursor.execute('UPDATE loja set {}={}{}{} where id={}'.format(
            coluna, coluna, '+' if somar else '-', valor, id_item))
        db.connection.commit()

    @staticmethod
    def lista()->tuple:
        '''
            Retorna uma lista com todos os dados da tabela Loja
        '''
        cursor = db.connection.cursor()
        cursor.execute('SELECT * from loja')
        dados = cursor.fetchall()
        return dados

    @staticmethod
    def verifica_estoque(id, valor)->bool:
        '''
            Verifica o estoque da tabela Loja
        '''
        cursor = db.connection.cursor()
        cursor.execute('SELECT estoque from loja where id={}'.format(id))
        estoque = cursor.fetchone()
        return int(estoque[0]) >= int(valor)


class Vendas:

    @staticmethod
    def adiciona(item, custo, preco, quantidade):
        cursor = db.connection.cursor()
        if(not Vendas.__verifica_existencia_item(item)):
            cursor.execute('INSERT INTO vendas values ({}, {}, {}, {}, {})'.format(
                item, custo, preco, quantidade, preco*quantidade))
        else:
            cursor.execute('UPDATE')

        db.connection.commit()
    @staticmethod
    def retira():
        ...

class Estoque:
    @staticmethod
    def adiciona(ItemEstoque, quantidade):
        '''
            Adiciona itens no estoque com o ID especifico
        '''
        query = 'UPDATE estoque set quantidade = quantidade + {} where id={}'.format(quantidade,ItemEstoque[0])
        executa_query(query)
    @staticmethod
    def remove(ItemEstoque, quantidade):
        query = 'UPDATE estoque set quantidade = quantidade - {} where id={}'.format(quantidade,ItemEstoque[0])
        executa_query(query)

class Historico:
    @staticmethod
    def adiciona_registro(item, operacao, quantidade_itens, usuario):
        gasto = quantidade_itens * item.custo_unidade
        lucro = (quantidade_itens * item.preco_unidade) - gasto        
        query = 'INSERT into historico {},{},{},{},{},{},{},{},{},{},{},{}'.format(usuario,item.nome,data(),hora,quantidade_itens,operacao,item.categoria,item.custo_unidade,item.preco_unidade,gasto,lucro,gasto + lucro)
        executa_query(query)

class Caixa:
    @staticmethod
    def calcula_valor():
        ...
