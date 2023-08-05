#============ Nielsen ================
# Created: 09/03/2019 / Classe Pilar 2
# Created by Jeiso Silva
#=====================================
#--------------------------------------------------------------------------------------------------------------------------------------------- 
import pandas as pd
import os
import glob
# Caracterização Massiva (SURGERY) - Pilar 2 - versao 2.0 - last update: 15/03/2019
def charMassivaP2(user,OGRDS,nameColumn,status_column,fileName,numero_char):
    '''
    Função criação de arquivos modelo.
    '''
    modelo = pd.read_csv('C:/Users/{}/Google Drive/_jupyter/_massivo/_model-file/csv-modelo.csv'.format(user),delimiter = ';') # WIN
    #modelo = pd.read_csv('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_massivo/_model-file/csv-modelo.csv',delimiter = ';') # MAC 
    charQuery = OGRDS[['Item Code','ITEM DESCRIPTIONS',nameColumn,status_column]] # CRIANDO VARIÁVEIS    
    charQuery = charQuery.loc[OGRDS[status_column] == 'ALTERADO']  # FILTERS
    modelo['ITEM_CODE'] = charQuery['Item Code'] # MODELO
    modelo['CHAR_CODE'] = numero_char
    modelo['CHAR_DSCR'] = charQuery[nameColumn] 
    modelo.to_csv('C:/Users/{}/Google Drive/_jupyter/_pilar-2/_csv-file/{}.csv'.format(user,fileName),index=False) # WIN
    #modelo.to_csv('/Users/{}/Google Drive Nielsen/_jupyter/_pilar-2/_csv-file/{}.csv'.format(user,fileName),index=False) # MAC
    return print(f'> Número de ALTERADO(s) \033[0;31m{len(charQuery)}\033[m\n> Processo concluído!\n>\033[0;31m Arquivo gerado com {len(modelo)} registro(s).\033[m ')       
#---------------------------------------------------------------------------------------------------------------------------------------------  
    # Função que encontra o chars no OGRDS - versao 1.0 - last update: 04/02/2019
def findChar(num):
    ''' 
    Esta função encontra Type_Code(OGRDS) de uma característica(IMDB) 
    ''' 
    df2 = pd.read_csv('file/car_id.csv') # local do arquivo
    file = df2.loc[df2['Car_id'] == num ]
    return file
#---------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------  
    # Função cria arquivos uma SHEETS para realisação de análises das Standards do  OGRDS - versao 2.0 - last update: 08/05/2019
def charControl(user,numCp):
    ''' 
    Falar sobre essa func
    ''' 
    #data = pd.read_excel('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_apoio/Chars_por_Categoria_OGRDS.xlsx') # MAC
    #modelo = pd.read_excel('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_apoio/charControl_modelo.xlsx')      # MAC
    #impactoFormato = pd.read_excel('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_apoio/impacto.xlsx')         # MAC
    data = pd.read_excel('C:/Users/{}/Google Drive/_jupyter/_apoio/Chars_por_Categoria_OGRDS.xlsx'.format(user)) # WIN
    modelo = pd.read_excel('C:/Users/{}/Google Drive/_jupyter/_apoio/charControl_modelo.xlsx'.format(user))      # WIN
    impactoFormato = pd.read_excel('C:/Users/{}/Google Drive/_jupyter/_apoio/impacto.xlsx'.format(user))         # WIN

    filtro = data.loc[data['Modulo_Legacy'] == numCp]
    dataset = filtro[['Modulo_Legacy','Car_id','DESC']] 
    modelo['aci_val_Id_Mod']   = dataset['Modulo_Legacy']
    modelo['car_id']           = dataset['Car_id']
    modelo['car_DescLarga_I1'] = dataset['DESC']
    #modelo['aci_OrdenAlta']    = '-'
    modelo['Base ou Destino?'] = 'Base' 
    # Não aplica
    modelo.set_value(modelo[modelo['car_id'] == 4].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 6].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 100026].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301010].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301171].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301172].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 302001].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 302002].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 302003].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 302004].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 900900].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 900901].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000001].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000002].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000003].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000004].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000005].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000006].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000007].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000008].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 1000009].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301166].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301175].index, 'Base ou Destino?', 'Não Aplica') 
    modelo.set_value(modelo[modelo['car_id'] == 301001].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301040].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301117].index, 'Base ou Destino?', 'Não Aplica')
    modelo.set_value(modelo[modelo['car_id'] == 301005].index, 'Base ou Destino?', 'Não Aplica') 
    #IBENCHMARK
    modelo.set_value(modelo[modelo['car_id'] == 300001].index, 'Standard PILAR 2', 'Standard')
    modelo.set_value(modelo[modelo['car_id'] == 300001].index, 'Base ou Destino?', 'Base')
    #MARCA
    modelo.set_value(modelo[modelo['car_id'] == 90090].index, 'Standard PILAR 2', 'Standard')
    modelo.set_value(modelo[modelo['car_id'] == 90090].index, 'Base ou Destino?', 'Base')
    #FABRICANTE
    modelo.set_value(modelo[modelo['car_id'] == 90080].index, 'Standard PILAR 2', 'Standard')
    modelo.set_value(modelo[modelo['car_id'] == 90080].index, 'Base ou Destino?', 'Base')
    #APRESENTACAO REGULAR
    modelo.set_value(modelo[modelo['car_id'] == 90050].index, 'Standard PILAR 2', 'Standard')
    modelo.set_value(modelo[modelo['car_id'] == 90050].index, 'Base ou Destino?', 'Base')
    #PROMOCAO
    modelo.set_value(modelo[modelo['car_id'] == 90020].index, 'Standard PILAR 2', 'Standard')
    modelo.set_value(modelo[modelo['car_id'] == 90020].index, 'Base ou Destino?', 'Base')
    #=================================================================================================
    modelo = modelo.reset_index(drop=True)
    # Verifica se existem chars em comum   
    #data = pd.read_excel('/Users/jeisosilva/Google Drive Nielsen/_jupyter/_apoio/Chars_por_Categoria_OGRDS.xlsx')
    def charComum(numCharComum,data):
        char = data.loc[data['Car_id'] == numCharComum]
        return char.shape[0]
    #=================================================================================================
    #impactoFormato
    def findServico(cp,char):     
        filtro1 = impactoFormato.loc[impactoFormato['ModuleId'] == cp]
        filtro2 = filtro1.loc[filtro1['CarId'] == char]
        filtro3 = pd.DataFrame()
        filtro3['servico'] = filtro2.Servico.unique()
        filtro3 = filtro3.reset_index(drop=True)
        if len(filtro3.servico) == 3:
            serv = filtro3.servico[0] +','+ filtro3.servico[1] +','+ filtro3.servico[2]
        elif len(filtro3.servico) == 2:
            serv = filtro3.servico[0] +','+ filtro3.servico[1]
        elif len(filtro3.servico) == 1:
            serv = filtro3.servico[0]
        else:
            serv = 'Sem Impacto'
        return serv
    #=================================================================================================
    y = 0
    while y < len(modelo):
        if modelo['Base ou Destino?'][y] == 'Base':
            #print(tt.car_id[y])
            char = modelo.car_id[y]
            modelo['char_comun'][y] = charComum(char,data)
            modelo['Impacto/Serviço'][y] = findServico(numCp,char)
        else:
            modelo['char_comun'][y] = 0 
            
        y += 1
    #=================================================================================================
    return modelo 
