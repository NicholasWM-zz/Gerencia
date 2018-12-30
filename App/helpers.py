
from datetime import datetime


def verifica_form(form):
    for k,v in form.items():
        if(k != "categoria"):
            if(not len(str(v))):
                print("FALSE")
                return False
    return True


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
