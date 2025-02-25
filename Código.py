import streamlit as st
import openai
from PIL import Image
import io
import base64

# Configurar API Key da OpenAI (substituir pela tua chave)
openai.api_key = "SUA_CHAVE_AQUI"

def encode_image(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

def transcribe_audio(audio_file):
    audio_bytes = audio_file.read()
    response = openai.Audio.transcribe(
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
        # Converter imagens para Base64
        panel_image = encode_image(Image.open(uploaded_panel))
        hood_image = encode_image(Image.open(uploaded_hood))
        
        # Criar o prompt para a API
        prompt = f"""
        O utilizador descreveu o seguinte problema com o carro:
        {description}
        
        Analise as imagens do painel de instrumentos e do motor e forneça um diagnóstico provável, incluindo possíveis causas e soluções recomendadas.
        """
        
        # Chamada à API
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "És um mecânico automotivo especializado em diagnóstico de problemas."},
                {"role": "user", "content": prompt},
                {"role": "user", "content": panel_image},
                {"role": "user", "content": hood_image}
            ],
            max_tokens=500
        )
        
        # Exibir resposta
        st.subheader("Diagnóstico do Problema")
        st.write(response["choices"][0]["message"]["content"])

