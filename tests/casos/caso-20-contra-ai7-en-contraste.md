<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-7 em EN — um único conector, marcando o contraste real do texto
genero: nao-ficcao
idioma: en
espera:
contra-teste: AI-7
nao-marca: On the other hand

## entrada
Postgres gives you transactional DDL, so a failed migration rolls back cleanly and you never wake up to a half-applied schema.

On the other hand, MySQL's replication has survived more production abuse than anything else in the field, and the tooling around it assumes failure in a way Postgres tooling still doesn't.

We picked Postgres. The migration story mattered more to us than the replication story, because we deploy eleven times a day and fail over twice a year.
