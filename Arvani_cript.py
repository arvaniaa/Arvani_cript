import streamlit as st
import random

# --- CONFIGURAÇÕES DA PÁGINA ---
st.set_page_config(
    page_title="Sphinx",
    page_icon="🔐",
    layout="wide"
)

# --- LÓGICA DA CRIPTOGRAFIA (SISTEMA 12 LETRAS) ---
VOGAIS = "aeiou"
CONSOANTES = "bcdfghjklmnpqrstvwxyz"
ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def gerar_bloco_cvvccv():
    """Gera o bloco básico de 6 letras: Consoante-Vogal-Vogal-Consoante-Consoante-Vogal"""
    return (random.choice(CONSOANTES) + random.choice(VOGAIS) + random.choice(VOGAIS) +
            random.choice(CONSOANTES) + random.choice(CONSOANTES) + random.choice(VOGAIS))

@st.cache_data
def get_mapa_cripto(seed=100):
    """Gera o dicionário de tradução fixo baseado em uma semente"""
    random.seed(seed)
    mapa = {}
    usados = set()
    for letra in ALFABETO:
        while True:
            # Padrão solicitado: C-V-V-C-C-V + C-V-V-C-C-V (12 letras)
            codigo = gerar_bloco_cvvccv() + gerar_bloco_cvvccv()
            if codigo not in usados:
                mapa[letra] = codigo
                usados.add(codigo)
                break
    return mapa

MAPA_LETRAS = get_mapa_cripto()
MAPA_REVERSO = {v: k for k, v in MAPA_LETRAS.items()}

def codificar(texto):
    resultado = []
    for char in texto.upper():
        if char in MAPA_LETRAS:
            resultado.append(MAPA_LETRAS[char])
        elif char == " ":
            resultado.append("[ESPACO]")
        else:
            resultado.append(char)
    return "-".join(resultado)

def decodificar(codigo_bruto):
    resultado = []
    # Divide pelos hífens para identificar cada letra de 12 caracteres
    blocos = codigo_bruto.split("-")
    for bloco in blocos:
        bloco = bloco.strip()
        if bloco in MAPA_REVERSO:
            resultado.append(MAPA_REVERSO[bloco])
        elif bloco == "[ESPACO]":
            resultado.append(" ")
        else:
            resultado.append(bloco)
    return "".join(resultado)

# --- INTERFACE STREAMLIT ---
st.title("🔐 Sphinx Poop Company")
st.write("Converta textos em códigos silábicos de 12 letras baseados no padrão **C-V-V-C-C-V-C-V-V-C-C-V**.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("📥 Codificar")
    texto_para_codificar = st.text_area("Texto original:", placeholder="Digite sua mensagem...", key="input_orig")
    
    if st.button("Gerar Código", type="primary"):
        if texto_para_codificar:
            resultado_cod = codificar(texto_para_codificar)
            st.subheader("Código Gerado:")
            st.code(resultado_cod, language="text")
        else:
            st.warning("Escreva algo para codificar.")

with col2:
    st.header("📤 Decodificar")
    codigo_para_decodificar = st.text_area("Código secreto:", placeholder="Cole os blocos com hífens aqui...", key="input_cipher")
    
    if st.button("Traduzir para Texto"):
        if codigo_para_decodificar:
            resultado_dec = decodificar(codigo_para_decodificar)
            st.subheader("Mensagem Revelada:")
            st.success(resultado_dec)
        else:
            st.warning("Cole um código para traduzir.")

st.divider()

# Visualização da Tabela de Tradução
with st.expander("🔍 Ver Tabela de Equivalência do Alfabeto"):
    st.write("Esta é a relação atual entre letras e códigos de 12 caracteres:")
    cols_tabela = st.columns(4)
    letras = list(MAPA_LETRAS.items())
    
    for i, (l, c) in enumerate(letras):
        target_col = i % 4
        with cols_tabela[target_col]:
            st.write(f"**{l}** : `{c}`")

# Rodapé simples
st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 0.8em; margin-top: 50px;">
        <hr>
        Poop Company | Desenvolvido por Luis Henrique Arvani
    </div>
    """,
    unsafe_allow_html=True
)

