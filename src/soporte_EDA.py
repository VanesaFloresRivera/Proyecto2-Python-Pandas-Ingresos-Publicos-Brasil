import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

#función para traducir el nombre de las columnas:
def traducción_columnas(df_estudio):

    column_translation = {
        'CÓDIGO ÓRGÃO SUPERIOR': 'CÓDIGO_ÓRGANO_SUPERIOR',
        'NOME ÓRGÃO SUPERIOR': 'NOMBRE_ÓRGANO_SUPERIOR',
        'CÓDIGO ÓRGÃO': 'CÓDIGO_ÓRGANO',
        'NOME ÓRGÃO': 'NOMBRE_ÓRGANO',
        'CÓDIGO UNIDADE GESTORA': 'CÓDIGO_UNIDAD_GESTORA',
        'NOME UNIDADE GESTORA': 'NOMBRE_UNIDAD_GESTORA',
        'CATEGORIA ECONÔMICA': 'CATEGORÍA_ECONÓMICA',
        'ORIGEM RECEITA': 'ORIGEN_INGRESO',
        'ESPÉCIE RECEITA': 'TIPO_INGRESO',
        'DETALHAMENTO': 'DETALLE',
        'VALOR PREVISTO ATUALIZADO': 'VALOR_PREVISTO_ACTUALIZADO',
        'VALOR LANÇADO': 'VALOR_REGISTRADO',
        'VALOR REALIZADO': 'VALOR_REALIZADO',
        'PERCENTUAL REALIZADO': 'PORCENTAJE_REALIZADO',
        'DATA LANÇAMENTO': 'FECHA_REGISTRO',
        'ANO EXERCÍCIO': 'AÑO_EJERCICIO'
    }

    df_estudio.rename(columns=column_translation, inplace=True)




#Creación de una función report que me reporte el número de nulos, su % y el tipo de dato para cada columna:

def reporte (df_estudio):

    df_report = pd.DataFrame()

    df_report["tipo_variables"] = pd.DataFrame(df_estudio.dtypes)
    df_report["contador_total"] = pd.DataFrame(df_estudio.count ())
    df_report["numero_nulos"]=df_estudio.isnull().sum()
    df_report["porcentaje_nulos"] = round((df_estudio.isnull().sum()/df_estudio.shape[0])*100,2)
    df_report["valores_unicos"] = pd.DataFrame(df_estudio.nunique ())
    

    diccionario_duplicados = {}
    for indice in range (0, df_estudio.shape[1]):
        k= df_estudio.columns[indice]
        v= df_estudio.iloc[:,indice].duplicated().sum()
        diccionario_duplicados.update({k:v})
    
    serie_duplicados = pd.Series(diccionario_duplicados)

    df_report["duplicados"] = pd.DataFrame(serie_duplicados)
    


    print(f'La tabla tiene {df_estudio.shape[0]} filas y {df_estudio.shape[1]} columnas')

    print(f'La tabla tiene {df_estudio.duplicated().sum()} filas duplicadas ')

    return df_report



#Creación función para el análisis de las variables categóricas:
def analisis_descriptivos_categóricas (df_estudio):
    df_categóricas = df_estudio.select_dtypes(include = "object")
    print(f'Las columnas categóricas son {df_categóricas.columns}')
    print(f'Algunos ejemplos de filas son:')
    display(df_categóricas.sample(5))
    df_estudio_categóricas = df_estudio.describe(include = "object").T
    print(f'Las características de estas columnas son:')
    return df_estudio_categóricas



#Creación función para el análisis de las variables no categóricas:
def analisis_descriptivos_numéricas(df_estudio):
    df_no_categoricas = df_estudio.select_dtypes(exclude = "object")      
    print(f'Las columnas no categóricas son {df_no_categoricas.columns}')
    print(f'Algunos ejemplos de filas son:')
    display(df_no_categoricas.sample(5))
    df_estudio_numéricas = np.round(df_no_categoricas.describe().T,2)
    print(f'Las características de estas columnas son:')
    return df_estudio_numéricas



