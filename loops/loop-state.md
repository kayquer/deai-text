# Estado do goal loop de cobertura

Uma linha por rodada. Objetivo e critério de parada em `goal-cobertura.md`.

## Rodadas

| # | ID atacado | Caso criado | `--cobertura` depois | `./init.sh` depois | Nota |
|---|---|---|---|---|---|
| 0 | — | 8 casos seed | positivo 7/12 · contra-teste 0/12 | **8/8, exit 0** | harness montado; nenhum `FLAKY` na primeira rodada, `DEAI_TENTATIVAS=3`, sonnet |
| 1 | todos | 16 casos (09–24) | **positivo 12/12 · contra-teste 12/12, exit 0** | 22/24, 3 flaky | matriz fechada; 1 achado real (A-1) e 1 defeito de caso corrigido |

Cobertura no fim da rodada 0:

```
positivo:     7/12  faltam AI-2, AI-3, AI-4, AI-5, AI-12
contra-teste: 0/12  faltam todos
```

`AI-1` tem contra-teste em `en` (caso-07) e falta em `pt`. `AI-9` tem em `pt` (caso-08) e falta em
`en`. Os dois são regras bilíngues — a matriz só fecha com os dois idiomas.

### Rodada 1 — fechamento da matriz

16 casos novos (09–24): 4 positivos e 12 contra-testes. `--cobertura` passou a sair **0**:
positivo 12/12, contra-teste 12/12.

**Desvio deliberado do protocolo "um ID por rodada".** Os 16 casos foram escritos numa tacada só, e
não um por rodada. O que o protocolo protege — saber qual caso quebrou o quê — continua valendo
porque cada caso é isolável com `./init.sh <caso>`; o que se perdeu foi a cadência. Se a próxima
sessão precisar de bisect fino, o motivo de ter ficado difícil está aqui.

Contra-testes combinados (um texto prova mais de uma regra), para não pagar 18 chamadas por rodada:

| Caso | Prova que NÃO dispara | Por quê o texto é armadilha |
|---|---|---|
| 13 | `AI-1`, `AI-2` (pt) | `erro-padrão robusto` e `escalabilidade horizontal` são termo técnico |
| 14 | `AI-9`, `AI-2` (en) | `represents` literal (nó → estado), `navigate` de teclado |
| 15/16 | `AI-3` (en/pt) | `statistically significant` / `estatisticamente significativo` |
| 17 | `AI-4`, `AI-10` | procedimento numerado é uniforme por desenho; `red, amber, and green` são três estados reais, não tríade retórica |
| 18 | `AI-5` | laudo de imagem — voz de autor ali seria erro clínico |
| 19 | `AI-6` (pt) | um travessão de propósito e negrito de documentação de referência |
| 20/21 | `AI-7` (en/pt) | um único `On the other hand` / `Por outro lado` marcando o contraste real |
| 22/23 | `AI-8` (en/pt) | `Let's start with` / `Vamos supor` são imperativo de aula, não tique |
| 24 | `AI-11`, `AI-12` | numa luta de boxe a descrição física **é** a cena, não substituta de emoção |

Resultado da rodada 1: **22/24, 3 instáveis, 2 vermelhos.** Um dos vermelhos era defeito do caso
(já corrigido, `caso-16` re-rodado verde). O outro é achado real — ver abaixo.

## Achados abertos

### A-2 · `AI-6` proíbe o primeiro travessão de textos curtos — **falso positivo real**

Medido: `caso-19` roda **4/5** com `DEAI_TENTATIVAS=1`. O FAIL imprime `corrigiu indevidamente: —`.

Não é asserção frágil. `nonfiction-patterns.md` § Em Dashes diz *"Target: zero. Hard max: one per
1,000 words"*. A entrada do `caso-19` tem ~90 palavras e um travessão deliberado, o que estoura o
orçamento declarado por um fator de dez. Uma em cada cinco rodadas a skill obedece a régua ao pé da
letra — e está certa, dado o texto da regra.

O orçamento por mil palavras é uma medida de **densidade** aplicada como se fosse **limite
absoluto**. Em qualquer texto abaixo de mil palavras ele proíbe o primeiro travessão, e o primeiro
travessão nunca é o problema: a acumulação é. Contradiz o Princípio da Acumulação, que é a tese
central da skill.

Conserto provável (outra sessão): separar as duas coisas. O piso — nenhum texto é marcado por um
único travessão, independente do tamanho — e a densidade, que só passa a valer acima de N
travessões. Gate: `caso-19` medido 5/5 com `DEAI_TENTATIVAS=1`, e um caso positivo novo provando
que travessão em rajada continua sendo marcado.

(Só o A-2. Ver "descartado" abaixo.)

## Achado descartado pela medição

### `AI-7` — **não é achado**

