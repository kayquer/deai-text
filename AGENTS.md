# AGENTS.md — desenvolvimento da skill deai-text

> **PARE.** Se você chegou aqui para **limpar um texto do usuário**, você está no arquivo errado —
> leia `SKILL.md` e aplique a skill. Este arquivo é para quem vai **editar a skill em si**.

---

## ⚠️ Este repositório contém texto de IA de propósito

**Não "melhore" o texto deste repositório.**

Os arquivos abaixo contêm exatamente os padrões que a skill existe para remover. Eles são o material
de trabalho, não defeitos:

| Arquivo | O que tem de errado de propósito |
|---|---|
| `tests/casos/*.md` | **entrada 100% slop de IA.** É o que os testes auditam. Limpar aqui faz o teste parar de testar. |
| `tests/casos/caso-*-contra-*.md` | o oposto: texto **correto** que a skill não pode marcar. "melhorar" também quebra. |
| `references/*.md` | as colunas "Evite" / "Replace" das tabelas |
| `SKILL.md` | os exemplos da tabela da seção 1 |

Um agente que passa a própria skill no repo quebra a suíte **em silêncio**: os testes continuam
rodando e passam a não detectar nada, porque a entrada deixou de ter o que detectar.

Este risco é maior aqui do que num repo comum. A skill dispara em "melhore este texto", e os
arquivos deste repo são texto ruim. A tentação é estrutural.

**Regra prática:** neste repositório, texto dentro de caso de teste, de tabela "evite→use" ou de
exemplo é **conteúdo**. Só mexa se a tarefa for explicitamente "adicionar/alterar um caso" ou
"corrigir um exemplo que ensina a regra errada".

### Como saber em que modo você está

| Sinal | Modo | O que fazer |
|---|---|---|
| O usuário colou um texto e quer ele limpo | **uso** | aplique `SKILL.md` ao texto dele |
| O usuário fala em regra, AI-N, caso de teste, catálogo, README, publicar | **desenvolvimento** | siga este arquivo; não reescreva nada do repo |
| Você está prestes a editar `SKILL.md` / `references/` / `tests/` | **desenvolvimento** | sempre |

Na dúvida, pergunte.

---

## Definition of done

Uma mudança na skill só está pronta quando **as quatro** valem:

1. `./init.sh` termina verde (exit 0).
2. A mudança tem caso de teste — novo, ou um existente atualizado.
3. Se a mudança criou ou ampliou uma regra, existe entrada em `nao-marca` de algum caso cobrindo o
   falso positivo correspondente.
4. A regra continua com exemplo antes/depois no catálogo.

**O item 3 é o que mais escapa, e aqui ele é o item mais importante do arquivo.** O modo de falha
característico de um de-AI não é deixar passar — é **corrigir o que já estava certo**: marcar o
`robust` de `robust standard errors`, arrancar o único travessão que um humano usou de propósito,
achatar uma voz distinta num outro tipo de média. Ampliar um catálogo quase sempre cria falso
positivo, e um caso que só prova o acerto positivo não pega nada disso.

