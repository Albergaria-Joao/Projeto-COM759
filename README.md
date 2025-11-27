# 🚀 Gestão de Tarefas e Equipes - Frontend

Bem-vindo ao repositório do **Frontend** do sistema de Gestão de Tarefas. Esta é uma Single Page Application (SPA) desenvolvida com **Vue.js**, focada na organização de projetos, equipes e monitoramento de atividades através de um painel estilo Kanban.

> **Nota:** Este documento refere-se apenas à camada de interface (Client-side). A documentação da API e Banco de Dados encontra-se na seção de Backend.

---

## 🖼️ Visão Geral

O projeto foi construído com um design system personalizado, focado em usabilidade e clareza visual. A aplicação consome uma API RESTful e gerencia o estado da sessão do usuário.

### Principais Tecnologias
* **Vue.js 2**: Framework JavaScript progressivo.
* **Vue Router**: Gerenciamento de rotas e navegação.
* **Axios**: Cliente HTTP para comunicação com o Backend.
* **CSS Scoped**: Estilização modular e responsiva (Design System próprio).

---

## ✨ Funcionalidades do Frontend

### 🔐 Autenticação e Segurança
* **Login de Usuário**: Interface de acesso com validação de credenciais.
* **Controle de Sessão**: Persistência de login utilizando Cookies seguros (`HttpOnly` via Backend) e armazenamento local de metadados do usuário.
* **Logout**: Encerramento seguro da sessão.
* **Controle de Acesso (RBAC)**: A interface se adapta dinamicamente dependendo do nível do usuário (**Admin**, **Gerente** ou **Peão/Membro**), ocultando ou exibindo botões de edição e exclusão.

### 📊 Dashboard (Kanban)
* **Visualização de Tarefas**: Organização visual em três colunas: *A Fazer*, *Em Execução* e *Concluída*.
* **Mudança de Status**: Atualização rápida do status da tarefa via dropdown direto no card.
* **Indicadores**: Contadores automáticos de tarefas por status.
* **Ações Rápidas**: Botões de Editar e Excluir tarefas diretamente no card (para usuários autorizados).

### 👥 Gestão de Membros e Equipes
* **CRUD Completo**: Interfaces para Criar, Ler, Atualizar e Deletar Equipes e Membros.
* **Associação**: Vínculo inteligente de membros a equipes específicas através de menus de seleção dinâmicos.
* **Listagem com Filtros**: Tabelas responsivas com badges coloridos para identificar níveis de permissão (Admin, Gerente, etc.).

### 📝 Gestão de Tarefas
* **Criação Detalhada**: Formulários para adicionar tarefas com nome, descrição, prazo, equipe e membro responsável.
* **Edição**: Carregamento automático dos dados atuais da tarefa para atualização.

---

## 🔧 Pré-requisitos

Antes de começar, certifique-se de ter instalado em sua máquina:
* [Node.js](https://nodejs.org/) (Versão 12 ou superior)
* [NPM](https://www.npmjs.com/) ou Yarn.

---

## 🚀 Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto/frontend
    ```

2.  **Instale as dependências:**
    ```bash
    npm install
    ```

3.  **Configure a API:**
    Verifique o arquivo `src/api.js`. Certifique-se de que a `baseURL` aponta para o endereço correto do seu Backend (Python/Flask).
    ```javascript
    // Exemplo em src/api.js
    baseURL: '[http://127.0.0.1:5000](http://127.0.0.1:5000)'
    ```

4.  **Execute o servidor de desenvolvimento:**
    ```bash
    npm run serve
    ```

5.  **Acesse a aplicação:**
    Abra o navegador em `http://localhost:8080` (ou o endereço indicado no terminal).

### Comandos Úteis
* `npm run lint -- --fix`: Verifica e corrige erros de estilo de código (ESLint).
* `npm run build`: Gera a versão de produção na pasta `dist`.

---

## 📱 Screenshots

*(Adicione aqui os prints das telas do seu projeto)*

| Login | Dashboard |
|-------|-----------|
| ![Login](./screenshots/login.png) | ![Dashboard](./screenshots/dashboard.png) |

| Gestão de Membros | Edição de Tarefa |
|-------|-----------|
| ![Membros](./screenshots/membros.png) | ![Editar](./screenshots/edit.png) |

---

# ⚙️ Backend (API)

*(Espaço reservado para a documentação do Python/Flask/MongoDB)*
...