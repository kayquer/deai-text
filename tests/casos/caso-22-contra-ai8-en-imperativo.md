<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-8 em EN — "Let's" como imperativo real de aula, não tique de assistente
genero: nao-ficcao
idioma: en
espera:
contra-teste: AI-8
nao-marca: Let's start with

## entrada
Let's start with the smallest case that still breaks: two goroutines, one map, no mutex.

Run it under `-race` and you'll get a report within a second or two. The report names both stacks — the write at line 14 and the read at line 22 — which is usually enough to see the fix without reading the rest of the file.
