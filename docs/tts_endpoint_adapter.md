# TTS Endpoint Adapter

Este adapter traduz o plano interno do Agenda Falante para o contrato real atual do motor TTS.

Ele não chama o endpoint.

Ele apenas prepara um preview dry-run do payload real.

A execução real controlada exige flag explícita e base URL explícita no comando de orquestração.

## O que entra no payload real

O payload adaptado mantém apenas os campos aceitos hoje pelo endpoint real:

- `text`
- `provider`
- `language`
- `voice`
- `speed`
- `humanization`

## O que não entra no payload real

Os seguintes campos continuam sendo metadados internos do Agenda Falante:

- `request_id`
- `segment_id`
- `cache_key`
- `output_path`
- `usage_profile`
- `metadata`

## Mapeamento inicial de usage_profile

- `fast_name`
  - `provider`: `elevenlabs`
  - `speed`: `1.0`
  - `humanization`: desativado

- `expressive_template`
  - `provider`: `elevenlabs`
  - `speed`: `1.0`
  - `humanization`: ativado

- `notification_short`
  - `provider`: `elevenlabs`
  - `speed`: `1.05`
  - `humanization`: desativado

- `urgent_alert`
  - `provider`: `elevenlabs`
  - `speed`: `0.95`
  - `humanization`: ativado

## Resultado esperado

O adapter mantém o plano interno desacoplado do endpoint real, enquanto prepara a chamada futura com o contrato já documentado no motor TTS.

O uso recomendado inicial continua sendo contra um endpoint local ou ambiente controlado, nunca contra produção por padrão.
