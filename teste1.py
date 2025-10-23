from ollama import Client
import subprocess
import textwrap
import sys

def format_response(text):
    """Formata a resposta para uma exibição mais legível"""
    paragraphs = text.split('\n\n')
    formatted = []
    for para in paragraphs:
        wrapped = textwrap.fill(
            para.strip(),
            width=80,
            break_long_words=False,
            replace_whitespace=False
        )
        formatted.append(wrapped)
    return '\n\n'.join(formatted)

def list_local_models():
    """Lista os modelos disponíveis localmente via CLI"""
    try:
        res = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        lines = [l.strip().split()[0] for l in res.stdout.splitlines() if l.strip()]
        return lines
    except Exception as e:
        print(f"Erro ao listar modelos locais: {e}")
        return []

# Configuração do cliente Ollama
client = Client(host='http://localhost:11434')

question = input("Digite sua pergunta: ").strip()
my_model = 'tinyllama'

# Verifica se o modelo está instalado localmente
available = list_local_models()
if not available:
    print("⚠️  Nenhum modelo foi encontrado. Verifique se o Ollama está rodando e acessível.")
    print("Execute no terminal: 'ollama list'")
    sys.exit(1)

if my_model not in available:
    print(f"❌ Modelo '{my_model}' não encontrado entre os modelos locais.\n")
    print("Modelos disponíveis:")
    for m in available:
        print("  -", m)
    print(f"\nPara instalar o '{my_model}':")
    print(f"  ollama pull {my_model}")
    sys.exit(1)

# Envia a mensagem para o modelo
try:
    print("\n=== Gerando resposta ===\n")

    response_text = ""
    for part in client.chat(
        model=my_model,
        messages=[
            {'role': 'system', 'content': 'Você é um assistente conciso e direto.'},
            {'role': 'user', 'content': question}
        ],
        stream=True
    ):
        content = part['message']['content']
        print(content, end='', flush=True)
        response_text += content

    print("\n\n=== Resposta formatada ===\n")
    print(format_response(response_text))
    print("\n==========================\n")

except Exception as e:
    err = str(e).lower()
    if 'not found' in err or '404' in err:
        print("❌ Erro: modelo não encontrado. Execute 'ollama list' para confirmar.")
    elif 'connection refused' in err:
        print("❌ Não foi possível conectar ao servidor Ollama.")
        print("Verifique se o container está rodando e com a porta 11434 exposta.")
    else:
        print("❌ Erro inesperado:", e)
