# -*- coding: utf-8 -*-
"""Projeto Final [CREDITO].ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FzD6XyBn17VBz9UQOWtGtsGjgGAgzlK5

**MBA em Ciência de Dados e Analytics do SENAI-CIMATEC**

**Disciplina - Introdução à Estatística**

**Professor - Jonatas Silva**

**Alunos:**

**Luan Hereda**

**Rafael Bahia**

**Vinícius Spencer Santos**






---




                                                          **Atividade Final**




---




**Insights**



1.   O que mais importa na hora de conceder um limite de cartão de crédito para o cliente: A sua renda ou a sua utilização?
2.   Considerando uma pessoa com escolaridade no nivel 'Mestrado', qual a probabilidade de ser liberado um limite de crédito maior ou igual a 25K?

### **O dataset**

Estes conjuntos de dados, criados pelo EBAC, e os atributos são:
idade; sexo; dependentes; escolaridade; estado_civil; salario_anual; tipo_cartao; qtd_produtos; iteracoes_12m; meses_inativo; limite_cartao; valor_transacoes; qtd_transacoes_12m.


- **idade:** Idade do cliente
- **sexo:** Sexo do cliente (F ou M)
- **dependentes:** Número de dependentes do cliente
- **escolaridade:** Nível de escolaridade do clientes
- **estado_civil:** Estado civil
- **salario_anual:** Salário por ano em dólares
- **tipo_cartao:** Categoria de cartao
- **qtd_produtos:** Quantidade de produtos adquiridos
- **iteracoes_12m:** Quantidade de iteracoes/transacoes nos últimos 12 meses
- **meses_inativo:** Quantidade de meses sem atividade junto à empresa
- **limite_cartao:** Valor de limite do cartao do cliente
- **valor_transacoes:** soma das transacoes dos últimos 12 meses
- **qtd_transacoes_12m:** Quantidade de transacoes em 12 meses

O conjunto de dados está disponível em um repositório no Kaggle que pode ser acessado através do link:

- https://www.kaggle.com/datasets/mateuscpinheiro/analise-credito-clientes-ebac-sql;
"""

# Importando o Pandas
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import seaborn as sns

# Importando o conjunto de dados do repositório do github
dt = pd.read_csv(
    filepath_or_buffer = 'https://raw.githubusercontent.com/bahia-rafael/statistic-data/main/credito8.csv',
    sep=',',
    decimal='.'
)

"""# Visualizando e tratando os valores da Base de Dados"""

# Validando que o dataset foi carregado

dt

"""Apesar de não aparecer valores nulos no dataset, é possivel identificar em algumas colunas valores "na", o que provavelmente significa que aquele valor seria nulo, mas ao invés de serem preenchidos com valores nulos, eles foram preenchidos com "na".
Vamos tratar esses dados para não haver complicações nos resultados.
"""

#transformando o 'na' em valores nulos de fato
dt.replace('na', np.nan, inplace = True)
# Excluindo os registros que possuem campos nulos da tabela
dt = dt.dropna()

dt.info()

dt.describe()

"""## Categorizando variáveis

### Idade

Ref.: [Categoria das Idades - Jovem](https://www12.senado.leg.br/radio/1/noticia/2022/08/12/20-anos-da-lei-que-instituiu-12-de-agosto-como-dia-nacional-da-juventude#:~:text=Comemorado%20no%20dia%2012%20de%20agosto%2C%20o%20Dia%20Nacional%20da,entre%2015%20e%2029%20anos.)

Ref.: [Categoria das Idades - Adulto](https://web.archive.org/web/20190225164941/https://www.redalyc.org/html/848/84806108/)

1.   Pessoa considerada jovem (idade <= 29 anos)
2.   Pessoa considerada jovem adulta (idade > 29 anos e idade <= 40 anos)
3.   Pessoa considerada na meia idade (idade > 40 anos e idade <= 65 anos)
4.   Pessoa considerada idosa (idade > 65 anos)
"""

# lista de intervalos de idade
conditions = [
    (dt['idade'] <= 29),
    (dt['idade'] > 29) & (dt['idade'] <= 40),
    (dt['idade'] > 40) & (dt['idade'] <= 65),
    (dt['idade'] > 65)
    ]

# Cria uma lista de tipos de faixa etaria, na sequencia das condições montadas acima
values = ['jovem', 'jovem_adulto', 'meia_idade', 'idoso']

# Cria uma coluna para categorizar os clientes pela sua idade
dt['faixa_etaria'] = np.select(conditions, values)

# Agrupando por faixa etaria
dt_faixa_etaria = dt.groupby(['faixa_etaria'])['faixa_etaria'].count()\
  .reset_index(name='qtd')\
  .sort_values('qtd', ascending=False)

