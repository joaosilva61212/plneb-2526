from flask import Flask, render_template, request
import json

app=Flask(__name__)

fd_b=open("Aula 3\\dicionario_medico.json", "r", encoding="utf-8")
db=json.load(fd_b)


@app.get("/")  #rota para humanos
def homepage():
    n_conceitos = len(db) # Conta quantos conceitos existem
    return render_template("home.html", total=n_conceitos)
@app.get("/api/conceitos")  #rota para máquina
def conceitos_api():
    return db

@app.get("/conceitos")  
def conceitos():
    # Vai buscar a letra ao URL (ex: ?letra=A). Se não houver, é None.
    letra_selecionada = request.args.get('letra', '').upper()
    
    todos_os_conceitos = list(db.keys()) 
    
    if letra_selecionada:
        # Filtra apenas os conceitos que começam pela letra escolhida
        conceitos_filtrados = [c for c in todos_os_conceitos if c.upper().startswith(letra_selecionada)]
    else:
        conceitos_filtrados = todos_os_conceitos

    # Alfabeto para gerar a barra no HTML
    alfabeto = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    return render_template("conceitos.html", 
                           conceitos=conceitos_filtrados, 
                           alfabeto=alfabeto,
                           letra_atual=letra_selecionada)


@app.get("/conceitos/<designacao>")  #link variável
def conceito(designacao):
    if designacao in db:
        descricao = db[designacao]
        return render_template("conceito.html", designacao=designacao, descricao=descricao)
    else:
        return render_template("erro.html", error="O conceito introduzido não existe.")

app.run(host="localhost", port=4002, debug=True)