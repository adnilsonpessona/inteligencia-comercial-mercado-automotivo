# Modelo Dimensional — Inteligência Comercial do Mercado Automotivo Brasileiro

## 1. Objetivo

Este documento descreve a estrutura dimensional implementada no schema
`analytics` do banco PostgreSQL `projeto_automotivo`.

O modelo integra duas fontes oficiais:

- **SENATRAN:** informações mensais sobre o estoque de veículos registrados.
- **FENABRAVE:** informações mensais sobre o fluxo de emplacamentos.

A estrutura foi projetada para permitir análises comerciais do mercado
brasileiro de automóveis e comerciais leves, com posterior consumo no Power BI.

## 2. Escopo analítico

### 2.1 Categorias de veículos

Na análise principal, o escopo contempla:

| Fonte | Categorias incluídas |
|---|---|
| SENATRAN | AUTOMOVEL, CAMINHONETE, CAMIONETA e UTILITARIO |
| FENABRAVE | Autos, Com. Leves e Autos + Com. Leves |

Motocicletas, caminhões, ônibus, implementos e demais categorias fora
do escopo não integram a análise principal.

Na FENABRAVE, `Autos + Com. Leves` é uma categoria consolidada publicada
pela fonte. Para agregados nacionais, deve-se utilizar essa categoria,
sem somá-la novamente às categorias componentes.

### 2.2 Período

O período integrado compreende janeiro de 2025 a setembro de 2026,
totalizando 21 competências mensais.

Comparações interanuais devem considerar somente meses equivalentes
entre 2025 e 2026.

### 2.3 Abrangência geográfica

A análise geográfica da primeira versão utiliza Unidade Federativa (UF)
e região.

O município permanece armazenado na tabela fato da SENATRAN para
preservar a granularidade e a rastreabilidade da fonte, mas não será
utilizado como dimensão de análise na primeira versão do Power BI.

## 3. Arquitetura

O schema `analytics` contém seis tabelas:

### 3.1 Dimensões

| Tabela | Finalidade | Registros |
|---|---|---:|
| dim_calendario | Competências mensais e atributos temporais | 21 |
| dim_uf | Unidades Federativas e regiões | 28 |
| dim_tipo_veiculo | Tipos de veículos SENATRAN | 4 |
| dim_especie_veiculo | Espécies de veículos SENATRAN | 8 |

A dimensão `dim_uf` contém 27 UFs e o registro SI (Sem Informação).

### 3.2 Tabelas fato

| Tabela | Finalidade | Registros |
|---|---|---:|
| fato_frota | Estoque mensal de veículos registrados | 1.998.557 |
| fato_emplacamentos | Emplacamentos mensais publicados pela FENABRAVE | 63 |

## 4. Granularidade das tabelas fato

### 4.1 fato_frota

Representa o estoque de veículos registrados por competência, UF, município, tipo de veículo, espécie e quantidade de eixos.

Sua granularidade física é uma linha por combinação de:

- data_referencia;
- id_uf;
- municipio;
- id_tipo_veiculo;
- id_especie_veiculo;
- eixos.

A quantidade de veículos é armazenada em `qtd_veiculos`, do tipo `bigint`.

Chave primária composta:

    PRIMARY KEY (data_referencia, id_uf, municipio, id_tipo_veiculo, id_especie_veiculo, eixos)

A medida representa estoque na data de referência mensal. Variações entre competências não devem ser denominadas emplacamentos.

### 4.2 fato_emplacamentos

Representa os volumes mensais de emplacamentos publicados pela FENABRAVE, por competência e categoria.

Sua granularidade é uma linha por combinação de competência e categoria.

Chave primária composta:

    PRIMARY KEY (competencia, categoria)

A tabela mantém os valores mensais, valores de comparação e percentuais publicados pela fonte:

- emplacamentos_mes;
- emplacamentos_mes_anterior;
- emplacamentos_acumulados;
- emplacamentos_mes_ano_anterior;
- emplacamentos_acumulados_ano_anterior;
- variacao_mensal_pct;
- variacao_anual_pct;
- variacao_acumulada_pct.

Os valores acumulados e os valores de comparação publicados são preservados conforme a fonte, sem forçar reconciliação com a soma da série mensal.

## 5. Chaves e relacionamentos

O modelo possui seis chaves primárias e cinco chaves estrangeiras.

### 5.1 Chaves primárias

| Tabela | Colunas |
|---|---|
| dim_calendario | competencia |
| dim_uf | id_uf |
| dim_tipo_veiculo | id_tipo_veiculo |
| dim_especie_veiculo | id_especie_veiculo |
| fato_frota | data_referencia, id_uf, municipio, id_tipo_veiculo, id_especie_veiculo, eixos |
| fato_emplacamentos | competencia, categoria |

