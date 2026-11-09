# Análise da Frota por Tipo de Veículo

## 1. Objetivo

Analisar a composição e a evolução da frota brasileira de automóveis e veículos comerciais leves, identificando diferenças de participação e crescimento entre os tipos de veículos.

## 2. Escopo e metodologia

- **Fonte:** SENATRAN — frota por UF, município, tipo, espécie e eixos.
- **Período:** janeiro de 2025 a setembro de 2026.
- **Tipos incluídos:** AUTOMOVEL, CAMINHONETE, CAMIONETA e UTILITARIO.
- **Indicador:** quantidade de veículos registrados na frota em cada competência.
- **Comparação interanual:** setembro de 2026 contra setembro de 2025.
- **Participação:** quantidade de veículos do tipo dividida pela frota total da competência.
- **Aumento do período:** diferença entre o estoque de janeiro de 2025 e o estoque de setembro de 2026.

A variação da frota representa uma mudança no estoque de veículos registrados. Não deve ser interpretada como quantidade de emplacamentos no período.

## 3. Comparativo por tipo

| Tipo | Frota set/2025 | Frota set/2026 | Crescimento absoluto | Crescimento interanual | Participação jan/2025 | Participação set/2026 | Variação da participação |
|---|---:|---:|---:|---:|---:|---:|---:|
| Automóvel | 64.410.967 | 66.145.154 | 1.734.187 | 2,69% | 79,31% | 78,18% | -1,13 p.p. |
| Caminhonete | 9.991.137 | 10.574.406 | 583.269 | 5,84% | 12,04% | 12,50% | +0,46 p.p. |
| Camioneta | 5.275.144 | 5.563.084 | 287.940 | 5,46% | 6,39% | 6,58% | +0,19 p.p. |
| Utilitário | 1.982.104 | 2.324.956 | 342.852 | 17,30% | 2,26% | 2,75% | +0,49 p.p. |

## 4. Crescimento absoluto e contribuição

O crescimento interanual da frota entre setembro de 2025 e setembro de 2026 foi de **2.948.248 veículos**.

| Tipo | Crescimento absoluto | Contribuição para o crescimento |
|---|---:|---:|
| Automóvel | 1.734.187 | 58,82% |
| Caminhonete | 583.269 | 19,78% |
| Utilitário | 342.852 | 11,63% |
| Camioneta | 287.940 | 9,77% |

O aumento do estoque entre janeiro de 2025 e setembro de 2026 foi de **4.584.170 veículos**.

## 5. Principais resultados

### 5.1 Automóveis

Os automóveis mantêm a maior participação na frota, com 78,18% em setembro de 2026. Embora tenham apresentado crescimento interanual de 2,69%, sua participação caiu 1,13 ponto percentual em relação a janeiro de 2025.

Apesar do crescimento percentual mais moderado, foram responsáveis por 58,82% do aumento absoluto da frota no comparativo entre setembro de 2025 e setembro de 2026.

### 5.2 Utilitários

Os utilitários apresentaram o maior crescimento percentual interanual, de 17,30%. Sua participação passou de 2,26% em janeiro de 2025 para 2,75% em setembro de 2026, um ganho de 0,49 ponto percentual.

É um segmento de menor participação, mas com expansão proporcional mais acelerada.

### 5.3 Caminhonetes

As caminhonetes cresceram 5,84% no comparativo interanual e ganharam 0,46 ponto percentual de participação entre janeiro de 2025 e setembro de 2026.

### 5.4 Camionetas

As camionetas cresceram 5,46% no comparativo interanual. Sua contribuição absoluta foi a menor entre os quatro tipos, correspondendo a 9,77% do crescimento interanual.

## 6. Rankings

**Crescimento percentual interanual:**

1. Utilitário: 17,30%
2. Caminhonete: 5,84%
3. Camioneta: 5,46%
4. Automóvel: 2,69%

**Crescimento absoluto interanual:**

1. Automóvel: 1.734.187
2. Caminhonete: 583.269
3. Utilitário: 342.852
4. Camioneta: 287.940

## 7. Validação dos dados

Foram aprovadas as nove verificações:

- 84 registros analisados.
- Quatro tipos de veículos.
- 21 competências mensais.
- Ausência de duplicidade por competência e tipo.
- Presença dos quatro tipos em todas as competências.
- Soma dos tipos igual à frota nacional em todos os meses.
- Soma das participações próxima de 100% em todas as competências.
- 36 comparações interanuais preenchidas.
- 48 comparações sem base anual anterior, correspondentes às competências de 2025.

A reconciliação mensal apresentou diferença zero entre a soma dos quatro tipos e a frota nacional nas 21 competências.

## 8. Recomendações para o Power BI

A análise pode alimentar:

- Gráfico de evolução mensal da frota por tipo.
- Gráfico de participação percentual por tipo.
- Indicadores de crescimento interanual absoluto e percentual.
- Ranking de tipos por crescimento.
- Comparação da composição da frota entre janeiro de 2025 e setembro de 2026.

Os indicadores devem distinguir crescimento absoluto, crescimento percentual e variação de participação em pontos percentuais.

## 9. Fonte analítica

Consulta baseada na tabela `analytics.fato_frota` e na dimensão `analytics.dim_tipo_veiculo`, com reconciliação dos totais contra `analytics.vw_frota_nacional_mensal`.

---
