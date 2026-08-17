#!/usr/bin/env bash
# Verificação da skill deai-text. Roda os casos de tests/casos/ contra o
# SKILL.md deste repo. Ver AGENTS.md para o fluxo de desenvolvimento.
#
#   ./init.sh                     todos os casos
#   ./init.sh caso-01             um caso (match por substring)
#   ./init.sh --cobertura         matriz de cobertura (não chama a API)
#   DEAI_MODELO=opus ./init.sh    outro modelo (default: sonnet)
#   DEAI_TENTATIVAS=1 ./init.sh   sem retry (para medir instabilidade)
set -euo pipefail
cd "$(dirname "$0")"

falta=0
command -v claude  >/dev/null || { echo "falta: claude (https://claude.com/claude-code)"; falta=1; }
command -v python3 >/dev/null || { echo "falta: python3"; falta=1; }
[ "$falta" -eq 0 ] || exit 1

# Só na rodada completa. Durante o desenvolvimento de um caso, prompts/ ainda
# não precisa estar em dia — regenerar a cada iteração só suja o diff. Na
# rodada que serve de gate, um prompt avulso defasado é uma skill publicada
# diferente da testada, e isso ninguém percebe olhando o verde dos casos.
if [ $# -eq 0 ] && [ -f tools/build.py ]; then
  python3 tools/build.py --verificar || exit 1
fi

exec python3 tests/verify.py "$@"