### 5.2 Chaves estrangeiras

| Tabela fato | Coluna de origem | Dimensão | Coluna referenciada |
|---|---|---|---|
| fato_frota | data_referencia | dim_calendario | competencia |
| fato_frota | id_uf | dim_uf | id_uf |
| fato_frota | id_tipo_veiculo | dim_tipo_veiculo | id_tipo_veiculo |
| fato_frota | id_especie_veiculo | dim_especie_veiculo | id_especie_veiculo |
| fato_emplacamentos | competencia | dim_calendario | competencia |

### 5.3 Cardinalidade e direção de filtro

Todos os relacionamentos são do tipo um-para-muitos (1:*).

A dimensão ocupa o lado 1 e a tabela fato ocupa o lado muitos.

As chaves estrangeiras garantem a integridade referencial no PostgreSQL. Na camada semântica do Power BI, recomenda-se configurar os relacionamentos com direção de filtro unidirecional, da dimensão para a tabela fato.

Não devem ser criados relacionamentos diretos entre as duas tabelas fato.

## 6. Regras de negócio e interpretação

### 6.1 Estoque e fluxo

- SENATRAN representa estoque de veículos registrados em uma data de referência mensal.
- FENABRAVE representa fluxo de emplacamentos durante um período.
- Variação da frota não equivale a volume de emplacamentos.
- As duas fontes devem permanecer em tabelas fato separadas.

### 6.2 Comparação interanual

As comparações YoY devem utilizar competências equivalentes: janeiro de 2025 com janeiro de 2026, fevereiro com fevereiro e assim sucessivamente, até setembro.

### 6.3 Categoria consolidada FENABRAVE

`Autos + Com. Leves` é o consolidado publicado pela FENABRAVE.

Para indicadores nacionais consolidados, utilizar diretamente essa categoria. Não somar o consolidado novamente a Autos e Com. Leves.

### 6.4 Município

O atributo `municipio` é mantido fisicamente em `fato_frota`, mas fica fora da experiência analítica da primeira versão.

Não será criada uma dimensão municipal nesta etapa.

### 6.5 Eixos

O atributo `eixos` é mantido na granularidade física da fato_frota para preservar a informação original.

Não constitui dimensão analítica prioritária da primeira versão.

## 7. Integridade e qualidade dos dados

As verificações realizadas no banco confirmaram:

- 21 competências na dimensão calendário.
- 1.998.557 registros na fato_frota.
- 63 registros na fato_emplacamentos.
- Ausência de chaves primárias duplicadas.
- Ausência de valores nulos nas colunas obrigatórias.
- Ausência de registros órfãos nas relações verificadas.
- Correspondência de todas as competências das tabelas fato com a dimensão calendário.
- Correspondência dos identificadores de UF, tipo e espécie com suas respectivas dimensões.
- 21 de 21 consolidações mensais da FENABRAVE validadas pela soma das categorias componentes.
- 63 de 63 percentuais publicados da FENABRAVE conferidos por recálculo, dentro da tolerância de 0,02 ponto percentual.

As restrições físicas incluem chaves primárias, estrangeiras, unicidade, obrigatoriedade e regras CHECK.

Uma anomalia identificada no atributo `eixos` em fevereiro de 2026 foi documentada e preservada, sem correção arbitrária dos dados de origem.

## 8. Orientações para o modelo semântico Power BI

Na construção do modelo semântico:

1. Manter as duas tabelas fato separadas.
2. Relacionar cada fato às dimensões correspondentes.
3. Utilizar direção de filtro unidirecional, dimensão para fato.
4. Ocultar o campo `municipio` na primeira versão.
5. Não disponibilizar `eixos` como atributo prioritário de análise.
6. Utilizar a categoria consolidada da FENABRAVE nos indicadores nacionais de Autos + Com. Leves.
7. Diferenciar claramente medidas de estoque e medidas de fluxo.
8. Utilizar a dimensão calendário para filtros e comparações temporais.

## 9. Evolução futura

Possíveis evoluções, condicionadas à necessidade analítica e à disponibilidade de dados:

- Inclusão de uma dimensão municipal, caso a análise municipal passe a fazer parte do escopo.
- Ampliação do histórico de competências.
- Inclusão de novas fontes oficiais.
- Expansão das análises comerciais e indicadores derivados.
- Revisão da camada semântica conforme novas necessidades de negócio.

## 10. Artefatos relacionados

- `diagrama_modelo.mmd`: representação Mermaid do modelo físico.
- `modelo_dimensional.md`: documentação técnica do modelo dimensional.
