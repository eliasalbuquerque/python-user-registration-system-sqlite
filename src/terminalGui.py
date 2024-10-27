import re
import os
import random
from src.db_manager import DatabaseManager


class TerminalGui:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        command = input("UserHub> ")

        match command:
            case "exit":
                print("Saindo do UserHub...")
                self.db.close_connection()
                exit()
            case "cls" | "clear":
                self.clear_terminal()
            case "--add":
                self.__add_user()
            case "--help":
                self._menu()
            case "":
                pass
            case _: 
                if command.startswith("--list"):
                    self._list_user(command.split())
                    print('')
                elif command.startswith("--remove"):
                    command_parts = command.split()
                    self.__remove_user(command_parts)
                elif command.startswith("--edit"):
                    self.__edit_user(command)
                else:
                    print("Comando inválido. Digite --help para ver os comandos disponíveis.")


    def _menu(self):
        message = """
    Ações do UserHub:

      --add          : Adiciona novo usuário. Exemplo:
                     : $ UserHub> --add
                     : $ Adicione um novo usuário:
                     : $ Nome: <str>
                     : $ Email: <exemplo@email.com.br>
                     : $ Idade: <int> 

      --list         : Lista todos os usuários. Exemplo:
                     : $ UserHub> --list
      --list nome    : Lista os nomes dos usuários cadastrados.
      --list email   : Lista os emails dos usuários cadastrados.
      --list idade   : Lista as idades dos usuários cadastrados.
      --list id <id> : Lista o ID de um usuário específico existente.

      --edit         : Edita um usuário existente.
                     : Como usar: 
                     : $ Editar: <id> <nome opcional> <email opcional> <idade opcional>
                     : Exemplo: 
                     : $ UserHub> --edit
                     : $ Editar: 1 João da Silva joao@email.com 32 

      --remove       : Remove um usuário existente. Ex:
                     : $ UserHub> --remove
                     : $ Remover o ID: <id do usuário existente>

      --help         : Mostra o menu de comandos do UserHub.
                     : $ UserHub> --help

      clear / cls    : Limpa o terminal.
                     : $ UserHub> clear
                     : $ UserHub> cls

      exit           : Finalizar a aplicação e fechar o terminal.
                     : $ UserHub> exit

      [Ctrl+C]       : Cancela operação ou finaliza o programa.
                     : Use [ctrl+c] para sair de um comando:
                     : $ Operação cancelada pelo usuário. Retornando ao menu principal.
                     : Ou finalize a aplicação a partir do menu principal do app:
                     : $ UserHub> <[ctrl+c]>
                     : $ Saindo do UserHub...
    """
        return print(message)


    def _list_user(self, command_parts=None, list_id=None, list_all=False, last_user=False):
        """Listar usuários com filtros."""

        # --list last_user
        if last_user:
            # Obtém o último usuário do banco
            user = self.db.get_user(last=True)
            if user:
                data = user[0]  # Pega a primeira linha da lista retornada
                print(f"ID: {data[0]}, Nome: {data[1]}, Email: {data[2]}, Idade: {data[3]}")
            else:
                print("Nenhum usuário cadastrado.")

        # --list <coluna>
        elif command_parts is not None and len(command_parts) == 2 and command_parts[0] == "--list":
            if command_parts[1] in ("name", "email", "age"):
                filter_column = command_parts[1]
                users = self.db.get_user(select=filter_column)
                if users:
                    print("Usuários cadastrados:")
                    for user in users:
                        print(f"ID: {user[0]}, {user[1]}")
                else:
                    print("Nenhum usuário cadastrado.")
            else:
                print("Comando inválido. Use: --list, --list name, --list email, --list age ou --list id <id>.")

        # --list id <id>
        elif (command_parts is not None and len(command_parts) == 3 and command_parts[0] == "--list") or list_id is not None:
            # Definir o ID a ser usado, seja do `list_id` ou do `command_parts`
            id = list_id if list_id is not None else command_parts[2]
            
            # Validar o ID
            if not self._validate_id(id):
                print("ID inválido. O ID deve ser um número inteiro positivo.")
                return

            # Buscar e imprimir usuário
            user = self.db.get_user(user_id=id)
            if user:
                for data in user:
                    print(f"ID: {data[0]}, Nome: {data[1]}, Email: {data[2]}, Idade: {data[3]}")
            else:
                print("Nenhum usuário encontrado com o ID especificado.")
        
        # --list tudo se o comando for apenas "--list"
        elif (command_parts is not None and command_parts[0] == "--list") or list_all==True:
            users = self.db.get_user()
            if users:
                print("Usuários cadastrados:")
                for user in users:
                    print(f"ID: {user[0]}, Nome: {user[1]}, Email: {user[2]}, Idade: {user[3]}")
            else:
                print("Nenhum usuário cadastrado.")
        
        else:
            print("Comando inválido. Use: --list, --list name, --list email, --list age ou --list id <id>.")


    def __add_user(self):
        """Adiciona um novo usuário ao banco de dados."""
        self.clear_terminal()
        print('UserHub> --add')

        while True:
            try:
                print("Adicione um novo usuário:")

                # Validação do nome (somente string)
                while True:
                    name = input("Nome: ")
                    if self._validate_name(name):
                        break
                    else:
                        print("Nome inválido. Use apenas letras.")

                # Validação do e-mail (exemplo@dominio.com)
                while True:
                    email = input("E-mail: ")
                    if self._validate_email(email):
                        break
                    else:
                        print('E-mail inválido. Use o formato correto "exemplo@dominio.com" (".br" opicional).')

                # Validação da idade (somente numero inteiro)
                while True:
                    age = input("Idade: ")
                    if self._validate_age(age):
                        break

                # Inserir o usuário no banco de dados
                self.db.insert_user(name, email, age)
                print('\nUsuário cadastrado com sucesso!')
                self._list_user(last_user=True)
                print('')

                # Perguntar se deseja adicionar outro usuário
                while True:
                    continuar = input(
                        "Deseja adicionar outro usuário? [Y/n]: ").lower()
                    if continuar in ("y", "yes", "sim"):
                        break
                    elif continuar in ("n", "no", "nao", "não"):
                        print("Encerrando adição de usuários.\n")
                        return
                    else:
                        print("Resposta inválida. Digite Y/n.")

            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário. Retornando ao _menu principal.\n")
                return

    def _validate_name(self, name):
        if re.match(r"^[A-Za-z\sàáâãäåçèéêëìíîïòóôõöùúûüýñçÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝÑÇ]{2,}$", name):
            return True
        else:
            return False

    def _validate_email(self, email):
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|com\.br)$", email):
            return True
        else:
            return False

    def _validate_age(self, age):
        try:
            age = int(age)

            if 1 <= age <= 120:
                return True
            elif age < 1:
                print('Idade inválida. A idade deve ser maior que 0.')
                return False
            else:
                # Ler a linha aleatória do arquivo age.txt
                with open("src/age.txt", "r", encoding="utf-8") as f:
                    age_lines = f.readlines()
                    random_age_line = random.choice(age_lines)
                    print(f'\n"{random_age_line.strip()}"\n')
                print('Idade inválida. A idade deve ser menor que 120.')
                return False
            return True
        except ValueError:
            print("Idade inválida. A idade deve ser um número inteiro positivo.")
            return False

    def _validate_id(self, id):
        try:
            id = int(id)
            return id > 0
        except ValueError:
            return False


    def __edit_user(self, command):
        """Edita um usuário existente."""

        self.clear_terminal()
        print('UserHub> --edit')
        self._list_user(list_all=True)
        print('')
        print('Modo Editor: Para ajuda digite --help, para sair Ctrl+C')

        while True:
            try:
                edit = input('Editar: ')
                edit_split_list = edit.split()

                match edit_split_list:
                    case ["--help"]:
                        self.__edit_help()
                        continue
                    case _:
                        # Verificar se há ao menos dois elementos: ID e outro comando
                        if len(edit_split_list) < 2:
                            print("Entrada inválida. Por favor, forneça um ID e um comando.")
                            continue

                        # Validar ID
                        id = edit_split_list[0]
                        if not self._validate_id(id):
                            print("ID inválido. O ID deve ser um número inteiro positivo.")
                            continue
                        user_id = int(id)

                        # Definindo variáveis para novos valores
                        name, email, age = None, None, None

                        # Itera pelos dados fornecidos para identificar name, e-mail e age
                        for data in edit_split_list[1:]:
                            match data:
                                case data if "@" in data:
                                    email = data
                                case data if data.isnumeric():
                                    age = data
                                case _:
                                    name = f"{name} {data}".strip() if name else data

                        # Valida nome
                        if name and not self._validate_name(name):
                            print("Nome inserido inválido. Tente novamente.")
                            continue

                        # Valida email
                        if email and not self._validate_email(email):
                            print("Email inserido inválido. Tente novamente.")
                            continue

                        # Valida idade
                        if age and not self._validate_age(age):
                            continue

                # Busca dados do usuário atual para verificar alterações
                user_current = self.db.get_user(user_id=user_id, select="*")[0]
                id_current, name_current, email_current, age_current = user_current

                # Define valores novos ou mantém os atuais
                name = name if name else name_current
                email = email if email else email_current
                age = age if age else age_current

                # Atualiza banco de dados
                self.db.update_user(user_id, name, email, age)

                # Exibe o usuário atualizado
                print("Usuário atualizado com sucesso!")
                self._list_user(list_id=user_id)
                print('')
                
                # Perguntar se deseja editar outro usuário
                while True:
                    continuar = input(
                        "Deseja editar outro usuário? [Y/n]: ").lower()
                    if continuar in ("y", "yes", "sim"):
                        break
                    elif continuar in ("n", "no", "nao", "não"):
                        print("Encerrando edição de usuários.\n")
                        return
                    else:
                        print("Resposta inválida. Digite Y/n.")

            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário. Retornando ao menu principal.\n")
                return


    def __edit_help(self):
        """Exibe a ajuda para o comando --edit."""
        message = """
    Menu comando --edit:

        Para editar um usuário cadastrado, digite o ID e os dados atualizados:

        Ex 1: Editar e-mail do ID 3
        $ Editar: 3 joao@email.com
      
        Ex 2: Editar nome e idade do ID 3
        $ Editar: 3 João da Silva 35

        Comando:
        $ Editar: <id> <nome opcional> <email opcional> <idade opcional>

    [Tip] Você pode editar mais de um dado no mesmo comando, mantendo os outros 
          inalterados. Por exemplo, para editar apenas o nome:

        $ Editar: 3 João da Silva 
        """
        return print(message)


    def __remove_user(self, command_parts):
        """Remove um usuário existente."""

        self.clear_terminal()
        print('UserHub> --remove')
        self._list_user(list_all=True)
        print('')
        print('Modo Remoção: Para sair Ctrl+C')

        while True:
            try:
                # Caso o comando seja apenas "--remove"
                if len(command_parts) == 1 and command_parts[0] == "--remove":

                    while True:
                        try:
                            user_id = input('Remover o ID: ')
                            if not self._validate_id(user_id):
                                print("ID inválido. O ID deve ser um número inteiro positivo.")
                                continue
                            user_id = int(user_id)
                            break
                        except ValueError:
                            print("ID inválido. O ID deve ser um número inteiro positivo.")

                    # Após obter o ID, remover o usuário:
                    self.db.delete_user(user_id)
                    self.clear_terminal()
                    print("UserHub> --remove")
                    self._list_user(list_all=True)
                    print(f"\nRemover o ID: {user_id}")
                    print(f"Usuário com ID {user_id} removido com sucesso!\n")

                # Caso o comando seja "--remove <id>"
                elif len(command_parts) == 2 and command_parts[0] == "--remove":
                    command, user_id = command_parts
                    if not self._validate_id(user_id):
                        print("ID inválido. O ID deve ser um número inteiro positivo.\n")
                        return
                    user_id = int(user_id)
                    self.db.delete_user(user_id)
                    print(f"Usuário ID {user_id} removido com sucesso!\n")
                    return
                else:
                    print("Formato inválido. Use: --remove ou --remove <id do usuario>\n")
                    return
                
                # Perguntar se deseja remover outro usuário
                while True:
                    continuar = input(
                        "Deseja remover outro usuário? [Y/n]: ").lower()
                    if continuar in ("y", "yes", "sim"):
                        break
                    elif continuar in ("n", "no", "nao", "não"):
                        print("Encerrando remoção de usuários.\n")
                        return
                    else:
                        print("Resposta inválida. Digite Y/n.")

            except KeyboardInterrupt:
                print("\nOperação cancelada pelo usuário. Retornando ao menu principal.\n")
                return
