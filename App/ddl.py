#DDL - Manipulação da tabela

import sqlite3



# con = sqlite3.connect('base_test_db.db')

# cur = con.cursor()
sql_1 = """
CREATE TABLE `estoque` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`nome`	text DEFAULT NULL,
	`quantidade`	int ( 11 ) DEFAULT NULL,
	`categoria`	text DEFAULT NULL,
	`custo`	float DEFAULT NULL,
	`preco`	float DEFAULT NULL
)
"""
sql_2 ="""
CREATE TABLE historico (
  id INTEGER AUTO_INCREMENT primary key,
  nome_produto text DEFAULT NULL,
  quantidade INTEGER DEFAULT NULL,
  categoria text DEFAULT NULL,
  custo float DEFAULT NULL,
  preco float DEFAULT NULL,
  data TEXT DEFAULT NULL,
  hora TEXT DEFAULT NULL,
  adicionado INTEGER DEFAULT '0',
  retirado INTEGER DEFAULT '0'
) 
"""
sql_3="""
CREATE TABLE produtos (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  nome TEXT,
  categoria TEXT
) 
"""

sql_4 = """
CREATE TABLE vendas (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  nome_produto text DEFAULT NULL,
  quantidade INTEGER DEFAULT NULL,
  categoria text DEFAULT NULL,
  custo float DEFAULT NULL,
  preco float DEFAULT NULL,
  data TEXT DEFAULT NULL,
  retirado INTEGER DEFAULT '0'
)
"""

sqls = [sql_1,
        sql_2,
        sql_3,
        sql_4]
#nome, quantidade, categoria, custo, preco
dados = [['produto_1', 5, 'teste', 5, 10], 
         ['produto_2', 5, 'teste', 5, 10],
         ['produto_3', 5, 'teste', 5, 10],
         ['produto_4', 5, 'teste', 5, 10],
         ['produto_5', 5, 'teste', 5, 10],
         ['produto_6', 5, 'teste', 5, 10]]

dados_produtos = ["produto_1","produto_2", "produto_3", "produto_4"]
# cur.execute(sql)
# con.commit()
# con.close()