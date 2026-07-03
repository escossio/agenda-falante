# Composition Manifest

O `Composition Manifest` descreve a sequência lógica de montagem de um anúncio.

Ele não descreve o áudio final em si. Ele descreve apenas a ordem e o tipo dos blocos que o compositor deve interpretar.

## Objetivo

Separar a intenção da composição da implementação sonora.

Em vez de gravar uma frase pronta para cada caso, o sistema descreve:

- quais blocos usar;
- em que ordem usar;
- quais partes podem variar;
- quais partes são reutilizáveis.

## Exemplo básico

```json
{
  "composition_id": "incoming_call_001",
  "sequence": [
    {
      "type": "template",
      "id": "friendly_intro_01"
    },
    {
      "type": "contact_name"
    },
    {
      "type": "template",
      "id": "friendly_outro_02"
    }
  ]
}
```

Neste exemplo:

- `template` aponta para um bloco reutilizável;
- `contact_name` representa o nome individualizado do contato;
- `sequence` define a ordem de montagem.

## Regras do manifesto

- O manifesto descreve a sequência lógica, não o áudio pronto.
- O manifesto não deve conter frases completas por contato.
- O compositor é responsável por interpretar o manifesto.
- Os blocos podem ser reutilizados entre diferentes composições.

## Tipos previstos

Os tipos iniciais e futuros podem incluir:

- `template`
- `contact_name`
- `silence`
- `beep`
- `random`
- `conditional`
- `variable`
- `notification_sound`

## Exemplo futuro

```text
[
  intro,
  random(
    outro_01,
    outro_02,
    outro_03
  ),
  contact_name,
  silence(250ms),
  random(
    final_01,
    final_02
  )
]
```

Neste formato, o manifesto ainda representa lógica de composição, não o arquivo sonoro final.

## Estrutura conceitual

Um manifesto pode ser entendido como:

- identificador da composição;
- lista ordenada de blocos;
- instruções de variação;
- parâmetros de tempo ou seleção, quando aplicável.

## Extensibilidade

O formato foi pensado para crescer sem quebrar o princípio básico:

- blocos fixos continuam reutilizáveis;
- blocos variáveis continuam declarados de forma explícita;
- o compositor continua sendo o único responsável pela montagem final.

