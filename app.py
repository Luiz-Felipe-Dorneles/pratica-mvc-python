from flask import Flask, redirect, render_template, request, url_for
from model.tarefa import Tarefa

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        titulo = request.form['titulo']
        data_conclusao = request.form['data_conclusao']
        tarefa = Tarefa(titulo=titulo, data_conclusao=data_conclusao)
        tarefa.salvarTarefa()
        return redirect(url_for('index'))

    tarefas = Tarefa.listarTarefas()
    return render_template("index.html", tarefas=tarefas, title='Minhas Tarefas')

@app.route('/delete/<int:idtarefa>')
def delete(idtarefa):
    tarefa = Tarefa(id=idtarefa)
    tarefa.apagarTarefa()
    return redirect(url_for('index'))

@app.route('/editar/<int:idtarefa>', methods=['GET', 'POST'])
def editar(idtarefa):
    tarefa = Tarefa(id=idtarefa)

    if request.method == 'POST':
        novo_titulo = request.form['titulo']
        nova_data_conclusao = request.form['data_conclusao']
        tarefa.editarTarefa(novo_titulo, nova_data_conclusao)
        return redirect(url_for('index'))

    # Exibe os dados da tarefa no formulário
    return render_template("editar.html", tarefa=tarefa)

if __name__ == "__main__":
    app.run(debug=True)
