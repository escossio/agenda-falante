# Exportação de Experience Package

Esta é a primeira exportação local de Experience Package no Agenda Falante Core.

Nesta etapa, o pacote exportado ainda é apenas uma pasta no filesystem. Ele não é um formato final nem depende de Android.

O exportador recebe:

- um catálogo de segmentos resolvido;
- um diretório base de áudio;
- um diretório de saída;
- um `package_id`.

O pacote gerado contém:

- `manifest.json`
- `metadata.json`
- `segments/`
- `announcements/`
- `checksums.json`

Comportamento desta primeira versão:

- copia somente segmentos com status `available`;
- ignora segmentos `missing`;
- copia os WAVs para `segments/`;
- gera `manifest.json` com a lista dos segmentos disponíveis;
- gera `metadata.json` com `package_id`, `package_type`, `created_at`, `version` e `source`;
- gera `checksums.json` com SHA-256 dos arquivos copiados;
- não chama TTS;
- não compõe áudio novo;
- não depende de Android.

No futuro, o Android consumirá este pacote pelo Bridge.