def analisis_individual_columnas(df_estudio, columna_analisis):

    df_columna = pd.DataFrame(df_estudio[columna_analisis].value_counts())
    print(f'La categoría {columna_analisis} tiene {df_columna.shape[0]} elementos diferentes: \n')

    print(f'Los elementos de la categoría son:')
    display(df_estudio[columna_analisis].unique())

    df_columna["Porcentaje_recuento"] = np.round(df_columna['count']/df_estudio.shape[0]*100,2)
    print(f'Los 10 {columna_analisis} que MAS aparecen son:')
    display(df_columna.head(10))

    print(f'Los 10 {columna_analisis} que MENOS aparecen son:')
    display(df_columna.tail(10))

    df_columna_contador_columnas = pd.DataFrame(df_columna['count'].value_counts())
    df_columna_contador_columnas['% repetición'] =df_columna_contador_columnas['count']/df_columna.shape[0]*100
    print(f' Las distribución de las repeticiones de los {columna_analisis} son:')
    display(df_columna_contador_columnas)



 #Función para la conversión de las columnas a los formatos correctos:   
def conversion_columnas (df_estudio):
    #convierto la columna FECHA_REGISTRO en Fecha:

    try:
        df_estudio['FECHA_REGISTRO'] = df_estudio['FECHA_REGISTRO'] .str.replace('/', '-') #sustituyo las barras por guiones
        df_estudio['FECHA_REGISTRO']= pd.to_datetime(df_estudio['FECHA_REGISTRO'])
    except:
        df_estudio['FECHA_REGISTRO'] = df_estudio['FECHA_REGISTRO'] .str.replace('/', '-') #sustituyo las barras por guiones
        df_estudio['FECHA_REGISTRO']= pd.to_datetime(df_estudio['FECHA_REGISTRO'], format="%d-%m-%Y")

    #convierto la columna VALOR_PREVISTO_ACTUALIZADO	en float:
    #1. Sustituyo las comas por puntos:
    df_estudio['VALOR_PREVISTO_ACTUALIZADO'] = df_estudio['VALOR_PREVISTO_ACTUALIZADO'] .str.replace(',', '.')
    #2. Hago la conversión a float:
    df_estudio['VALOR_PREVISTO_ACTUALIZADO']= df_estudio['VALOR_PREVISTO_ACTUALIZADO'].astype("float", errors = "ignore")

    #convierto la columna VALOR_REGISTRADO	en float:
    #1. Sustituyo las comas por puntos:
    df_estudio['VALOR_REGISTRADO'] = df_estudio['VALOR_REGISTRADO'] .str.replace(',', '.')
    #2. Hago la conversión a float:
    df_estudio['VALOR_REGISTRADO']= df_estudio['VALOR_REGISTRADO'].astype("float", errors = "ignore")

    #convierto la columna VALOR_REALIZADO en float:
    #1. Sustituyo las comas por puntos:
    df_estudio['VALOR_REALIZADO'] = df_estudio['VALOR_REALIZADO'] .str.replace(',', '.')
    #2. Hago la conversión a float:
    df_estudio['VALOR_REALIZADO']= df_estudio['VALOR_REALIZADO'].astype("float", errors = "ignore")


    #convierto la columna PORCENTAJE_REALIZADO en float:
    #1. Sustituyo las comas por puntos:
    df_estudio['PORCENTAJE_REALIZADO'] = df_estudio['PORCENTAJE_REALIZADO'] .str.replace(',', '.')
    #2. Hago la conversión a float:
    df_estudio['PORCENTAJE_REALIZADO']= df_estudio['PORCENTAJE_REALIZADO'].astype("float", errors = "ignore")

    #convierto la columna CÓDIGO_ÓRGANO_SUPERIOR en string:
    df_estudio['CÓDIGO_ÓRGANO_SUPERIOR']= df_estudio['CÓDIGO_ÓRGANO_SUPERIOR'].astype("str", errors = "ignore")

    #convierto la columna CÓDIGO_ÓRGANO	 en integer:
    df_estudio['CÓDIGO_ÓRGANO']= df_estudio['CÓDIGO_ÓRGANO'].astype("str", errors = "ignore")

    #convierto la columna CÓDIGO UNIDADE GESTORA en integer:
    df_estudio['CÓDIGO_UNIDAD_GESTORA']= df_estudio['CÓDIGO_UNIDAD_GESTORA'].astype("str", errors = "ignore")
    return reporte(df_estudio)

# Función para cargar los ficheros
def carga_ficheros(lista_ficheros):
    diccionario_datos ={}
    for fichero in lista_ficheros:
        clave = 'df_'+fichero[6:10]
        diccionario_datos[clave] = pd.read_csv(f"../datos/raw/{fichero}", sep=';', encoding='latin-1')
    return diccionario_datos