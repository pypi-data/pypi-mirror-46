 #============ Nielsen ==================
# Created: 09/03/2019 / Classe Ap&Promo
# Created by Jeiso Silva
#=======================================
#--------------------------------------------------------------------------------------------------------------------------------------------- 
import pandas as pd 
import os
import glob
# Caracterização Massiva - Ap. Regular & Promocao - versao 2.1 - last update: 01/04/2019
def charMassivaAp(user,BASE,OGRDS,nameColumn1,charNum1,nameColumn2,charNum2,fileName):
    """
    DOCSTRING
    """
    def findChar(num):
        df2 = pd.read_csv('file/car_id.csv') # local do arquivo
        file = df2.loc[df2['Car_id'] == num ]
        return file
# ---------------------------------------------------------------------------------------
    ''' Função criação de arquivos modelo.'''  
    modelo = pd.read_csv('C:/Users/{}/Google Drive/_jupyter/_massivo/_model-file/csv-modelo.csv'.format(user),delimiter = ';') # WIN
    modelo2 = pd.read_csv('C:/Users/{}/Google Drive/_jupyter/_massivo/_model-file/csv-modelo.csv'.format(user),delimiter = ';')

    #modelo = pd.read_csv('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_massivo/_model-file/csv-modelo.csv',delimiter = ';') # MAC
    #modelo2 = pd.read_csv('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_massivo/_model-file/csv-modelo.csv',delimiter = ';')

    OGRDS['ItmId'] = OGRDS['#BR LOC 0002 : PC ITEM'].str.slice(1,50) # OGRDS CLEANING  
    OGRDS['ItmId'] = OGRDS['ItmId'].astype(float) # CONVERSÃO DE COLUNAS to FLOAT
    BASE['ItmId'] = BASE['ItmId'].astype(float) 
    
    #=================================================================================================================    
    # Log Error
    queryError = pd.merge(BASE[['ItmId','VALIDAÇÃO (90050)','VALIDAÇÃO (90020)']],
                OGRDS[['ItmId','ITEM DESCRIPTIONS','Item Code']],
                on='ItmId', how='left',indicator=True)

    apError = queryError[['ItmId','Item Code','VALIDAÇÃO (90050)']]
    promoError = queryError[['ItmId','Item Code','VALIDAÇÃO (90020)']]

    varErrorAp = apError.loc[apError['VALIDAÇÃO (90050)'] == 'ALTERADO']
    varErrorPromo = promoError.loc[promoError['VALIDAÇÃO (90020)'] == 'ALTERADO']

    #contando
    contaAp = len(varErrorAp)
    contaPromo = len(varErrorPromo)
    contaTotal = contaAp + contaPromo

    logErrorAp = varErrorAp.loc[varErrorAp['Item Code'].isnull()]
    logErrorPromo = varErrorPromo.loc[varErrorPromo['Item Code'].isnull()]
    #=================================================================================================================    
    query = pd.merge(OGRDS[['ItmId','ITEM DESCRIPTIONS','Item Code']],
                BASE[['ItmId','APRESENTACAO REGULAR (90050)','STATUS (90050)','VALIDAÇÃO (90050)','PROMOCAO (90020)','STATUS (90020)','VALIDAÇÃO (90020)']],
                on='ItmId')# MERGE/PROCV

    char90050 = query[['Item Code','APRESENTACAO REGULAR (90050)','STATUS (90050)','VALIDAÇÃO (90050)']] # CRIANDO VARIÁVEIS
    char90020 = query[['Item Code','PROMOCAO (90020)','STATUS (90020)','VALIDAÇÃO (90020)']]    
    var90050 = char90050.loc[char90050['VALIDAÇÃO (90050)'] == 'ALTERADO'] # FILTERS
    var90020 = char90020.loc[char90020['VALIDAÇÃO (90020)'] == 'ALTERADO']
    num1 = findChar(charNum1) # Pegando novo valor CHARS
    numAP = num1['Type_Code']
    numAP = int(numAP) 
    num2 = findChar(charNum2) # Pegando novo valor CHARS
    numPROMO = num2['Type_Code']
    numPROMO = int(numPROMO)
    modelo['ITEM_CODE'] = var90050['Item Code'] # MODELO1
    modelo['CHAR_CODE'] = numAP
    modelo['CHAR_DSCR'] = var90050[nameColumn1]
    modelo2['ITEM_CODE'] = var90020['Item Code'] # MODELO2
    modelo2['CHAR_CODE'] = numPROMO
    modelo2['CHAR_DSCR'] = var90020[nameColumn2] 
    final = pd.concat([modelo, modelo2], axis=0, join='inner') # Concatenando modelos
    final.to_csv('C:/Users/{}/Google Drive/_jupyter/_massivo\_csv-file/{}.csv'.format(user,fileName),index=False) # WIN
    #final.to_csv('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_massivo/_csv-file/{}.csv'.format(fileName),index=False) # MAC
    return print(f' ALTERADO(s) AP. REGULAR: \033[0;31m{contaAp}\033[m ALTERADO(s) PROMO: \033[0;31m{contaPromo}\033[m  TOTAL de ALTERADOS:\033[0;31m {contaTotal}\033[m\n > Processo concluído!  \n > \033[0;31mNúmero total de registro(s) \033[m{len(final)}\n > Itens não Encontrados: \033[0;31mAp. Regular: \033[m {len(logErrorAp)}  \033[0;31mPromocao: \033[m {len(logErrorPromo)}')
