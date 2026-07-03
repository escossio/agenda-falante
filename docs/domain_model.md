# Domain Model

Este documento define o modelo conceitual de dados do Agenda Falante.

Ele descreve as entidades centrais do domínio e as relações entre elas, sem implementar código ou estruturas concretas.

## Entidades principais

### 1. Event

`Event` representa um acontecimento que poderá gerar um anúncio.

Exemplos de Event:

- ligação recebida;
- notificação;
- alarme;
- mensagem;
- lembrete.

Um `Event` contém apenas contexto.

Ele nunca contém referências para arquivos de áudio.

Sua função é descrever o que aconteceu, quando aconteceu e em que condições aconteceu.

### 2. Composition Plan

`Composition Plan` representa o plano produzido pelo Planner.

Esse plano descreve como o anúncio deverá ser construído, mas não contém áudio.

Um `Composition Plan` poderá conter:

- categoria;
- humor;
- idioma;
- voz;
- estratégia;
- sequência lógica;
- regras de composição.

Ele traduz o contexto do `Event` em instruções conceituais para composição.

### 3. Audio Segment

`Audio Segment` representa um bloco reutilizável de áudio.

Exemplos de Audio Segment:

- introdução;
- nome do contato;
- efeito sonoro;
- pausa;
- encerramento.

Audio Segments são independentes e podem ser reutilizados por milhares de anúncios.

Eles são os componentes básicos que permitem a composição por partes.

### 4. Composition Result

`Composition Result` representa o áudio produzido pelo Composer.

Ele poderá conter:

- arquivo WAV;
- arquivo MP3;
- metadados;
- tempo total;
- hash da composição;
- informações de cache.

Esse resultado é a materialização final do plano em mídia reproduzível.

## Relação entre entidades

O fluxo conceitual entre as entidades é o seguinte:

`Event` gera um `Composition Plan`.

O `Composition Plan` referencia `Audio Segments`.

O Composer utiliza os `Audio Segments`.

O Composer produz um `Composition Result`.

Em termos práticos:

```text
Event
↓
Composition Plan
↓
Audio Segments
↓
Composer
↓
Composition Result
```

## Princípios do modelo

O modelo de domínio do Agenda Falante é guiado pelos seguintes princípios:

### Separação entre contexto e mídia

O `Event` representa contexto.

Os `Audio Segments` representam mídia.

Esses dois mundos devem permanecer separados.

### Reutilização máxima

Os mesmos segmentos devem poder ser usados em múltiplas composições e cenários.

### Baixo custo de geração TTS

A geração textual para voz deve ser concentrada apenas no que for individual ou realmente necessário.

### Composição determinística

Dado um plano e os segmentos correspondentes, o resultado deve ser previsível e controlável.

### Escalabilidade

O modelo deve permitir crescimento em quantidade de eventos, categorias, templates, idiomas e variações sem exigir geração completa por contato.

### Desacoplamento entre inteligência e reprodução

A lógica de decisão e o mecanismo de reprodução devem permanecer separados.

Isso permite evoluir o sistema sem misturar planejamento com montagem de áudio.

## Papel do modelo no projeto

Este modelo conceitual organiza a base do sistema em torno de eventos, planos, segmentos e resultados.

Ele serve como referência para entender como o Planner e o Composer se relacionam com o domínio.

Este modelo de domínio servirá como base para toda a implementação futura do Agenda Falante.

