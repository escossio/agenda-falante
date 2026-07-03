# Planner Architecture

Esta arquitetura divide o Agenda Falante em duas camadas principais:

1. Planner
2. Composer

O objetivo dessa separação é manter a inteligência de decisão isolada da montagem de áudio.

## Visão geral

O Planner opera em nível de eventos e contexto.

O Composer opera em nível de segmentos de áudio.

Essa divisão é intencional:

- o Planner decide o que deve ser dito e como a composição deve se comportar;
- o Composer executa a montagem do áudio sem tomar decisões de produto.

## Planner

O Planner é a camada responsável pela inteligência da composição.

Ele nunca:

- manipula arquivos de áudio;
- concatena WAV;
- conhece detalhes de implementação do Composer.

Sua única responsabilidade é interpretar o evento recebido e produzir um plano completo de composição.

## Dados de entrada do Planner

Um evento pode conter informações como:

- tipo do evento;
- nome do contato;
- primeiro nome;
- relação do contato;
- grupo do contato;
- apelido do usuário;
- idioma;
- voz;
- humor desejado;
- horário;
- período do dia;
- prioridade;
- quantidade de chamadas repetidas;
- configurações do usuário.

O Planner usa esses dados para decidir a forma da composição.

## Decisões do Planner

Após interpretar o evento, o Planner deve decidir:

- qual categoria de template utilizar;
- qual estilo utilizar;
- qual personalidade utilizar;
- qual voz utilizar;
- qual idioma utilizar;
- se utiliza primeiro nome ou nome completo;
- se repete o nome;
- se utiliza efeitos sonoros;
- se adiciona pausas conceituais;
- qual estratégia probabilística utilizar;
- quais segmentos deverão compor o anúncio.

O resultado produzido pelo Planner deve ser um `Composition Manifest` completamente definido.

## Composer

O Composer é a camada responsável exclusivamente pela montagem do áudio.

Ele nunca toma decisões de conteúdo ou de contexto.

Ele apenas recebe um `Composition Manifest`.

Suas responsabilidades são exclusivamente:

- localizar segmentos;
- validar segmentos;
- validar sample rate;
- validar canais de áudio;
- aplicar pausas;
- aplicar fades;
- normalizar volume;
- concatenar segmentos;
- exportar WAV;
- exportar MP3;
- permitir cache.

## Fluxo completo

```text
Evento
↓
Planner
↓
Composition Manifest
↓
Composer
↓
Áudio Final
```

## Exemplos

### 1. Ligação de um familiar com estilo descontraído

Evento:

- contato identificado como familiar;
- nome disponível;
- idioma pt-BR;
- tom informal;
- humor desejado leve.

Decisão do Planner:

- escolher template de família;
- usar estilo descontraído;
- usar voz compatível com proximidade;
- optar por primeiro nome, se apropriado;
- selecionar segmentos com abertura mais leve e fechamento informal.

### 2. Ligação de trabalho com estilo profissional

Evento:

- contato identificado como trabalho;
- horário comercial;
- prioridade normal;
- configuração do usuário orientada a formalidade.

Decisão do Planner:

- escolher template profissional;
- usar estilo formal;
- usar voz neutra ou corporativa;
- usar nome completo se necessário;
- evitar efeitos sonoros excessivos;
- selecionar segmentos objetivos e discretos.

### 3. Ligação repetida durante a madrugada com estilo urgente

Evento:

- chamadas repetidas;
- horário de madrugada;
- prioridade alta;
- contexto de urgência.

Decisão do Planner:

- escolher template urgente;
- usar estilo direto;
- aumentar intensidade perceptiva da composição;
- considerar repetição do nome ou do alerta;
- incluir pausas mínimas;
- priorizar blocos probabilisticamente mais raros ou mais incisivos.

## Benefícios da arquitetura

Separar Planner e Composer traz benefícios estruturais claros:

- a inteligência do sistema pode evoluir sem modificar a engine de composição;
- novos comportamentos podem ser adicionados apenas evoluindo o Planner;
- a montagem sonora permanece estável;
- o Composer continua simples e previsível;
- o sistema fica mais fácil de manter e testar conceitualmente;
- a composição se torna compatível com múltiplos cenários e personalidades.

## Evoluções futuras

Essa separação permite expandir o Planner com novas capacidades, como:

- Android Auto;
- Wear OS;
- notificações de aplicativos;
- Bluetooth;
- múltiplos idiomas;
- múltiplas vozes;
- regras por contato;
- regras por grupos;
- contexto por horário;
- integração com agenda;
- integração com calendário;
- personalidades diferentes;
- novos motores TTS.

## Observação final

Planner e Composer possuem responsabilidades completamente independentes e devem permanecer desacoplados durante toda a evolução do projeto.

