# Perfis de Uso TTS

Este documento define a camada conceitual de perfis de uso TTS do Agenda Falante.

O Agenda Falante não deve solicitar provedores ou modelos diretamente.

Em vez disso, o Agenda Falante deverá solicitar perfis de uso TTS.

Esses perfis representam a intenção de uso do áudio.

O motor TTS do ecossistema Escossio será responsável por mapear cada perfil para o provedor e o modelo mais adequado.

## Perfis iniciais

### `fast_name`

- Uso: nomes de contatos e segmentos curtos.
- Prioridade: velocidade, baixo custo, boa pronúncia.
- Exemplo: `Nilvanda Escossio`.

### `expressive_template`

- Uso: introduções, encerramentos e templates reutilizáveis.
- Prioridade: naturalidade, expressividade, consistência de voz.
- Exemplo: `Atenção Leo, você está recebendo uma ligação.`

### `notification_short`

- Uso: notificações rápidas.
- Prioridade: clareza e baixa latência.
- Exemplo: `Nova mensagem recebida.`

### `urgent_alert`

- Uso: alertas importantes ou chamadas repetidas.
- Prioridade: impacto, clareza e entonação firme.
- Exemplo: `Atenção, chamada repetida durante a madrugada.`

## Regra Arquitetural

Agenda Falante conhece perfis de uso.

Agenda Falante não conhece provedores.

Agenda Falante não conhece modelos.

Planner pode escolher perfil de uso.

Composer não escolhe perfil de uso.

Motor TTS converte perfil de uso em provedor, modelo, voz e parâmetros.

## Benefícios

Essa camada permite trocar modelos sem alterar o Agenda Falante.

Ela permite usar modelos baratos para nomes e modelos mais expressivos para templates.

Ela mantém o custo controlado.

Ela preserva a naturalidade nos segmentos reutilizáveis.

## Futuras Evoluções

Perfis adicionais poderão ser introduzidos no futuro, como:

- `family_warm`;
- `work_professional`;
- `funny_personality`;
- `night_low_volume`;
- `car_bluetooth_clear`;
- `accessibility_slow_speech`.

## Resultado Esperado

Os perfis de uso TTS são uma camada semântica entre o Planner e o motor TTS.

O Agenda Falante permanece desacoplado da seleção interna de provedores e modelos.
