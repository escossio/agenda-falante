# GitHub Roadmap v0.1.0-alpha

Este documento prepara a organização inicial de roadmap para o Agenda Falante.

Como o `gh` não estava autenticado neste ambiente, a milestone e as issues foram registradas localmente para posterior criação no GitHub.

## Milestone

### `v0.1.0-alpha`

Descrição:

Primeira versão alpha do Agenda Falante, cobrindo geração real de segmentos, templates reutilizáveis, Composer inicial, Planner inicial e preparação para integração Android.

## Issues iniciais

### 1. Gerar segmentos reais `contact_name` usando motor TTS Escossio

Usar o plano TTS existente e a execução real controlada para gerar segmentos de nomes de contatos, mantendo limite seguro, base URL explícita e sem execução em lote descontrolada.

### 2. Criar templates reutilizáveis de chamada recebida

Criar catálogo inicial de templates reutilizáveis para chamadas recebidas, incluindo intro, outro e variações de estilo amigável, profissional e urgente.

### 3. Implementar Composer inicial de áudio

Implementar composição simples de segmentos WAV com sequência definida por manifesto, incluindo validação de arquivos, concatenação, pausas e saída final.

### 4. Implementar Planner inicial para `incoming_call`

Criar Planner mínimo capaz de receber evento de chamada recebida, escolher estratégia simples e produzir `Composition Manifest`.

### 5. Exportar pacote Android inicial

Criar exportação dos áudios e manifestos para uma estrutura compatível com Android, Tasker ou MacroDroid.

### 6. Validar reprodução no Android com Tasker ou MacroDroid

Testar fluxo manual no Android para tocar áudio correspondente a um contato durante chamada recebida.

### 7. Adicionar cache real de segmentos TTS

Evitar geração repetida de segmentos já existentes usando `cache_key`, `segment_id` e verificação de arquivos disponíveis.

### 8. Documentar primeira execução real controlada

Criar documentação de operação segura para executar geração real de 1 segmento contra o motor TTS local Escossio.

## Próximo passo

Quando o `gh` estiver autenticado, estas entradas podem ser convertidas em milestone e issues no GitHub sem alterar o conteúdo aqui documentado.