#---------------------------------------------------------------------------------------------------------------------------------------------
# Validação de campo PROMOCAO  - versao 1.0 - last update: 25/02/2019
def validaCampoPROMO(dataset,coluna,arg1,arg2,arg3):
    """
    DOCSTRING
    """
    ''' Esta função tem como objetivo fazer a verificação se os argumentos estão corretos '''
    dataset[coluna] = dataset[coluna].astype(str)
    count = len(dataset)
    correto, incorreto = 0,0
    for i in range(0, count):
        if len(dataset[coluna][i]) == len(arg1) and arg1 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg2) and arg2 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg3) and arg3 in dataset[coluna][i]:
            correto +=1      
        else:
            incorreto +=1
            print(f'Linha: {i} Valor: ',dataset[coluna][i])
    return  print('\033[0;31mCorretos: \033[m',correto ,' ','\033[0;31mIncorretos: \033[m',incorreto)
#---------------------------------------------------------------------------------------------------------------------------------------------
# Validação de campo APRESENTACAO REGULAR - versao 1.0 - last update: 25/02/2019    
def validaCampoAP(dataset,coluna,arg1,arg2,arg3,arg4,arg5,arg6):
    """
    DOCSTRING
    """
    ''' Esta função tem como objetivo fazer a verificação se os argumentos estão corretos '''
    dataset[coluna] = dataset[coluna].astype(str) 
    count = len(dataset)
    correto, incorreto = 0,0
    for i in range(0, count):
        if len(dataset[coluna][i]) == len(arg1) and arg1 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg2) and arg2 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg3) and arg3 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg4) and arg4 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg5) and arg5 in dataset[coluna][i] or len(dataset[coluna][i]) == len(arg6) and arg6 in dataset[coluna][i]:
            correto +=1      
        else:
            incorreto +=1
            print(f'Linha:{i} Valor: ',dataset[coluna][i])
    return  print('\033[0;31mCorretos: \033[m',correto ,' ','\033[0;31mIncorretos: \033[m',incorreto)
#---------------------------------------------------------------------------------------------------------------------------------------------  
def concatena(user,name):
    '''
    Função Contatenar aarquivo de diretório / SURGERY
    '''
    os.chdir(f'/Users/{user}/Google Drive Nielsen/_jupyter/_massivo/_csv-file') # MAC
    #os.chdir('C:/Users/sije8002/Google Drive/_jupyter/_massivo/_csv-file')     # WIN
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(f"{name}.csv", index=False, encoding='utf-8')
    return print('\033[0;31m Processo concluído!\033[m')

#---------------------------------------------------------------------------------------------------------------------------------------------  