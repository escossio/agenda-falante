# 0004 - Android App and Play Store Strategy

## Status

Accepted

## Context

O Agenda Falante começou como um core capaz de importar contatos, gerar segmentos de áudio, planejar geração TTS, integrar com o motor TTS Escossio e compor áudio.

A visão final do projeto é evoluir para um aplicativo Android instalável em APK e, futuramente, publicável na Google Play Store.

Sem uma separação explícita entre core e app mobile, o projeto corre o risco de acoplar regras de domínio, execução de áudio, permissões Android e detalhes de distribuição em uma única base difícil de evoluir.

## Decisão

O projeto será separado em duas camadas conceituais:

- Agenda Falante Core;
- Agenda Falante Android.

O Agenda Falante Core será responsável por:

- importação de contatos;
- normalização de contatos;
- catálogo de segmentos;
- planejamento de geração TTS;
- integração com o motor TTS Escossio;
- cache;
- composição de áudio;
- exportação de pacotes para Android.

O Agenda Falante Android será responsável por:

- interface do usuário;
- permissões Android;
- leitura de chamadas recebidas;
- leitura de notificações, quando autorizado;
- reprodução local dos áudios;
- configurações do usuário;
- integração com Bluetooth;
- integração com Android Auto, se viável;
- execução em segundo plano conforme permitido pelo Android.

O Core não deve depender do Android.

O Android não deve conhecer detalhes internos do motor TTS.

A comunicação entre Core e Android deverá ocorrer por manifestos, pacotes exportados ou APIs claramente definidas.

## Play Store Considerations

Uma futura publicação na Google Play Store exigirá atenção explícita a:

- política de privacidade;
- justificativa clara para uso de contatos;
- justificativa clara para uso de estado de telefone e chamadas recebidas;
- justificativa clara para uso de notificações;
- consentimento explícito do usuário;
- armazenamento local seguro;
- evitar envio automático da agenda para servidores externos;
- controle do usuário sobre quais contatos serão processados;
- opção de excluir dados gerados;
- compatibilidade com permissões modernas do Android;
- respeito às políticas de execução em segundo plano.

## Privacy by Design

Contatos e nomes devem ser tratados como dados sensíveis.

O projeto deve priorizar processamento local sempre que possível.

Quando o motor TTS externo for usado, o usuário deverá saber que o texto poderá sair do dispositivo ou do ambiente local.

O usuário deverá poder escolher quais contatos serão processados.

O usuário deverá poder apagar áudios e manifestos.

## Android Technical Direction

A versão Android futura deve preferencialmente ser nativa, usando Kotlin.

A primeira integração prática poderá usar exportação de arquivos e automação com Tasker ou MacroDroid antes do APK completo.

A implementação Android completa deverá ser planejada em etapa própria.

## Consequências Positivas

- Core reutilizável;
- APK mais limpo;
- facilidade de testes;
- menor acoplamento;
- possibilidade de usar o Core em desktop, servidor ou mobile;
- preparação para Play Store.

## Consequências Negativas

- mais camadas;
- necessidade de contrato entre Core e Android;
- maior cuidado com privacidade;
- maior complexidade de distribuição.

## Próximas Etapas

- criar exportação Android inicial;
- validar reprodução via Tasker ou MacroDroid;
- definir manifesto Android de áudios;
- definir permissões mínimas necessárias;
- criar política de privacidade preliminar;
- planejar projeto Android nativo.

## Resultado Esperado

O Agenda Falante mantém o Core desacoplado do app mobile, preserva a possibilidade de evoluir para APK e prepara a base arquitetural para uma futura publicação na Play Store sem contaminar o núcleo do sistema.

