import sqlite3
from interface import *


banco = sqlite3.connect("database.db")

cursor = banco.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY AUTOINCREMENT, titulo TEXT NOT NULL, tarefa TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'Pendente')")


def add_tarefa(titulo, tarefa):
    
    cursor.execute("INSERT INTO tarefas (titulo, tarefa) VALUES (?,?)", (titulo, tarefa))

    banco.commit()
    
    print("\nTarefa adicionada com sucesso!")

def del_tarefas(del_id):
   
    try:

        cursor.execute("DELETE FROM tarefas WHERE id=?", (del_id,))

        if cursor.rowcount == 0:
            print(f"\nID {del_id} não existe.")
                     

        else:
            banco.commit()
            print(f"\nTarefa com ID: {del_id} deletada com sucesso!")
            
    except sqlite3.Error as erro:
        print("Erro ao excluir:", erro)

def editar_tarefas(edit_id, novo_titulo, nova_tarefa):

    try:
        cursor.execute("UPDATE tarefas SET titulo = ?, tarefa = ? WHERE id = ?", (novo_titulo, nova_tarefa, edit_id))

        if cursor.rowcount == 0:
                print(f"\nID {edit_id} não existe.")
        
        else:
            banco.commit()
            print(f"\nTítulo da tarefa com ID: {edit_id} editado com sucesso!")
    
    except sqlite3.Error as erro:
        print("Erro ao editar:", erro)    

def status(concluir_id):

    cursor.execute("UPDATE tarefas SET status = CASE WHEN status = 'Concluída' THEN 'Pendente' ELSE 'Concluída' END WHERE id = ?", (concluir_id,))
    banco.commit()