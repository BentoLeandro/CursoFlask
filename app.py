from flask import Flask, render_template, request, redirect, session, flash, url_for  

# $env:FLASK_APP="app"

app = Flask(__name__)
app.secret_key = 'test435679'

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console  

class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usua1 = Usuario('bento', 'Bento Leandro', '123')
usua2 = Usuario('kellen', 'Kellen Xaxier', '222')
usua3 = Usuario('Jess', 'Jess.. da Silva', '555')
usuarios = {usua1.id: usua1,
            usua2.id: usua2,
            usua3.id: usua3}

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', ' GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
lista = [jogo1, jogo2, jogo3]

@app.route('/')
@app.route('/inicio')
def index():
    return render_template('lista.html', titulo='Jogos!', jogos=lista)

@app.route('/novo')
def novo():
    if session['usuario_logado'] == None or 'usuario_logado' not in session:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:    
        return render_template('novo.html', titulo='Novo Jogo Teste')    

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    return redirect(url_for('index'))  #render_template('lista.html', titulo='Jogos!', jogos=lista)

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima_pg=proxima)

@app.route('/logout')
def logout():
    if session['usuario_logado'] != '':
        session['usuario_logado'] = None

    flash('Usuário foi deslogado...')
    return redirect(url_for('index'))    

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            pagina = request.form['proxima']
            flash(usuario.nome+' Logou com sucesso!')
            return redirect(pagina) #'/{}'.format(pagina) 
        else:
            flash('Senha do usuário está Errada!') 
            return redirect(url_for('login'))                          
    else:
        flash('Usuário não localizado na Base! Tente novamente!')
        return redirect(url_for('login'))  



app.run(host='127.0.0.1', port=5500, debug=True)





