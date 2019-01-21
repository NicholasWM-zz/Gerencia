import os
from datetime import datetime

#Pega a imagem na pasta uploads
def recupera_imagem(id):
    pasta_upload = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
    #Pega todos os arquivos do diretorio
    for nome_arquivo in os.listdir(pasta_upload):
        #Procura pelo arquivo que contenha a string
        if("capa{}".format(id) in nome_arquivo):
            return nome_arquivo
    return "capa_padrao.jpg"

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    print(arquivo)
    #remove o arquivo, o join concatena os paths
    if(arquivo != 'capa_padrao.jpg'):
        os.remove(os.path.join(pasta_upload, arquivo))

def verifica_form(form):
    for k,v in form.items():
        if(k != "categoria"):
            if(not len(str(v))):
                print("FALSE")
                return False
    return True

def excluir_base_teste_db():
    
    paths = ['.','..']
    for path in paths:
        dir = os.listdir(path)
        for file in dir:
            if file == "base_test_db.db":
                os.remove(file)

def hora()->str:
    '''
        Retorna a hora atual em formato String
    '''
    return '{}:{}:{}'.format(datetime.now().hour,
                             datetime.now().minute,
                             datetime.now().second)


def data()->str:
    '''
        Retorna a data atual em formato String
    '''
    return str(datetime.now().date())
