#!/usr/bin/env bash
set -euo pipefail

MILESTONE_TITLE="v0.1.0-alpha"
MILESTONE_DESC="Primeira versão alpha do Agenda Falante, cobrindo geração real de segmentos, templates reutilizáveis, Composer inicial, Planner inicial e preparação para integração Android."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
ROADMAP_FILE="${PROJECT_ROOT}/docs/github_roadmap_v0_1_alpha.md"

if ! command -v gh >/dev/null 2>&1; then
  echo "Erro: GitHub CLI (gh) não está instalado." >&2
  exit 1
fi

if ! gh auth status >/dev/null 2>&1; then
  echo "Erro: gh auth status falhou. Autentique o GitHub CLI antes de executar." >&2
  exit 1
fi

if ! git -C "${PROJECT_ROOT}" remote get-url origin >/dev/null 2>&1; then
  echo "Erro: repositório remoto 'origin' não está configurado." >&2
  exit 1
fi

if [[ ! -f "${ROADMAP_FILE}" ]]; then
  echo "Erro: roadmap não encontrado em ${ROADMAP_FILE}." >&2
  exit 1
fi

REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"

ensure_milestone() {
  local milestone_number
  milestone_number="$(gh api "repos/${REPO}/milestones" --paginate --jq ".[] | select(.title == \"${MILESTONE_TITLE}\") | .number" | head -n1 || true)"
  if [[ -n "${milestone_number}" ]]; then
    echo "Milestone já existe: ${MILESTONE_TITLE} (#${milestone_number})"
    return 0
  fi

  gh api "repos/${REPO}/milestones" \
    --method POST \
    -f title="${MILESTONE_TITLE}" \
    -f description="${MILESTONE_DESC}" \
    >/dev/null
  echo "Milestone criada: ${MILESTONE_TITLE}"
}

create_issue_if_missing() {
  local title="$1"
  local body="$2"

  local existing_number
  existing_number="$(gh issue list --repo "${REPO}" --state all --limit 100 --json number,title --jq '.[] | select(.title == "'"${title}"'") | .number' | head -n1 || true)"
  if [[ -n "${existing_number}" ]]; then
    echo "Issue já existe: ${title} (#${existing_number})"
    return 0
  fi

  gh issue create \
    --repo "${REPO}" \
    --title "${title}" \
    --body "${body}" \
    --milestone "${MILESTONE_TITLE}" \
    >/dev/null
  echo "Issue criada: ${title}"
}

ensure_milestone

create_issue_if_missing \
  "Gerar segmentos reais \`contact_name\` usando motor TTS Escossio" \
  "Usar o plano TTS existente e a execução real controlada para gerar segmentos de nomes de contatos, mantendo limite seguro, base URL explícita e sem execução em lote descontrolada."

create_issue_if_missing \
  "Criar templates reutilizáveis de chamada recebida" \
  "Criar catálogo inicial de templates reutilizáveis para chamadas recebidas, incluindo intro, outro e variações de estilo amigável, profissional e urgente."

create_issue_if_missing \
  "Implementar Composer inicial de áudio" \
  "Implementar composição simples de segmentos WAV com sequência definida por manifesto, incluindo validação de arquivos, concatenação, pausas e saída final."

create_issue_if_missing \
  "Implementar Planner inicial para \`incoming_call\`" \
  "Criar Planner mínimo capaz de receber evento de chamada recebida, escolher estratégia simples e produzir \`Composition Manifest\`."

create_issue_if_missing \
  "Exportar pacote Android inicial" \
  "Criar exportação dos áudios e manifestos para uma estrutura compatível com Android, Tasker ou MacroDroid."

create_issue_if_missing \
  "Validar reprodução no Android com Tasker ou MacroDroid" \
  "Testar fluxo manual no Android para tocar áudio correspondente a um contato durante chamada recebida."

create_issue_if_missing \
  "Adicionar cache real de segmentos TTS" \
  "Evitar geração repetida de segmentos já existentes usando \`cache_key\`, \`segment_id\` e verificação de arquivos disponíveis."

create_issue_if_missing \
  "Documentar primeira execução real controlada" \
  "Criar documentação de operação segura para executar geração real de 1 segmento contra o motor TTS local Escossio."
