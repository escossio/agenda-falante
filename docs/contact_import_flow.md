# Contact Import Flow

O fluxo inicial de contatos do Agenda Falante segue estas etapas:

```text
Arquivo VCF ou CSV
↓
Importador
↓
Normalizador
↓
Manifesto de contatos
↓
Catálogo de segmentos
↓
Próximas etapas
```

## CLI recomendada

A forma recomendada de gerar o manifesto de contatos normalizados é pela CLI:

```bash
python scripts/generate_contacts_manifest.py --input fixtures/sample_contacts.vcf --format vcf --output manifest/contacts_normalized.json
python scripts/generate_contacts_manifest.py --input fixtures/sample_contacts.csv --format csv --output manifest/contacts_normalized.csv.json
```

## Arquivo VCF

O arquivo VCF é a fonte inicial de entrada para importação de contatos.

## Arquivo CSV

O arquivo CSV também é suportado como fonte de entrada para importação de contatos.

O importador aceita colunas comuns como:

- `name`
- `phone`
- `email`
- `organization`

E variações frequentes como:

- `full_name`
- `display_name`
- `nome`
- `telefone`
- `phone_number`
- `email_address`
- `empresa`
- `organization`

## Importador

O importador lê VCF ou CSV, extrai os dados relevantes e prepara a estrutura intermediária dos contatos.

## Normalizador

O normalizador padroniza nomes, telefones e e-mails, remove duplicidades e ignora registros vazios ou sem nome.

## Manifesto de contatos

O manifesto contém apenas informações de identidade dos contatos, sem qualquer dado de áudio.

## Catálogo de segmentos

Após o manifesto de contatos, o próximo artefato é o catálogo de segmentos.

Nesta etapa, o sistema identifica quais segmentos de áudio precisam existir, ainda sem gerar áudio.

## Próximas etapas

Após esse fluxo, o projeto poderá evoluir para geração de templates, Planner e Composer.
