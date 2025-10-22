
# import ollama

# question = input("Digite a sua dúvida: ")

# response = ollama.chat(model='llama2', messages=[
#   {
#     'role': 'user',
#     'content': question,
#   },
# ])
# print(response['message']['content'])


from ollama import Client

# Simplifica a criação do cliente - remove headers desnecessários
client = Client(host='http://localhost:11434')

question = input("Digite a sua dúvida: ")

try:
    response = client.chat(model='llama2', messages=[
        {'role': 'user', 'content': question}
    ])
    
    # Extrai o conteúdo da resposta
    if isinstance(response, dict):
        content = response.get('message', {}).get('content') or response.get('response') or str(response)
    else:
        msg = getattr(response, 'message', None)
        if isinstance(msg, dict):
            content = msg.get('content') or str(response)
        else:
            content = str(response)

    print("\nResposta:")
    print(content)

except Exception as e:
    err = str(e).lower()
    if 'not found' in err or '404' in err:
        print(f"Erro: modelo 'llama2' não encontrado.")
        print("Verifique modelos locais com: ollama ls")
        print("Para baixar o modelo use: ollama pull llama2")
    else:
        print("Erro ao chamar o modelo:", e)