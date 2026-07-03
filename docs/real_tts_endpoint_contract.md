# Contrato Real do Endpoint TTS

Este documento registra o contrato real encontrado no serviço TTS do ecossistema Escossio em `/srv/projetos/tts-api-switcher`.

## Endpoint real encontrado

- Método HTTP: `POST`
- Rota: `/api/generate-audio`

O endpoint existe no código em [`/srv/projetos/tts-api-switcher/app/main.py`](/srv/projetos/tts-api-switcher/app/main.py).

## Payload aceito

O payload é definido pela classe `GenerateAudioRequest` em [`app/main.py`](/srv/projetos/tts-api-switcher/app/main.py).

### Campos obrigatórios

- `text`
- `provider`

### Campos opcionais

- `language`
- `voice`
- `speed`
- `humanization`

### Exemplo de payload real

```json
{
  "text": "Olá Davi.",
  "provider": "mock",
  "language": "pt-BR",
  "voice": "",
  "speed": 1.0,
  "humanization": {
    "enabled": true,
    "preset": "natural"
  }
}
```

## Resposta real

Quando a geração dá certo, o endpoint retorna JSON com:

- `status`
- `provider`
- `audio_url`
- `filename`
- `original_text`
- `tts_text`
- `humanization_applied`
- `preset_resolved`
- `conservative_mode`
- `segments_count`
- `technical_segments_count`
- `human_segments_count`

### Exemplo de resposta real

```json
{
  "status": "ok",
  "provider": "mock",
  "audio_url": "/generated/mock_20260703123456_abcd1234ef56.wav",
  "filename": "mock_20260703123456_abcd1234ef56.wav",
  "original_text": "Olá Davi.",
  "tts_text": "Olá Davi.",
  "humanization_applied": false,
  "preset_resolved": null,
  "conservative_mode": false,
  "segments_count": 0,
  "technical_segments_count": 0,
  "human_segments_count": 0
}
```

Quando há erro, a resposta usa o formato:

```json
{
  "status": "error",
  "provider": "mock",
  "error_code": "unknown_provider_error",
  "error": "Falha ao gerar áudio.",
  "detail": "Falha ao gerar áudio."
}
```

## Como o áudio é retornado

O endpoint não retorna binário direto na resposta JSON.

O áudio é gravado em disco pelo provider e exposto como arquivo estático em `/generated/{filename}`.

Na resposta de sucesso, o campo `audio_url` aponta para esse arquivo.

## Mapeamento de capabilities do endpoint

### Provider

Há suporte explícito a provider via campo `provider`.

Os providers disponíveis no código são:

- `mock`
- `openai`
- `google`
- `elevenlabs`
- `azure`
- `polly`

### Voice

Há suporte explícito a `voice`.

O nome exato da voz é repassado ao provider selecionado.

### Preset

Não existe campo `preset` no payload do endpoint.

O que existe é `humanization`, com presets internos do serviço.

### Humanização

Há suporte a `humanization` no payload.

O serviço aplica humanização antes de chamar o provider.

### Formato WAV ou MP3

O formato é determinado pelo provider, não pelo payload externo.

O `mock` gera WAV.

Os providers reais observados no código geram MP3:

- OpenAI
- Google
- ElevenLabs
- Azure Speech
- Amazon Polly

### Autenticação

Não há autenticação explícita no endpoint HTTP observado em `app/main.py`.

O controle de acesso fica no nível das credenciais de cada provider.

### Token e Basic Auth

Não há uso de token ou Basic Auth no contrato HTTP do endpoint observado.

### Variáveis de ambiente relacionadas

O contrato do endpoint é influenciado por estas variáveis, lidas em [`app/config.py`](/srv/projetos/tts-api-switcher/app/config.py):

- `OPENAI_API_KEY`
- `OPENAI_TTS_MODEL`
- `OPENAI_TTS_VOICE`
- `OPENAI_TTS_FORMAT`
- `GOOGLE_TTS_ENABLED`
- `GOOGLE_APPLICATION_CREDENTIALS`
- `GOOGLE_TTS_VOICE`
- `GOOGLE_TTS_LANGUAGE_CODE`
- `GOOGLE_TTS_AUDIO_ENCODING`
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_MODEL`
- `ELEVENLABS_VOICE_ID`
- `ELEVENLABS_OUTPUT_FORMAT`
- `AZURE_SPEECH_KEY`
- `AZURE_SPEECH_REGION`
- `AZURE_SPEECH_ENDPOINT`
- `AZURE_SPEECH_VOICE`
- `AZURE_SPEECH_OUTPUT_FORMAT`
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AWS_POLLY_VOICE_ID`
- `AWS_POLLY_ENGINE`
- `AWS_POLLY_OUTPUT_FORMAT`

