# Importação do roadmap GitHub

Este repositório mantém o roadmap da milestone `v0.1.0-alpha` em `docs/github_roadmap_v0_1_alpha.md`.

## Script

Use o script abaixo para criar a milestone e importar as issues no GitHub:

```bash
./scripts/create_github_roadmap_v0_1_alpha.sh
```

## O que o script faz

1. Valida se `gh` está instalado.
1. Valida se `gh auth status` passa.
1. Valida se o remoto `origin` está configurado no repositório.
1. Cria a milestone `v0.1.0-alpha` se ela ainda não existir.
1. Cria as issues documentadas no roadmap.
1. Evita duplicação por título de issue.
1. Associa todas as issues à milestone `v0.1.0-alpha`.

## Observações

- O script é idempotente para a milestone e para as issues listadas.
- Se uma issue com o mesmo título já existir, ela não será recriada.
- O conteúdo de referência para as issues permanece em `docs/github_roadmap_v0_1_alpha.md`.

