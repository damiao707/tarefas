from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
import os
from flask import send_file
import pandas as pd

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_banco():
    conn = sqlite3.connect('tarefas.db')
    return conn

# Rota inicial
@app.route('/')
def index():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Seleciona todas as tarefas do banco
    cursor.execute("SELECT id, nome, concluida FROM tarefas")
    tarefas = cursor.fetchall()
    conn.close()

    # Renderiza a tabela de tarefas
    return render_template('index.html', tarefas=tarefas)

# Rota para adicionar uma nova tarefa
@app.route('/add', methods=['POST'])
def adicionar_tarefa():
    nome_tarefa = request.form.get('nome_tarefa')
    if nome_tarefa:
        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            # Insere a tarefa no banco de dados como pendente
            cursor.execute("INSERT INTO tarefas (nome, concluida) VALUES (?, ?)", (nome_tarefa, 0))
            conn.commit()  # Certifique-se de que o commit está sendo feito
            conn.close()

            print(f"Tarefa '{nome_tarefa}' adicionada com sucesso.")  # Log para debug
        except Exception as e:
            print(f"Erro ao adicionar tarefa: {e}")  # Log de erro
    else:
        print("Nenhuma tarefa foi fornecida no formulário.")  # Log para debug

    return redirect(url_for('index'))
@app.route('/export')
def exportar_dados():
    try:
        conn = conectar_banco()
        cursor = conn.cursor()

        # Consulta todas as tarefas no banco de dados
        cursor.execute("SELECT * FROM tarefas")
        tarefas = cursor.fetchall()

        # Define o nome do arquivo exportado
        caminho_arquivo = os.path.join(os.getcwd(), 'tarefas_export.csv')

        # Gera o arquivo CSV
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Cabeçalhos do CSV
            csvwriter.writerow(['ID', 'Nome', 'Concluída'])
            # Dados
            csvwriter.writerows(tarefas)

        # Fecha a conexão com o banco
        conn.close()

        print(f'Dados exportados com sucesso para {caminho_arquivo}.')  # Log
        return send_file(caminho_arquivo, as_attachment=True)

    except Exception as e:
        print(f'Erro ao exportar os dados: {e}')
        return 'Erro ao exportar os dados', 500

# Rota para marcar uma tarefa como concluída
@app.route('/concluir/<int:tarefa_id>')
def concluir_tarefa(tarefa_id):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Atualiza a tarefa para concluída
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Rota para deletar uma tarefa
@app.route('/delete/<int:tarefa_id>')
def deletar_tarefa(tarefa_id):
    conn = conectar_banco()
    cursor = conn.cursor()

    # Remove a tarefa do banco de dados
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Criação inicial do banco de dados
def criar_banco():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Criação da tabela de tarefas, caso não exista
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            concluida INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)
