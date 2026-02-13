from flask import Flask, render_template, redirect, request, flash, send_file
import requests
from io import BytesIO

ENDPOINT_API = "https://api.thecatapi.com/v1/images/search"

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/cat', methods=['GET','POST'])
def cat():
    if request.method == 'GET':
        return redirect('/')
    
    nome = request.form.get('nome', None)

    if not nome:
        flash("ERRO! O nome do gato é obrigatório.")
        return redirect('/')

    resposta = requests.get(ENDPOINT_API)
    if resposta.status_code == 200:
        dados = resposta.json()
        url_gato = dados[0]['url']
    else:
        flash("ERRO! Não foi possível obter a imagem do gato.")
        return redirect('/')
    
    return render_template("index.html", nome=nome, url=url_gato)


@app.route('/download')
def download():
    url = request.args.get('url')

    if not url:
        return redirect('/')

    response = requests.get(url)
    img = BytesIO(response.content)

    return send_file(img, mimetype='image/jpeg',
                     as_attachment=True,
                     download_name='gato.jpg')


if __name__ == '__main__':
    app.secret_key = 'sua_chave_secreta_aqui'
    app.run(debug=True)
