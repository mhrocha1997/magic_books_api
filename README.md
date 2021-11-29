<h1 align="center"> Magic Books API</h1>
<p align="center"> Cadastro de Livros com código mágico e suas páginas</p>


Tabela de Conteúdos
=================

<!--ts-->
   * [Como Usar](#como-usar)
        * [Pré-requisitos](#pré-requisitos)
        * [Executando](#executando)
        * [Utilizando a Aplicação](#utilizando)
        * [Testes](#testes)
   * [O Projeto](#projeto)
        * [Estrutura do Projeto](#estrutura-do-projeto)
        * [Processo de Desenvolvimento](#processo-de-desenvolvimento)
            *[Banco de Dados](#banco-de-dados)
<!--te-->

## Como Usar

### Pré-requisitos
Para começar, você precisará ter instalado o [Docker](https://docs.docker.com/engine/install/) e o [Docker Compose](https://docs.docker.com/compose/install/).

### Executando
Com Docker e Docker Compose instalados, basta clonar este repositório, e dentro de sua pasta principal, rodar:

```bash
  docker-compose up
```

O banco de dados e a aplicação irão inicializar automaticamente.

### Utilizando a Aplicação
    O FastAPI gera uma documentação em Swagger de forma a facilitar os testes.
    Acessando `http://localhost:8000`você será redirecionado para `http://localhost:8000/docs`, onde fica o Swagger da API:\

![swagger_magic_books](https://user-images.githubusercontent.com/52762669/143844222-f5879166-b5cc-4365-b5e9-6b495ae01f63.png)

Para utilizar você deve abrir a aba da requisição que deseja realizar. Você verá o exemplo do body que é esperado (caso tenha), o que é esperado de retorno, e um botão `Try it Out`, que lhe permitirá realizar o teste, como na imagem abaixo.\

![Swagger Post Example](https://user-images.githubusercontent.com/52762669/143845672-3237baf4-1e62-418c-a376-c5f855f60ea0.png)

Ao clicar em `Try it Out` um botão `Execute` irá aparecer. Ao pressioná-lo, a requisição será feita e você poderá ver a resposta em seguida.

Caso seja necessário o `id` do objeto que será modificado, você deverá inseri-lo num campo como no exemplo:\
![id_example](https://user-images.githubusercontent.com/52762669/143933852-5833cefb-7a54-4b93-a90d-2fdb4d528fd0.png)


### Testes

Para executar os testes, primeiro você deve deixar a aplicação em execução como descrito em [Executando](#executando).
Em seguida, rode o seguinte comando: 

```bash
    docker exec -it magic-books-container pytest -o log_cli=True
```

Será possível visualizar o que está sendo testado em cada etapa e seu resultado no terminal.

## O Projeto

### Estrutura
```
app/
├── __init__.py
├── controllers/
│   ├── endpoints/
│   │   ├── books.py
│   │   └── pages.py
│   └── routes.py
├── database/
│   ├── connection.py
│   └── models.py
├── Dockerfile
├── main.py
├── requirements.txt
├── schemas.py
├── services/
│   ├── books.py
│   └── pages.py
├── test_setup.py
└── tests/
    ├── __init__.py
    ├── test_books.py
    └── test_pages.py
```

Dentro de `app`, o main.py instancia o router que se encontra dentro de `app/controllers`, que por sua vez inclui as rotas de Books e Pages dentro de `app/controllers/endpoints`, com suas respectivas tags e prefixos.

Os controllers, que definem os endpoints da aplicação, executam as operações que encontram-se dentro de `app/services`. Dentro de cada serviço encontra-se os CRUDs da API, além de outras funções auxilares, como a de geração do Código Mágico do livro.

Dentro de `app/database` encontra se o script de conexão com o banco de dados em `connection.py` e os modelos em `models.py` que definem as tabelas e relacionamentos.

Em `app/tests` encontram-se os testes de Books e Pages que serão executados como descrito em [Testes](#testes). O `test_setup.py` possibilita que as importações funcionem corretamente durante a execução dos testes.

Dessa forma, o projeto toma uma forma modular, facilitando manutenções futuras e também o entendimento da estrutura.
### Banco de Dados
Requisito: Criação de Livros com 6 páginas contendo texto e imagem.

Para isso, partiu-se do seguinte moedlo para desenvolvimento da aplicação.\
![database](https://user-images.githubusercontent.com/52762669/143943647-bffdb912-c033-46b8-8f88-4291377de475.png)

As Páginas foram criadas como uma entidade separada dos Livros, por, além de possuir seus próprios atributos de texto e imagem, também isolar cada alteração que o usuário poderá realizar.

Dessa forma é possível editar, deletar, e criar somente uma página por vez, não tendo assim a necessidade de, para que uma única página fosse atualizada, fazer a requisição atualizando a entidade Livro inteira.

### Processo de Desenvolvimento
#### Dia 1:
    * Criação das funcionalidades básicas: cadastro de livro e página, busca de livro pelo Código Mágico.
    * Entendimento implementação do ORM SQLAlchemy.
    * Criação do Dockerfile e docker-compose
Durante essa fase, o foco foi implementar as funções básicas requisitadas. O principal trabalho foi de ler a documentação, tanto do FastAPI quanto do SQLAlchemy para conectar a aplicação ao banco de dados (rodando em um container Docker) e realização das operações no Banco de Dados da Aplicação.

#### Dia 2:
    * Melhorias na estrutura do projeto, separando endpoints e services.
    * Implementação do CRUD de Páginas e Livros.
    * Utilização de Schemas para formatação da resposta.
    * Tratamento de Exceções.

Além do desenvolvimento das rotas de Update e Delete, o foco desse dia foi melhorar o projeto como um todo, pesquisando qual a melhor estrutura para um projeto em FastAPI e seguindo a documentação para implementar os Schemas. Uma vez implementado, foi possível corrigir diversas respostas de `endpoints` que não estavam antes no formato adequado. 
AS exceções foram feitas da seguinte forma: caso seja recebida uma `HTTPException`, ele irá retorná-la. Caso contrário, ele retorna um erro com Status Code 400, representando um erro interno não previsto.\
![exceptions](https://user-images.githubusercontent.com/52762669/143947585-1aa2492c-eab8-4f21-b2ae-2d3234fbd8cb.png)


#### Dia 3: 
    * Implementação de Testes.
    * Documentação deste README.

A principal saída dessa etapa foram os testes, que foram implementados de forma a testar cada `endpoint` separadamente, dado que é uma API simples e não há muitas funções além dos serviços de CRUD e geração do Código Mágico. Dada a importância da realização de testes, eles de fato permitiram identificar e corrigir alguns erros que não haviam sido gerados anteriormente.
