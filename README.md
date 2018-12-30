 Histórico
 Adicionar peças no estoque com custo diferentes
 Manter produtos iguais com preços diferentes separados mas sendo exibidos em um unico conjunto exibindo apenas o preço daquele produto mais barato e registrar saida primeiro do mais barato e depois do mais caro
    
    Dois registros
    Um produto sendo exibido
    Com o custo/preco do mais barato
    Mas a quantidade dos dois somados
    Quando acaba o mais barato, o custo/preco do mais caro aparece
    
Quando se adiciona ao estoque, se verifica o preco e custo e se compara com o preco e o custo do mesmo produto existente na tabela, caso seja o mesmo preco/custo, a quantidade daquele é somada ao de entrada, caso contrario, é criado um segundo item do mesmo produto

    Tabela mestra -> Loja
        Params: item
                preco
                venda
                estoque
                vendidos
                Quantidade
                categoria

        É a tabela que vai estar sendo exibida ao usuario com o resumo dos dados
        Variavel, só demonstra como está o estoque de forma resumida e da seus valores
    
    Tabela Histórico
        CREATE TABLE historico (item varchar(255), data date, hora time, quantidade integer, categoria varchar(200), custo_unidade float, preco_venda_unidade float, gasto_total float, lucro_total float, total float);
        Params: Item,

                Data,
                Hora,

                Quantidade,

                Situação(Venda, Adicionado ao Estoque, Saque do Caixa),
                
                Categoria(loja, iscas...)

                Custo Unidade,
                Preco_venda_unidade,
                
                Gasto Total,
                Lucro Total,

                Total 
        Registra tudo oque entra e sai, com data e horario de registro
        Mesmas caracteristicas da tabela loja, só que costuma ser bem maior
    
    Tabela Estoque
        Params:
        CREATE TABLE estoque (nome varchar(255), custo float, preco float, quantidade integer)
            Nome,
            Custo,
            Preço,
            Quantidade

        Verifica se o item já e existe
        Verifica se o item tem o mesmo preço/custo do mesmo item existente
        Registra todas as entradas ao estoque
        É modificada conforme saem itens do estoque
        Responsavel por armazenar os dados que serão resumidos na tabela Loja referentes ao Estoque e linhas(itens que estão disponiveis)

    Tabela de Vendas
        Params:
        CREATE TABLE vendas (nome varchar(255), custo float, preco float, quantidade integer, total_p_retirada float)
            Nome,
            Custo,
            Preço,
            Quantidade
            Total p/Retirada

        Representa os produtos que foram vendidos cujo valor da venda está em caixa
        Registra todas as saidas de produtos
        Possui data e hora de saida
        Responsavel por armazenar dados referentes a saida de produtos, resumo que vai para a tabela loja
        
    Tabela Caixa
    CREATE TABLE caixa (origem varchar(255), data date, hora time, operacao varchar(100), dinheiro_giro float, lucro float, total float);
        Params: 
            Origem(Loja/Iscas...),
            Data,
            Hora,
            operacao(adicionado/retirado),
            Dinheiro de giro,
            Lucro,
            Total
        Responsavel por cuidar do fluxo financeiro das vendas
        Registra quanto de dinheiro entrou no caixa e quanto foi retirado
        Tambem registra a retirada do dinheiro restante dos produtos vendidos, exibindo quanto está no caixa e fazendo a relação com o quanto que foi tirado