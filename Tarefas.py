import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Função para conectar ao banco de dados SQLite
def conectar_bd():
    return sqlite3.connect('meu_banco.db')


# Criar a tabela de tarefas, se não existir
def criar_tabela():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        concluida BOOLEAN NOT NULL DEFAULT 0
    )
    ''')
    conn.commit()
    conn.close()


# Rota para a página principal, onde as tarefas serão listadas
@app.route('/')
def index():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas')
    tarefas = cursor.fetchall()  # Pega todas as tarefas
    conn.close()

    # Converte as tarefas para um formato mais fácil de manipular no template
    tarefas_formatadas = [{"id": t[0], "nome": t[1], "concluida": t[2]} for t in tarefas]

    return render_template('index.html', tarefas=tarefas_formatadas)


# Rota para adicionar novas tarefas
@app.route('/add', methods=["POST"])
def adicionar_tarefa():
    nome_tarefa = request.form.get('nome_tarefa')

    if nome_tarefa:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO tarefas (nome, concluida) VALUES (?, ?)
        ''', (nome_tarefa, False))  # Por padrão, a tarefa é pendente (concluida=False)
        conn.commit()
        conn.close()

    return redirect(url_for('index'))


# Rota para marcar a tarefa como concluída
@app.route('/concluir/<int:tarefa_id>')
def concluir_tarefa(tarefa_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE tarefas SET concluida = ? WHERE id = ?
    ''', (True, tarefa_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Rota para remover uma tarefa
@app.route('/delete/<int:tarefa_id>')
def deletar_tarefa(tarefa_id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM tarefas WHERE id = ?
    ''', (tarefa_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))


# Rota para listar apenas tarefas pendentes
@app.route('/pendentes')
def listar_pendentes():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE concluida = 0')
    tarefas = cursor.fetchall()
    conn.close()

    tarefas_formatadas = [{"id": t[0], "nome": t[1], "concluida": t[2]} for t in tarefas]

    return render_template('index.html', tarefas=tarefas_formatadas)


# Rota para listar apenas tarefas concluídas
@app.route('/concluidas')
def listar_concluidas():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tarefas WHERE concluida = 1')
    tarefas = cursor.fetchall()
    conn.close()

    tarefas_formatadas = [{"id": t[0], "nome": t[1], "concluida": t[2]} for t in tarefas]

    return render_template('index.html', tarefas=tarefas_formatadas)


if __name__ == '__main__':
    criar_tabela()  # Garantir que a tabela seja criada quando o app iniciar
    app.run(debug=True)
