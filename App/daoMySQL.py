from helpers import data, hora
from models import Produto_Estoque, Produto, AcoesBanco, Produto_Historico, Produto_Venda
from copy import copy

class Historico(AcoesBanco):
    
    def __init__(self):
        super().__init__()

    def registra_historico(self ,produto , quantidade, situacao=0):
        '''
            Responsavel por inserir dados de carga adicionada ou retirada do estoque.

            situacao = 0 -> Retirada
            situacao = 1 -> Adição
        '''
        acao = "retirado"
        if(situacao):
            acao = "adicionado"
        super().executa_query('INSERT INTO historico(nome_produto, quantidade, categoria, custo, preco, data, hora, {}) values ("{}", {}, "{}", {}, {}, "{}", "{}", {})'.format(
            acao, produto[1], quantidade, produto[3], produto[4], produto[5], data(), hora(), 1))


class Produtos_Tabela(Historico):
    '''
        Responsavel por todas as ações relacionadas a tabela Produtos
    '''
    def __init__(self):
        super().__init__()

    def busca_id_por_nome(self, produto:Produto)->int:
        '''
            Verifica se o produto está registrado na tabela produtos
            Caso não, um novo produto é criado e é retornado o seu ID referente a tabela produtos
            Caso sim, é retornado o seu id
        '''
        produto_estoque = self._busca_id(produto.nome)

        if(not produto_estoque):  # EXISTE NA TABELA PRODUTOS O PRODUTO?
            novo_produto = self.cria_produto(produto)    #CASO NÃO CRIA UM NOVO PRODUTO
            return novo_produto.id                     #DEVOLVE O ID
        return produto_estoque

    def cria_produto(self, produto:Produto)->int:
        '''
            Insere um novo produto na tabela
            e retorna o ID do novo produto
        '''
        super().executa_query('INSERT INTO Produtos(nome, custo, preco, quantidade) values ("{}", {}, {}, {})'.format(
            produto.nome, produto.custo, produto.preco, produto.quantidade))
        return super().executa_query_um_resultado('SELECT id from Produtos where nome = "{}"'.format(produto.nome))[0]

    def _busca_id(self, nome_produto:str)->int:
        '''
            Busca o ID do produto através do nome e retorna o inteiro,
            caso não exista na tabela retorna False
        '''
        return super().executa_query_um_resultado('SELECT id from produtos where nome = "{}"'.format(nome_produto))[0]

