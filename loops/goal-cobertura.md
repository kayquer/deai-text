# Goal: fechar a matriz de cobertura dos 12 IDs

Goal loop. Rode com `/loop` sem intervalo — o modelo se auto-pauta.

## Objetivo

Cada `AI-N` precisa de **dois** casos em `tests/casos/`:

1. **positivo** — um texto que faz a regra disparar (declarado em `espera:`)
2. **contra-teste** — um texto onde a regra **não** deve disparar, provando que ela não gera falso
   positivo (declarado em `contra-teste:` e com os termos em `nao-marca:`)

Para `AI-1`, `AI-2`, `AI-3`, `AI-7`, `AI-8` e `AI-9`, os dois em **cada idioma** (`pt` e `en`) — o
catálogo de vocabulário é diferente por idioma, e um catálogo PT sem caso PT é um catálogo que
ninguém verificou. Os outros seis IDs são neutros: um caso em qualquer idioma basta.

**O contra-teste é o que importa.** Um de-AI falha muito mais por corrigir o que já estava certo do
que por deixar passar. Um caso que só prova o acerto positivo não protege contra nada.

## Verificação

```bash
./init.sh --cobertura    # matriz. Exit 0 = fechada. Grátis, não chama a API.
./init.sh                # todos os casos continuam verdes. Exit 0 = ok.
```

**As duas precisam sair 0.** Fechar a matriz quebrando um caso existente não conta como progresso.

## Condição de parada

Pare quando **qualquer uma** ocorrer:

- `./init.sh --cobertura` sai 0 **e** `./init.sh` sai 0 — objetivo atingido
- 16 rodadas completadas
- 2 rodadas seguidas sem nenhum caso novo entrar verde — o loop travou, escale para humano
- Um caso antes verde ficou vermelho e 1 rodada não recuperou — pare e reporte, não insista

## Restrições

**Não altere** para fazer a matriz fechar:

- `SKILL.md` e `skills/references/*.md` — o objetivo é cobrir a skill com testes, não mudar a skill. Se um
  contra-teste revelar falso positivo real, **pare e reporte**; corrigir o catálogo é outra sessão.
- `tests/verify.py` — mexer no avaliador para o caso passar é fraudar a verificação.
- Casos existentes — só adicione. Alterar `espera:` de caso que já existe mascara regressão.

**Não invente texto artificial.** A entrada tem que ser texto que alguém escreveria de verdade — um
post de blog, um release note, um trecho de romance, um parecer. Slop plausível para o positivo,
prosa boa de verdade para o contra-teste. Um contra-teste que ninguém escreveria não protege contra
nada.

## Por rodada

1. Rode `./init.sh --cobertura` e escolha **uma** célula vermelha.
2. Se for contra-teste, pense em qual leitura correta a regra poderia atropelar:
   - **AI-1** — termo técnico que coincide com a lista (`robust standard errors`, `escalabilidade`
     em documento de arquitetura, `possui` em texto jurídico)
   - **AI-2** — uma palavra do nível 2 sozinha no parágrafo, no sentido próprio (`navegar` num texto
     sobre náutica; `foster` como sobrenome)
   - **AI-3** — `significativo` num texto estatístico, onde é o termo técnico
   - **AI-4** — texto legitimamente uniforme: uma lista de passos, uma tabela em prosa, um contrato
   - **AI-5** — texto que **deve** ser neutro: laudo, norma, documentação de API
   - **AI-6** — um travessão usado de propósito por um humano; negrito em documentação de referência
   - **AI-7** — `Por outro lado` abrindo o contraste real do texto; um único conector necessário
   - **AI-8** — texto em que "Vamos" é imperativo de verdade, não tique de assistente
   - **AI-9** — `possui` com posse real; `representa` num texto sobre representação gráfica
   - **AI-10** — tríade legítima (três itens que são mesmo três); gerúndio em perífrase durativa
   - **AI-11** — descrição física que **é** a cena (um soco, uma corrida), não substituta de emoção
   - **AI-12** — abertura com ambiente quando o ambiente é o assunto; narrador onisciente que
     comenta por escolha de estilo
3. Crie o caso. Contra-teste declara `contra-teste:` e lista os termos em `nao-marca:`.
4. Rode `./init.sh <novo-caso>`. Verde → siga. Vermelho → o caso está errado **ou** você achou falso
   positivo real; decida qual, e no segundo caso pare e reporte.
5. Rode `./init.sh` inteiro para confirmar que nada mais quebrou.
6. Anote a rodada em `loops/loop-state.md`.

## Escopo por rodada

**Um ID por rodada.** Dois ao mesmo tempo impedem saber qual caso quebrou o quê.

## Custo

Uma chamada por caso quando passa de primeira, até 3 com retry (`DEAI_TENTATIVAS`). Prefira
`./init.sh <caso-novo>` durante a rodada e deixe a suíte inteira para o fim. `--cobertura` é grátis.
