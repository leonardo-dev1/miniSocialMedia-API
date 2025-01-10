# Mini-Twitter API

### Sobre o Projeto

- Este projeto é uma API que simula um mini-twitter, permitindo que os usuarios registram-se, façam login, criem publicações, criem comentarios nelas e tenha uma interação básica.

### Funcionalidades Principais

- Registro de Usuários: Permite que novos usuarios registrem no sistema com um usuario e senha.

- Login de Usuários: Permite que usuários cadastrados façam login com o seu usuario e senha.

- Gerenciamento de Publicações: Permite o usuário criar, editar e excluir suas publicações.

- gerenciamento de Comentarios: permite o usuario criar, editar e excluir seus comentarios feito em uma publicação.

- Autenticação e Autorização: A API usa a autenticação JWT, garantindo que o usuario realize ações apenas com seus próprios dados e para garantir mais segurança de dados.

## Instalação e Execução

### 1. Clone o Repositório.

- git clone (url)

### 2. Acesse o Projeto.

- cd mini-twitter-api

### 3. Crie um Ambiente Virtual.

- python -m venv venv

### 4. Ative o Ambiente Virtual.

- Windows: .\venv\Scripts\Activate
 Linux: source venv/bin/activate.bat

### 5. Instale as Requisições.

- pip install -r requirements.txt

### 6. Configure o Banco de Dados.

- python manage.py migrate

### 7. Inicie o Servidor Localmente.

- python manage.py runserver

rota principal da api: http://127.0.0.1:8000/

## Dependência da API

Principais bibliotecas utilizadas:

- Django.
- Django Rest Framework.
- JWT Authentication (djangorestframework-simplejwt).
- Swagger (drf-yasg).

## Documentação da API

A API utiliza o swagger como forma de documentação do prjeto.

### Para Acessar o Swagger

1. inicie a aplicação:
python manage.py runserver

2. acesse o endpoint:
http://127.0.0.1:8000/swagger/

### Endpoints Principais

#### Usuários

- GET /usuarios/: lista todos os usuarios cadastrados.
- POST /register/: registrar novos usuarios.
- POST /login/: login e retorna o token nos cookies do navegador.

#### Postagens

- GET /postagens/: lista de todas as postagens de todos os usuarios
- POST /postagens/: permite criar postagens.

- GET /usuario/<int:pk>/feed/: retorna todas as publicações feitas por um usuario
- PUT/PATCH/DELETE /postagens/<int:pk>/editar/: retorna a postagem que deseja editar e excluir, apenas o dono da publicação e admins podem editar e excluir.

#### Comentários

- GET /comentarios/: lista de todos os comentarios de todos os usuarios
- POST /comentario/: permite criar um comentario.

- GET /postagem/<int:pk>/comentarios/: retorna todos os comentários de uma publicação.
- PUT/PATCH/DELETE /comentario/<int:pk>/editar/: retorna o comentario que deseja editar e excluir, apenas o dono do comentario e admins podem editar e excluir.