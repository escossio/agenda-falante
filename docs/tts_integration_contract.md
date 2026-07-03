# TTS Integration Contract

Este documento define o contrato conceitual entre o Agenda Falante e o motor TTS do ecossistema Escossio.

Ele descreve apenas a interface pública esperada entre os sistemas, sem implementar integração real.

## Visão geral

O Agenda Falante consumirá o motor TTS externo somente por meio de uma interface pública.

Esse consumo existe para gerar segmentos de áudio reutilizáveis, como:

- nomes de contatos;
- introduções;
- encerramentos;
- efeitos falados;
- frases curtas.

O objetivo é manter a síntese de voz fora do escopo interno do Agenda Falante.

## Requisição conceitual ao TTS

Uma requisição conceitual para o TTS poderá conter:

- texto a ser sintetizado;
- idioma;
- voz;
- estilo;
- humor;
- velocidade;
- formato de saída desejado;
- identificador de cache;
- metadados do uso.

Esses dados permitem que o Agenda Falante solicite segmentos consistentes com o contexto da composição.

## Resposta conceitual do TTS

Uma resposta conceitual do TTS poderá conter:

- caminho ou URL do áudio gerado;
- formato do áudio;
- duração;
- hash;
- idioma utilizado;
- voz utilizada;
- informações de cache;
- status da geração.

Esses dados permitem que o Agenda Falante armazene e reutilize os segmentos de forma eficiente.

## Limites de conhecimento do Agenda Falante

O Agenda Falante não deve conhecer detalhes internos do TTS, como:

- provedor;
- modelo;
- pipeline de humanização;
- mecanismo de síntese.

A dependência deve ser restrita ao contrato público.

## Responsabilidades do Agenda Falante

O Agenda Falante deve:

- decidir quais segmentos precisam existir;
- solicitar a geração quando necessário;
- armazenar referências aos segmentos;
- reutilizar o máximo possível.

Ele atua como orquestrador do uso dos segmentos, não como implementador da síntese.

## Responsabilidades do Motor TTS

O Motor TTS deve:

- gerar áudio a partir de texto;
- aplicar voz, idioma e estilo solicitados quando suportado;
- retornar metadados úteis;
- manter sua implementação interna isolada.

Ele é o componente responsável pela síntese de voz, não pela composição do anúncio.

## Regras de cache

O mesmo texto, com a mesma voz, idioma, estilo e formato, deve poder reutilizar o mesmo segmento gerado.

Isso reduz geração redundante e fortalece o reaproveitamento dos ativos de áudio.

## Futuras evoluções

O contrato poderá futuramente incluir:

- pronúncia personalizada;
- emoções;
- perfis de voz;
- fallback de voz;
- normalização automática;
- humanização avançada.

Essas evoluções devem poder ocorrer sem quebrar o princípio de desacoplamento entre Agenda Falante e motor TTS.

## Encerramento

Este documento define apenas um contrato conceitual e não uma implementação.

