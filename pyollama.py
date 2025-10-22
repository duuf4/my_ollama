from ollama import Client
import subprocess


client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)

question = input("Digite a(s) sua(s) dúvida(s): ")


try:
    response = client.chat(model='llama2', messages=[{ 'role': 'user', 'content': question }])

    
    if isinstance(response, dict):
        content = response.get('message', {}).get('content') or response.get('response') or response.get('content') or str(response)
    else:
        msg = getattr(response, 'message', None)
        if isinstance(msg, dict):
            content = msg.get('content') or str(response)
        else:
            content = str(response)

    print(content)

except Exception as e:
    err = str(e).lower()
    if 'not found' in err or '404' in err:
        print("Verifique modelos locais: ollama ls")
    else:
        print("Erro ao chamar o modelo:", e)

print(content)


