# Dock Challenge

A Dock está crescendo e expandindo seus negócios, gerando novas oportunidades de revolucionar o mercado financeiro e criar produtos diferenciados.
Nossa próxima missão é construir uma nova conta digital Dock para nossos clientes utilizarem através de endpoints, onde receberemos requisições em um novo backend que deverá gerenciar as contas e seus portadores (os donos das contas digitais).

# Tecnologias
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [PostgreSQL](https://www.postgresql.org)
- Testes Automatizados

# Instalação

Para acessar a aplicação, primeiro, clone esse repositório.
```bash
git clone https://github.com/filipenascimento98/desafio-dev-api-rest.git
```

# Variáveis de ambiente
A aplicação precisa de uma série de variáveis de ambiente. Abaixo segue algumas de exemplo para teste.
```bash
POSTGRES_DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres123
POSTGRES_DB_HOST=db
POSTGRES_DB_PORT=5432
SECRET_KEY=tdt0*xi^t7^v-fg1wj2cg4#abxg9owz2te!_wf%s5(p97nx-%0
```
Salve essas variáveis em um arquivo chamado __.env__ na raíz do diretório do projeto.

# Como usar?
Esse projeto depende do [Docker](https://www.docker.com/) e do [Docker Compose](https://docs.docker.com/compose/). Com as dependência resolvidas, navegue até o diretório do projeto que contém o arquivo __docker_compose.yml__ e execute o seguinte comando que irá buildar e executar a aplicação.
```bash
docker-compose up -d --build
```
Assim, a aplicação será iniciada em containers Docker.

# Endpoints
Os endpoints da aplicação são:
```bash
GET    /api/extract/                -->  Endpoint para consulta de extrato
POST   /api/transaction/            -->  Endpoint para saque e depósito
POST   /api/account/deactivate/     -->  Endpoint para desativar uma conta
POST   /api/account/block/          -->  Endpoint para bloquear e desbloquear uma conta
GET    /api/account/<int:document>/ -->  Endpoint para consultar os dados de uma conta
POST   /api/account/                -->  Endpoint para criação de conta
POST   /portador/                   -->  Endpoint para criação de portador
DELETE /portador/<int:document>/    -->  Endpoint para exclusão de um portador
```
Para maiores detalhes há uma documentação na aplicação que pode ser acessada por meio da url __/api/docs/__.

# Collection para utilizar no Postman
Uma collection para ser utilizada no Postman está disponível em https://drive.google.com/file/d/10STu0triyfWpqgHKXtnQq5P-Gt4GgZBq/view?usp=sharing

# Estrutura do Projeto
Foi adotada uma arquitetura MVC para este projeto com o intuito de que com a modularização fornecida pelas camadas o acoplamento com o framework fosse diminuído para que a troca de framework fosse mais fácil e rápido de ser realizada.
* Principais diretórios
    * data_access: Camada com as classes que fazem acesso a base de dados.
    * domain: Contém as classes que detenhe as regras de negócios e que acessam a camada de dados
    * view: Camada que contém as classes que implementam as endpoints onde temos recepeção das requisições.
* Demais diretórios e arquivos:
    * test: Contém os testes automatizados.
    * serializer: É um recurso do django que permiti serializar e deserializer a entrada e a saída dos dados da requisição, além de que também pode validar esses mesmos dados.
    * validators: Arquivo contendo uma classe com validações usada em algumas partes do projeto.

Os demais arquivos e pastas fazem parte do padrão de estrutura do Django.

# Testes Automatizados
## Containerizado
Se está rodando a aplicação em um container, execute os testes entrando no container. Comando para acessar o container:
```bash
docker exec -it <container-name> /bin/bash
```
Uma vez dentro do container execute:
```bash
python manage.py test
```
## Local
É possível executar os testes fora do container, para isso navegue até o diretório que contém o arquivo __manage.py__ e execute o seguinte comando. Caso acuse falta de dependência, será necessário instalar com o __pip__ as bibliotecas listadas em __requirements.txt__
```bash
python manage.py test
```