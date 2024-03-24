import PySimpleGUI as sg
from tarefas import *
import sys

def carregar_tarefas():
    global tarefa_ids

    cursor.execute("SELECT id FROM tarefas")
    tarefa_ids = cursor.fetchall()

    dados_tarefas = []
    
    for ids in tarefa_ids:
        cursor.execute("SELECT titulo, tarefa, status FROM tarefas WHERE id=?", ids)
        titulo, tarefa, status = cursor.fetchone()
        dados_tarefas.append((ids[0], titulo, tarefa, status))
    
    return dados_tarefas

try:
    dados_tarefas = carregar_tarefas()
except (sqlite3.ProgrammingError, sqlite3.Error):
    sys.exit()

layout = [
    [sg.Table(values=dados_tarefas, headings=["ID", "Título", "Tarefa", "Status"], enable_events=True, key="table", display_row_numbers=False, auto_size_columns=False, col_widths=[4,20,50,8], justification= "left")],
    [sg.Button("Editar"), sg.DD(tarefa_ids, size=(10, 8), default_value="Selecione", key= "Editar_DD")],
    [sg.Button("Excluir"), sg.DD(tarefa_ids, size=(10, 8), default_value="Selecione", key= "Excluir_DD")],
    [sg.Button("Des/Marcar como concluída"), sg.DD(tarefa_ids, size=(10, 8), default_value="Selecione", key= "Concluir_DD")],
    [sg.Button("Adicionar")]
    

]

janela = sg.Window("Tarefas", layout)

janela_editar = None

janela_add = None

def atualizar():

    dados_tarefas = carregar_tarefas()
    janela["table"].update(values=dados_tarefas)
    janela["Editar_DD"].update(values=tarefa_ids)
    janela["Excluir_DD"].update(values=tarefa_ids)
    janela["Concluir_DD"].update(values=tarefa_ids)    

while True:
    evento, valores = janela.read()
    if evento == sg.WIN_CLOSED:
        break
    
    # Excluir
    try:
        if evento == "Excluir":

            del_id_tupla = valores["Excluir_DD"]
            del_id = del_id_tupla[0]
            del_tarefas(del_id)
            
            atualizar()
            sg.popup("Tarefa excluída com sucesso!")
            
    except (IndexError, TypeError):
        sg.popup("Selecione um ID.")
    
    # Editar
    try:
        if evento == "Editar":
            edit_id_tupla = valores["Editar_DD"]
            edit_id = edit_id_tupla[0]

            if janela_editar is None:
                cursor.execute("SELECT titulo, tarefa FROM tarefas WHERE id=?", (edit_id,))
                tarefa_selecionada = cursor.fetchone()

                edit_layout = [
                    
                    [sg.Text("Título:")],
                    [sg.InputText(key="novo titulo", default_text=tarefa_selecionada[0])],
                    [sg.Text("")],
                    [sg.Text("Tarefa:")],
                    [sg.InputText(key="nova tarefa", default_text=tarefa_selecionada[1])],
                    [sg.Text("")],
                    [sg.Button("Cancelar"), sg.Button("Salvar")]
                ]

                

                janela_editar = sg.Window("Editar tarefa", edit_layout)

                while True:

                    evento, valores = janela_editar.read()
                    if evento == sg.WIN_CLOSED or evento == "Cancelar":
                        janela_editar.close()
                        janela_editar = None
                        break
                    
                    

                    if evento == "Salvar":
                        
                        novo_titulo = valores["novo titulo"]
                        nova_tarefa = valores["nova tarefa"]
                        editar_tarefas(edit_id, novo_titulo, nova_tarefa)
                        
                        atualizar()
                        sg.popup("Tarefa editada com sucesso!")

    except (IndexError, TypeError):
        sg.popup("Selecione um ID.")

    # Adicionar
    try:
        if evento == "Adicionar":
            
            if janela_add is None:
                
                add_layout = [

                        [sg.Text("Título:")],
                        [sg.InputText(key="titulo")],
                        [sg.Text("")],
                        [sg.Text("Tarefa:")],
                        [sg.InputText(key="tarefa")],
                        [sg.Text("")],
                        [sg.Button("Cancelar"), sg.Button("Salvar")]
                    ]

                janela_add = sg.Window("Adicionar tarefa", add_layout)

                while True:

                    evento, valores = janela_add.read()
                    if evento == sg.WIN_CLOSED or evento == "Cancelar":
                        janela_add.close()
                        janela_add = None
                        break
                    
                    

                    if evento == "Salvar":
                        
                        titulo = valores["titulo"]
                        tarefa = valores["tarefa"]
                        add_tarefa(titulo, tarefa)

                        atualizar()
                        sg.popup("Tarefa adicionada com sucesso!")

    except (IndexError, TypeError):
        sg.popup("Selecione um ID.")

    # Marcar como concluída
    try:
        if evento == "Des/Marcar como concluída":    

            concluir_id_tupla = valores["Concluir_DD"]
            concluir_id = concluir_id_tupla[0]
                        
            status(concluir_id)

            atualizar()

    except (IndexError, TypeError):
        sg.popup("Selecione um ID.")
        
        """ dados_tarefas = carregar_tarefas()
        janela["table"].update(values=dados_tarefas)
        janela["Editar_DD"].update(values=tarefa_ids)
        janela["Excluir_DD"].update(values=tarefa_ids)
        sg.popup("Tarefa editada com sucesso!") """


        
 



banco.close()
janela.close()