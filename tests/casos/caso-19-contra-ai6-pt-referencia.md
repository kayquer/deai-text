<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-6 em PT — um travessão de propósito e negrito de documentação
genero: nao-ficcao
idioma: pt
espera:
contra-teste: AI-6
nao-marca: —, `--force`

## entrada
O `sync` copia `dist/` para os dois destinos e falha se o destino tiver mudanças locais. Esse guard existe porque alguém já editou o CSS buildado direto no monólito e a produção ficou meses à frente do repo.

**`--force`** ignora o guard. Use só quando você souber que as mudanças locais são descartáveis — é a única flag do comando que apaga trabalho de outra pessoa sem perguntar.
