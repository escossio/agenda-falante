# Composer mínimo

Esta é a primeira implementação funcional do Composer do Agenda Falante.

## O que ele faz

- recebe uma sequência explícita de arquivos WAV;
- valida se todos existem;
- valida se todos são WAV válidos;
- valida compatibilidade básica entre os segmentos;
- concatena os segmentos na ordem recebida;
- exporta um único WAV final.

## O que ele não faz

- não aplica fades;
- não normaliza volume;
- não altera velocidade;
- não altera sample rate;
- não implementa composição probabilística;
- não chama TTS;
- não toma decisões de Planner;
- não depende de Android.

## Escopo técnico

A implementação usa apenas a biblioteca padrão do Python. O comportamento é propositalmente simples para servir como base da evolução do Composer.

## Uso

```bash
python3 scripts/compose_announcement.py \
  --segments fixtures/audio/intro.wav fixtures/audio/contact_name.wav fixtures/audio/outro.wav \
  --output output/audio/announcements/demo_announcement.wav
```

## Evolução futura

Etapas posteriores podem adicionar:

- fades curtos entre segmentos;
- pausas inteligentes;
- normalização;
- estratégias probabilísticas;
- composição guiada por manifesto;
- otimizações de cache.

