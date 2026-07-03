# Audio Composition

Este projeto usa composição de áudio por partes, não geração de frases completas por contato.

## Filosofia

A ideia central é reduzir drasticamente a quantidade de TTS necessária. Em vez de gerar um áudio único para cada contato, cada anúncio é montado a partir de trechos reutilizáveis:

- uma abertura reutilizável;
- o nome do contato, gerado de forma individual;
- um fechamento reutilizável.

Exemplo de composição:

- `intro.wav`
- `contact_name.wav`
- `outro.wav`

Isso permite reaproveitar o mesmo material para muitos contatos e muitos cenários, com custo menor, menos variação desnecessária e mais consistência de voz.

## Reuso obrigatório

Os arquivos de abertura e fechamento são compartilhados por todos os contatos dentro de um mesmo template.

- `intro.wav` é reutilizado por todos os contatos daquele template;
- `outro.wav` é reutilizado por todos os contatos daquele template;
- apenas o nome do contato é individual.

Exemplos de composição final:

- `Atenção, Leo...` + `Nilvanda Escossio` + `está te ligando. Atende rapaz.`
- `Leo...` + `Nilvanda` + `está chamando.`
- `Você recebeu uma ligação de` + `João Silva` + `.`

## Estrutura lógica

Proposta de organização:

```text
agenda-falante/
templates/
  incoming_call/
    friendly/
    urgent/
    professional/
    funny/
  notifications/
contact_names/
manifest/
cache/
output/
docs/
```

Essas pastas separam:

- templates reutilizáveis por contexto;
- componentes de nomes;
- manifestos de composição;
- cache de áudio gerado;
- saída final.

## Pipeline conceitual

```text
CSV/VCF
↓
Normalização
↓
Extração dos nomes
↓
Gerar apenas os nomes
↓
Gerar templates reutilizáveis
↓
Compositor
↓
Áudio final
```

### Etapas

- CSV/VCF: entrada de contatos.
- Normalização: limpeza e padronização dos dados.
- Extração dos nomes: definição do texto base que será falado.
- Gerar apenas os nomes: TTS restrito ao componente individual.
- Gerar templates reutilizáveis: produção dos trechos comuns.
- Compositor: união dos segmentos.
- Áudio final: exportação para uso imediato.

## Futuro Audio Composer

O Composer será o componente responsável por montar o áudio final a partir dos segmentos. Ele deverá:

- unir arquivos WAV;
- preservar a taxa de amostragem;
- normalizar volume;
- aplicar pequenos fades entre os segmentos;
- exportar em WAV ou MP3.

Importante: este documento define apenas a arquitetura. Nenhuma implementação de composição deve existir ainda.

## Categorias futuras de templates

O sistema deve acomodar, no futuro, categorias como:

- Formal
- Divertido
- Família
- Trabalho
- Urgente
- Humor
- Inteligência Artificial
- Voz feminina
- Voz masculina

Essas categorias devem servir para selecionar variações de abertura, fechamento, voz e tom, sem alterar o princípio de composição por partes.

