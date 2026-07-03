# Segment Catalog

O catálogo de segmentos define o que precisa existir como áudio, sem conter áudio nesta etapa.

Nesta primeira versão, o catálogo transforma contatos normalizados em necessidades de segmentos do tipo `contact_name`.

Cada segmento descreve:

- identificador estável;
- tipo do segmento;
- texto que deverá ser falado;
- idioma;
- voz;
- contato de origem;
- status.

O catálogo é uma etapa intermediária entre os contatos normalizados e futuras etapas de geração ou composição.

## Status dos segmentos

Nesta fase, os segmentos podem estar em dois estados:

- `missing`: o áudio ainda precisa ser gerado;
- `available`: o áudio já existe no disco.

Quando um segmento está `available`, o catálogo resolvido pode incluir `audio_path`.

Quando um segmento está `missing`, não há caminho de áudio associado.

