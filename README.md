## **Guias de administração e instalação das ferramentas**
[Link para os guias do e-Democracia](http://www.edemocracia.leg.br/#links)

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

## **Colocando em Produção**

### Requisitos

* Docker versão 1.10.0 ou superior
* Servidor de aplicação (nginx ou apache, por exemplo)

### Arquivo de Configuração

Você pode personalizar a sua instalação do e-Democracia alterando as variáveis de ambiente do `docker-compose.yml`. No repositório, colocamos um exemplo para produção: `docker-compose.production.yml`. Algumas variáveis devem, obrigatoriamente, ser alteradas para o contexto da sua instância. Abaixo, temos a relação de variáveis que podem ser alteradas, organizadas por serviço:

#### nginx

|Variável|Descrição|Obrigatório|
|---|---|---|
|NAME_RESOLVER|Utilizado para resolver os nomes dentro da rede do docker-compose.| Não|

### db

|Variável|Descrição|Obrigatório|
|---|---|---|
|POSTGRES_PASSWORD|Senha do usuário root no banco de dados|Não|

### edemocracia

|Variável|Descrição|Obrigatório|
|---|---|---|
|ADMIN_EMAIL|Email da conta de admin|Sim|
|ADMIN_PASSWORD|Senha da conta de admin|Sim|
|ADMIN_USERNAME|Nome de usuário da conta de admin|Sim|
|SITE_NAME|Nome do site|Sim|
|SITE_LOGO|URL da logo do site|Não|
|SITE_URL|URL do site|Sim|
|SECRET_KEY|Chave utilizada para criptografar as senhas|Sim|
|RECAPTCHA_SITE_KEY|Chave pública do reCAPTCHA|Sim|
|RECAPTCHA_PRIVATE_KEY|Chave privada do reCAPTCHA|Sim|
|ALLOWED_HOSTS|Lista de hostnames permitidos para acessar a aplicação, separados por vírgulas. É importante conter o domínio da sua instância, por exemplo: `edemocracia.camara.leg.br`|Sim|
|DATABASE_PASSWORD|Senha do banco de dados. Deve ser a mesma do serviço anterior|Sim|
|SOCIAL_AUTH_GOOGLE_OAUTH2_KEY|Chave pública para login social com Google|Sim|
|SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET|Chave privada para login social com Google|Sim|
|SOCIAL_AUTH_FACEBOOK_KEY|Chave pública para login social com Facebook|Sim|
|SOCIAL_AUTH_FACEBOOK_SECRET|Chave privada para login social com FAcebook|Sim|
|SOCIAL_AUTH_CD_KEY|Chave pública para login social com login único da Câmara dos Deputados|Não|
|SOCIAL_AUTH_CD_SECRET|Chave privada para login social com login único da Câmara dos Deputados|Não|
|SOCIAL_AUTH_CD_VERIFY_SSL|Boleano. Verificar SSL no login com login único da Câmara dos Deputados|Não|
|CD_AUTHORIZATION_URL|URL de autorização do login único da Câmara| Não|
|CD_ACCESS_TOKEN_URL|URL do token de acesso do login único da Câmara| Não|
|CD_METADATA_URL|URL de metadata do login único da Câmara| Não|
|SOCIAL_AUTH_REDIRECT_IS_HTTPS|Boleano. `True`se utilizar HTTPS| Não|
|EMAIL_HOST|Host do servidor de email|Sim|
|EMAIL_PORT|Porta do servidor de email|Sim|
|EMAIL_HOST_USER|Usuário do servidor de email|Sim|
|EMAIL_HOST_PASSWORD|Senha do usuário acima|Sim|
|EMAIL_USE_TLS|Boleano. `True` se o servidor de email utililizar TLS|Sim|
|DEFAULT_FROM_EMAIL|Remetente do email no formato `'Nome do Remetente <email@do.remetente>'`|Sim|
|WIKILEGIS_ENABLED|Boleano. `True`se quiser ativar o Wikilegis no e-Democracia|Sim|
|WIKILEGIS_API_KEY|Chave da API do Wikilegis|Não|
|AUDIENCIAS_ENABLED|Boleano. `True`se quiser ativar o Audiencias no e-Democracia|Sim|
|AUDIENCIAS_API_KEY|Chave da API do Audiencias|Não|
|DISCOURSE_ENABLED|Boleano. `True`se quiser ativar o Expressão (Discourse) no e-Democracia|Sim|
|DISCOURSE_SSO_SECRET|Chave de login SSO do Discourse|Não|

### wikilegis

|Variável|Descrição|Obrigatório|
|---|---|---|
|ADMIN_EMAIL|Email da conta de admin|Sim|
|ADMIN_PASSWORD|Senha da conta de admin|Sim|
|API_KEY|Chave da API|Sim|
|SECRET_KEY|Chave utilizada para criptografar as senhas|Sim|
|EMAIL_HOST|Host do servidor de email|Sim|
|EMAIL_PORT|Porta do servidor de email|Sim|
|EMAIL_HOST_USER|Usuário do servidor de email|Sim|
|EMAIL_HOST_PASSWORD|Senha do usuário acima|Sim|
|EMAIL_USE_TLS|Boleano. `True` se o servidor de email utililizar TLS|Sim|
|DEFAULT_FROM_EMAIL|Remetente do email|Não|
|DATABASE_PASSWORD|Senha do banco de dados. Deve ser a mesma do serviço anterior|Sim|

### audienciasweb e audienciasworker

|Variável|Descrição|Obrigatório|
|---|---|---|
|ADMIN_EMAIL|Email da conta de admin|Sim|
|ADMIN_PASSWORD|Senha da conta de admin|Sim|
|ADMIN_USERNAME|Nome de usuário da conta de admin|Sim|
|DJANGO_SECRET_KEY|Chave utilizada para criptografar as senhas e chave da API|Sim|
|EMAIL_HOST|Host do servidor de email|Sim|
|EMAIL_PORT|Porta do servidor de email|Sim|
|EMAIL_HOST_USER|Usuário do servidor de email|Sim|
|EMAIL_HOST_PASSWORD|Senha do usuário acima|Sim|
|EMAIL_USE_TLS|Boleano. `True` se o servidor de email utililizar TLS|Sim|
|DEFAULT_FROM_EMAIL|Remetente do email|Não|
|DATABASE_PASSWORD|Senha do banco de dados. Deve ser a mesma do serviço anterior|Sim|
|NOTIFICATION_EMAIL_LIST|Lista de emails que serão notificados sempre que uma sala for criada separada por vírgulas.|Não|


### discourse

|Variável|Descrição|Obrigatório|
|---|---|---|
|ADMIN_EMAIL|Email da conta de admin|Sim|
|ADMIN_PASSWORD|Senha da conta de admin|Sim|
|ADMIN_USERNAME|Nome de usuário da conta de admin|Sim|
|DISCOURSE_DB_PASSWORD|Senha do banco de dados. Deve ser a mesma do serviço anterior|Sim|
|DISCOURSE_SMTP_ADDRESS|Host do servidor de email|Sim|
|DISCOURSE_SMTP_PORT|Porta do servidor de email|Sim|
|DISCOURSE_SMTP_USER_NAME|Usuário do servidor de email|Sim|
|DISCOURSE_SMTP_PASSWORD|Senha do usuário acima|Sim|


## Subindo sua instância

Após atualizar o seu arquivo de configuração, basta subir os containers utilizando o `docker-compose`:

```
docker-compose -f <caminho para o seu arquivo> up
```

O e-Democracia estará disponível na porta 8000 do servidor. Para acessá-lo de fora do servidor, é necessário configurar um servidor de aplicações como apache ou nginx, por exemplo, e direcionar as requisições da porta 80 (HTTP) para a porta 8000 (e-Democracia).
