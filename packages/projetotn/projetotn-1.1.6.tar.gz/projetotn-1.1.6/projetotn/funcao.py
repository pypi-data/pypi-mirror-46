#============ Nielsen ================
# Created: 22/03/2019 / Funções Geral
# Created by Jeiso Silva
#=====================================
#--------------------------------------------------------------------------------------------------------------------------------------------- 
import pandas as pd

# Função que conta uma lista de CPs - versao 2.0 - last update: 15/03/2019
def contaCps(user,lista):
    quantidade_linhas = 0
    conta = len(lista)
    lista_erros = []
    for i in range(0,conta):
        try:
            IMDB = pd.read_csv('C:/Users/{}/Google Drive/_jupyter/_imdb/{}_IMDB_TN.csv'.format(user,lista[i])) # WIN
            #IMDB = pd.read_csv('/Users/{}/Google Drive Nielsen/_jupyter/_imdb/{}_IMDB_TN.csv'.format(user,lista[i])) # MAC
            quantidade_linhas += IMDB.shape[0] -1
        except:
            lista_erros.append(lista[i])
            continue
    erro = len(lista_erros)
    return print(' Quantidade total de linhas: {} '.format(quantidade_linhas),' \n \033[0;31mQuantidade de ERRO na leitura:\033[m {} \n \033[0;31mlog de ERRO:\033[m {}'.format(erro,lista_erros))
#---------------------------------------------------------------------------------------------------------------------------------------------     
def ACN(user,num):
    file = pd.read_excel('/Users/{}/Google Drive/_jupyter/_apoio/_file/Modulos_Chars_Ambientes.xlsx'.format(user))
    char = file.loc[file['aci_val_Id_Mod'] == num]  
    return char
#--------------------------------------------------------------------------------------------------------------------------------------------- 
def formato(user,num_char):
    file = pd.read_excel('/Users/{}/Google Drive/_jupyter/_apoio/_file/Formatos_Chars.xlsx'.format(user))
    seach = file.loc[file['CarId'] == num_char]
    mod = pd.unique(file['ModuleId'])
    return seach
#--------------------------------------------------------------------------------------------------------------------------------------------- 
def modulos(user,num_char):
    file = pd.read_excel('/Users/{}/Google Drive/_jupyter/_apoio/_file/Formatos_Chars.xlsx'.format(user))
    seach = file.loc[file['CarId'] == num_char]
    mod = pd.unique(seach['ModuleId'])
    return mod
#--------------------------------------------------------------------------------------------------------------------------------------------- 
def entrega(user,num):
    file = pd.read_excel('/Users/{}/Google Drive/_jupyter/_apoio/_file/Entregas_Bases.xlsx'.format(user))
    seach = file.loc[file['FormatId'] == num]
    return seach