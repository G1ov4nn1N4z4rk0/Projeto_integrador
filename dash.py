import numpy as np
import streamlit as st
import pandas as pd
import plotly.express as px
from query import *

# Consulta no banco de dados
query = "SELECT * FROM tb_registro"

# Carregar os dados do MySQL
df = conexao(query)

# Botão para atualização dos dados
if st.button("Atualizar dados"):
    df = conexao(query)

# Menu lateral
st.sidebar.header("Selecione a informação para gerar o gráfico")

# Seleção de colunas X e Y
colunaX = st.sidebar.selectbox(
    "Eixo X",
    options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
    index=0
)

colunaY = st.sidebar.selectbox(
    "Eixo Y",
    options=["umidade", "temperatura", "pressao", "altitude", "co2", "poeira"],
    index=1
)

# Função para verificar se um atributo está nos eixos selecionados
def filtros(atributo):
    return atributo in [colunaX, colunaY]

# Filtro de range (slider) para atributos
st.sidebar.header("Selecione o filtro")

# Temperatura
if filtros("temperatura"):
    temperatura_range = st.sidebar.slider(
        "Temperatura (°C)",
        min_value=float(df["temperatura"].min()),
        max_value=float(df["temperatura"].max()),
        value=(float(df["temperatura"].min()), float(df["temperatura"].max())),
        step=0.1
    )

# Umidade
if filtros("umidade"):
    umidade_range = st.sidebar.slider(
        "Umidade",
        min_value=float(df["umidade"].min()),
        max_value=float(df["umidade"].max()),
        value=(float(df["umidade"].min()), float(df["umidade"].max())),
        step=0.1
    )

# Altitude
if filtros("altitude"):
    altitude_range = st.sidebar.slider(
        "Altitude",
        min_value=float(df["altitude"].min()),
        max_value=float(df["altitude"].max()),
        value=(float(df["altitude"].min()), float(df["altitude"].max())),
        step=0.1
    )

# Pressão
if filtros("pressao"):
    pressao_range = st.sidebar.slider(
        "Pressão",
        min_value=float(df["pressao"].min()),
        max_value=float(df["pressao"].max()),
        value=(float(df["pressao"].min()), float(df["pressao"].max())),
        step=0.1
    )

# CO2
if filtros("co2"):
    co2_range = st.sidebar.slider(
        "CO2",
        min_value=float(df["co2"].min()),
        max_value=float(df["co2"].max()),
        value=(float(df["co2"].min()), float(df["co2"].max())),
        step=0.1
    )

# Poeira
if filtros("poeira"):
    poeira_range = st.sidebar.slider(
        "Poeira",
        min_value=float(df["poeira"].min()),
        max_value=float(df["poeira"].max()),
        value=(float(df["poeira"].min()), float(df["poeira"].max())),
        step=0.1
    )

# Aplicação dos filtros
df_selecionado = df.copy()
if filtros("temperatura"):
    df_selecionado = df_selecionado[
        (df_selecionado["temperatura"] >= temperatura_range[0]) &
        (df_selecionado["temperatura"] <= temperatura_range[1])
    ]
if filtros("umidade"):
    df_selecionado = df_selecionado[
        (df_selecionado["umidade"] >= umidade_range[0]) &
        (df_selecionado["umidade"] <= umidade_range[1])
    ]
if filtros("altitude"):
    df_selecionado = df_selecionado[
        (df_selecionado["altitude"] >= altitude_range[0]) &
        (df_selecionado["altitude"] <= altitude_range[1])
    ]
if filtros("pressao"):
    df_selecionado = df_selecionado[
        (df_selecionado["pressao"] >= pressao_range[0]) &
        (df_selecionado["pressao"] <= pressao_range[1])
    ]
if filtros("co2"):
    df_selecionado = df_selecionado[
        (df_selecionado["co2"] >= co2_range[0]) &
        (df_selecionado["co2"] <= co2_range[1])
    ]
if filtros("poeira"):
    df_selecionado = df_selecionado[
        (df_selecionado["poeira"] >= poeira_range[0]) &
        (df_selecionado["poeira"] <= poeira_range[1])
    ]

# Função para exibir informações
def Home():
    with st.expander("Tabela"):
        mostrarDados = st.multiselect(
            "Filtros:",
            df_selecionado.columns,
            default=[],
            key="showData_home"
        )
        if mostrarDados:
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        media_umidade = df_selecionado['umidade'].mean()
        media_temperatura = df_selecionado['temperatura'].mean()
        media_co2 = df_selecionado['co2'].mean()

        media1, media2, media3 = st.columns(3, gap='large')
        with media1:
            st.info('Média de Registros de Umidade')
            st.metric(label='Média', value=f'{media_umidade:.2f}')
        with media2:
            st.info('Média de Registros de Temperatura')
            st.metric(label='Média', value=f'{media_temperatura:.2f}')
        with media3:
            st.info('Média de Registros de CO2')
            st.metric(label='Média', value=f'{media_co2:.2f}')
        st.markdown("""-------------------""")

# Função para exibir gráficos
def graficos():
    st.title('Dashboard de Monitoramento')
    
    aba1, aba2 = st.tabs(['Gráfico de Linha', 'Gráfico de Dispersão'])

    # Gráfico de Linha
    with aba1:
        if df_selecionado.empty:
            st.write('Nenhum dado está disponível para gerar o gráfico')
        elif colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
        else:
            try:
                grupo_dados1 = df_selecionado.groupby(by=[colunaX]).size().reset_index(name="contagem")

                fig_valores = px.bar(
                    grupo_dados1,
                    x=colunaX,
                    y="contagem",
                    orientation="h",
                    title=f"Contagem de Registros por {colunaX.capitalize()}",
                    color_discrete_sequence=["#0083b8"],
                    template="plotly_white"
                )
                st.plotly_chart(fig_valores, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erro ao criar o gráfico de barras: {e}")

    # Gráfico de Dispersão
    with aba2:
        if df_selecionado.empty:
            st.write('Nenhum dado está disponível para gerar o gráfico de dispersão')
        elif colunaX == colunaY:
            st.warning('Selecione uma opção diferente para os eixos X e Y')
        else:
            try:
                fig_disp = px.scatter(
                    df_selecionado,
                    x=colunaX,
                    y=colunaY,
                    title=f"Gráfico de Dispersão: {colunaX.capitalize()} vs {colunaY.capitalize()}",
                    color_discrete_sequence=["#ff6600"],  # Cor do gráfico
                    template="plotly_white"
                )
                st.plotly_chart(fig_disp, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erro ao criar o gráfico de dispersão: {e}")

Home()
graficos()