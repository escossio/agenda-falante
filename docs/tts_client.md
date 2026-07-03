# TTS Client

O cliente TTS do Agenda Falante está em modo dry-run.

Nesta etapa, ele apenas prepara a requisição pública esperada pelo motor TTS do ecossistema Escossio.

O preview inclui `usage_profile`, que representa a intenção de uso do áudio e não o provedor nem o modelo.

O dry-run é o modo seguro padrão.

A execução real exige flag explícita.

A execução real controlada exige também base URL explícita.

A execução real ainda não está implementada nesta etapa.

Nenhuma chamada real ao serviço é feita.

A integração real com o motor TTS deverá ler configuração por variáveis de ambiente.

Tokens reais nunca devem ser versionados.

O arquivo `config/tts.example.env` existe apenas como referência de configuração.

## Objetivo

Validar a forma da requisição antes de qualquer integração real.

## Escopo atual

- montar o preview da requisição;
- preservar os dados do plano;
- indicar o motor TTS configurado;
- manter a operação sem rede.

O perfil `fast_name` é usado inicialmente para nomes de contatos.

## Dry-run safety

O modo dry-run é proibido de usar rede, proibido de gerar áudio e serve apenas para visualizar a requisição que seria enviada futuramente ao motor TTS.

Nenhuma chamada de rede deve ocorrer sem confirmação explícita.

O uso recomendado inicial da execução real controlada é contra um endpoint local ou um ambiente explicitamente controlado.