dt_faixa_etaria

# Gerando um gráfico de barras
dt_faixa_etaria.sort_values('faixa_etaria', ascending=False)\
  .plot.barh(
    x='faixa_etaria',
    y = 'qtd',
    color = 'darkblue',
    figsize=(10, 6),
    title = 'Faixa Etária dos clientes do banco EBAC.',
    ylabel='Faixa Etária',
    xlabel='Quantidade de clientes',
    legend = False,
    width = 0.8
);

"""### Salário Anual

Ref.: [Salário - Classe Social](https://capitalist.com.br/voce-se-considera-classe-media-no-pais-saiba-como-descobrir/#:~:text=N%C3%A3o%20existe%20um%20valor%20estabelecido,a%20R%24%209.847%20por%20m%C3%AAs)


1.   Pessoa considerada Classe D/E   (salario_anual < 40k)
2.   Pessoa considerada Classe Média (salario_anual >= 40k e salario_anual < 80k)
3.   Pessoa considerada Classe Alta  (salario_anual > 80k)



"""

# lista de intervalos de salario anial
conditions = [
    (dt['salario_anual'] == 'menos que $40K'),
    (dt['salario_anual'] == '$40K - $60K') | (dt['salario_anual'] == '$60K - $80K'),
    (dt['salario_anual'] == '$80K - $120K') | (dt['salario_anual'] == '$120K +')
    ]

# Cria uma lista de tipos de faixa etaria, na sequencia das condições montadas acima
values = ['classe_baixa', 'classe_media', 'classe_alta']

# Cria uma coluna para categorizar os clientes pelo seu salario anual
dt['classe_social'] = np.select(conditions, values)

# Agrupando pela classe social
classe_social = dt.groupby(['classe_social'])['classe_social'].count()\
  .reset_index(name='qtd')\
  .sort_values('qtd', ascending=False)

# Verificando o resultado do dataframe gerado
classe_social.iloc[[0, 1]] = classe_social.iloc[[1, 0]]

classe_social

# Gerando um gráfico de barras
classe_social.plot.barh(
    x='classe_social',
    y = 'qtd',
    color = 'darkgreen',
    figsize=(10, 6),
    title = 'Faixa Etária dos clientes do banco EBAC.',
    ylabel='Faixa Etária',
    xlabel='Quantidade de clientes',
    legend = False,
    width = 0.8
);

dt

"""

# 1. Análise da Idade em relação as variáveis númericas

*   1.1 - QTD Produtos
*   1.2 - Iterações em 12 meses
*   1.3 - Meses Inativos
*   1.4 - Limite do Cartão
*   1.5 - Valor das transações
*   1.6 - Quantidade de Transações em 12 meses












"""

#sabendo que a média de idade dos clientes é aprox. 46 anos, vamos entender visualmente nossa distribuição de idades
grafico1 = px.histogram(dt, x='idade', text_auto=True, histfunc='count')
grafico1.show()

dt_idade_media = dt.groupby(['faixa_etaria'], as_index=False).mean()
dt_idade_media.head(5)

dt_idade_min = dt.groupby(['faixa_etaria'], as_index=False).min()
dt_idade_min = dt_idade_min[['faixa_etaria','qtd_produtos','iteracoes_12m','meses_inativo','limite_cartao','valor_transacoes','qtd_transacoes_12m']]
dt_idade_min.head(5)

dt_idade_max = dt.groupby(['faixa_etaria'], as_index=False).max()
dt_idade_max = dt_idade_max[['faixa_etaria','qtd_produtos','iteracoes_12m','meses_inativo','limite_cartao','valor_transacoes','qtd_transacoes_12m']]
dt_idade_max.head(5)

"""## 1.1 - QTD Produtos"""

dt_idadeqtdprodmed = dt_idade_media[['faixa_etaria','qtd_produtos']]
dt_idadeqtdprodmed.rename(columns={'qtd_produtos': 'qtd_produtos_med'})
dt_idadeqtdprodmed.head(5)

dt_idadeqtdprodmin = dt_idade_min[['faixa_etaria','qtd_produtos']]
dt_idadeqtdprodmin.rename(columns={'qtd_produtos': 'qtd_produtos_min'})
dt_idadeqtdprodmin.head(5)

dt_idadeqtdprodmax = dt_idade_max[['faixa_etaria','qtd_produtos']]
dt_idadeqtdprodmax.rename(columns={'qtd_produtos': 'qtd_produtos_max'})
dt_idadeqtdprodmax.head(5)

