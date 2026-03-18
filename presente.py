import streamlit as st
import datetime
import google.generativeai as genai
import streamlit.components.v1 as components
from PIL import Image # Nova biblioteca para carregar a imagem

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Pri Vale • Studio", layout="wide", initial_sidebar_state="expanded")

# --- CSS CUSTOMIZADO PARA UM VISUAL PREMIUM ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #fcfcfc;
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }
    
    .app-title {
        font-size: 38px;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .app-subtitle {
        font-size: 16px;
        font-weight: 500;
        color: #c9a9a6;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }
    .app-tags {
        font-size: 13px;
        color: #95a5a6;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 400;
    }
    
    .result-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #eaeaea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        color: #34495e;
        line-height: 1.6;
    }
    
    /* Estilo exclusivo para a tela de Boas-Vindas */
    .splash-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 40px;
        background-color: #ffffff; /* Fundo branco para destacar a foto */
        border-radius: 20px;
        border: 1px solid #f0eaec;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        margin-top: 5vh;
        margin-bottom: 30px;
        max-width: 850px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# 2. CHAVE DA API E CONFIGURAÇÕES INICIAIS
# COLE SUA CHAVE DA API REAL AQUI:
api_key = st.secrets["GEMINI_KEY"]
data_aniversario = datetime.date(2026, 3, 23)
hoje = datetime.date.today()

if 'tela_abertura_ok' not in st.session_state:
    st.session_state.tela_abertura_ok = False

@st.cache_data(ttl=86400)
def gerar_reflexao_biblica(chave_api):
    try:
        genai.configure(api_key=chave_api)
        modelo_valido = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                modelo_valido = m.name
                break
        modelo = genai.GenerativeModel(modelo_valido)
        prompt = """
        Gere uma reflexão bíblica muito curta (apenas 1 parágrafo) e inclua um versículo inspirador para encorajar a nutricionista materno-infantil Priscila Vale no início do seu dia de trabalho. tom acolhedor.
        """
        return modelo.generate_content(prompt).text
    except Exception:
        return "**O Senhor te abençoe e te guarde.** (Números 6:24)\n\nBom dia, Pri! Que Deus encha o seu coração de sabedoria hoje."


# 3. TELA DE ABERTURA COM FOTO DE FAMÍLIA (ANIVERSÁRIO)
if not st.session_state.tela_abertura_ok:
    
    st.markdown("<div class='splash-container'>", unsafe_allow_html=True)
    
    if hoje <= data_aniversario:
        # --- NOVO: ADICIONANDO A FOTO DE FAMÍLIA ---
        # Tenta carregar a imagem 'familia.jpg' que deve estar na mesma pasta
        try:
            foto_familia = Image.open("familia.jpg")
            # Exibe a foto centralizada, com largura ajustada automaticamente (ex: 600px)
            st.image(foto_familia, width=600, caption="Família Vale • Um presente de amor")
        except FileNotFoundError:
            st.error("⚠️ Fernando, não encontrei o arquivo 'familia.jpg'. Salve a foto na mesma pasta do código!")
        
        # Título e Mensagem de Aniversário
        st.markdown("<h1 style='color: #c9a9a6; font-family: Georgia, serif; font-size: 34px; margin-top: 25px;'>Feliz Aniversário, Meu Amor!</h1>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size: 19px; font-style: italic; color: #555; margin-top: 15px; max-width: 800px; line-height: 1.8;'>
            "Você é a luz que ilumina nossa caminhada. Desejo-lhe muita saúde, prosperidade e sucesso. 
            Que a imagem e a semelhança de Deus resplandeçam sobre sua vida; você é filha do Altíssimo, e todas as coisas cooperam para o bem daqueles que O amam. 
            Admiro sua força, dedicação e amor, tanto no lar quanto na sua jornada profissional. Você nos guia e nos inspira. 
            Parabéns por ser essa pessoa linda e maravilhosa. Te amo demais!"
            <br><br><b>— Fernando</b>
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("<h1 style='color: #2c3e50; font-family: Georgia, serif; font-size: 32px;'>Bom dia, meu amor! 🕊️</h1>", unsafe_allow_html=True)
        reflexao = gerar_reflexao_biblica(api_key)
        st.markdown(f"<div style='font-size: 18px; color: #555; margin-top: 20px; max-width: 800px; line-height: 1.8;'>{reflexao}</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("Ir para o App (Pular) ➔", use_container_width=True):
            st.session_state.tela_abertura_ok = True
            st.rerun()

    components.html(
        """
        <script>
        setTimeout(function() {
            var buttons = window.parent.document.querySelectorAll('button');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].innerText === 'Ir para o App (Pular) ➔') {
                    buttons[i].click();
                    break;
                }
            }
        }, 30000);
        </script>
        """,
        height=0
    )
    st.stop()


# 4. INTERFACE PRINCIPAL (CONTENT STUDIO)
# [O resto do código do Content Studio permanece o mesmo]
with st.sidebar:
    st.markdown("<h2 style='color: #2c3e50; text-align: center;'>Studio Settings</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #7f8c8d; font-size: 14px;'>Painel de Controle</p>", unsafe_allow_html=True)
    st.divider()
    st.markdown("🔒 *Logado como: Priscila Vale*")

st.markdown("<div class='app-title'>Pri Vale • Content Studio</div>", unsafe_allow_html=True)
st.markdown("<div class='app-subtitle'>Inteligência em Nutrição Materno-Infantil</div>", unsafe_allow_html=True)
st.markdown("<div class='app-tags'>Mãe do Bernardo • Esposa do Fernando • Nutrição com Afeto</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📝 Briefing do Conteúdo")
    tema = st.text_area("Qual a dor ou dúvida da mãe que vamos resolver hoje?", placeholder="Ex: Meu bebê de 1 ano joga a comida no chão...")
    formato = st.selectbox("Formato de Entrega", ["Carrossel Estratégico (Instagram)", "Roteiro de Reels/TikTok", "Post Único (Foto)"])

with col2:
    st.markdown("#### 🎯 Direcionamento")
    publico = st.selectbox("Público-Alvo", ["Mães na Introdução Alimentar", "Mães lidando com Seletividade", "Gestantes", "Tentantes"])
    tom = st.selectbox("Tom de Voz", ["Acolhedor e Empático (Mãe para Mãe)", "Técnico e Científico (Autoridade)", "Divertido e Descontraído", "Direto e Motivacional"])

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Gerar Planejamento Estratégico", type="primary", use_container_width=True):
    if api_key == "COLE_SUA_CHAVE_AQUI":
        st.error("⚠️ Fernando, cole a sua chave da API na linha 58 do código!")
    elif not tema:
        st.warning("⚠️ Pri, digite o tema central do post para iniciarmos a análise.")
    else:
        with st.spinner("Processando dados e desenhando estratégia..."):
            try:
                genai.configure(api_key=api_key)
                
                modelo_valido = None
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        modelo_valido = m.name
                        break
                
                if not modelo_valido:
                    st.error("Erro de comunicação. Verifique a chave API.")
                    st.stop()
                    
                modelo = genai.GenerativeModel(modelo_valido)
                
                prompt = f"""
                Você é o assistente pessoal de marketing e copywriter sênior trabalhando exclusivamente para a Dra. Priscila Vale.
                
                PERFIL DA PRISCILA:
                Nutricionista Materno-Infantil de excelência. Mãe do Bernardo (pouco mais de 1 ano) e esposa do Fernando. 
                Ela vive a maternidade real, entende o cansaço materno e NUNCA julga as mães. Sua comunicação une acolhimento e autoridade técnica.
                
                Briefing da postagem:
                - Tema: {tema}
                - Formato: {formato}
                - Público: {publico}
                - Tom: {tom}
                
                Crie um planejamento de conteúdo ALTO PADRÃO, estruturado em:
                
                1. GANCHO MAGNÉTICO: 3 opções de frases iniciais irresistíveis.
                2. ROTEIRO/TEXTO COMPLETO: O conteúdo denso, com linguagem humana e exemplos reais. Assine como 'Nutri Pri Vale'.
                3. DIREÇÃO DE ARTE/VÍDEO: Sugestão clara do que ela deve gravar ou fotografar.
                4. CALL TO ACTION (CTA): Chamada para ação focada em engajamento ou captação.
                5. HASHTAGS: 6 hashtags de cauda longa para o nicho.
                
                Use formatação Markdown para um visual limpo e profissional.
                """
                
                resposta = modelo.generate_content(prompt)
                
                st.markdown("### 📊 Resultado da Estratégia")
                st.markdown(f"<div class='result-box'>{resposta.text}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error("Ocorreu uma instabilidade na conexão. Clique no botão novamente.")