## Mapeamento Agenda Falante para TTS

Mapeamento dos campos atuais do plano TTS do Agenda Falante para o endpoint real:

- `request_id`: não suportado atualmente; não há campo equivalente no payload do endpoint.
- `segment_id`: não suportado atualmente; não há campo equivalente no payload do endpoint.
- `segment_type`: não suportado atualmente; não há campo equivalente no payload do endpoint.
- `text`: suportado como `text`.
- `language`: suportado como `language`.
- `voice`: suportado como `voice`.
- `format`: não suportado atualmente como campo de entrada; o formato é definido pelo provider.
- `output_path`: não suportado atualmente; o endpoint gera e publica o arquivo internamente.
- `cache_key`: não suportado atualmente.
- `usage_profile`: não suportado atualmente.
- `metadata`: não suportado atualmente.

## Lacunas

Lacunas identificadas entre o que o Agenda Falante precisa e o que o motor TTS oferece hoje:

- `usage_profile` ainda não suportado.
- `cache_key` ainda não suportado.
- `output_path` ainda não suportado.
- `request_id` e `segment_id` não fazem parte do contrato real.
- o formato não é um campo explícito do request; ele depende do provider.
- não há contrato de autenticação no endpoint HTTP.
- não há campo explícito de preset no payload.
- o serviço expõe `audio_url` em vez de caminho local.

## Limitações atuais do endpoint

- o contrato é orientado a provider;
- a humanização existe no payload, mas é interna ao serviço;
- o endpoint retorna URL do arquivo gerado, não o áudio binário na resposta JSON;
- o contrato atual não carrega metadados do Agenda Falante;
- o contrato não carrega cache semântico do lado do consumidor.

## Riscos de integração

- o Agenda Falante precisará adaptar seu plano para uma chamada orientada a provider;
- o campo `usage_profile` não tem equivalente direto no endpoint atual;
- o contrato atual não preserva `request_id` nem `segment_id`;
- a saída baseada em `audio_url` pode exigir ajuste no fluxo de consumo local;
- diferenças de formato entre providers podem exigir normalização adicional.

## Recomendações para a próxima etapa

1. Criar um adapter intermediário no Agenda Falante para traduzir plano interno em payload do TTS.
2. Manter `usage_profile` como metadado interno do Agenda Falante até o motor TTS suportá-lo nativamente.
3. Preservar o `request_id` e o `cache_key` no lado do consumidor.
4. Definir uma estratégia explícita para tratar `audio_url` versus caminho local.

## Decisão Recomendada

A melhor próxima etapa é criar um adapter intermediário no Agenda Falante, em vez de adaptar diretamente o plano atual ao contrato do endpoint.

Isso mantém o Agenda Falante desacoplado e permite evoluir o motor TTS sem quebrar o plano interno.

## Validação

Esta documentação foi baseada no código real existente em:

- [`/srv/projetos/tts-api-switcher/app/main.py`](/srv/projetos/tts-api-switcher/app/main.py)
- [`/srv/projetos/tts-api-switcher/app/config.py`](/srv/projetos/tts-api-switcher/app/config.py)
- [`/srv/projetos/tts-api-switcher/app/providers/openai_provider.py`](/srv/projetos/tts-api-switcher/app/providers/openai_provider.py)
- [`/srv/projetos/tts-api-switcher/app/providers/google_provider.py`](/srv/projetos/tts-api-switcher/app/providers/google_provider.py)
- [`/srv/projetos/tts-api-switcher/app/providers/elevenlabs_provider.py`](/srv/projetos/tts-api-switcher/app/providers/elevenlabs_provider.py)
- [`/srv/projetos/tts-api-switcher/app/providers/azure_provider.py`](/srv/projetos/tts-api-switcher/app/providers/azure_provider.py)
- [`/srv/projetos/tts-api-switcher/app/providers/polly_provider.py`](/srv/projetos/tts-api-switcher/app/providers/polly_provider.py)