dt_idade_qtdprod = pd.merge(dt_idadeqtdprodmin, dt_idadeqtdprodmax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idade_qtdprod = pd.merge(dt_idade_qtdprod,dt_idadeqtdprodmed, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idade_qtdprod = dt_idade_qtdprod.rename(columns={'qtd_produtos_x': 'qtd_min_produtos'})
dt_idade_qtdprod = dt_idade_qtdprod.rename(columns={'qtd_produtos_y': 'qtd_max_produtos'})
dt_idade_qtdprod = dt_idade_qtdprod.rename(columns={'qtd_produtos': 'qtd_med_produtos'})
dt_idade_qtdprod = dt_idade_qtdprod[['faixa_etaria', 'qtd_min_produtos', 'qtd_med_produtos', 'qtd_max_produtos']]
dt_idade_qtdprod.head(20)

dt_idade_qtdprod.iloc[[0, 1]] = dt_idade_qtdprod.iloc[[1, 0]]
dt_idade_qtdprod

dt_idade_qtdprod.iloc[[1, 2]] = dt_idade_qtdprod.iloc[[2, 1]]
dt_idade_qtdprod

dt_idade_qtdprod.iloc[[2, 3]] = dt_idade_qtdprod.iloc[[3, 2]]
dt_idade_qtdprod

x_pos = range(len(dt_idade_qtdprod['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idade_qtdprod['qtd_med_produtos'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idade_qtdprod['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Qtd de Produtos')
plt.title('Qtd de Produtos por faixa etária')

plt.show()

x_pos = range(len(dt_idade_qtdprod['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idade_qtdprod['qtd_min_produtos'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idade_qtdprod['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Qtd de Produtos')
plt.title('Qtd de Produtos minimos por faixa etária')

plt.show()

x_pos = range(len(dt_idade_qtdprod['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idade_qtdprod['qtd_max_produtos'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idade_qtdprod['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Qtd de Produtos')
plt.title('Qtd de Produtos Máximos por faixa etária')

plt.show()

"""## 1.2 Iterações em 12 meses"""

#iterações medias por idade
dt_idadeitermedia = dt_idade_media[['faixa_etaria','iteracoes_12m']]
dt_idadeitermedia.head(10)

#iterações minimas por idade
dt_idadeitermin = dt_idade_min[['faixa_etaria','iteracoes_12m']]
dt_idadeitermin = dt_idadeitermin.rename(columns={'iteracoes_12m': 'iteracoes_12m_min'})
dt_idadeitermin.head(5)

#iterações máximas por idade
dt_idadeitermax = dt_idade_max[['faixa_etaria','iteracoes_12m']]
dt_idadeitermax = dt_idadeitermax.rename(columns={'iteracoes_12m': 'iteracoes_12m_max'})
dt_idadeitermax.head(5)

#juntando as 3 em 1 só
dt_idadeiter12m = pd.merge(dt_idadeitermin, dt_idadeitermax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeiter12m = pd.merge(dt_idadeiter12m,dt_idadeitermedia, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeiter12m = dt_idadeiter12m.rename(columns={'iteracoes_12m_x': 'iteracoes_12m_med_'})
dt_idadeiter12m = dt_idadeiter12m[['faixa_etaria', 'iteracoes_12m_min', 'iteracoes_12m', 'iteracoes_12m_max']]
dt_idadeiter12m.head(5)

nova_ordemiter = [1,2,3,0]
dt_idadeiter12m = dt_idadeiter12m.iloc[nova_ordemiter]
dt_idadeiter12m

x_pos = range(len(dt_idadeiter12m['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeiter12m['iteracoes_12m'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeiter12m['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Iterações')
plt.title('Iterações por faixa etária')

plt.show()

x_pos = range(len(dt_idadeiter12m['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeiter12m['iteracoes_12m_max'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeiter12m['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Iterações máximas')
plt.title('Iterações máximas por faixa etária')

plt.show()

x_pos = range(len(dt_idadeiter12m['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeiter12m['iteracoes_12m_min'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeiter12m['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Iterações minimas')
plt.title('Iterações minimas por faixa etária')

plt.show()

"""## 1.3 Meses Inativos"""

#iterações medias por idade
dt_idadeinativmedia = dt_idade_media[['faixa_etaria','meses_inativo']]
dt_idadeinativmedia.head(10)

#iterações minimas por idade
dt_idadeinativmin = dt_idade_min[['faixa_etaria','meses_inativo']]
dt_idadeinativmin = dt_idadeinativmin.rename(columns={'meses_inativo': 'meses_inativo_min'})
dt_idadeinativmin.head(5)

#iterações máximas por idade
dt_idadeinativmax = dt_idade_max[['faixa_etaria','meses_inativo']]
dt_idadeinativmax = dt_idadeinativmax.rename(columns={'meses_inativo': 'meses_inativo_max'})
dt_idadeinativmax.head(5)

#juntando as 3 em 1 só
dt_idadeinativ = pd.merge(dt_idadeinativmin, dt_idadeinativmax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeinativ = pd.merge(dt_idadeinativ,dt_idadeinativmedia, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeinativ = dt_idadeinativ.rename(columns={'meses_inativo': 'meses_inativo_med'})
dt_idadeinativ = dt_idadeinativ[['faixa_etaria', 'meses_inativo_min', 'meses_inativo_med', 'meses_inativo_max']]
dt_idadeinativ.head(5)

nova_ordeminativ = [1,2,3,0]
dt_idadeinativ = dt_idadeinativ.iloc[nova_ordeminativ]

x_pos = range(len(dt_idadeinativ['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeinativ['meses_inativo_med'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeinativ['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Meses Inativos')
plt.title('Meses Inativos por faixa etária')

plt.show()

x_pos = range(len(dt_idadeinativ['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeinativ['meses_inativo_min'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeinativ['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Meses Inativos')
plt.title('Minimo de Meses Inativos por faixa etária')

plt.show()

x_pos = range(len(dt_idadeinativ['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeinativ['meses_inativo_max'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeinativ['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Meses Inativos')
plt.title('Máximo de Meses Inativos por faixa etária')

plt.show()

"""## 1.4 Limite do Cartão"""

#Limite médio do cartão por idade
dt_idadelimitemedio = dt_idade_media[['faixa_etaria','limite_cartao']]
dt_idadelimitemedio.head(10)

#iterações minimas por idade
dt_idadelimitemin = dt_idade_min[['faixa_etaria','limite_cartao']]
dt_idadelimitemin = dt_idadelimitemin.rename(columns={'limite_cartao': 'limite_cartao_min'})
dt_idadelimitemin.head(5)

#iterações máximas por idade
dt_idadelimitemax = dt_idade_max[['faixa_etaria','limite_cartao']]
dt_idadelimitemax = dt_idadelimitemax.rename(columns={'limite_cartao': 'limite_cartao_max'})
dt_idadelimitemax.head(5)

#juntando as 3 em 1 só
dt_idadelimite = pd.merge(dt_idadelimitemin, dt_idadelimitemax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadelimite = pd.merge(dt_idadelimite,dt_idadelimitemedio, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadelimite = dt_idadelimite.rename(columns={'limite_cartao': 'limite_cartao_medio'})
dt_idadelimite = dt_idadelimite[['faixa_etaria', 'limite_cartao_min', 'limite_cartao_medio', 'limite_cartao_max']]
dt_idadelimite.head(5)

nova_ordemlimite = [1,2,3,0]
dt_idadelimite= dt_idadelimite.iloc[nova_ordemlimite]
dt_idadelimite

x_pos = range(len(dt_idadelimite['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadelimite['limite_cartao_medio'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadelimite['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Limite do Cartão')
plt.title('Limite do Cartão por faixa etária')

plt.show()

x_pos = range(len(dt_idadelimite['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadelimite['limite_cartao_min'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadelimite['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Limite do Cartão')
plt.title('Limite mínimo do Cartão por faixa etária')

plt.show()

x_pos = range(len(dt_idadelimite['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadelimite['limite_cartao_max'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadelimite['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Limite do Cartão')
plt.title('Limite máximo do Cartão por faixa etária')

plt.show()

"""## 1.5 Valor das Transações"""

#Valor de transações por idade
dt_idadevalortranmed = dt_idade_media[['faixa_etaria','valor_transacoes']]
dt_idadevalortranmed.head(10)

#Valor de transações por idade
dt_idadevalortranmin = dt_idade_min[['faixa_etaria','valor_transacoes']]
dt_idadevalortranmin = dt_idadevalortranmin.rename(columns={'valor_transacoes': 'valor_transacoes_min'})
dt_idadevalortranmin.head(5)

#iterações máximas por idade
dt_idadevalortranmax = dt_idade_max[['faixa_etaria','valor_transacoes']]
dt_idadevalortranmax = dt_idadevalortranmax.rename(columns={'valor_transacoes': 'valor_transacoes_max'})
dt_idadevalortranmax.head(5)

#juntando as 3 em 1 só
dt_idadevalortran = pd.merge(dt_idadevalortranmin, dt_idadevalortranmax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadevalortran = pd.merge(dt_idadevalortran,dt_idadevalortranmed, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadevalortran = dt_idadevalortran.rename(columns={'valor_transacoes': 'valor_transacoes_medio'})
dt_idadevalortran = dt_idadevalortran[['faixa_etaria', 'valor_transacoes_min', 'valor_transacoes_medio', 'valor_transacoes_max']]
dt_idadevalortran.head(5)

nova_ordemvalortran = [1,2,3,0]
dt_idadevalortran = dt_idadevalortran.iloc[nova_ordemvalortran]
dt_idadevalortran

x_pos = range(len(dt_idadevalortran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadevalortran['valor_transacoes_medio'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadevalortran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Valor de Transações')
plt.title('Valor de Transações por faixa etária')

plt.show()

x_pos = range(len(dt_idadevalortran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadevalortran['valor_transacoes_min'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadevalortran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Valor de Transações')
plt.title('Valores mínimo de Transações por faixa etária')

plt.show()

x_pos = range(len(dt_idadevalortran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadevalortran['valor_transacoes_max'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadevalortran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Valor de Transações')
plt.title('Valores máximos de Transações por faixa etária')

plt.show()

"""## 1.6 - Quantidade de Transações em 12 meses



"""

#Qtd de transações por idade
dt_idadeqtdtranmed = dt_idade_media[['faixa_etaria','qtd_transacoes_12m']]
dt_idadeqtdtranmed.head(10)

#qtd de transações minimas por idade
dt_idadeqtdtranmin = dt_idade_min[['faixa_etaria','qtd_transacoes_12m']]
dt_idadeqtdtranmin = dt_idadeqtdtranmin.rename(columns={'qtd_transacoes_12m': 'qtd_transacoes_min'})
dt_idadeqtdtranmin.head(5)

#qtd de transações maximas por idade
dt_idadeqtdtranmax = dt_idade_max[['faixa_etaria','qtd_transacoes_12m']]
dt_idadeqtdtranmax = dt_idadeqtdtranmax.rename(columns={'qtd_transacoes_12m': 'qtd_transacoes_max'})
dt_idadeqtdtranmax.head(5)

#juntando as 3 em 1 só
dt_idadeqtdtran = pd.merge(dt_idadeqtdtranmin, dt_idadeqtdtranmax, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeqtdtran = pd.merge(dt_idadeqtdtran,dt_idadeqtdtranmed, left_on='faixa_etaria', right_on='faixa_etaria')
dt_idadeqtdtran = dt_idadeqtdtran.rename(columns={'qtd_transacoes_12m': 'qtd_transacoes_medio'})
dt_idadeqtdtran = dt_idadeqtdtran.rename(columns={'qtd_transacoes_12m_min': 'qtd_transacoes_min'})
dt_idadeqtdtran = dt_idadeqtdtran[['faixa_etaria', 'qtd_transacoes_min', 'qtd_transacoes_medio', 'qtd_transacoes_max']]
dt_idadeqtdtran.head(5)

nova_ordemqtdtran = [1,2,3,0]
dt_idadeqtdtran= dt_idadeqtdtran.iloc[nova_ordemqtdtran]
dt_idadeqtdtran

x_pos = range(len(dt_idadeqtdtran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeqtdtran['qtd_transacoes_medio'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeqtdtran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Transações')
plt.title('Quantidade de transações por faixa etária')

plt.show()

x_pos = range(len(dt_idadeqtdtran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeqtdtran['qtd_transacoes_min'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeqtdtran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Transações')
plt.title('Quantidade mínimas de transações por faixa etária')

plt.show()

x_pos = range(len(dt_idadeqtdtran['faixa_etaria']))
bar_width = 0.5

plt.bar(x_pos, dt_idadeqtdtran['qtd_transacoes_max'], width=bar_width, align='center')

plt.xticks(x_pos, dt_idadeqtdtran['faixa_etaria'])

plt.xlabel('Faixa Etária')
plt.ylabel('Quantidade de Transações')
plt.title('Quantidade máximas de transações por faixa etária')

plt.show()

"""# 2- Limite do cartão concedido ao cliente é medido pela renda ou pela utilização e pagamento?



*   Renda (Salário Anual)
*   iterações_12m
*   Valor de transações






"""

dt_limite = dt['limite_cartao'].value_counts().rename_axis('limite_cartao').reset_index(name='counts')
dt_limite.head(5)

plt.hist(dt_limite['limite_cartao'], density=False, bins=30, color = 'Purple')
plt.ylabel('Count')
plt.xlabel('Limite do Cartão');

"""##  2.1 - Por Renda (Salário Anual)?



"""

dt_salarioanual = dt['salario_anual'].value_counts().rename_axis('salario_anual').reset_index(name='counts')
dt_salarioanual

dt_salariolimite_med = dt.groupby(['salario_anual'], as_index=False).mean()
dt_salariolimite_med = dt_salariolimite_med[['salario_anual', 'limite_cartao']]
dt_salariolimite_med

dt_salariolimite_min = dt.groupby(['salario_anual'], as_index=False).min()
dt_salariolimite_min = dt_salariolimite_min[['salario_anual', 'limite_cartao']]
dt_salariolimite_min

dt_salariolimite_max = dt.groupby(['salario_anual'], as_index=False).max()
dt_salariolimite_max = dt_salariolimite_max[['salario_anual', 'limite_cartao']]
dt_salariolimite_max

dt_salariolimite = pd.merge(dt_salariolimite_min, dt_salariolimite_max, left_on='salario_anual', right_on='salario_anual')
dt_salariolimite = pd.merge(dt_salariolimite, dt_salariolimite_med, left_on='salario_anual', right_on='salario_anual')
dt_salariolimite = dt_salariolimite.rename(columns={'limite_cartao_x': 'limite_minimo'})
dt_salariolimite = dt_salariolimite.rename(columns={'limite_cartao_y': 'limite_maximo'})
dt_salariolimite = dt_salariolimite.rename(columns={'limite_cartao': 'limite_medio'})
dt_salariolimite = dt_salariolimite[['salario_anual', 'limite_minimo', 'limite_medio', 'limite_maximo']]
dt_salariolimite

dt_salariolimite = dt_salariolimite.sort_values(by='salario_anual', ascending=False)
dt_salariolimite

dt_salariolimite.iloc[[3, 1]] = dt_salariolimite.iloc[[1, 3]]
dt_salariolimite

x = dt_salariolimite['salario_anual']
y1 = dt_salariolimite['limite_minimo']
y2 = dt_salariolimite['limite_medio']
y3 = dt_salariolimite['limite_maximo']


plt.plot(x, y1, color='red', label='Limite Mínimo')
plt.plot(x, y2, color='purple', label='Limite Médio')
plt.plot(x, y3, color='blue', label='Limite Máximo')


plt.legend()
plt.title('Limite oferecido de acordo com a faixa salarial anual do cliente')


plt.show()

"""##   2.2 - Por valor de transações?



"""

dt_limite = dt.groupby('limite_cartao', as_index=False).mean()
dt_limitevalortran = dt_limite[['limite_cartao', 'valor_transacoes']]
dt_limitevalortran

plt.scatter(dt_limitevalortran['valor_transacoes'], dt_limitevalortran['limite_cartao'])
plt.xlabel('Valor de Transações')
plt.ylabel('Limite do Cartão')
plt.title('Relação entre o valor das transações realizadas e o limite concedido')
plt.show()

"""## 2.3 - Por iterações?






"""

dt_limiteiterac = dt_limite[['limite_cartao', 'iteracoes_12m']]
dt_limiteiterac

plt.scatter(dt_limiteiterac['iteracoes_12m'], dt_limiteiterac['limite_cartao'])
plt.xlabel('Numero de iterações em 12 meses')
plt.ylabel('Limite do Cartão')
plt.title('Relação entre o número de iterações realizadas e o limite concedido')
plt.show()

"""## *R.2: Concluímos que, através dos gráficos gerados, o limite de crédito, definido pelo banco, varia baseado na renda do cliente (Salário Anual). Visto que os valores de transações e a quantidade de interações não variam de acordo com o limite. Ex.: Uma pessoa com aproximadamente R\$ 25k de limite de crédito utiliza a mesma quantidade de uma pessoa com aproximadamente R\$ 5k de limite.*

# 3 - Qual a probabilidade de um cliente possuir um limite de crédito igual ou superior a R\$ 25k, dado que ele possui uma formação em nível de "Mestrado".

## Cálculo

*   A = limite_cartao >= 25000
*   B = escolaridade == "Mestrado"

P(A|B) = P(B ∩ A) / P(B)
"""

dt_escolaridademedia = dt.groupby(['escolaridade'], as_index=False).mean()

x_pos = range(len(dt_escolaridademedia['escolaridade']))
bar_width = 0.5

plt.bar(x_pos, dt_escolaridademedia['limite_cartao'], width=bar_width, align='center')

plt.xticks(x_pos, dt_escolaridademedia['escolaridade'])

plt.xlabel('Grau de Escolaridade')
plt.ylabel('Limite do Cartão')
plt.title('Limite do Cartão por Grau de Escolaridade')

plt.show()

dt_mestrado = dt.loc[dt['escolaridade'] == 'mestrado']
dt_mestrado = dt_mestrado[['escolaridade', 'limite_cartao']]
dt_mestrado

probabnum = (dt_mestrado.loc[dt_mestrado['limite_cartao'] >= 25000.00])
probabnum.head(5)

len(probabnum)

probabdenom = len(dt_mestrado)

probab = len(probabnum) / (probabdenom)
probab

dt_limite_escolaridade = dt.query('limite_cartao>=25000.00')\
  .query('escolaridade=="mestrado"')

p_a_inter_b = len(dt_limite_escolaridade)/len(dt)

print(f' A probabilidade de B ∩ A é: {round((len(dt_limite_escolaridade)/len(dt))*100, 2)} %')

dt_escolaridade_mestrado = dt.query('escolaridade=="mestrado"')

p_b = len(dt_escolaridade_mestrado)/len(dt)

print(f' A probabilidade de B é: {round((len(dt_escolaridade_mestrado)/len(dt))*100, 2)} %')

print(f'A probabilidade de um cliente possuir um limite de crédito igual ou superior a R\$ 25k, dado que ele possui uma formação em nível de "Mestrado" é de {round((p_a_inter_b/p_b) * 100, 2)} %')

"""## R.3: Concluímos que a probabilidade de um cliente possuir um limite de crédito igual ou superior a R\$ 25k, dado que ele possui uma formação em nível de "Mestrado" é de aproximadamente 7.66 %.

# Público Alvo

## Definindo o público alvo:

Clientes que atendem as seguintes características:
*   Estado civil solteira ou casada
*   No mínimo 2 dependentes
"""

new_pop = dt\
      .query('(estado_civil=="solteiro") | (estado_civil=="casado")')\
      .query('(dependentes>=2)')

new_pop

# Analisando estatísticas
new_pop.describe(percentiles=[.25, .5, .75,0.9,0.95,.99])

"""# Amostragem"""

# Retirando uma amostra
amostra = new_pop.sample(n=300, random_state = 2018)

# Analisando estatísticas
amostra.describe(percentiles=[.25, .5, .75,0.9,0.95,.99])

"""# Análise Limite de Crédito"""

amostra.limite_cartao.describe()

amostra.limite_cartao.hist(bins=30)

# Calculando a média e o erro padrão da média
media_amostral = amostra.limite_cartao.mean()
erro_padrao_media = amostra.limite_cartao.sem()
media_amostral, erro_padrao_media

# carregando norm da biblioteca scipy
from scipy.stats import norm

# Dado que o grau de confiança é 95%, sobra 5% nas caudas, 2,5% para cada lado
z = norm(loc=0,scale=1).ppf(0.975).round(2)

# Calculo do intervalo de confiança 95% do valor do limite do cartão
lim_inf_ic = media_amostral - z*erro_padrao_media
lim_sup_ic = media_amostral + z*erro_padrao_media

print(f'Espero, com 95% de confiança que o valor médio do limite de credito desses clientes é um valor entre R$ {lim_inf_ic:.2f} e R$ {lim_sup_ic:.2f}')

"""# 4 - Teste de Hipótese

## Análise do limite do cartão estratificado pelo estado civil do cliente ser solteiro ou casado

Queremos testar se o valor de transações difere em decorrência do estado civil do cliente.

*   H0: As amostras tem distribuições iguais
*   H1: As amostras tem distribuições diferentes
"""

amostra.loc[amostra['estado_civil'] == 'solteiro', 'estado_civil'] = 0
amostra.loc[amostra['estado_civil'] == 'casado', 'estado_civil'] = 1
amostra.loc[amostra['estado_civil'] == 'divorciado', 'estado_civil'] = 2
amostra['estado_civil'] = pd.to_numeric(amostra['estado_civil'])

# Calculo do intervalo de confiança 95% do valor do limite do cartao
# Considerando que o cliente possui um estado de Solteiro ('estado_civil=="solteiro"')
z = norm(loc=0,scale=1).ppf(0.975).round(2)

media_2 = amostra.query('estado_civil==0').limite_cartao.mean()
erro_padrao_2 = amostra.query('estado_civil==0').limite_cartao.sem()

lim_inf_2 = (media_2 - z*erro_padrao_2).round(2)
lim_sup_2 = (media_2 + z*erro_padrao_2).round(2)

print('solteiro', [lim_inf_2,lim_sup_2])

# Considerando que o cliente possui um estado de Casado ('estado_civil=="casado"')

media_1 = amostra.query('estado_civil==1').limite_cartao.mean()
erro_padrao_1 = amostra.query('estado_civil==1').limite_cartao.sem()

lim_inf_1 = (media_1 - z*erro_padrao_1).round(2)
lim_sup_1 = (media_1 + z*erro_padrao_1).round(2)

print('casado', [lim_inf_1,lim_sup_1])

"""Como há interseção entre os intervalos, espera-se com 95% de confiança que os valores médios dos limites de crédito não diferem entre os clientes solteiros e os casados.

## Verificando se os dados possui uma distribuição semelhante a uma distribuição Normal (estado civil)

Utilizaremos o Teste Shapiro-Wilk para avaliar se o limite de crédito da nossa amostra segue ou não uma distribuição normal. Para dizer que uma distribuição é normal, o valor p precisa ser maior do que **0,05**.
"""

import scipy.stats as stats

p_value_shapiro = stats.shapiro(amostra.limite_cartao)[1]

print(f'P Valor: {p_value_shapiro}')
if (p_value_shapiro > 0.05):
  print('O teste de Shapiro-Wilk mostra evidências que esta amostra segue distribuição normal.')
else:
  print('O teste de Shapiro-Wilk mostra evidências que esta amostra não segue distribuição normal.')

amostra.limite_cartao.hist(bins=30)

"""## Testando se as variâncias são homogeneas (estado civil)

Pelo fato dos dados da amostra estarem bem distantes de uma distribuição normal, como vimos no tópico anterior. Utilizaremos o Teste de Levene para verificar se as variâncias de diferentes amostras são semelhantes. Se o p-valor retornado pelo teste de Levene é menor que o nível de significância 0.05, isso significa que há evidências suficientes para rejeitar a hipótese de que as variâncias são semelhantes.

*   H0: As amostras são de populações com variâncias iguais
*   Nível de significância de 5%
"""

# Calculando as estatísticas descritivas
amostra[['estado_civil','limite_cartao']].groupby('estado_civil').describe()

p_value_levene = stats.levene(
    amostra.loc[amostra['estado_civil'] == 0].limite_cartao,
    amostra.loc[amostra['estado_civil'] == 1].limite_cartao
)[1]

print(f'P Valor: {p_value_levene}')

if (p_value_levene < 0.05):
  print('O teste de Levene mostra evidências que as amostras não possuem variâncias semelhantes.')
else:
  print('O teste de Levene mostra evidências que as amostras possuem variâncias semelhantes.')

"""## Testando se as médias são iguais (estado civil)

Como as amostras possuem variâncias semelhantes, para testar a diferença entre as médias aritméticas das amostras vamos utilizar o teste t para as amostras independentes. Caso, as variâncias fossem heterogêneas iríamos utilizar o teste t-Welch, adicionando o parâmetro *equal_var = False* na função stats.ttest_ind

 Se o valor de p retornado do teste T for menor do que 0.05 indica que a nossa amostra improvável de ter ocorrido. Portanto rejeitamos a hipótese nula de médias iguais.

 $H_0: \mu_0  = \mu_1$

 $H_1: \mu_0  \neq \mu_1$
"""

from scipy.stats import ttest_ind

p_value_t = stats.ttest_ind(
    amostra.loc[amostra['estado_civil'] == 0].limite_cartao,
    amostra.loc[amostra['estado_civil'] == 1].limite_cartao
)[1]

print(f'P Valor: {p_value_t}')

if (p_value_t > 0.05):
  print('O teste de T mostra evidências que as amostras possuem médias iguais.')
else:
  print('O teste de T mostra evidências que as amostras não possuem médias iguais.')

"""# 5 - Correlação de Variações"""

amostra

"""O coeficiente de correlação de Pearson mede a relação linear entre dois conjuntos de dados. Esta correlação pode varia de -1 à +1. As correlações positivas implicam que, à medida que x aumenta, y também aumenta. Já as negativas implicam que, à medida que X aumenta, Y diminui.

Interpretação do coeficiente de correlação produto-momento retornado pela função pearsonr():

* 0.9 para mais ou para menos indica uma correlação muito forte.
* 0.7 a 0.9 positivo ou negativo indica uma correlação forte.
* 0.5 a 0.7 positivo ou negativo indica uma correlação moderada.
* 0.3 a 0.5 positivo ou negativo indica uma correlação fraca.
* 0 a 0.3 positivo ou negativo indica uma correlação desprezível.

Ref.: [Definição coeficiente de correlação de Pearson](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html#)

Ref.: [Interpretação de Coeficiente](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3576830/table/T1/?report=objectonly)
"""

from scipy.stats import pearsonr
corr = pearsonr(amostra.valor_transacoes, amostra.limite_cartao)
corr

"""A estatística de -0.0640552005981735 indica uma correlação fraca e próxima de zero entre as variáveis analisadas. O valor p de 0.2687381661323436 sugere que não há evidências estatisticamente significativas para rejeitar a hipótese nula de que não há correlação entre as variáveis. Isso significa que, com base nos dados disponíveis, não podemos afirmar que há uma relação linear significativa entre as variáveis.

# 6 - Regressão Linear
"""

amostra

amostra.valor_transacoes.hist()

amostra.limite_cartao.hist()

# Normalizacao Logaritmica dos valores dos limites de credito
amostra['limite_cartao_transf']= np.log(amostra['limite_cartao'])

amostra['limite_cartao_transf'].hist()

import statsmodels.api as sm

y = amostra['limite_cartao_transf']
x = amostra[['dependentes', 'qtd_produtos', 'valor_transacoes']]

modelo = sm.OLS(y,x)
resultado = modelo.fit()
print(resultado.summary())