# Gerenciador de Lista de Tarefas
def exibir_menu():
    print("\nBem-vindo ao Gerenciador de Tarefas!")
    print("Escolha uma opção:")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Marcar tarefa como concluída")
    print("4. Remover tarefa")
    print("5. Sair")

def adicionar_tarefa(tarefas):
    tarefa = input("Digite a descrição da tarefa: ")
    tarefas.append({"descricao": tarefa, "concluida": False})
    print("Tarefa adicionada com sucesso!")

def listar_tarefas(tarefas):
    if not tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    print("\nLista de Tarefas:")
    for i, tarefa in enumerate(tarefas):
        status = "Concluída" if tarefa["concluida"] else "Pendente"
        print(f"{i + 1}. {tarefa['descricao']} - {status}")

def marcar_concluida(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        indice= int (input("Digite o numero da tarefa que deseja marcar como concluida ")) - 1
        if 0 <= indice < len (tarefas):
            tarefas[indice]["Concluida"]=True
            print ("Tarefa marcada como concluida !")
        else:
            print("Numero invalido")
    except ValueError:
        print("Por favor, digite um numero valido")

def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    if not tarefas:
        return
    try:
        indice = int(input("Digite o número da tarefa que deseja remover: ")) - 1
        if 0<= indice<len(tarefas):
            tarefas.pop(indice)
            print("Tarefas removidas com sucesso ")
        else:
            print("Numero invalido")
    except ValueError:
        print("Por favor,digite um número Válido")
def main():
            tarefas = []
            while True:
                opcao = input("Escolha uma opção")
                if opcao == "1":
                    adicionar_tarefa(tarefas)
                elif opcao == "2":
                    listar_tarefas(tarefas)
                elif opcao == "3":
                    marcar_concluida(tarefas)
                elif opcao == "4":
                    remover_tarefa(tarefas)
                elif opcao == "5":
                    print("Saindo do programa Até logo")
                    break
                else:
                    print("Opção Invalida.Tente novamente ")



if __name__ == "__main__":
    main()

