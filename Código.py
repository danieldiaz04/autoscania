import streamlit as st
from openai import OpenAI
import io
import base64
from PIL import Image

# Definir a chave da API diretamente no código (⚠️ NÃO RECOMENDADO PARA PRODUÇÃO)
OPENAI_API_KEY = "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"


# Inicializar o cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def encode_image(image):
    """Codifica a imagem em base64 para envio à API."""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="JPEG")
    return base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

def transcribe_audio(audio_file):
    """Transcreve um ficheiro de áudio usando a API Whisper da OpenAI."""
    audio_bytes = audio_file.read()
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=io.BytesIO(audio_bytes),
        response_format="text"
    )
    return response

st.title("Diagnóstico Automóvel com IA")
st.write("Descreva o problema do seu carro ou envie um áudio e imagens para análise.")

# Input de texto
description = st.text_area("Descreva o problema do seu carro:")

# Upload de áudio
uploaded_audio = st.file_uploader("Ou carregue um áudio descrevendo o problema", type=["mp3", "wav", "m4a"])
if uploaded_audio:
    description = transcribe_audio(uploaded_audio)
    st.write("Texto transcrito:", description)

# Upload das imagens
uploaded_panel = st.file_uploader("Carregue uma imagem do painel de instrumentos", type=["jpg", "png", "jpeg"])
uploaded_hood = st.file_uploader("Carregue uma imagem do motor (capô aberto)", type=["jpg", "png", "jpeg"])

if st.button("Analisar Problema"):
    if not description:
        st.error("Por favor, insira uma descrição do problema ou envie um áudio.")
    elif not uploaded_panel or not uploaded_hood:
        st.error("Por favor, carregue ambas as imagens.")
    else:
        try:
            # Converter imagens para Base64
            panel_image = encode_image(Image.open(uploaded_panel))
            hood_image = encode_image(Image.open(uploaded_hood))
            
            # Criar o prompt para a API
            prompt = f"""
            O utilizador descreveu o seguinte problema com o carro:
            {description}
            
            Analise as imagens do painel de instrumentos e do motor e forneça um diagnóstico provável, incluindo possíveis causas e soluções recomendadas.
            """
            
            # Chamada à API Vision para processar as imagens
            response = client.chat.completions.create(
                model="gpt-4-vision-preview",  # Use o modelo GPT-4 Vision
                messages=[
                    {"role": "system", "content": "És um mecânico automotivo especializado em diagnóstico de problemas."},
                    {"role": "user", "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{panel_image}"}},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{hood_image}"}}
                    ]}
                ],
                max_tokens=500
            )
            
            # Exibir resposta
            st.subheader("Diagnóstico do Problema")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Erro ao chamar a API da OpenAI: {e}")