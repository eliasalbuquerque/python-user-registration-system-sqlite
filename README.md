<!--
title: 'README: Registro de Usuário Python com SQLite'
author: 'Elias Albuquerque'
created: '2024-10-25'
update: '2024-10-27'
-->

# UserHub: Sistema de Registro de Usuários em Python com SQLite

Este projeto demonstra um sistema de registro de usuários simples, desenvolvido 
em Python e utilizando o banco de dados SQLite. O UserHub permite adicionar, 
listar, editar e remover registros de usuários através de um menu interativo no 
terminal.

## Funcionalidades

* **Adicionar Usuários:** Permite inserir novos usuários com nome, email e 
  idade. A validação de dados garante a integridade das informações.
* **Listar Usuários:** Exibe todos os usuários cadastrados ou permite filtrar 
  por nome, email, idade ou ID.
* **Editar Usuários:** Permite modificar as informações de um usuário 
  existente, incluindo nome, email e idade.
* **Remover Usuários:** Remove um usuário específico pelo seu ID.
* **Menu Interativo:** Apresenta um menu de comandos no terminal para navegação 
  e interação com o sistema.
* **Validação de Dados:** Garante a entrada de dados válidos, como nome, email 
  e idade, através de expressões regulares.
* **Banco de Dados SQLite:** Armazena os dados dos usuários em um banco de 
  dados SQLite, garantindo persistência das informações.

## Como usar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/eliasalbuquerque/python-user-registration-system-sqlite
   ```

2. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Executar o script:**
   ```bash
   python app.py
   ```
   
   * O app iniciará com um menu de comandos da aplicação no primeiro uso.
   * Esse menu pode ser acessado a qualquer momento utilizando o comando 
     `--help`.

## Menu de comandos básicos da aplicação:

```
    $ UserHub> <comando>

    --add    : Adiciona usuário.
    --list   : Lista todos os usuários cadastrados ou filtre por dados:
             : --list name
             : --list email
             : --list age
             : --list id <id> 
    --edit   : Edita um usuário existente.
    --remove : Remove um usuário existente.
    --help   : Mostra o menu de comandos da aplicação.
    --clear  : Limpa o terminal.
    --exit   : Finaliza a aplicação.
    [ctrl+c] : Cancela a operação ou finaliza a aplicação.
```

## Contribuições

Contribuições para este projeto são bem-vindas! Você pode:

* Relatar bugs ou problemas.
* Sugerir novas funcionalidades.
* Enviar códigos para corrigir problemas ou adicionar novas funcionalidades.

## Licença

Este projeto é licenciado sob a licença GNU General Public License. 
