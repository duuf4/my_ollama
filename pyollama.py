from ollama import Client
import subprocess
import textwrap

def format_response(text):
    # Quebra o texto em parágrafos mais legíveis
    paragraphs = text.split('\n\n')
    formatted = []
    
    for para in paragraphs:
        # Limita cada linha a 80 caracteres e mantém indentação
        wrapped = textwrap.fill(para.strip(), width=80, 
                              break_long_words=False,
                              replace_whitespace=False)
        formatted.append(wrapped)
    
    return '\n\n'.join(formatted)

client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
)

question = input("Digite a(s) sua(s) dúvida(s): ")
my_model = 'llama2'



try:
    response = client.chat(model=my_model, messages=[{'role': 'user', 'content': question}])

    

    
    if isinstance(response, dict):
        content = (response.get('message', {}).get('content') 
                  or response.get('response') 
                  or response.get('content') 
                  or str(response))
    else:
        msg = getattr(response, 'message', None)
        if isinstance(msg, dict):
            content = msg.get('content') or str(response)
        else:
            content = str(response)

    # Formata e imprime a resposta de forma organizada
    print("\n=== Resposta ===\n")
    print(format_response(content))
    print("\n==============\n")

except Exception as e:
    err = str(e).lower()
    if 'not found' in err or '404' in err:
        print("Verifique modelos locais: ollama ls")
    else:
        print("Erro ao chamar o modelo:", e)


