<!-- TEXTO CORRETO DE PROPÓSITO — contra-teste. A regra NÃO deve disparar aqui.
     NÃO 'melhore' este texto — ver AGENTS.md. -->
# caso: contra-teste AI-8 em PT — "Vamos" como imperativo real, não tique de assistente
genero: nao-ficcao
idioma: pt
espera:
contra-teste: AI-8
nao-marca: Vamos supor

## entrada
Vamos supor que o corretor tenha 400 imóveis na carteira e queira filtrar por bairro e faixa de preço ao mesmo tempo.

O índice composto em `(bairro_id, valor)` resolve os dois filtros numa varredura só. Invertida, a ordem não serve: `valor` sozinho é seletivo demais e o banco cai em varredura sequencial quando o bairro é o filtro forte.
