# Configuração e reprodução do projeto

## 1. Escopo deste guia

Este documento explica como preparar o ambiente Python e configurar a conexão com PostgreSQL para explorar os artefatos publicados no repositório.

**Limitação importante da versão publicada:** o repositório não inclui os arquivos brutos da SENATRAN/FENABRAVE, um backup PostgreSQL, nem scripts SQL/ETL completos para recriar automaticamente as tabelas, dimensões e views. Portanto, clonar o repositório e instalar as dependências não é suficiente para reconstruir integralmente o banco utilizado nos dashboards.

Os resultados e a arquitetura estão documentados para transparência e avaliação técnica. A reprodução integral do banco depende da obtenção das fontes originais e da reconstrução da camada de dados, que não está automatizada nesta versão.

## 2. Requisitos

- Git
- Python compatível com as versões declaradas em `requirements.txt`
- PostgreSQL (o projeto foi desenvolvido e validado com PostgreSQL 18.6)
- Acesso aos arquivos de dados oficiais utilizados nas análises
- Metabase para explorar os dashboards, caso tenha acesso a uma instância configurada

## 3. Clonar e preparar o ambiente Python

```bash
git clone https://github.com/adnilsonpessona/inteligencia-comercial-mercado-automotivo.git
cd inteligencia-comercial-mercado-automotivo

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No Windows PowerShell, ative o ambiente com:

```powershell
.venv\\Scripts\\Activate.ps1
```

## 4. Configurar a conexão PostgreSQL

Copie o modelo de variáveis de ambiente:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com os dados da sua instalação PostgreSQL:

- `DB_USER`: usuário do banco.
- `DB_PASSWORD`: senha do usuário.
- `DB_HOST`: endereço do servidor, normalmente `localhost`.
- `DB_PORT`: porta PostgreSQL, normalmente `5432`.
- `DB_NAME`: nome do banco, neste projeto `projeto_automotivo`.

O arquivo `.env` contém credenciais e é ignorado pelo Git. Não publique esse arquivo nem inclua senhas em notebooks.

## 5. Validar a conexão

Com o ambiente virtual ativado e o arquivo `.env` preenchido, execute na raiz do repositório:

```bash
python -c "from src.database import criar_engine; e=criar_engine(); c=e.connect(); print(c.exec_driver_sql('SELECT current_database()').scalar()); c.close(); e.dispose()"
```

O comando deve imprimir o nome do banco configurado. Isso valida a conexão, mas não cria as tabelas ou views analíticas.

## 6. Fontes de dados

Consulte as fontes oficiais para obter os arquivos correspondentes ao período documentado:

- [SENATRAN — Ministério dos Transportes](https://www.gov.br/transportes/pt-br/assuntos/transito)
- [FENABRAVE](https://fenabrave.org.br/)

A seleção dos arquivos, o período e as regras de interpretação estão descritos nos notebooks, nas análises e na documentação de qualidade.

## 7. Estrutura analítica esperada

O banco utilizado pelo projeto contém os schemas `staging` e `analytics`. A camada analítica documenta as tabelas fato, dimensões e views:

- [Modelo dimensional](arquitetura/modelo_dimensional.md)
- [Camada analítica e inventário de views](arquitetura/camada_analitica.md)
- [Auditoria FENABRAVE](qualidade/auditoria_fenabrave.md)

**Atenção:** os documentos descrevem a estrutura implementada e validada no ambiente original, mas não substituem scripts DDL ou um backup restaurável. A criação de um processo reproduzível de carga e reconstrução do banco fica como evolução futura.

## 8. Dashboards

Os quatro dashboards desta versão foram construídos no Metabase. As capturas de tela estão disponíveis em [docs/images](images/).

O repositório contém imagens ilustrativas dos dashboards, não uma exportação/importação da configuração do Metabase. Para reproduzir os painéis, é necessário ter o banco e as views disponíveis e recriar as perguntas e visualizações na instância Metabase.

## 9. Segurança

- Nunca compartilhe o arquivo `.env`.
- Não versione credenciais, dumps ou dados brutos restritos.
- Utilize credenciais com permissões mínimas necessárias.
- Revise os arquivos antes de publicar alterações no GitHub.
