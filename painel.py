import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time


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


# Definindo os preços e variações dos produtos
produtos_variacoes = {
    "ES SCRIPT": {
        "8 HORAS": 13.70,
        "1 DIA": 16.90,
        "7 DIAS": 86.90,
        "30 DIAS": 186.90
    },
    "HANBOT SCRIPT": {
        "1 DIA": 8.90,
        "30 DIAS": 196.70
    },
    "NV BYPASS": {
        "1 DIA": 16.90
    },
    "LS SCRIPT": {
        "1 DIA": 26.70,
        "7 DIAS": 153.90,
        "30 DIAS": 516.70
    },
    "SMURFS/NFA (BR)": {
        "HANDLEVEL": 19.70,
        "NFA 100+": 8.59,
        "NFA 60+": 3.57
    },
    "RTX SCRIPT": {
        "1 DIA": 16.90,
        "7 DIAS": 76.90,
        "30 DIAS": 119.90
    },
    "BLCG/NS CLUB": {
        "7 DIAS": 250.00,
        "30 DIAS": 700.00
    },
    "SVGC Skeet - Valorant VIP Menu": {
        "1 DIA": 34.90,
        "7 DIAS": 146.90,
        "30 DIAS": 386.90,
        "365 DIAS": 896.90
    },
    "Fecurity Menu": {
        "1 DIA": 18.90,
        "7 DIAS": 54.90,
        "30 DIAS": 96.90
    },
    "SafestCheats - Valorant Menu": {
        "3 DIAS": 65.00,
        "7 DIAS": 150.00,
        "30 DIAS": 350.00
    },
    "SVGC Skeet - Vanguard Bypass": {
        "7 DIAS": 44.90,
        "30 DIAS": 119.90,
        "LIFETIME": 374.90
    },
    "The Nexus - Perm Woofer": {
        "30 DIAS": 86.90
    },
    "SafestCheats - Perm Spoofer": {
        "One Time Unban": 96.40
    }
}


# Selecionar categoria e produto
categoria = st.radio(
    'Categoria', ['League of Legends', 'Valorant', 'Call of Duty',
                  'Vanguard Bypass', 'HWID Spoofer']
)

match categoria:
    case "League of Legends":
        produto = st.radio(
            'Produto', ['ES SCRIPT', 'HANBOT SCRIPT', 'NV BYPASS', 'LS SCRIPT',
                        'SMURFS/NFA (BR)', 'RTX SCRIPT', 'BLCG/NS CLUB']
        )
    case "Valorant":
        produto = st.radio(
            'Produto', ['SVGC Skeet - Valorant VIP Menu',
                        'SafestCheats - Valorant Menu',]
        )
    case "Call of Duty":
        produto = st.radio('Produto', ['Fecurity Menu'])
    case "Vanguard Bypass":
        produto = st.radio('Produto', ['SVGC Skeet - Vanguard Bypass'])
    case "HWID Spoofer":
        produto = st.radio('Produto', ['The Nexus - Perm Woofer',
                                       'SafestCheats - Perm Spoofer'])


# Selecionar tipo
tipo = st.radio('Tipo', ['Entrada', 'Saída'])

if tipo == 'Entrada':
    itens_vendidos = st.number_input('Itens vendidos',
                                     min_value=0, step=1, format="%d")
    
    # Pega as variações disponíveis para o produto
    variacoes_disponiveis = list(produtos_variacoes[produto].keys())
    
    # Deixa o usuário escolher uma variação
    variacao = st.radio('Variação', variacoes_disponiveis)
    
    # Pega o preço da variação e calcula
    valor_unitario = produtos_variacoes[produto][variacao]
    valor = itens_vendidos * valor_unitario

elif tipo == 'Saída':
    valor = st.number_input('Valor (R$)', min_value=0.0, format="%.2f")


# Inicializar estados
if "fase" not in st.session_state:
    st.session_state["fase"] = "normal"  # normal, adicionando, sucesso

# Define se o botão está habilitado ou não
botao_habilitado = st.session_state["fase"] == "normal"

# Formulário para adicionar dados
with st.form("formulario_adicionar"):
    enviar = st.form_submit_button('Adicionar', disabled=not botao_habilitado)

    if enviar:
        if tipo == 'Entrada':
            nova_linha = {
                'Categoria': categoria, 'Produto': produto, 'Tipo': tipo,
                'Itens vendidos': itens_vendidos, 'Valor (R$)': valor
            }
        elif tipo == 'Saída':
            nova_linha = {
                'Categoria': categoria, 'Produto': produto, 'Tipo': tipo,
                'Valor (R$)': valor
            }

        dados = pd.concat(
            [dados, pd.DataFrame([nova_linha])], ignore_index=True)

        dados.to_csv(caminho_arquivo, index=False)

        st.session_state["fase"] = "sucesso"
        st.rerun()

# Mostrar mensagem
if st.session_state["fase"] == "sucesso":
    st.success('Movimentação adicionada com sucesso!')
    time.sleep(0.5)  # Esperar meio segundo
    st.session_state["fase"] = "normal"
    st.rerun()


# Exibir a tabela
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
st.metric("Saldo", f"R$ {lucro:.2f}")


# Gráfico
if not dados.empty:
    # Definir as cores para 'Entrada' e 'Saída'
    color_map = {
        'Entrada': 'lime',   # Cor para Entradas
        'Saída': 'red'       # Cor para Saídas
    }

    fig = px.bar(
        dados, x="Produto", y="Valor (R$)", color="Tipo",
        barmode="group", title="Movimentação Financeira",
        color_discrete_map=color_map
    )

    st.plotly_chart(fig)
