# Camada Analítica — Inteligência Comercial do Mercado Automotivo Brasileiro

## 1. Objetivo

A camada analítica do projeto organiza os dados tratados no PostgreSQL em views destinadas à análise de negócio e à integração com o Power BI.

Seu objetivo é disponibilizar indicadores consistentes sobre:

- Evolução mensal da frota brasileira de automóveis e comerciais leves.
- Distribuição geográfica da frota por Unidade da Federação.
- Composição da frota por tipo e espécie de veículo.
- Evolução mensal dos emplacamentos de automóveis e comerciais leves.
- Comparação entre a evolução do estoque da frota e o fluxo de emplacamentos.

As views são construídas sobre as tabelas do schema `analytics`, cuja estrutura dimensional está documentada em `modelo_dimensional.md`.

## 2. Escopo analítico

### 2.1 Período

- Início: janeiro de 2025.
- Fim: setembro de 2026.
- Total: 21 competências mensais.

Outubro de 2026 é tratado como informação suplementar, fora da versão integrada principal.

### 2.2 Categorias de veículos

O escopo considera:

- AUTOMOVEL
- CAMINHONETE
- CAMIONETA
- UTILITARIO

Na fonte FENABRAVE, são utilizadas as categorias originais `Autos` e `Com. Leves`, além da categoria consolidada `Autos + Com. Leves`.

Motocicletas, caminhões, ônibus e demais categorias fora do escopo não integram as análises principais.

### 2.3 Fontes e conceitos

**SENATRAN — Frota**

Representa o estoque de veículos registrados na data de referência mensal.

Variações da frota representam crescimento ou redução do estoque. Não devem ser denominadas emplacamentos.

**FENABRAVE — Emplacamentos**

Representa o fluxo de veículos emplacados durante determinado período.

Os indicadores publicados pela entidade são preservados conforme a fonte, inclusive quando apresentam diferenças em relação a cálculos derivados da série mensal histórica.

## 3. Inventário das views

Todas as views estão no schema `analytics`.

| View | Granularidade | Registros |
|---|---|---:|
| `vw_frota_nacional_mensal` | Uma linha por competência | 21 |
| `vw_emplacamentos_nacionais_mensais` | Uma linha por competência | 21 |
| `vw_frota_uf_mensal` | Competência e UF | 588 |
| `vw_indicadores_nacionais_mensais` | Uma linha por competência | 21 |
| `vw_frota_tipo_mensal` | Competência e tipo de veículo | 84 |
| `vw_frota_especie_mensal` | Competência e espécie de veículo | 168 |

## 4. Descrição das views

### 4.1 vw_frota_nacional_mensal

Apresenta a evolução mensal da frota nacional.

**Granularidade:** uma linha por competência.

Principais campos:

- `competencia`: data de referência mensal.
- `ano`, `mes`: componentes temporais.
- `nome_mes`, `mes_abreviado`, `ano_mes`: atributos para apresentação e ordenação.
- `frota_total`: quantidade total de veículos da frota considerada.

A view consolida os registros da tabela `fato_frota`.

### 4.2 vw_emplacamentos_nacionais_mensais

Apresenta os emplacamentos nacionais mensais da categoria consolidada `Autos + Com. Leves`.

**Granularidade:** uma linha por competência.

Principais campos:

- `competencia`, `ano`, `mes`, `nome_mes`, `mes_abreviado`, `ano_mes`.
- `emplacamentos_mes`.
- `emplacamentos_mes_anterior`.
- `emplacamentos_acumulados`.
- `emplacamentos_mes_ano_anterior`.
- `emplacamentos_acumulados_ano_anterior`.
- `variacao_mensal_pct`.
- `variacao_anual_pct`.
- `variacao_acumulada_pct`.

Os valores publicados pela FENABRAVE são preservados. Não se força a reconciliação entre acumulados publicados e a soma dos valores mensais da série histórica.

### 4.3 vw_frota_uf_mensal

Apresenta a distribuição da frota por Unidade da Federação ao longo do período.

**Granularidade:** uma linha por competência e UF.

Principais campos:

- `competencia`, `ano`, `mes`.
- `id_uf`, `sigla_uf`, `nome_uf`.
- `regiao`.
- `frota_total`.

A view possui 588 registros, correspondentes a 28 identificações geográficas por 21 competências. A identificação `SI` representa registros sem informação de UF.

A análise geográfica da primeira versão utiliza UF e região, sem detalhamento municipal.

### 4.4 vw_indicadores_nacionais_mensais

Integra os indicadores nacionais de frota e emplacamentos.

**Granularidade:** uma linha por competência.

Principais campos:

- Atributos temporais.
- `frota_total`.
- Indicadores mensais, acumulados e publicados de emplacamentos.
- `variacao_frota_pct`.
- `variacao_emplacamentos_serie_pct`.
- `diferenca_frota_vs_emplacamentos_serie_pp`.
- `diferenca_frota_vs_emplacamentos_publicada_pp`.

A view permite comparar a evolução do estoque da frota com o fluxo de emplacamentos.

As diferenças em pontos percentuais devem ser interpretadas conforme a base de comparação utilizada: série mensal histórica ou variação anual publicada pela FENABRAVE.

Os indicadores interanuais calculados para 2025 permanecem nulos quando dependem de uma base de 2024 não disponível no escopo.

### 4.5 vw_frota_tipo_mensal

