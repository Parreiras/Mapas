# -*- coding: utf-8 -*-
"""meso.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R07L2FB6ZWvwkfk4Jhg8niGdi7XeLGWK
"""

# Commented out IPython magic to ensure Python compatibility.
#INSTALANDO AS BIBLIOTECAS NECESSÁRIAS

!pip install geopandas
!pip install mapclassify
!pip install geoplot
!pip install descartes
# %matplotlib inline
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import mapclassify
import geoplot
import geopandas as gpd
import matplotlib.colors as colors
import seaborn

from google.colab import drive
drive.mount('/content/drive')

#CARREGANDO O MAPA DO BRASIL POR MESORREGIÕES

br = '/content/drive/MyDrive/Minas Gerais/31MUE250GC_SIR.shp'
map = gpd.read_file(br)
map



#CARREGANDO O DATAFRAME COM OS VALORES QUE QUEREMOS PLOTAR
tabela = pd.read_csv('/content/Municipio.txt')
tabela

#ACHANDO VALORES COM ESCRITA DIFERENTE PARA PODER FAZER CORREÇÃO

lista1 = set(tabela['Munip'])
lista2 = map.loc[map['NM_MUNICIP'].isin(tabela['Munip'])]
lista2 = set(lista2['NM_MUNICIP'])

lista1.symmetric_difference(lista2)

#JUNTANDO OS DOIS DATAFRAMES
plota = pd.merge(map,tabela, right_on = 'Munip', left_on = 'NM_MUNICIP', how = 'left')

#MUDANDO OS NaN DA CLASSE NÚMERO POR 0 E EXCLUINDO A COLUNA MESO QUE ESTÁ REPETIDA
plota['Qtd'] = plota['Qtd'].fillna(0)
plota = plota.drop(columns = 'Munip')
plota

#CRIANDO UM FRAME PARA NOMEAR AS MESOREGIÕES DADA A IDENTIFICAÇÃO ATRIBUIDAS A ELAS
nome = map.loc[map['NM_MUNICIP'].isin(tabela['Munip'])]
nome1 = pd.merge(nome,tabela, right_on='Munip' ,  left_on='NM_MUNICIP', how = 'left')
nome1 = nome1.drop(columns='Munip')
nome1

#ESCOLHENDO A COLUNA NA QUAL SERÃO CLASSIFICADAS AS ZONAS DO MAPA

classificador = nome1['Qtd']

#ENCONTRANDO O MELHOR CLASSIFICADOR PARA AS FAIXAS DO MAPA
#ADCM é calculado e fornece uma medida de ajuste que permite a comparação de classificadores alternativos para o mesmo valor de K. 
#O ADCM nos dará uma noção de quão compacto é cada grupo. Para ver isso, podemos comparar diferentes classificadores. 
#Quanto menor o valor do ADCM melhor ajustado é aquele classificador


t1 =  mapclassify.Quantiles(classificador,  k = 2)
t2 = mapclassify.EqualInterval(classificador,  k = 2)
t3 =  mapclassify.HeadTailBreaks(classificador)
t4 =  mapclassify.MaximumBreaks(classificador,  k = 2)
t5 = mapclassify.StdMean(classificador)
t6 = mapclassify.FisherJenks(classificador,  k = 2)
#t7 =  mapclassify.JenksCaspall(classificador,  k = 5)
#t9 = mapclassify.UserDefined(classificador,[0, 5, 8, 10 ,26])

#VISUALIZAÇÃO PARA ESCOLHER O MELHOR CLASSIFICADOR

class5 = t1, t2, t3, t4, t5, t6,

fits = np.array([ c.adcm for c in class5])

adcms = pd.DataFrame(fits)

adcms['classificador'] = [c.name for c in class5]

adcms.columns = ['ADCM', 'Classificador']
ax = seaborn.barplot(
    y='Classificador', x='ADCM', data=adcms, palette='Pastel1'
)

#USANDO O CLASSIFICADOR

scheme =  t6

#PALETA DE CORES

from numpy.core.function_base import linspace
def coresnovas (cmap, minval = 0.0, maxval = 1, n = 1000):
  cor = colors.LinearSegmentedColormap.from_list(
      'trunc({n}, {a:.2f}, {b:.2f})'.format(n = cmap.name, a = minval, b = maxval), 
      cmap(np.linspace(minval, maxval, n )))
  return cor

arr = np.linspace(0, 50, 100).reshape((10,10))
fig, ax = plt.subplots(ncols = 2)

cmap = plt.get_cmap('Greens')
cor = coresnovas(cmap, 0.6,  1)
ax[0].imshow(arr, interpolation = 'nearest', cmap = cmap)
ax[1].imshow(arr, interpolation = 'nearest', cmap = cor)
plt.show()

#filtra a tabela pelo valor especificado na coluna


#df_tab = tabela['numero']>8

#filtered_df = tabela[df_tab]
#filtered_df



fig, ax = plt.subplots(1, figsize=(20, 10
                                   ))


ax.axis('off')

ax.set_title('Municipios', fontdict={'fontsize': '25', 'fontweight' : '3'})


geoplot.choropleth(nome1, hue = classificador , scheme = scheme, ax = ax, cmap = cor, legend = True, edgecolor = '0',
                    legend_kwargs={"loc":"lower right",
                                  "fontsize": "large",
                                  "title":"Pacientes Covid",
                                  "title_fontsize":"large"},
                  
                   
                   
                  
              
 )
nome1['coords'] = nome1['geometry'].apply(lambda x: x.representative_point().coords[:])
nome1['coords'] = [coords[0] for coords in nome1['coords']]

for idx, row in nome1.iterrows():
    plt.annotate(s=row['Ident'], xy=row['coords'],horizontalalignment='center',fontsize = '14', color = 'Black')



