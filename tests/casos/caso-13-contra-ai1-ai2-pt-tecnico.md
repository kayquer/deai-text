<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. As regras NÃO devem disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-1 e AI-2 em PT — termo técnico que coincide com o catálogo
genero: nao-ficcao
idioma: pt
espera:
contra-teste: AI-1, AI-2
nao-marca: erro-padrão robusto, escalabilidade horizontal

## entrada
Estimamos o modelo com erro-padrão robusto agrupado por município. O coeficiente de renda per capita ficou em 0,21, com intervalo de confiança de 0,17 a 0,25.

O gargalo do serviço não é CPU: é o pool de conexões do Postgres. A escalabilidade horizontal só ajuda depois que o pool for movido para o PgBouncer, porque hoje cada réplica nova abre mais cem conexões e o banco satura antes do app.
