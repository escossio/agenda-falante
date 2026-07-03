# TTS Generation Plan

O plano de geração TTS é apenas uma lista de solicitações futuras ao motor TTS.

Ele não executa TTS e não gera áudio.

O plano evita chamadas desnecessárias porque ignora segmentos que já estão `available`.

Cada requisição descreve os dados necessários para gerar um segmento faltante, incluindo texto, idioma, voz, formato e destino esperado.

Cada item do plano também carrega `usage_profile`, que representa a intenção de uso do áudio e não o provedor nem o modelo.

Inicialmente, segmentos do tipo `contact_name` usam `fast_name`.

## Executor fake

Existe um executor fake/local apenas para validação do pipeline.

Ele cria arquivos WAV mínimos válidos em ambiente local para confirmar resolução de segmentos e fluxo de arquivos, sem chamar o motor TTS real.

Esse executor não representa a implementação final de geração de voz.