class Estoque_Tabela(Historico):
    def __init__(self):
        super().__init__()

    def listar(self):
        itens = super().executa_query_varios_resultados(
            'SELECT * from estoque where quantidade != 0 order by nome')
        indices = []
        tamanho = len(itens)
        item = 0
        while(item < tamanho):
            i = 0
            while(i < tamanho):
                if(itens[item][1] == itens[i][1] and itens[item][3] == itens[i][3]):
                    if(i != item and [i, item] not in indices):
                        indices.append([item, i])
                i += 1
            item += 1
        return self.cria_objeto(itens)

    def __getitem__(self,position):
        itens = []
        for i in self.listar():
            itens.append(i)
        return itens[position]

    def insere_estoque(self, produto, quantidade=None):
        '''
            Verifica se o id do produto(dado da tabela produtos), existe em alguma linha da coluna
            nome_id da tabela estoque. 

            Caso sim, retorna o id referente ao nome_id
            Caso não, um novo registro é criado
        '''
        if(type(produto) == list):
            item = self.cria_objeto(self.procura(produto[0],'id'))[0]

            self.adiciona_ao_estoque(item.id, produto[1])
            super().registra_historico(
                item, produto[1], situacao=1)
        else:
            item = Produto_Estoque(produto)
            busca_estoque = self.procura(produto.nome, 'nome')
            if(not len(busca_estoque)):   # Caso o produto não tenha registro no estoque
                # Cria um novo registro no estoque
                self.cria_item_estoque(produto)
                super().registra_historico(
                    self.cria_objeto(self.procura(produto.nome, 'nome'))[0], quantidade, situacao=1)
                
            else:
                estoque = self.cria_objeto(busca_estoque)     # Retorna um array com um objeto para cada resultado
                
                duplicado = self._verifica_duplicacao(estoque, produto)      #Verifica se valor e preço do produto inserido 
                                                                                #são iguais ao do estoque
                if(not duplicado):                  
                    # Insere o produto em uma linha diferente
                    self.cria_item_estoque(item)
                    super().registra_historico(
                        self.cria_objeto(self.procura(produto.nome, 'nome'))[0], quantidade, situacao=1)
                else:
                    self.adiciona_ao_estoque(duplicado, produto.quantidade) # Soma as quantidades(adiciona itens ao estoque)
                    super().registra_historico(
                        self.procura(duplicado, 'id')[0], quantidade,situacao=1)
            
        
    def _verifica_duplicacao(self, estoque, produto):
        '''
            Verifica se valor e preço do produto inserido são iguais ao do estoque
        '''
        duplicados = []
        for item in estoque:
            if(item.preco == float(produto.preco) and item.custo == float(produto.custo)):
                return item.id
        return duplicados[-1].id if len(duplicados) else None

    def procura(self, dado, consulta="nome"):
        return super().executa_query_varios_resultados("SELECT * from estoque where {} = '{}'".format(consulta, dado))

    def cria_objeto(self, produto:Produto):
        if(type(produto) == tuple):
            resultados = []
            for i in produto:
                resultados.append(Produto_Estoque(i))
            return resultados
        else:
            return Produto_Estoque(produto)
    
    def cria_item_estoque(self, produto: Produto_Estoque)->int:
        '''
            Insere um novo produto na tabela
            e retorna o ID do novo produto
        '''
        super().executa_query('INSERT INTO estoque(nome, custo, preco, quantidade,categoria) values ("{}", {}, {}, {}, "{}")'.format(
            produto.nome, produto.custo, produto.preco, produto.quantidade, produto.categoria))

    def adiciona_ao_estoque(self, id_item, quantidade):
        super().executa_query(
            'UPDATE estoque set quantidade = quantidade + {1} where id = {0}'.format(id_item, quantidade))

    def verifica_estoque(self, id_item:int, quantidade:int)->bool:
        '''
            Verifica se existem itens suficientes no estoque
        '''
        n_itens_estoque = super().executa_query_um_resultado("SELECT quantidade from estoque where id = {}".format(id_item))[0]
        
        return n_itens_estoque >= int(quantidade)

    def adiciona_venda(self, id_item:int, quantidade:int):
        '''
            Retira itens do estoque e adiciona uma nova venda
        '''
        self.__remove_do_estoque(id_item, quantidade)
        produto = Produto_Estoque(self.procura(id_item,'id')[0])
        resultado = super().executa_query('INSERT INTO vendas(nome_produto, quantidade, categoria, custo, preco, data) values ("{}", {}, "{}", {}, {}, "{}")'.format(
            produto.nome, quantidade, produto.categoria, produto.custo, produto.preco, data()))
        
    def __remove_do_estoque(self, id_item, quantidade):
        if(self.verifica_estoque(id_item, quantidade)):
            super().executa_query("UPDATE estoque set quantidade = quantidade - {1} where id = {0}".format(id_item,quantidade))
            super().registra_historico(
                Produto_Estoque(self.procura(id_item, 'id')[0]), quantidade=quantidade)
            return True
        return False




class Vendas_Tabela(AcoesBanco):
    def __init__(self):
        super().__init__()

    def listar(self):
        itens = super().executa_query_varios_resultados(
            'SELECT * from vendas where quantidade != 0')
        indices = []
        tamanho = len(itens)
        item = 0
        while(item < tamanho):
            i = 0
            while(i < tamanho):
                if(itens[item][1] == itens[i][1] and itens[item][3] == itens[i][3]):
                    if(i != item and [i, item] not in indices):
                        indices.append([item, i])
                i += 1
            item += 1
        return self.cria_objeto(itens)

    def cria_objeto(self, produto: Produto):
        if(type(produto) == tuple):
            resultados = []
            for i in produto:
                resultados.append(Produto_Venda(i))
            return resultados
        else:
            return Produto_Venda(produto)
    
class Historico_Tabela(AcoesBanco):
    def __init__(self):
        super().__init__()

    def listar(self):
        itens = super().executa_query_varios_resultados(
            'SELECT * from historico where quantidade != 0')
        indices = []
        tamanho = len(itens)
        item = 0
        while(item < tamanho):
            i = 0
            while(i < tamanho):
                if(itens[item][1] == itens[i][1] and itens[item][3] == itens[i][3]):
                    if(i != item and [i, item] not in indices):
                        indices.append([item, i])
                i += 1
            item += 1
        return self.cria_objeto(itens)
        
    def cria_objeto(self, produto:Produto):
        if(type(produto) == tuple):
            resultados = []
            for i in produto:
                resultados.append(Produto_Historico(i))
            return resultados
        else:
            return Produto_Historico(produto)
    
