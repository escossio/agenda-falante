# 0003 - TTS Model Selection Strategy

## Status

Accepted

## Context

O Agenda Falante depende do motor TTS do ecossistema Escossio para a geração dos segmentos de áudio usados na composição.

O Agenda Falante não conhece provedores externos e não deve tomar decisões sobre seleção de infraestrutura de síntese.

Toda decisão sobre provedores, modelos e trade-offs de síntese pertence ao motor TTS.

## Decisão

O motor TTS deverá suportar múltiplos provedores de síntese de voz.

O Agenda Falante continuará solicitando apenas:

- texto;
- idioma;
- voz;
- estilo;
- humor;
- formato.

O motor TTS será responsável por selecionar o melhor provedor e o melhor modelo para cada solicitação.

## Estratégia Inicial

Para segmentos simples e curtos, como nomes de contatos, o motor TTS deverá priorizar modelos rápidos e de baixo custo.

Para templates reutilizáveis, o motor TTS deverá priorizar modelos com maior naturalidade e expressividade.

A recomendação inicial para essa estratégia é:

- `ElevenLabs Turbo` para segmentos curtos;
- `ElevenLabs Multilingual` para templates reutilizáveis.

Essa escolha é uma recomendação inicial, não uma dependência permanente da arquitetura.

## Critérios Futuros de Seleção

A seleção de modelo e provedor poderá considerar, no futuro:

- naturalidade;
- velocidade;
- latência;
- custo;
- consumo de créditos;
- qualidade da pronúncia em português;
- consistência entre segmentos;
- capacidade de controle de emoção;
- capacidade de controle de velocidade;
- capacidade de controle de entonação.

## Arquitetura

O Agenda Falante nunca conhece provedores.

O Planner nunca conhece provedores.

O Composer nunca conhece provedores.

Somente o motor TTS conhece provedores e modelos.

Isso preserva o desacoplamento entre o Agenda Falante e as tecnologias internas de síntese usadas pelo motor TTS.

## Evoluções Futuras

O motor TTS poderá futuramente incorporar novos provedores e motores, como:

- OpenAI;
- Google;
- Azure;
- Amazon Polly;
- Coqui;
- Piper;
- modelos locais.

A inclusão dessas opções não deve exigir alterações na arquitetura do Agenda Falante.

## Resultado Esperado

O Agenda Falante depende apenas da interface pública do motor TTS.

A seleção de provedor e modelo fica encapsulada no ecossistema Escossio.

O Agenda Falante permanece completamente desacoplado das tecnologias de síntese utilizadas internamente.
