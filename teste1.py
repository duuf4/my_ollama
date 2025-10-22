
import ollama

question = input("Digite a sua dúvida: ")

response = ollama.chat(model='llama2', messages=[
  {
    'role': 'user',
    'content': question,
  },
])
print(response['message']['content'])