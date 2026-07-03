# Template Manifest

Este documento define o formato do manifesto de cada template de áudio.

## Objetivo

O manifesto descreve como um template é montado e quais partes ele usa para compor o áudio final.

O foco é reutilização:

- partes comuns ficam no template;
- o nome do contato fica separado;
- a composição final junta tudo no momento da execução.

## Exemplo de manifesto

```json
{
  "template_id": "incoming_call_friendly_001",
  "language": "pt-BR",
  "parts": [
    "intro.wav",
    "contact_name",
    "outro.wav"
  ],
  "random_weight": 1
}
```

## Campos

### `template_id`

Identificador único do template.

Exemplo:

- `incoming_call_friendly_001`

### `language`

Idioma do template.

Exemplo:

- `pt-BR`

### `parts`

Lista ordenada das partes que compõem o anúncio.

Valores possíveis:

- nome de arquivo, como `intro.wav` e `outro.wav`;
- marcador lógico, como `contact_name`, que representa o trecho individual do contato.

O significado prático é:

- `intro.wav`: abertura reutilizável;
- `contact_name`: nome do contato gerado individualmente;
- `outro.wav`: fechamento reutilizável.

### `random_weight`

Peso para seleção probabilística entre templates equivalentes ou variações do mesmo contexto.

Exemplo:

- `1` para peso neutro;
- valores maiores para aumentar a chance de escolha daquele template.

## Regras de uso

- O manifesto não deve conter frase completa pronta para cada contato.
- O manifesto deve descrever apenas peças reutilizáveis e pontos de inserção do nome.
- O compositor é quem monta a saída final.
- A geração TTS deve ser aplicada somente às partes necessárias.

## Relação com o Composer

O futuro Audio Composer deverá ler este manifesto e:

- localizar as partes de áudio;
- montar a sequência definida em `parts`;
- aplicar processamento final;
- exportar o arquivo final.

## Convenção de diretórios

Os manifestos devem ficar em:

```text
manifest/
```

Os templates de áudio devem ficar em:

```text
templates/
```

Os áudios intermediários ou reaproveitáveis podem usar:

```text
cache/
```

e a saída final:

```text
output/
```

