from flask import Flask, render_template, request, jsonify
import unicodedata

app = Flask(__name__)

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto)
                  if unicodedata.category(c) != 'Mn').lower()

def carregar_dados():
    dados = []
    try:
        with open('procedimentos.txt', 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith('*'): # Pula linhas vazias ou divisores
                    dados.append(linha)
    except FileNotFoundError:
        return ["Erro: Arquivo procedimentos.txt não encontrado."]
    return dados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar')
def buscar():
    termo = remover_acentos(request.args.get('q', ''))
    if not termo:
        return jsonify([])

    todos_dados = carregar_dados()
    # Filtra se o termo está no nome, código ou abreviação (tudo normalizado)
    resultados = [item for item in todos_dados if termo in remover_acentos(item)]
    
    return jsonify(resultados)

if __name__ == '__main__':
    app.run(debug=True)