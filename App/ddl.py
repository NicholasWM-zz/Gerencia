#DDL - Manipulação da tabela

import sqlite3



con = sqlite3.connect('base.db')

cur = con.cursor()
"""
CREATE TABLE estoque (
  id integer AUTO_INCREMENT primary key,
  nome text DEFAULT NULL,
  quantidade INTEGER DEFAULT NULL,
  categoria text DEFAULT NULL,
  custo float DEFAULT NULL,
  preco float DEFAULT NULL
)
"""
"""
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
"""
CREATE TABLE produtos (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  nome text 
) 
"""

sql = """
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
cur.execute(sql)
con.commit()
con.close()