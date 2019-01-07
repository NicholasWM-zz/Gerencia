from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import sqlite3

class AcoesBanco():
        def __init__(self, db):
                self.db = db

        def executa_query(self, query):
                con = sqlite3.connect('base.db')

                cur = con.cursor()
                cur.execute(query)
                con.commit()
                con.close()

        def executa_query_um_resultado(self, query):
                con = sqlite3.connect('base.db')
                cur = con.cursor()
                cur.execute(query)
                data = cur.fetchone()
                print(data)
                con.close()
                return data
    
        def executa_query_varios_resultados(self, query):
                con = sqlite3.connect('base.db')
                cur = con.cursor()
                cur.execute(query)
                data = tuple(cur.fetchall())
                print(data)
                con.close()
                return data

class Produto:
    '''
        Abstração do produto individualmente
    '''
    def __init__(self, produto:tuple):
        self.id = produto[0]
        self.nome = produto[1]

    def __repr__(self):
        return '{}'.format(self.nome)


class Produto_Estoque:
    '''
        Abstração do estoque de determinado produto e suas caracteristicas
    '''
    def __init__(self, produto):
        print(produto)
        self.quantidade_atributos = len(produto)
        if(self.quantidade_atributos > 5):
            self.id = produto[0]
            self.nome = produto[1] 
            self.quantidade = produto[2] 
            self.categoria = produto[3] 
            self.custo = produto[4]
            self.preco = produto[5]
            if(self.quantidade_atributos == 7):
                self.estiloCSS = 1
        else:
            self.nome = produto[0]
            self.quantidade = produto[1]
            self.categoria = produto[2]
            self.custo = produto[3]
            self.preco = produto[4]
    
    def __getitem__(self, position):
        if(self.quantidade_atributos == 7):
            return (self.id,self.nome,self.quantidade,self.categoria,self.custo,self.preco, self.estiloCSS)[position]
        elif(self.quantidade_atributos > 5):
            return (self.id,self.nome,self.quantidade,self.categoria,self.custo,self.preco)[position]
        else:
            return (self.nome,self.quantidade,self.categoria,self.custo,self.preco)[position]

    def __len__(self):
        return self.quantidade_atributos

class Produto_Venda:
    
    def __init__(self, produto):
        self.quantidade_itens = len(produto)
        self.id = produto[0]
        self.nome = produto[1]
        self.quantidade = produto[2]
        self.categoria = produto[3]
        self.custo = produto[4]
        self.preco = produto[5]
        self.data = produto[6]
        self.retirado = produto[7]
    
    def __getitem__(self, position):
        return (self.id,self.nome,self.quantidade,self.categoria,self.custo,self.preco,self.data,self.retirado)[position]
    
    def __len__(self):
        return self.quantidade_itens


class Produto_Historico:
    def __init__(self, produto):
        self.quantidade_itens = len(produto)
        self.id =produto[0]
        self.nome =produto[1]
        self.quantidade =produto[2]
        self.categoria =produto[3]
        self.custo =produto[4]
        self.preco =produto[5]
        self.data =produto[6]
        self.hora =produto[7]
        self.adicionado =produto[8]
        self.retirado =produto[9]

    def __getitem__(self, position):
        return (self.id,self.nome,self.quantidade,self.categoria,self.custo,self.preco,self.data,self.hora,self.adicionado,self.retirado)[position]
    
    def __len__(self):
        return self.quantidade_itens
    
    
