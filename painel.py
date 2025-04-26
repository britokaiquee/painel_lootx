import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Título do painel
st.title("Painel de Gestão Financeira - LootX Store")

# Caminho do arquivo CSV
caminho_arquivo = "dados_financeiros.csv"


# Função para carregar os dados
def carregar_dados():
    if os.path.exists(caminho_arquivo):
        return pd.read_csv(caminho_arquivo)
    else:
        return pd.DataFrame(
            columns=['Categoria', 'Produto', 'Tipo', 'Valor (R$)']
            )


dados = carregar_dados()

# Formulário para adicionar dados
with st.form("formulario_adicionar"):
    categoria = st.selectbox(
        'Categoria', ['League of Legends',
                      'Valorant', 'Vanguard', 'HWID Spoofer'])
    produto = st.text_input('Produto')
    tipo = st.selectbox('Tipo', ['Entrada', 'Saída'])
    valor = st.number_input('Valor (R$)', min_value=0.0, format="%.2f")
    enviar = st.form_submit_button('Adicionar')

    if enviar:
        nova_linha = {'Categoria': categoria, 'Produto': produto,
                      'Tipo': tipo, 'Valor (R$)': valor}
        dados = pd.concat(
            [dados, pd.DataFrame([nova_linha])], ignore_index=True)

        # Salvar os dados no CSV
        dados.to_csv(caminho_arquivo, index=False)

        st.success('Item adicionado!')

# Exibir tabela
st.subheader("Movimentações")
dados_com_indice = dados.copy()
dados_com_indice.index = dados_com_indice.index + 1
st.dataframe(dados_com_indice)

# Cálculos financeiros
entrada = dados[dados['Tipo'] == 'Entrada']['Valor (R$)'].sum()
saida = dados[dados['Tipo'] == 'Saída']['Valor (R$)'].sum()
lucro = entrada - saida

st.metric("Total de Entradas", f"R$ {entrada:.2f}")
st.metric("Total de Saídas", f"R$ {saida:.2f}")
st.metric("Lucro Atual", f"R$ {lucro:.2f}")

# Gráfico
if not dados.empty:
    # Definir as cores para 'Entrada' e 'Saída'
    color_map = {
        'Entrada': 'lime',   # Cor para Entradas
        'Saída': 'red'       # Cor para Saídas
    }
    
    fig = px.bar(dados, x="Produto", y="Valor (R$)", color="Tipo",
                 barmode="group", title="Movimentação Financeira", 
                 color_discrete_map=color_map)
    
    st.plotly_chart(fig)