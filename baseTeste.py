import pandas as pd
import streamlit as st
import plotly.express as px

# Configuração da página
st.set_page_config(page_title='Painel Logístico', layout='wide')

# Função para carregar os dados
def carregar_dados():
    entrega = st.file_uploader("Por favor, colocar sua tabela de dados aqui:", type=['xlsx'])
    if entrega is None:
        return None
    return pd.read_excel(entrega, sheet_name="Entregas")

# Carregar os dados
dataframe = carregar_dados()

if dataframe is not None:
    # Exibindo as primeiras linhas do dataframe
    st.write("Visualizando os dados:", dataframe.head())

    # Filtros
    filtro1, filtro2 = st.columns(2)
    Produto = dataframe['Produto'].unique()
    Veiculos = dataframe['Veiculo'].unique()
    
    with filtro1:
        produto_selecionado = st.selectbox('Filtrar por categoria de produto', Produto)

    with filtro2:
        veiculo_selecionado = st.selectbox('Filtrar por veículo', Veiculos)


    # filtro por todos
    Produto = ['Todos'] + list(Produto)
    Veiculos = ['Todos'] + list(Veiculos)

    if produto_selecionado != 'Todos':
        df_filtrado = dataframe[dataframe['Produto'] == produto_selecionado]
    else:
        if veiculo_selecionado != 'Todos':
            df_filtrado = dataframe[dataframe['Veiculo'] == veiculo_selecionado]
        else:
            df_filtrado = dataframe 
        df_filtrado = dataframe[(dataframe['Produto'] == produto_selecionado) & (dataframe['Veiculo'] == veiculo_selecionado)]

        # Métricas principais
        total_entregas = len(df_filtrado)
        soma_fretes = df_filtrado['Valor_Frete'].sum()

        # Exibindo as métricas principais
        st.subheader("Métricas Principais")
        st.metric("Total de entregas", total_entregas)
        st.metric(f"Soma do valor dos fretes R$", f"{soma_fretes:,.2f}")

        # Gráfico de Barras: Quantidade de entregas por estado
        entregas_estado = df_filtrado['Estado_Entrega'].value_counts().reset_index()
        entregas_estado.columns = ['Estado_Entrega', 'Quantidade de Entregas']
        fig = px.bar(
        entregas_estado,
        x='Estado_Entrega',
        y='Quantidade de Entregas',
        title="Quantidade de Entregas por Estado",
        color_discrete_sequence=["#F81904"])
        
        st.plotly_chart(fig)

        # Tabela de dados filtrados
        st.subheader("Tabela de Dados Filtrados")
        st.dataframe(df_filtrado)

else:
    st.write("Por favor, carregue a planilha para continuar.")