# 0002 - External TTS Engine

## Status

Accepted

## Context

O Agenda Falante precisa de síntese de voz para gerar os segmentos de áudio usados na composição.

Se o próprio projeto fosse responsável por implementar geração de voz, ele passaria a carregar complexidade desnecessária em áreas como síntese, evolução de vozes, suporte a idiomas e ajustes de qualidade vocal.

## Decisão

O Agenda Falante utilizará exclusivamente o motor TTS do ecossistema Escossio.

O Agenda Falante não será responsável pela geração de voz.

Toda geração de áudio será delegada ao motor TTS do ecossistema Escossio.

Nesse modelo, o Agenda Falante é um consumidor do serviço TTS.

## Consequências positivas

- centralização da evolução da voz;
- reutilização do mesmo motor por outros projetos;
- redução de duplicação de código;
- desacoplamento entre composição e síntese de voz;
- capacidade de evoluir o TTS independentemente do Agenda Falante.

## Regras arquiteturais

O Planner e o Composer nunca deverão implementar regras internas de síntese de voz.

Sua única responsabilidade será solicitar ao motor TTS a geração dos segmentos necessários.

O Agenda Falante deve conhecer apenas a interface pública do motor TTS, sem depender de seus detalhes internos.

## Futuras evoluções

O motor TTS poderá futuramente oferecer:

- novas vozes;
- novos idiomas;
- humanização;
- emoções;
- controle de velocidade;
- controle de entonação;
- pausas inteligentes;
- pronúncia personalizada.

Nenhuma dessas evoluções exigirá alterações na arquitetura do Agenda Falante.

## Resultado esperado

A arquitetura permanece focada em composição e orquestração, enquanto a síntese de voz fica encapsulada no ecossistema Escossio.

Isso mantém o Agenda Falante totalmente desacoplado do mecanismo interno do TTS, conhecendo apenas sua interface pública.

