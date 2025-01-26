import sqlite3

# Conectar ao banco de dados (irá criar o banco de dados se ele não existir)
conn = sqlite3.connect('meu_banco.db')

# Criar um cursor para interagir com o banco de dados
cursor = conn.cursor()

# Criar a tabela, se ela não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS tarefas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    concluida BOOLEAN NOT NULL DEFAULT 0
)
''')

# Função para adicionar uma nova tarefa
def adicionar_tarefa(nome, concluida=False):
    cursor.execute('''
    INSERT INTO tarefas (nome, concluida) VALUES (?, ?)
    ''', (nome, concluida))
    conn.commit()  # Salvar as alterações no banco de dados
    print(f"Tarefa '{nome}' adicionada com sucesso!")

# Exemplo de inserção de dados
adicionar_tarefa('Estudar Python', False)
adicionar_tarefa('Finalizar projeto', True)

# Consultar todas as tarefas
cursor.execute('SELECT * FROM tarefas')
tarefas = cursor.fetchall()
print("\nTarefas cadastradas:")
for tarefa in tarefas:
    print(f"{tarefa[0]} - {tarefa[1]} - {'Concluída' if tarefa[2] else 'Pendente'}")

# Fechar a conexão com o banco de dados
conn.close()
