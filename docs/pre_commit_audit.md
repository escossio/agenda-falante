# Pre-Commit Architecture Audit

Data da auditoria: 2026-07-03

Escopo: revisão arquitetural completa do Agenda Falante antes do primeiro commit.

## Arquitetura validada

- O Agenda Falante permanece desacoplado do motor TTS interno.
- O Planner continua sem implementação.
- O Composer continua sem implementação.
- O fluxo de contatos, catálogo de segmentos, plano TTS, preview dry-run e execução fake continuam separados.
- A execução real controlada está isolada por flags explícitas e por base URL explícita.
- O adapter conhece apenas o contrato público do endpoint real.
- O Agenda Falante conhece apenas o motor Escossio, não detalhes internos de providers.

## Itens revisados

- Documentação conceitual do domínio.
- ADRs de arquitetura de composição, motor TTS externo e seleção de modelos.
- Documento de perfis de uso TTS.
- Documento do contrato real do endpoint TTS.
- Documento do adapter do endpoint TTS.
- Documento do plano TTS e do cliente TTS.
- Módulos `segment_catalog`, `segment_resolver`, `tts_generation_plan`, `tts_client`, `tts_endpoint_adapter` e `fake_tts_executor`.
- CLIs de preview, execução fake e execução real controlada.
- Testes automatizados cobrindo plano, preview, adapter, fake executor, guardrails e execução real controlada.

## Consistência validada

### Documentação vs implementação

Consistente.

- O `segment_catalog` gera segmentos de contato como `contact_name`.
- O `tts_generation_plan` adiciona `usage_profile` e mantém `cache_key` determinístico.
- O `tts_client` mantém dry-run separado e preserva `usage_profile`.
- O `tts_endpoint_adapter` gera payload somente com `text`, `provider`, `language`, `voice`, `speed` e `humanization`.
- O contrato real documentado em `docs/real_tts_endpoint_contract.md` corresponde ao endpoint observado em `app/main.py` do motor TTS.

### ADRs vs código

Consistente.

- O ADR de motor TTS externo está alinhado com o uso exclusivo do motor Escossio.
- O ADR de seleção de modelos está alinhado com o mapeamento inicial do motor TTS, sem acoplamento permanente.
- O documento de perfis de uso TTS está refletido no plano e no adapter.

### Modelo de domínio vs módulos implementados

Consistente.

- `Event`, `Composition Plan`, `Audio Segment` e `Composition Result` permanecem como conceitos separados.
- A implementação atual cobre importação, normalização, catálogo, resolução, plano e execução isolada.
- O Planner e o Composer seguem somente documentados.

### Contrato do motor TTS vs adapter

Consistente.

- O adapter usa apenas o contrato público de `/api/generate-audio`.
- O payload real não inclui campos internos do Agenda Falante.
- O mapeamento de `usage_profile` está restrito a parâmetros suportados pelo contrato atual.

### Plano TTS vs adapter

Consistente.

- O plano carrega `request_id`, `segment_id`, `segment_type`, `text`, `language`, `voice`, `format`, `output_path`, `cache_key`, `usage_profile` e `metadata`.
- O adapter converte apenas o que o endpoint suporta e preserva o restante como metadado interno.

### Adapter vs cliente TTS

Consistente.

- O adapter prepara o payload.
- O cliente executa dry-run, validação real controlada e download do áudio.
- A trilha real continua protegida por confirmação explícita.

### Cliente TTS vs CLI

Consistente.

- O dry-run continua separado.
- A execução real controlada exige `--execute-real-tts` e `--base-url`.
- A CLI de execução real controlada executa apenas 1 item por vez.

## Responsabilidades desacopladas

- Planner não conhece providers.
- Composer não conhece providers.
- O adapter não conhece implementações internas dos providers.
- O cliente TTS não assume detalhes do provider interno.
- O executor fake não depende do motor TTS real.

## Verificações de sanidade

- O executor fake continua funcionando.
- O dry-run continua funcionando.
- A execução real continua protegida por `--execute-real-tts` e `--base-url`.
- Nenhum módulo do Agenda Falante conhece detalhes internos dos providers.
- Não houve uso de endpoint público nesta auditoria.

## Problemas encontrados

- Não foram encontrados problemas funcionais bloqueantes na arquitetura revisada.
- Há sobreposição temática entre documentação conceitual de TTS e documentação do contrato real, mas sem conflito de comportamento.
- A árvore contém `__pycache__` gerados pela execução local; são artefatos esperados e não afetam o código-fonte.

## Problemas corrigidos

- Nenhuma correção de comportamento foi necessária nesta auditoria.
- Nenhuma refatoração desnecessária foi aplicada.

## Riscos remanescentes

- A execução real controlada ainda depende do contrato HTTP do motor TTS permanecer estável.
- O uso de `audio_url` exige que o motor TTS continue exposto de forma acessível ao consumidor.
- O mapeamento inicial de `usage_profile` é conservador e pode precisar de revisão conforme novos perfis forem introduzidos.

## Recomendações para a próxima fase

1. Manter o adapter como única fronteira entre o plano interno e o contrato real do TTS.
2. Consolidar a estratégia de observabilidade da execução real controlada.
3. Evoluir o contrato apenas com validação conjunta entre Agenda Falante e motor Escossio.
4. Evitar introduzir acesso direto a providers no Agenda Falante.
5. Preservar os modos `dry-run`, fake e execução real controlada como trilhas separadas.

## Conclusão

A auditoria arquitetural pré-commit foi concluída.

O projeto permanece coerente com a documentação, com os ADRs e com as responsabilidades já definidas.

Não foram observadas violações arquiteturais que exijam mudança imediata de implementação.
