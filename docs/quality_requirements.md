# Quality Requirements

Este documento define os critérios de qualidade e validação do Agenda Falante antes do início da implementação.

Ele serve como referência para orientar decisões futuras de arquitetura, composição e validação.

## Qualidade da Composição

Um anúncio deverá parecer natural para o usuário.

Ele não deverá apresentar:

- cortes perceptíveis entre segmentos;
- diferenças perceptíveis de volume;
- diferenças perceptíveis de velocidade da fala;
- diferenças perceptíveis de timbre.

A composição deve preservar fluidez sonora e consistência perceptiva entre as partes.

## Requisitos Funcionais

O sistema deverá:

- compor anúncios utilizando segmentos reutilizáveis;
- permitir múltiplos templates;
- permitir múltiplas vozes;
- permitir múltiplos idiomas;
- permitir cache;
- permitir composição probabilística.

## Requisitos Não Funcionais

O Composer deverá ser determinístico quando solicitado.

O sistema também deverá:

- permitir comportamento aleatório controlado;
- minimizar geração desnecessária de TTS;
- maximizar reutilização de segmentos;
- permitir crescimento do catálogo sem impacto significativo de desempenho.

## Critérios de Aceitação

Um anúncio deverá ser considerado válido quando:

- a composição ocorrer sem erros;
- todos os segmentos existirem;
- a sequência for respeitada;
- o áudio final puder ser reproduzido normalmente;
- o resultado não apresentar diferenças perceptíveis entre os segmentos.

## Futuras Métricas

Indicadores que poderão ser acompanhados no futuro:

- quantidade de segmentos reutilizados;
- economia de geração TTS;
- tempo médio de composição;
- tempo médio de geração;
- quantidade de templates;
- quantidade de vozes;
- taxa de reutilização;
- tamanho do cache.

## Papel destes requisitos

Esses requisitos servirão como referência para validação das próximas implementações.