`caso-20` ficou FLAKY na rodada 1 e parecia a mesma família do A-1 e do A-2. Medido 5× com
`DEAI_TENTATIVAS=1`: **5/5**. O FLAKY era oscilação normal do modelo, não sobredisparo da regra.

Vale o registro porque a hipótese estava escrita e era plausível — "os três FLAKY são o mesmo
padrão, não três acidentes". Eram dois padrões e um acidente. Medir custou 5 chamadas e evitou
mexer numa regra que está certa, que é o modo de falha que este repo inteiro existe para não
cometer.

## Achados fechados

### A-1 · `AI-8` sobredisparava em imperativo legítimo — **fechado**

**Diagnóstico corrigido.** A hipótese inicial era que o catálogo não tinha a distinção. Ele tinha:
`nonfiction-patterns.md` § "Let's" Constructions já dizia *"functioning as a transition rather than
a genuine invitation to act"*. O que faltava era exemplo do lado certo — quatro exemplos do lado
errado e zero do outro, e a lista vence a cláusula.

Conserto: tabela `Flag | Leave alone` nos dois catálogos, com o teste de portabilidade que já
existia em `fiction-phrases.md` ("se caberia sem mudança em outro texto, não está fazendo
trabalho"). Não foi princípio novo — foi aplicar um princípio que o repo já tinha.

Gate rodado: `caso-22` (era FAIL 3/3) PASS · `caso-23` (era FLAKY) PASS · `caso-03` e `caso-04`
continuam disparando `AI-8` — sem falso negativo simétrico.

### Histórico do A-1 (diagnóstico original)

`caso-22-contra-ai8-en-imperativo` falhou **3/3**: `corrigiu indevidamente: Let's start with`. A
entrada é uma explicação técnica que abre com `Let's start with the smallest case that still
breaks` — imperativo de quem ensina, não tique de assistente. A skill arranca do mesmo jeito.

`caso-23-contra-ai8-pt-imperativo` é a mesma regra em português (`Vamos supor que…`) e ficou
`FLAKY` (2ª de 3). Mesma causa, manifestação mais fraca: o catálogo PT lista `Vamos lá!` e `Vamos
por partes` com exclamação e sem complemento, e o modelo generaliza para qualquer `Vamos`.

Diagnóstico: o catálogo trata a **forma** (`Let's` / `Vamos`) como se fosse o tique, quando o tique
é a **função** — abertura performática que não carrega informação. `Let's dive in!` não tem
complemento real; `Let's start with the smallest case that still breaks` tem. A distinção existe e
o catálogo não a escreve.

Conserto provável (outra sessão, escopo próprio): em `nonfiction-patterns.md` § "Let's"
Constructions e em `vocabulary-pt-br.md` § AI-8, dizer onde a regra **não** mora — `Let's`/`Vamos`
seguido de complemento concreto e verificável é imperativo, não artefato. Ao mexer, `caso-22` e
`caso-23` são o gate.

## Casos com histórico de instabilidade

| Caso | Estado | Detalhe impresso | Leitura |
|---|---|---|---|
| `caso-19-contra-ai6-pt-referencia` | FLAKY (2ª de 3) | `corrigiu indevidamente: —` | o `AI-6` mira travessão em **zero**, então oscila entre respeitar e arrancar o único travessão deliberado. Ainda não decidido se é asserção frágil ou o mesmo defeito do A-1 noutra regra. Precisa de uma rodada com `DEAI_TENTATIVAS=1` 5× para medir. |
| `caso-20-contra-ai7-en-contraste` | FLAKY (2ª de 3) | `corrigiu indevidamente: On the other hand` | mesma família: o catálogo lista o conector sem dizer que um conector único marcando o contraste real do texto é o uso correto. |
| `caso-23-contra-ai8-pt-imperativo` | FLAKY (2ª de 3) | `corrigiu indevidamente: Vamos supor` | ver A-1 |

Os três são `corrigiu indevidamente` em contra-teste. É um padrão, não três acidentes: os catálogos
listam **formas** e a skill não tem, em nenhuma das três regras, a cláusula de fronteira que diz
onde a forma é uso correto. O `SKILL.md` tem essa cláusula só para colisão entre IDs.

## Falsos positivos reais encontrados

- **A-1** (acima) — `AI-8` × imperativo legítimo. Confirmado 3/3 em inglês.

## Defeitos de caso corrigidos

| Caso | O que estava errado | Guard criado |
|---|---|---|
| `caso-16-contra-ai3-pt-estatistica` | `nao-marca` asseria `estatisticamente significativo`; a entrada diz `significativa`, concordando com "diferença". Falhava 3/3 acusando falso positivo inexistente. | `parse_caso` agora recusa termo de `nao-marca` que não esteja literalmente na entrada — o erro passou a custar 0 chamadas de API em vez de 3. |
