# import pytest
import sqlite3
from daoMySQL import Estoque_Tabela, Vendas_Tabela, Produtos_Tabela, Historico_Tabela
from models import AcoesBanco, Produto_Estoque, Produto_Model
from ddl import sqls, dados, dados_produtos
from unittest import TestCase, main
from random import randint
from helpers import excluir_base_teste_db

class TesteFuncionalidades(TestCase):
    def setUp(self):
        db = 'base_test_db.db'
        
        self.produto_tabela = Produtos_Tabela(db)
        self.estoque_tabela = Estoque_Tabela(db)
        self.vendas_tabela = Vendas_Tabela(db)
        self.historico_tabela = Historico_Tabela(db)
        self.acao_banco = AcoesBanco(db)
        
    def test_deve_retornar_uma_lista_do_banco(self):
        '''
            Simulação do Index
        '''
        listas = [self.estoque_tabela.listar(), 
                self.vendas_tabela.listar(),
                self.historico_tabela.listar()]
        for lista in listas:
            self.assertEqual(type(lista), list)

    def test_deve_adicionar_quantidade_ao_estoque(self):
        '''
            Caso simples de adicionar ao estoque

            Função de View -> atualiza_estoque

            Parametro -> add_est
        '''
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.estoque_tabela.insere_estoque(
            [produto[0], 2])
        
        nova_consulta = self.acao_banco.executa_query_um_resultado(f'SELECT * from estoque where id = {produto[0]}')

        self.assertEqual(nova_consulta[2], (int(produto[2]) + 2))

    def test_deve_somar_quantidades_quando_novo_produto_inserido_tiver_nome_e_custo_igual_a_algum_produto_existente_na_tabela_sem_adicionar_uma_nova_linha_na_tabela(self):
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        tamanho_tabela_antes = self.acao_banco.executa_query_um_resultado(f'SELECT count(*) from estoque') 
        
        item = Produto_Estoque((produto[1],
                                produto[2],
                                produto[3],
                                produto[4],
                                produto[5]))

        self.estoque_tabela.insere_estoque(item, quantidade=produto[2])
        
        tamanho_tabela_depois = self.acao_banco.executa_query_um_resultado(f'SELECT count(*) from estoque') 
        

        nova_consulta = self.acao_banco.executa_query_um_resultado(f'SELECT * from estoque where id = {produto[0]}')
        self.assertEqual(tamanho_tabela_antes,tamanho_tabela_depois)
        self.assertEqual(produto[2] + produto[2] , nova_consulta[2])

    def test_deve_criar_nova_linha_caso_nao_exista_produto_com_mesmo_nome_na_tabela(self):
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        tamanho_tabela_antes = self.acao_banco.executa_query_um_resultado(f'SELECT count(*) from estoque') 
        novo_produto = 'produto_3' 
        self.estoque_tabela.insere_estoque(Produto_Estoque((novo_produto,
                                                            produto[2],
                                                            produto[3],
                                                            float(produto[4]) + 2,
                                                            float(produto[5]) + 2)),
                                           quantidade=produto[2])
        tamanho_tabela_depois = self.acao_banco.executa_query_um_resultado(f'SELECT count(*) from estoque') 

        self.assertGreater(tamanho_tabela_depois, tamanho_tabela_antes)

    def test_deve_criar_nova_linha_caso_produto_inserido_tenha_mesmo_nome_com_custo_diferente(self):
        # Consulta o estoque e pega o primeiro resultado
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        

        produtos_mesmo_nome_anterior = self.acao_banco.executa_query_um_resultado(f'SELECT COUNT(*) from estoque where nome = "{produto[1]}"')[0]

        self.estoque_tabela.insere_estoque(Produto_Estoque((produto[1],
                                                            produto[2],
                                                            produto[3],
                                                            float(produto[4]) + 2,
                                                            float(produto[5]) + 2)),
                                           quantidade=produto[2])
        
        produtos_mesmo_nome_atualizada = self.acao_banco.executa_query_um_resultado(f'SELECT count(*) from estoque where nome = "{produto[1]}"')[0]
        # print(produtos_mesmo_nome_anterior)
        # print(produtos_mesmo_nome_atualizada)
        self.assertLess(produtos_mesmo_nome_anterior, produtos_mesmo_nome_atualizada)
        
    def test_nao_deve_permitir_que_seja_vendido_mais_do_que_tem_disponivel_no_estoque(self):
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.estoque_tabela.adiciona_venda(
                    produto[0], float(produto[2])+1)
        
        nova_consulta = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.assertEqual(produto[2], nova_consulta[2])

    def test_deve_permitir_remover_do_estoque_quando_quantidade_de_itens_for_menor_que_a_quantidade_de_itens_no_estoque(self):
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[1]     #Corrigir para pegar o primeiro resultado apenas
        
        self.estoque_tabela.adiciona_venda(
                    produto[0], float(produto[2])-1)
        
        nova_consulta = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[1]     #Corrigir para pegar o primeiro resultado apenas
        
        self.assertLess(nova_consulta[2], produto[2])

    def test_deve_permitir_remover_do_estoque_quando_quantidade_de_itens_for_igual_a_quantidade_de_itens_no_estoque(self):
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.estoque_tabela.adiciona_venda(
                    produto[0], float(produto[2]))
        
        nova_consulta = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.assertEqual(nova_consulta[2], 0)
        
    def test_deve_adicionar_marcação_a_tabela_histórico_quando_itens_forem_adicionados_ao_estoque(self):
        #Consulta quantidade de linhas no historico
        consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from historico')[0]
        
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        #Adiciona ao estoque
        item = Produto_Estoque((produto[1],
                                produto[2],
                                produto[3],
                                produto[4],
                                produto[5]))

        self.estoque_tabela.insere_estoque(item, quantidade=produto[2])
        
        #Consulta quantidade de linhas no historico
        nova_consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from historico')[0]
        self.assertGreater(nova_consulta, consulta)


    def test_deve_adicionar_marcação_a_tabela_histórico_quando_itens_forem_vendidos(self):
        #Consulta quantidade de linhas no historico
        consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from historico')[0]
        
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        #Adiciona ao estoque
        self.estoque_tabela.adiciona_venda(
                    produto[0], 1)
        
        #Consulta quantidade de linhas no historico
        nova_consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from historico')[0]
        self.assertGreater(nova_consulta, consulta)
        
    def test_deve_adicionar_marcação_na_tabela_vendas_quando_itens_forem_vendidos(self):
        consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from vendas')[0]
        produto = self.acao_banco.executa_query_varios_resultados('SELECT * from estoque')[0]     #Corrigir para pegar o primeiro resultado apenas
        
        self.estoque_tabela.adiciona_venda(
                    produto[0], float(produto[2])+1)
        
        nova_consulta = self.acao_banco.executa_query_um_resultado('SELECT COUNT(*) from vendas')[0]     #Corrigir para pegar o primeiro resultado apenas
        self.assertGreater(nova_consulta, consulta)

    def test_deve_registrar_produto_caso_nao_exista_na_tabela(self):
        novo_produto = Produto_Model("Nome_Produto", "Categorico")
        consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from produtos")
        self.produto_tabela.salvar(novo_produto)
        nova_consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from produtos")
        # print(f">>>>>>{nova_consulta} x {consulta} <<<<<<<<")
        self.assertGreater(nova_consulta, consulta)
    
    def test_nao_deve_registrar_produto_na_tabela_produtos_caso_ja_exista_na_tabela_e_o_retorno_deve_ser_false(self):
        novo_produto = Produto_Model("Nome_Produto", "Categorico")
        
        self.produto_tabela.salvar(novo_produto)

        consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from produtos")
        retorno = self.produto_tabela.salvar(novo_produto)

        nova_consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from produtos")
        # print(f">>>>>>{nova_consulta} x {consulta} <<<<<<<<")

        self.assertEqual(nova_consulta, consulta)
        self.assertEqual(False, retorno)

    def test_nao_deve_permitir_inserir_no_estoque_produtos_que_nao_estejam_registrados_na_tabela_produtos_e_deve_retornar_false(self):
        
        consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")
        
        item = Produto_Estoque(('nomealskdnlkasdaiwdin',
                                5,
                                'TESTE',
                                5,
                                10))
        retorno = self.estoque_tabela.insere_estoque(item, quantidade=item.quantidade)

        nova_consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")

        self.assertEqual(nova_consulta[0], consulta[0])
        self.assertEqual(retorno, False)

    def test_deve_inserir_produto_no_estoque_caso_o_produto_esteja_registrado_na_tabela_produtos_e_exista_no_estoque_e_deve_retornar_true(self):
        produto = self.acao_banco.executa_query_um_resultado('SELECT * from estoque')
        consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")
        
        item = Produto_Estoque((produto[1],
                                5,
                                'TESTE',
                                5,
                                10))
        retorno = self.estoque_tabela.insere_estoque(item, quantidade=item.quantidade)

        nova_consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")

        self.assertEqual(nova_consulta[0], consulta[0])
        self.assertEqual(retorno, True)
    
    def test_deve_inserir_produto_no_estoque_caso_o_produto_esteja_registrado_na_tabela_produtos_e_nao_exista_no_estoque_e_deve_retornar_true(self):
        produto = self.acao_banco.executa_query_um_resultado('SELECT * from estoque')
        self.acao_banco.executa_query(f'delete from estoque where nome = "{produto[1]}"')
        
        consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")
        
        item = Produto_Estoque((produto[1],
                                5,
                                'TESTE',
                                5,
                                10))
        retorno = self.estoque_tabela.insere_estoque(item, quantidade=item.quantidade)

        nova_consulta = self.acao_banco.executa_query_um_resultado(
            "SELECT COUNT(*) from estoque")

        self.assertGreater(nova_consulta[0], consulta[0])
        self.assertEqual(retorno, True)


if __name__ == '__main__':
    #Exclui banco de testes caso exista
    excluir_base_teste_db()
    #Inicializa arquivo do banco
    acao_banco = AcoesBanco('base_test_db.db')
    #Cria estrutura do banco
    for sql in sqls:
            acao_banco.executa_query(sql)
    #Insere dados no banco
    for dado in dados:
        acao_banco.executa_query(f"INSERT into estoque(nome, quantidade, categoria, custo, preco) values ('{dado[0]}',{dado[1]},'{dado[2]}',{dado[3]},{dado[4]})")
    for dado in dados_produtos:
        acao_banco.executa_query(f"INSERT into produtos(nome) values ('{dado}')")
    #Executa os testes
    main()