Apresenta a composição e a evolução da frota por tipo de veículo.

**Granularidade:** uma linha por competência e tipo.

Principais campos:

- Atributos temporais.
- `id_tipo_veiculo`, `tipo_veiculo`.
- `frota_total`.
- `participacao_pct`.
- `frota_mes_ano_anterior`.
- `crescimento_absoluto`.
- `crescimento_pct`.

A participação percentual é calculada sobre o total da frota na mesma competência.

A comparação interanual utiliza o mesmo mês do ano anterior, por meio de defasagem de 12 competências.

### 4.6 vw_frota_especie_mensal

Apresenta a composição e a evolução da frota por espécie de veículo.

**Granularidade:** uma linha por competência e espécie.

Principais campos:

- Atributos temporais.
- `id_especie_veiculo`, `especie_veiculo`.
- `frota_total`.
- `participacao_pct`.
- `frota_mes_ano_anterior`.
- `crescimento_absoluto`.
- `crescimento_pct`.

A view mantém as oito espécies existentes na dimensão, inclusive `Sem Informação`, `CORRIDA` e `TRACAO`.

A participação percentual utiliza o total da frota na mesma competência. O crescimento interanual compara competências equivalentes.

## 5. Regras metodológicas

### 5.1 Estoque versus fluxo

Frota e emplacamentos representam fenômenos diferentes:

- Frota: estoque de veículos registrados em uma data.
- Emplacamentos: fluxo de registros realizados durante um período.

Não se deve interpretar o crescimento da frota como equivalente ao volume de emplacamentos.

### 5.2 Comparação interanual

As comparações interanuais utilizam somente meses equivalentes entre 2025 e 2026.

Não há comparação interanual calculada para 2025 quando a base de 2024 não está disponível.

### 5.3 Participação percentual

Nas views por tipo e espécie, a participação é calculada dividindo a frota de cada grupo pelo total da frota na respectiva competência.

### 5.4 Crescimento

- Crescimento absoluto: diferença entre a frota atual e a frota do mesmo mês do ano anterior.
- Crescimento percentual: variação relativa entre essas duas quantidades.

### 5.5 Valores publicados

Os indicadores publicados pela FENABRAVE são preservados como fornecidos pela fonte. Diferenças entre valores publicados e valores recalculados a partir da série mensal não são corrigidas artificialmente.

## 6. Auditoria e validação

As seis views passaram pelas verificações realizadas no PostgreSQL.

### 6.1 Existência e volume

| View | Volume esperado | Resultado |
|---|---:|---|
| `vw_frota_nacional_mensal` | 21 | Aprovado |
| `vw_emplacamentos_nacionais_mensais` | 21 | Aprovado |
| `vw_frota_uf_mensal` | 588 | Aprovado |
| `vw_indicadores_nacionais_mensais` | 21 | Aprovado |
| `vw_frota_tipo_mensal` | 84 | Aprovado |
| `vw_frota_especie_mensal` | 168 | Aprovado |

### 6.2 Granularidade e consistência

- Unicidade das chaves esperadas nas seis views: aprovada.
- Reconciliação dos totais nacionais com a agregação por UF: aprovada.
- Reconciliação dos totais nacionais com a agregação por tipo: aprovada.
- Reconciliação dos totais nacionais com a agregação por espécie: aprovada.
- Integração entre as views nacionais de frota, emplacamentos e indicadores: aprovada.

Resultado: 10 de 10 verificações aprovadas.

### 6.3 Cobertura e valores nulos

- Cobertura de janeiro de 2025 a setembro de 2026 nas seis views: aprovada.
- Campos essenciais sem valores nulos: aprovado.
- Nulos em indicadores interanuais sem base de comparação: permitidos conforme a metodologia.

### 6.4 Equivalência com análises anteriores

- `vw_frota_tipo_mensal`: 9 de 9 verificações aprovadas.
- `vw_frota_especie_mensal`: 11 de 11 verificações aprovadas.

As duas views reproduzem integralmente os resultados das análises realizadas anteriormente no notebook.

## 7. Orientações para o Power BI

- Utilizar as views do schema `analytics` como fontes para os relatórios.
- Priorizar as views agregadas conforme a pergunta analítica.
- Manter a coluna `competencia` como referência temporal.
- Ordenar nomes de meses por seus respectivos números ou utilizar `ano_mes` para eixos cronológicos.
- Não somar novamente categorias consolidadas aos seus componentes.
- Não relacionar diretamente fatos independentes.
- Preservar a distinção entre estoque de frota e fluxo de emplacamentos.
- Tratar valores nulos interanuais de 2025 como ausência de base histórica, e não como zero.

A conexão será realizada ao PostgreSQL instalado no Fedora, quando o ambiente estiver acessível a partir do Windows, onde será utilizado o Power BI Desktop.

## 8. Artefatos relacionados

- `modelo_dimensional.md`: documentação do modelo dimensional.
- `diagrama_modelo.mmd`: diagrama do modelo dimensional.
- `docs/analises/analise_geografica_frota.md`: análise geográfica.
- `docs/analises/evolucao_regional_frota.md`: evolução regional.
- `docs/analises/analise_frota_tipo_veiculo.md`: análise por tipo.
- `docs/analises/analise_frota_especie_veiculo.md`: análise por espécie.
- `docs/qualidade/auditoria_fenabrave.md`: auditoria dos dados FENABRAVE.
