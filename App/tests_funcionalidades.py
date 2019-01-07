import pytest
from views import Estoque_Tabela, Vendas_Tabela, Historico_Tabela
from app import db


estoque_tabela = Estoque_Tabela(db)
vendas_tabela = Vendas_Tabela(db)
historico_tabela = Historico_Tabela(db)
# print(estoque_tabela.procura(1, 'id'))
# def test_deve_adicionar_ao_Estoque_quando_for_inserido_algum_numero():
#     '''
    
#     '''
#     id_item = 1
#     quantidade = 5
    
#     estoque_tabela.insere_estoque(
#         [id_item, quantidade])
    
