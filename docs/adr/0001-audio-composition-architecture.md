# 0001 - Audio Composition Architecture

## Status

Accepted

## Context

Uma abordagem ingênua para o Agenda Falante seria gerar um áudio completo para cada contato.

Exemplos:

- "João está ligando"
- "Maria está ligando"
- "Carlos está ligando"

Essa estratégia é simples de imaginar, mas traz problemas claros:

- alto custo de TTS;
- alto consumo de armazenamento;
- dificuldade para atualizar frases;
- baixa reutilização.

Quanto mais contatos existirem, maior será o custo de manter e regenerar os áudios.

## Decisão

Adotar uma arquitetura baseada em composição.

Nesse modelo, um anúncio é montado a partir de segmentos reutilizáveis, em vez de ser gerado como uma frase completa para cada contato.

Exemplo:

```text
intro.wav
+ 
contact_name.wav
+ 
outro.wav
```

A composição permite que apenas a parte individual do contato precise ser tratada de forma específica, enquanto os demais trechos permanecem reutilizáveis.

## Consequências positivas

- enorme redução de geração TTS;
- reutilização de áudio;
- novos templates sem regenerar contatos;
- cache eficiente;
- composição probabilística;
- escalabilidade.

## Consequências negativas

- necessidade de um compositor;
- gerenciamento de sample rate;
- sincronização entre segmentos;
- aplicação de fades.

## Futuras evoluções

Essa arquitetura abre espaço para evoluções como:

- vocabulário reutilizável;
- fragmentação de nomes;
- notificações;
- Android Auto;
- Wear OS;
- Bluetooth;
- múltiplos idiomas.

## Resultado esperado

A decisão arquitetural prioriza reutilização, manutenção simples e escalabilidade, aceitando a complexidade adicional do compositor como custo necessário para reduzir drasticamente a geração de áudio redundante.

