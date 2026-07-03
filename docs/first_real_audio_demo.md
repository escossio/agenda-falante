# Primeira demonstração funcional de áudio real

Esta demonstração executa o primeiro fluxo ponta a ponta do Agenda Falante:

1. importa contatos;
1. normaliza os dados;
1. seleciona apenas o primeiro contato normalizado;
1. gera o catálogo de segmentos;
1. resolve os segmentos existentes;
1. cria o plano TTS;
1. seleciona somente o primeiro segmento `missing`;
1. usa o adapter real do endpoint;
1. executa geração real contra o motor TTS Escossio;
1. salva o WAV em `output/audio/segments/{segment_id}.wav`;
1. resolve o catálogo novamente;
1. confirma que o segmento passou de `missing` para `available`.

## Pré-requisitos

- Python disponível no ambiente.
- Servidor local do motor TTS Escossio acessível.
- O endpoint de geração deve responder em `POST /api/generate-audio`.
- O endpoint deve devolver `audio_url` para download do arquivo WAV.

## Como executar

Use uma base de contatos em `vcf` ou `csv` e informe um diretório de trabalho vazio:

```bash
python scripts/demo_generate_first_contact_audio.py \
  --input fixtures/sample_contacts.csv \
  --format csv \
  --workdir /tmp/agenda-falante-demo \
  --base-url http://127.0.0.1:8000
```

## O que a CLI gera

- `contacts_normalized.json`
- `segment_catalog.json`
- `segment_catalog_resolved_initial.json`
- `tts_generation_plan_execution.json`
- `real_tts_single_execution_report.json`
- `segment_catalog_resolved_final.json`
- `output/audio/segments/{segment_id}.wav`

## Como validar a geração real

1. Verifique que a CLI terminou com `Status final: available`.
1. Confirme que existe exatamente um arquivo WAV em `output/audio/segments/`.
1. Abra `segment_catalog_resolved_final.json` e confirme que o segmento está como `available`.
1. Verifique que o relatório de execução real mostra status `generated`.
1. Confirme que nenhum fluxo em lote foi usado, porque a demonstração seleciona apenas o primeiro contato e cria apenas um request.

