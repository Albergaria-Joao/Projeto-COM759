# Projeto Final COM759 - Gestão de Tarefas e Equipes

Facamp - Faculdades de Campinas, Novembro de 2025

Programação Avançada - COM759, Prof. Dr. José Martins Jr.

* João Vítor Albergaria Barbosa | 202310501
* Gabriel Palace Novaes Henrique | 202310491

---

## Visão Geral

Este projeto é uma aplicação web para gerenciamento de tarefas, equipes e membros, inspirada em plataformas de Kanban como o Trello.

### Principais Tecnologias

#### No frontend:
* **Vue.js 2**: Framework JavaScript progressivo.
* **Vue Router**: Gerenciamento de rotas e navegação.
* **Axios**: Cliente HTTP para comunicação com o backend.
* **CSS Scoped**: Estilização modular e responsiva.

#### No backend:
* **Flask**: Framework para desenvolver aplicações web em Python. Usado para construir a API.
* **PyMongo**: Conexão com banco de dados NoSQL.

---

## Funcionalidades principais

### Autenticação e Segurança
* **Login de Usuário**: Interface de acesso com validação de credenciais.
* **Controle de Sessão**: Persistência de login utilizando Cookies seguros (`HttpOnly` via Backend) e armazenamento local de metadados do usuário.
* **Logout**: Encerramento seguro da sessão.
* **Controle de Acesso (RBAC)**: A interface se adapta dinamicamente dependendo do nível do usuário (**Admin**, **Gerente** ou **Peão/Membro**), ocultando ou exibindo botões de edição e exclusão. Além disso, as rotas do backend são bloqueadas de acordo com essa hierarquia usando decoradores, o que garante uma camada extra de segurança.

### Dashboard (Kanban)
* **Visualização de Tarefas**: Organização visual em três colunas: *A Fazer*, *Em Execução* e *Concluída*.
* **Mudança de Status**: Atualização rápida do status da tarefa via dropdown direto no card.
* **Indicadores**: Contadores automáticos de tarefas por status.
* **Ações Rápidas**: Botões de Editar e Excluir tarefas diretamente no card (para usuários autorizados).

### Gestão de Membros e Equipes
* **CRUD Completo**: Interfaces para Criar, Ler, Atualizar e Deletar Equipes e Membros.
* **Associação**: Vínculo inteligente de membros a equipes específicas através de menus de seleção dinâmicos atualizados por regras estabelecidas no backend
* **Listagem com Filtros**: Tabelas responsivas com badges coloridos para identificar níveis de permissão (Admin, Gerente, etc.).

### Gestão de Tarefas
* **Criação Detalhada**: Formulários para adicionar tarefas com nome, descrição, prazo, equipe e membro responsável.
* **Edição**: Carregamento automático dos dados atuais da tarefa para atualização.

---

## Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* [Node.js](https://nodejs.org/) (Versão 12 ou superior)
* [NPM](https://www.npmjs.com/) ou Yarn.
* [Python](https://www.python.org/downloads/).
---

## Como rodar o Projeto

1.  **Clone o repositório**

    Utilizando Github Desktop ou linha de comando git

2.  **Crie um arquivo `.env`**

    Com o conteúdo:
    ```
    MONGO_URI="mongodb+srv://usuario:senha@cluster.xxxxx.mongodb.net/database"
    // Substituta o valor pela URI do seu banco de dados MongoDB
    ```

    Você já deverá ter criado um cluster com as collections membro, tarefa e equipe.

    Para criar uma conta admin com senha admin e conseguir testar, na sua collection membro, cole os seguintes valores em um novo registro:
    ```
    login: "admin"
    senha: Binary.createFromBase64('JDJiJDEyJHFJT0Z5VmpKS0NvNkpBUEE2WEhRZHUxMGJNVFRJTkJ5RDBlQlRoUmdzTHYwbTFZT1haSGtP', 0)
    auth: "admin"
    ```
    
3.  **Inicie o ambiente virtual Python**

    Na pasta `backend`, execute
    ```bash
    python -m venv venv
    ```

    E para ativar:
    ```bash
    venv\Scripts\Activate
    ```

4.  **Instale as bibliotecas Python**

    Ainda no backend e com venv ativado, rode:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Suba o backend**

    ```bash
    python -m flask run
    ```

6.  **Instale as dependências do frontend:**

    Agora, na pasta do frontend:
    ```bash
    npm install
    ```

7.  **Configure a API:**

    Verifique o arquivo `src/api.js`. Certifique-se de que a `baseURL` aponta para o endereço correto do seu Backend (Python/Flask).
    ```javascript
    // Exemplo em src/api.js
    baseURL: '[http://localhost:5000](http://localhost:5000)'
    ```

8.  **Execute o servidor de desenvolvimento:**

    ```bash
    npm run dev
    ```

9.  **Garanta que o CORS no backend libera a porta correta:**

    Um erro comum é que o backend não autorize o acesso a suas rotas pelo frontend por uma configuração errada do CORS. 

    Certifique-se de que, no arquivo `backend/app/__init__.py`, o parâmetro `origins` tenha a mesma porta indicada no terminal ao rodar o frontend (geralmente 8080 ou 8081)

10.  **Acesse a aplicação:**

    Abra o navegador em `http://localhost:8081` (ou o endereço indicado no terminal).


---