O item 2 tem piso mecânico: o parser recusa caso que não assere nada (ver "O parser recusa caso
inválido"). Antes disso, um typo no nome da chave produzia caso verde que verificava zero.

## Escopo

**Uma regra AI-N por sessão.** Mexer em duas ao mesmo tempo impede saber qual delas quebrou o caso —
o runner só diz que a regra não disparou, não por quê.

## Não mexa sem intenção explícita

| Item | Por quê |
|---|---|
| `description` do frontmatter | É o que faz a skill disparar. Alterar muda quando ela é invocada. |
| Numeração `AI-N` | Os casos referenciam por número. Renumerar quebra todos de uma vez. |
| Cabeçalhos numerados da saída (`## 2. Rewrite` / `## 2. Reescrita`) | O runner ancora no **número** para isolar a reescrita. Trocar o número cega o teste de falso positivo — e ele passa a dar verde. |
| Separação `vocabulary.md` × `vocabulary-pt-br.md` | Não são traduções um do outro. Fundir os dois faz a auditoria em português procurar `delve` e a em inglês procurar `possui`. |
| `"skills": ["."]` no `plugin.json` | É o que faz o `SKILL.md` da raiz ser descoberto quando o repo é instalado como plugin de marketplace. **`"./"` não funciona** — o campo `skills` é a exceção que aceita `"."`. Sem ele, `claude plugin details` reporta `Skills (0)` e o install entrega nada. |
| Seção "O que NÃO é erro" (`vocabulary-pt-br.md`) | É o que impede a skill de virar corretor que conserta português correto. |

## Verificação

```bash
./init.sh                          # roda tudo
./init.sh caso-01                  # um caso só (match por substring)
./init.sh --cobertura              # matriz AI-N × (positivo, contra-teste) — não chama a API
DEAI_MODELO=opus ./init.sh         # modelo diferente (default: sonnet)
DEAI_TENTATIVAS=1 ./init.sh        # sem retry (para medir flakiness)
DEAI_TIMEOUT=600 ./init.sh         # timeout por chamada (default: 300s)
```

O runner concatena `SKILL.md` + `references/*.md` **deste repo** e manda para `claude -p`. Ele testa
o arquivo que você acabou de editar, não a cópia instalada em `~/.claude/skills/`.

Ele **não compara texto** — output de LLM não é determinístico, e aqui o produto é prosa reescrita,
que muda a cada rodada por desenho. Verifica três coisas:

- **cobertura** — todo ID de `espera:` apareceu na saída
- **falso positivo** — todo termo de `nao-marca:` sobreviveu intacto na **seção 2** (Reescrita)
- **âncora** — todo termo de `deve-conter:` apareceu na saída inteira

Regra extra não reprova o caso.

### Por que `nao-marca` olha só a seção 2

A tabela da seção 1 cita o trecho original inteiro na coluna "Excerpt". Procurar o termo na saída
completa acharia ele lá — na linha que diz que ele é problema — e todo contra-teste passaria. A
seção 2 é o único lugar onde dá para afirmar que a skill **não** mudou um termo.

Se a saída não tiver seção 2, o caso é `FAIL` com `sem seção '2.'`. É proposital: sem ela não há o
que verificar, e dar verde seria pior.

### FLAKY não é PASS silencioso

O runner repete cada caso até `DEAI_TENTATIVAS` (3) antes de reprovar, porque a suíte oscila.

| Estado | Significado |
|---|---|
| `PASS` | passou de primeira |
| `FLAKY` | passou numa retentativa — conta como ok, mas aparece destacado |
| `FAIL` | falhou as 3 tentativas — quebra real |

**Flaky recorrente merece investigação**, não tolerância. A linha de detalhe abaixo do `FAIL` diz
para onde ir:

| Detalhe impresso | Causa | Conserto |
|---|---|---|
| `corrigiu indevidamente: <termo>` | **asserção frágil** — o termo de `nao-marca` some numa reescrita legítima do entorno | encurtar o termo para o núcleo que prova a regra |
| `corrigiu indevidamente: <termo>` | **asserção que nunca podia casar** — o termo do cabeçalho não é literalmente o termo da entrada | conferir a entrada caractere a caractere. Em português, concordância: `caso-16` asseria `estatisticamente significativo` e a entrada dizia `significativa`, concordando com "diferença". Falhava 3/3 e parecia falso positivo da skill. |
| `corrigiu indevidamente: <termo>` | **falso positivo real** — a skill marcou o que estava certo | corrigir o catálogo, **não** o teste. É um achado, não ruído. |
| `faltou: AI-N` | **regra ambígua** — o modelo hesita porque a regra não decide o caso | no `SKILL.md`/catálogo, **não** no teste |
| `faltou: AI-N` | **colisão de rótulo** — o achado sai certo e é etiquetado com outro ID | usar a seção "Where a rule does *not* live" do `SKILL.md`: dizer onde a regra **não** mora |
| `não apareceu: <termo>` | **âncora frágil** — o `deve-conter` fixa uma escolha que a skill não é obrigada a fazer | desambiguar a **entrada**, não encurtar a âncora |
| `sem seção '2.'` | o formato de saída não foi seguido | ver se algum edit no `SKILL.md` mexeu nos cabeçalhos numerados |
| `sem resposta do modelo` | **infra** — timeout ou erro da API | nenhum; rode de novo |

As duas primeiras linhas dão a mesma saída e mandam para lugares opostos. **Olhe a saída bruta
antes de decidir** — rode o caso à mão com `claude -p` e leia a seção 2.

### Custo

Cada caso é **até `DEAI_TENTATIVAS` (3) chamadas** ao Claude. O default é `sonnet`: Opus a cada
rodada fica caro, e a asserção é sobre qual regra disparou, não sobre a qualidade da prosa.

Durante o desenvolvimento, prefira `./init.sh <caso>` e deixe a suíte inteira para o fim.
`--cobertura` é grátis.

**Se um caso falhar, rode com `DEAI_MODELO=opus` antes de concluir que a skill quebrou.** Modelo
menor às vezes aplica a correção sem citar o ID na tabela.

## Formato de caso

```markdown
<!-- TEXTO RUIM DE PROPÓSITO. É a entrada do teste — NÃO 'melhore'. Ver AGENTS.md. -->
# caso: descrição curta
genero: nao-ficcao
idioma: pt
espera: AI-1, AI-7, AI-9

## entrada
<texto que viola as regras esperadas>
```

| Chave | O que faz |
|---|---|
| `genero` | `nao-ficcao`, `ficcao` ou `marketing` — decide quais catálogos a skill lê |
| `idioma` | `pt` ou `en` — decide qual catálogo de vocabulário, e alimenta a matriz bilíngue |
| `espera` | IDs que **devem** aparecer na saída |
| `nao-marca` | termos que **não podem** ser tocados — checados só na seção 2 |
| `deve-conter` | termos que **devem** aparecer — checados na saída inteira |
| `contra-teste` | IDs que este caso prova não dispararem. Só alimenta `--cobertura` |

### A matriz de cobertura é bilíngue onde precisa ser

`AI-1`, `AI-2`, `AI-3`, `AI-7`, `AI-8` e `AI-9` dependem do catálogo de vocabulário, que é diferente
por idioma. Para essas, `--cobertura` exige caso positivo **e** contra-teste **em cada idioma** — um
catálogo PT sem caso PT é um catálogo que ninguém verificou. As outras seis são neutras: um caso em
qualquer idioma basta.

### O parser recusa caso inválido

`parse_caso` mata o runner em vez de aceitar em silêncio. Um caso que não assere nada é pior que caso
nenhum: ele conta como cobertura.

| Erro | Por que é fatal |
|---|---|
| chave desconhecida | `espra: AI-1` dava `PASS` sem verificar nada |
| `espera`, `nao-marca` e `deve-conter` todos vazios | caso sem asserção |
| `contra-teste` preenchido com `nao-marca` vazio | a matriz contava a regra coberta sem asserção por trás |
| ID fora de `AI-1..12` | `AI-13` caía num `.get(..., [])` e sumia |
| `genero` / `idioma` que não existe | ia para o prompt como parâmetro inventado |
| `## entrada` vazia | o modelo recebia um prompt sem texto para auditar |
| termo de `nao-marca` que não está na entrada | um termo ausente do texto não sobrevive a nada: 3 chamadas de API para reportar um falso positivo inexistente |

## O que o harness NÃO cobre

A suíte testa o comportamento **dado que** a skill disparou — o runner injeta `SKILL.md` +
`references/*.md` no prompt por stdin. Ela não testa **se** a skill dispara.

Isso deixa o `description` do frontmatter sem verificação nenhuma, e ele é justamente o campo que
esta AGENTS.md manda não mexer sem intenção. Uma edição que estreite o `description` passa por toda
a suíte em verde e mesmo assim faz a skill parar de ser invocada.

O mecanismo nativo para isso é `claude plugin eval` com casos `should_trigger` — em early access e
indisponível nesta conta na data em que o harness foi escrito. Quando liberar, é `evals/` na raiz.
Até lá, o gatilho é verificado só por uso.

## Loops

`loops/goal-cobertura.md` é um goal loop. Rode com `/loop` sem intervalo — o modelo se auto-pauta e
para no critério do próprio arquivo. O critério é **mecânico**: `./init.sh --cobertura` sai 0 quando
toda regra tem caso positivo e contra-teste, nos idiomas exigidos.

Estado entre rodadas em `loops/loop-state.md`.

## Clean-state checklist

- [ ] `./init.sh` roda e termina verde
- [ ] Cada regra alterada tem caso cobrindo acerto **e** falso positivo
- [ ] Nenhum texto de caso ou de tabela "evite→use" foi "limpo" por engano
- [ ] `README.md` reflete a mudança, se ela for visível para quem usa
- [ ] A próxima sessão consegue continuar sem conserto manual

## Estrutura

```
SKILL.md                       # 12 IDs, método de detecção, formato de saída
references/
  vocabulary.md                # níveis 1/2/3 em inglês
  vocabulary-pt-br.md          # níveis 1/2/3 em português + gerúndio, cópula, decalque
  constructions.md             # 31 construções estruturais
  fiction-phrases.md           # descrição física, metáfora morta, clichê
  nonfiction-patterns.md       # formatação, transição, artefato de assistente
tests/
  verify.py                    # runner (Python 3 stdlib, sem dependências)
  casos/*.md                   # casos de regressão
loops/
  goal-cobertura.md            # goal loop: matriz AI-N × (positivo, contra-teste)
  loop-state.md                # estado entre rodadas + achados abertos
prompts/                       # prompts avulsos para LLM sem suporte a skills
init.sh                        # checa pré-requisitos e roda o verify
AGENTS.md                      # este arquivo
```

Só `SKILL.md` e `references/*.md` vão para o prompt. O resto é harness.
