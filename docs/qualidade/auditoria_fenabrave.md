# Auditoria das bases de comparação — FENABRAVE

**Projeto:** Inteligência Comercial do Mercado Automotivo Brasileiro
**Data do registro:** 09/11/2026
**Período auditado:** janeiro a setembro de 2026
**Categoria:** Autos + Com. Leves

## 1. Objetivo

Verificar a consistência entre os volumes mensais de 2025 armazenados na série histórica da FENABRAVE e os valores de referência de 2025 publicados nos relatórios mensais de 2026.

A auditoria busca identificar diferenças entre as bases utilizadas no cálculo da variação anual, sem pressupor que uma das fontes esteja incorreta.

## 2. Resultado da comparação

A comparação foi realizada para os nove meses equivalentes, de janeiro a setembro.

| Mês | Série 2025 | Referência publicada 2025 | Diferença | Variação pela série (%) | Variação publicada (%) |
|---|---:|---:|---:|---:|---:|
| Janeiro | 159.846 | 159.862 | 16 | 1,65 | 1,64 |
| Fevereiro | 173.809 | 173.840 | 31 | 1,72 | 1,70 |
| Março | 184.046 | 184.141 | 95 | 40,30 | 40,23 |
| Abril | 197.053 | 197.129 | 76 | 20,40 | 20,36 |
| Maio | 214.357 | 214.408 | 51 | 23,18 | 23,15 |
| Junho | 202.164 | 202.199 | 35 | 28,84 | 28,82 |
| Julho | 229.948 | 229.967 | 19 | 15,55 | 15,54 |
| Agosto | 214.490 | 214.439 | -51 | 22,64 | 22,67 |
| Setembro | 231.370 | 231.330 | -40 | 16,14 | 16,16 |

A diferença é calculada como:

`referencia_2025_publicada - emplacamentos_2025_serie`

## 3. Síntese da auditoria

- Meses auditados: 9.
- Meses com referências diferentes: 9.
- Soma das diferenças absolutas: 414 veículos.
- Diferença líquida (referência publicada menos série histórica): 232 veículos.
- Maior diferença absoluta: março, com 95 veículos.
- De janeiro a julho, as referências publicadas são maiores que os valores da série histórica.
- Em agosto e setembro, as referências publicadas são menores.

As diferenças são pequenas em relação aos volumes mensais, mas produzem divergências nos percentuais de variação anual.

## 4. Interpretação metodológica

Foram identificadas duas bases de comparação:

**Variação calculada pela série histórica**

Compara o volume mensal de 2026 com o volume do mês equivalente de 2025 armazenado na série histórica utilizada pelo projeto.

**Variação anual publicada**

Corresponde ao percentual informado diretamente pela FENABRAVE no relatório mensal de 2026, utilizando a referência de 2025 apresentada naquele relatório.

Os resultados não são necessariamente idênticos porque os valores de referência de 2025 diferem entre as duas bases.

A auditoria identifica a divergência, mas não determina sua causa. Não há evidência suficiente nesta análise para atribuí-la a revisões, ajustes ou outro procedimento específico da fonte.

## 5. Decisão para o projeto

1. Preservar os volumes mensais de 2025 da série histórica.
2. Preservar os valores de referência de 2025 publicados nos relatórios de 2026.
3. Manter `variacao_anual_pct` como indicador publicado pela FENABRAVE.
4. Não sobrescrever nem recalcular o indicador publicado para forçar igualdade com a série histórica.
5. Utilizar a série histórica quando a análise exigir comparação calculada diretamente entre competências.
6. Utilizar o percentual publicado quando o objetivo for reproduzir o indicador divulgado pela FENABRAVE.
7. Informar a existência dessa diferença em análises ou apresentações nas quais a distinção seja relevante.

## 6. Impacto na arquitetura de dados

A auditoria não identificou necessidade de alteração estrutural nas tabelas ou views existentes.

Permanecem preservadas:

- `analytics.fato_emplacamentos`
- `analytics.vw_emplacamentos_nacionais_mensais`

A estrutura atual mantém os valores publicados e os volumes mensais da série histórica necessários para distinguir as duas referências.

**Conclusão:** divergência documentada, dados preservados e nenhuma correção estrutural necessária.
