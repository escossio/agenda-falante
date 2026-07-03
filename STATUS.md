# STATUS

O projeto Agenda Falante está em fase inicial de arquitetura e documentação.

## Estado Atual

Já foram criados documentos para:

- Arquitetura de composição de áudio;
- Manifesto de template;
- Manifesto de composição;
- Engine Composer;
- Planner Architecture;
- Modelo de domínio;
- Contrato conceitual com o motor TTS;
- ADR da arquitetura de composição;
- ADR do uso do motor TTS externo.
- ADR da estratégia de seleção de modelos TTS.
- Documento da camada de perfis de uso TTS.
- Contrato real do endpoint TTS analisado e documentado.

A primeira implementação funcional do projeto foi iniciada com a camada de importação e normalização de contatos.

## Decisões Arquiteturais

- O Agenda Falante utilizará composição por segmentos reutilizáveis.
- O sistema não deve gerar um áudio completo por contato.
- Nomes de contatos serão tratados como segmentos individuais reutilizáveis.
- O Planner decidirá o que será falado.
- O Composer decidirá apenas como montar o áudio final.
- O Composer não deve conhecer regras de negócio, contatos, humor ou contexto.
- O Agenda Falante usará exclusivamente o motor TTS do ecossistema Escossio.
- O Agenda Falante não terá motor TTS próprio.
- A seleção de provedor e modelo de TTS fica encapsulada no motor TTS.

## Implementação Funcional Iniciada

- Importador de Contatos implementado.
- Normalizador de Contatos implementado.
- Suporte VCF implementado.
- Suporte CSV implementado.
- Normalização compartilhada entre VCF e CSV.
- CLI inicial para geração de manifesto de contatos implementada.
- Testes automatizados iniciais do fluxo de contatos adicionados.
- Catálogo inicial de segmentos implementado para `contact_name`.
- Resolvedor inicial de segmentos implementado sem TTS e sem geração de áudio.
- Primeira exportação local de Experience Package implementada.
- Plano inicial de geração TTS implementado sem integração real.
- Executor fake/local para validação do pipeline implementado sem TTS real.
- Relatório consolidado do pipeline inicial implementado.
- Cliente TTS dry-run criado sem integração real.
- Configuração segura do cliente TTS preparada.
- Guardrails anti-rede adicionados ao cliente TTS dry-run.
- Estratégia de seleção de modelos TTS documentada oficialmente.
- Camada conceitual de perfis de uso TTS documentada.
- Plano de geração TTS enriquecido com `usage_profile`.
- Estrutura segura para execução real do TTS preparada.
- Contrato real do endpoint TTS documentado.
- Adapter dry-run para o endpoint real do TTS criado.
- Execução real controlada de um item do plano TTS preparada.
- CLI de execução real controlada agora exige base URL explícita.
- Auditoria arquitetural pré-commit concluída.
- Repositório limpo.
- Versionamento inicial criado.
- Branch principal padronizada.
- Identidade Git configurada localmente.
- Roadmap GitHub da milestone `v0.1.0-alpha` planejado.
- Script de importação do roadmap GitHub criado.
- Importação do roadmap GitHub `v0.1.0-alpha` executada com sucesso.
- Primeira demonstração ponta a ponta do Agenda Falante implementada.
- Documentação da primeira demonstração funcional de áudio real criada.
- Composer mínimo implementado para concatenação simples de WAVs.
- Estratégia futura de APK Android e Play Store documentada em ADR.
- Manifesto de contatos normalizados gerado sem informações de áudio.
- Validação básica executada com arquivo VCF de exemplo.
- Validação básica executada com arquivo CSV de exemplo.

## Pendências Confirmadas

- Geração de áudio.
- TTS.
- Planner.
- Composer.
- Android.

## Componentes Ainda Não Implementados

- Geração de segmentos de nomes.
- Geração de templates reutilizáveis.
- Cliente de integração com o TTS.
- Planner.
- Composer.
- Cache.
- Exportação Android.
- Integração com chamadas no Android.
- Integração com notificações.

## Próximo Passo Recomendado

O próximo passo recomendado é iniciar a implementação mínima da leitura e normalização de contatos, mantendo a arquitetura documentada como referência.

## Restrições Importantes

- Não implementar lógica fora do escopo solicitado.
- Não acoplar o projeto ao mecanismo interno do TTS.
- Não fazer o Composer tomar decisões de negócio.
- Não gerar áudio completo por contato como abordagem principal.
- Não realizar commit sem validação e autorização.

## Observação Final

O projeto ainda não possui funcionalidade operacional implementada.
