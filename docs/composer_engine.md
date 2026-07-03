# Composer Engine

O Composer é o componente responsável por transformar um `Composition Manifest` em áudio final.

Ele não decide a intenção do anúncio. Ele executa a montagem.

## Responsabilidades

O Composer deve:

- localizar segmentos de áudio;
- validar sample rate;
- normalizar volume;
- inserir pausas;
- aplicar fade in e fade out;
- unir os WAV;
- exportar WAV;
- exportar MP3;
- permitir cache.

## Escopo

O Composer atua apenas sobre a composição declarada no manifesto.

Ele não deve:

- criar frases completas;
- decidir conteúdo textual;
- implementar lógica de seleção fora do manifesto;
- gerar TTS por conta própria.

## Fluxo esperado

1. Ler o manifesto de composição.
2. Resolver os blocos declarados.
3. Localizar os segmentos correspondentes.
4. Validar compatibilidade técnica dos áudios.
5. Aplicar tratamento de volume e transições.
6. Unir os segmentos.
7. Exportar o resultado final.

## Cache

O Composer pode usar cache para evitar recomputar composições já resolvidas.

O cache pode ser usado para:

- blocos reutilizáveis;
- combinações frequentes;
- saídas já montadas;
- resultados intermediários.

O uso de cache não muda a semântica da composição.

## Composição probabilística

Alguns blocos podem ser escolhidos aleatoriamente por peso.

Exemplo:

- `intro_01` peso `10`
- `intro_02` peso `5`
- `intro_03` peso `1`

Nesse caso:

- `intro_01` tende a aparecer com mais frequência;
- `intro_02` aparece menos;
- `intro_03` se torna raro.

Isso permite variedade sem perder padronização.

### Objetivo da ponderação

Usar pesos ajuda a:

- reduzir repetição perceptível;
- variar a experiência do usuário;
- manter frases ou blocos raros sob controle;
- preservar consistência entre composições.

### Importante

A seleção probabilística é uma decisão de composição, não de geração de conteúdo.

O compositor deve respeitar o manifesto e aplicar a regra de peso apenas quando o bloco estiver definido como variável ou concorrente.

## Requisitos técnicos futuros

O Composer deverá considerar:

- taxa de amostragem consistente;
- volume uniforme entre blocos;
- pequenas transições para evitar cortes bruscos;
- formatos de exportação compatíveis com uso móvel e desktop.

## Resultado esperado

Ao final, o Composer entrega um arquivo pronto para reprodução, mantendo a composição previsível, reutilizável e eficiente.

