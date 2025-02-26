from openai import OpenAI

# Substitua pela sua chave da API
OPENAI_API_KEY = "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"


# Inicializar o cliente da OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

try:
    # Tentar fazer uma chamada ao GPT-4
    response = client.chat.completions.create(
        model="gpt-4",  # Tente usar o modelo GPT-4
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": "Olá, qual é o seu nome?"}
        ],
        max_tokens=50
    )
    # Se a chamada for bem-sucedida, exibir a resposta
    print("Resposta do GPT-4:", response.choices[0].message.content)
    print("✅ Você tem acesso ao GPT-4!")
except Exception as e:
    # Se ocorrer um erro, exibir a mensagem de erro
    print(f"❌ Erro ao chamar a API: {e}")
    if "model_not_found" in str(e):
        print("Você NÃO tem acesso ao GPT-4.")
    else:
        print("Verifique sua chave da API ou conexão com a internet.")