#--------------------------------------------------------------------------------------------------------------------------------------------- 
# Função faz a junção das SHEETS e salve o arquivo - versao 1.0 - last update: 9/03/2019
def fileSheets(user,char_control,name):
    '''
    Gera o arquide de análise para o Pilar 2
    '''
    IMDB = pd.read_csv('C:/Users/{}/Google Drive/_jupyter/_imdb/{}_IMDB_TN.CSV'.format(user,name))           # WIN
    #IMDB = pd.read_csv('/Users/{}/Google Drive Nielsen/_jupyter/_imdb/{}_IMDB_TN.CSV'.format(user,name))    # MAC
    writer = pd.ExcelWriter('C:/Users/{}/Google Drive/_jupyter/Char_control/{}_OGRDS.xlsx'.format(user,name),engine='xlsxwriter')        # WIN
    #writer = pd.ExcelWriter('/Users/{}/Google Drive Nielsen/_jupyter/Char_control/{}_OGRDS.xlsx'.format(user,name),engine='xlsxwriter') # MAC 
    IMDB.to_excel(writer, sheet_name='{}_OGRDS'.format(name),index=False) # Montando o arquivo
    char_control.to_excel(writer, sheet_name='Char control',index=False)
    writer.save()
    return print(f'>\033[0;31m Gerando arquivos...\033[m \n>\033[0;31m Processo Concluído!\033[m')
#---------------------------------------------------------------------------------------------------------------------------------------------
def importa(user, NameCp_OGRDS):
    '''
    Função que retorna um DataFrame
    '''
    OGRDS = pd.read_excel('C:/Users/{}/Google Drive/_jupyter/_pilar-2/_ogrds-file/{}_OGRDS.xlsx'.format(user,NameCp_OGRDS))        # WIN
    #OGRDS = pd.read_excel('/Users/{}/Google Drive Nielsen/_jupyter/_pilar-2/_ogrds-file/{}_OGRDS.xlsx'.format(user,NameCp_OGRDS)) # MAC
    return OGRDS
#---------------------------------------------------------------------------------------------------------------------------------------------
def concatena(user,name):
    '''
    Função Contatenar aarquivo de diretório / SURGERY
    '''
    #os.chdir(f'/Users/{user}/Google Drive Nielsen/_jupyter/_pilar-2/_csv-file') # MAC
    os.chdir(f'C:/Users/{user}/Google Drive/_jupyter/_pilar-2/_csv-file')       # WIN
    all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    #export to csv
    combined_csv.to_csv(f"{name}.csv", index=False, encoding='utf-8')
    return print('\033[0;31m Concatenado!\033[m')
#---------------------------------------------------------------------------------------------------------------------------------------------
