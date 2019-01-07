import sqlite3

def commit_close(func):
    def decorator(*args):
        con = sqlite3.connect('base.db')

        cur = con.cursor()
        sql = func(*args)
        cur.execute(sql)
        con.commit()
        con.close()
    return decorator
@commit_close
def db_insert_estoque(item):
    return """
    INSERT INTO estoque (nome, quantidade, categoria, custo, preco) VALUES ('{}', {}, '{}', {}, {})""".format(item[0], item[1], item[2], item[3], item[4])
@commit_close
def db_insert_vendas(item):
    return """
    INSERT INTO vendas (nome_produto, quantidade, categoria, custo, preco, data, retirado) VALUES ('{}', {}, '{}', {}, {}, '{}', {})""".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
@commit_close
def db_insert_historico(item):
    return """
    INSERT INTO historico (nome_produto, quantidade, categoria, custo, preco, data, hora, adicionado, retirado) VALUES ('{}', {}, '{}', {}, {}, '{}', '{}', {}, {})""".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8])


estoque = [('Sardinha', 100, 'Iscas', 8, 15),
           ('Boia de Pesca', 3, 'Equipamentos de Pesca', 12, 18),
           ('Cabo de Aco 50lbs 10m', 2, 'Equipamentos de Pesca', 8, 15),
           ('Pacote Anzol Maruseigo 24 c/ 10pcs', 8, 'Equipamentos de Pesca', 3.5, 5),
           ('Pacote Anzol Maruseigo 22 c/ 10pcs', 5, 'Equipamentos de Pesca', 3.5, 5),
           ('Linha Grilon 0.50mm', 9, 'E', 7.5, 12),
           ('Pacote Anzol n 12 c/ 50pcs', 2, 'Equipamentos de Pesca', 8, 14),
           ('Elasticon', 6, 'Equipamentos de Pesca', 2.5, 5),
           ('Snao c/ girador 5pcs', 2, 'Equipamentos de Pesca', 3.8, 3.8),
           ('Garateia 2/0', 84, 'Equipamentos de Pesca', 0.96, 1.5),
           ('Castroados Soltos', 93, 'Equipamentos de Pesca', 0.58, 1),
           ('Sardinha 5KG Ensacada', 19, 'Iscas Ensacadas', 40, 150),
           ('Sardinha 2KG Ensacada', 4, 'Iscas', 16, 30),
           ('Sardinha 3KG Ensacada', 1, 'Iscas', 24, 45)]

historico = [
    ('Sardinha', 100, 'Iscas', 8, 15, '2018-12-30', '00:54:19', 1, 0),
    ('Boia de Pesca', 3, 'Equipamentos de Pesca', 12, 18, '2018-12-31', '10:10:02', 1, 0),
    ('Boia de Pesca', 2, 'Equipamentos de Pesca', 12, 18, '2018-12-31', '10:10:46', 0, 1),
    ('Boia de Pesca', 2, 'Equipamentos de Pesca', 12, 18, '2019-01-04', '06:13:29', 1, 0),  
    ('Cabo de Aco 50lbs 10m', 2, 'Equipamentos de Pesca', 8, 15, '2019-01-04', '06:15:57',   1, 0),
    ('Pacote Anzol Maruseigo 24 c/ 10pcs', 8, 'Equipamentos de Pesca', 3.5, 5, '2019-01-04', '06:17:04', 1, 0),
    ('Pacote Anzol Maruseigo 22 c/ 10pcs', 5, 'Equipamentos de Pesca', 3.5, 5, '2019-01-04', '06:17:53', 1, 0),
    ('Linha Grilon 0.50mm', 9, 'E', 7.5, 12, '2019-01-04', '06:18:55', 1, 0),
    ('Pacote Anzol n 12 c/ 50pcs', 2, 'Equipamentos de Pesca', 8, 14, '2019-01-04', '06:19:57', 1, 0),
    ('Elasticon', 6, 'Equipamentos de Pesca', 2.5, 5, '2019-01-04', '06:20:41', 1, 0),
    ('Snao c/ girador 5pcs', 2, 'Equipamentos de Pesca', 3.8, 3.8, '2019-01-04', '06:21:29', 1, 0),
    ('Garateia 2/0', 84, 'Equipamentos de Pesca', 0.96, 1.5, '2019-01-04', '06:25:20', 1, 0),
    ('Castroados Soltos', 93, 'Equipamentos de Pesca', 0.58, 1, '2019-01-04', '06:31:03', 1, 0),
    ('Sardinha 5KG Ensacada', 23, 'Iscas Ensacadas', 40, 150, '2019-01-04', '06:33:51', 1, 0),
    ('Sardinha 5KG Ensacada', 2, 'Iscas Ensacadas', 40, 150, '2019-01-04', '06:36:54', 1, 0),
    ('Sardinha 2KG Ensacada', 1, 'Iscas', 16, 30, '2019-01-04', '06:43:28', 1, 0),
    ('Sardinha 3KG Ensacada', 1, 'Iscas', 24, 45, '2019-01-04', '06:43:58', 1, 0),
    ('Sardinha 2KG Ensacada', 4, 'Iscas', 16, 30, '2019-01-04', '06:51:12', 1, 0),
    ('Sardinha 5KG Ensacada', 6, 'Iscas Ensacadas', 40, 150, '2019-01-05', '17:48:07', 0, 1),
    ('Sardinha 2KG Ensacada', 1, 'Iscas', 16, 30, '2019-01-05', '17:49:16', 0, 1)]

vendas = [
    ('Boia de Pesca', 2, 'Equipamentos de Pesca', 12, 18, '2018-12-31', 0),
    ('Sardinha 5KG Ensacada', 6, 'Iscas Ensacadas', 40, 150, '2019-01-05', 0),
    ('Sardinha 2KG Ensacada', 1, 'Iscas', 16, 30, '2019-01-05', 0)]

# for i in historico:
#     db_insert_historico(i)

# for i in estoque:
#     db_insert_estoque(i)

# for i in vendas:
#     db_insert_vendas(i)


def db_select(data):
    con = sqlite3.connect('base.db')

    cur = con.cursor()
    cur.execute(data)
    data = cur.fetchone()
    print(data)
    con.close()

# db_select('SELECT * from historico')