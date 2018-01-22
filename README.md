## **Configurando Ambiente de Desenvolvimento**

Primeiramente, para rodar o e-Democracia, é preciso instalar algumas dependências e o [Node.js](https://nodejs.org/en/download/) no sistema para que algumas bibliotecas funcionem adequadamente:


    sudo dnf install libxml2-devel libxslt-devel # Fedora/CentOS
    # ou
    sudo apt-get install libxml2-dev libxslt-dev

Além disso, usamos o `pipenv` para gerênciar as dependências python do projeto, então você também precisa instalá-lo:


    sudo pip install pipenv

Em seguida, basta executar o seguinte comando para instalar todas as bibliotecas:


    pipenv install --dev
    npm install

**Obs:** A configuração das outras ferramentas (Audiências Interativas, Discourse, Pauta Participativa ou Wikilegis) deve ser feita individualmente.

## **Contribuindo com o e-Democracia**
1. Faça um *fork*  do repositório (https://github.com/eDemocracia/edemocracia)
2. Faça todas as implementações necessárias no seu próprio *fork*
3. Quando terminar é só submeter um *Pull Request* para o repositório principal 😃 

Caso esteja trabalhando em uma *issue* específica, pedimos apenas para você comentar na *issue*, dizendo que começou a fazer, pra não termos problemas de duas pessoas trabalhando na mesma coisa.

Você também pode seguir nosso [Guia de Desenvolvimento](https://paper.dropbox.com/doc/Guia-de-Desenvolvimento-G4x38rz4ctNlseA4IIV4H?_tk=share_copylink).

## **Tecnologias Utilizadas**
- Python 3.6+
- Django 2.0+
- Node.js + npm

## **Arquitetura do projeto**

O e-Democracia é formado por um conjunto de 4 ferramentas: Audiências Interativas, Discourse, Pauta Participativa e Wikilegis. Cada ferramenta funciona independentemente, possuem *stacks* diferentes e são versionadas em repositórios diferentes. Para juntar tudo isso, o e-Democracia funciona como um *reverse proxy*, conforme o diagrama:

![](https://d2mxuefqeaa7sj.cloudfront.net/s_D883ADE33F36F76087DE519EA82DCF2FCD9D39CF76CEB0F810E99EB141F91A63_1516296177301_diagrama-edem.png)


Todas as requisições passam pelo e-Democracia e ele redireciona cada uma de acordo com a URL:


- `/audiencias` → Audiências Interativas
- `/pautaparticipativa` → Pauta Participativa
- `/wikilegis` → Wikilegis
- `/expressao` → Discourse

A comunicação do e-Democracia com cada aplicação é feita através de um `app` django. Cada aplicação tem seu `app` respectivo dentro do projeto do e-Democracia e dentro de cada `app` estão presentes funções de autenticação nas ferramentas (disparadas quando um usuário faz login no e-Democracia), funções para propagar as alterações nas informações dos usuários para as outras ferramentas, entre outras.
