<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-7 em PT — um único conector, marcando o contraste real do texto
genero: nao-ficcao
idioma: pt
espera:
contra-teste: AI-7
nao-marca: Por outro lado

## entrada
O banco em latin1 resolve o problema imediato: o monólito grava e lê sem conversão, e nenhum dos mil arquivos PHP precisa mudar.

Por outro lado, toda borda nova paga o pedágio. A API converte na entrada e na saída, o app trata UTF-8, e qualquer campo que escapar da conversão chega no celular do corretor com `Ã§` no lugar do cedilha.

Migrar o banco custa uma janela de manutenção. Não migrar custa um bug por trimestre, sempre no mesmo lugar.
