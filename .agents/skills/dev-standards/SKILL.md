---
name: dev-standards
description: Padronização de desenvolvimento, microcopy e documentação contínua. Governa micro-textos de UI, atualização mandatória de HISTORICO.md em mudanças arquiteturais/deploy/DB e alinhamento de READMEs internos.
---

# 🛠️ Padrões de Desenvolvimento, Microcopy e Documentação

Esta skill governa o rigor de documentação contínua, consistência de micro-interações/microcopy na interface e organização modular entre o README principal e subdiretórios.

---

## 1. UI/UX e Microcopy Rigoroso

Ao inspecionar ou alterar arquivos de interface (`.html`, `.js`, templates):
- **Botões (CTAs):** Eliminar verbos vagos como "Enviar", "Clique aqui" ou "Confirmar". Usar verbos de ação específicos do domínio:
  - *Exemplos:* `"Registrar Transação"`, `"Atualizar Saldo"`, `"Salvar Categoria"`, `"Exportar Relatório CSV"`.
- **Mensagens de Erro & Validação:**
  - Proibido expor códigos crus como `"Erro 500"` ou `"Falha no fetch"`.
  - Sempre explicar o que aconteceu de forma humana e indicar o próximo passo:
  - *Exemplo:* `"Não foi possível conectar ao servidor. Verifique sua conexão e tente novamente."`
- **Placeholders Descritivos:**
  - Nunca deixar campos sem contexto ou com placeholders genéricos. Usar exemplos de valor reais:
  - *Exemplos:* `"Ex: Salário Mensal"`, `"Ex: Mercado - R$ 150,00"`, `"Ex: Minha Reserva de Emergência"`.
- **Textos Vazios & Anti-AI Tells:**
  - Remover qualquer parágrafo de preenchimento ("Lorem ipsum", "Bem-vindo ao futuro..."). Manter microcopys informativos, concisos e sem ambiguidades.

---

## 2. Documentação Obrigatória no `HISTORICO.md`

Toda vez que ocorrer uma das seguintes ações no repositório:
1. **Alteração Arquitetural** (novos routers, autenticação, refatorações de serviços);
2. **Deploy / Infraestrutura** (ajustes em Vercel, Render, variáveis de ambiente ou CI/CD);
3. **Mudança de Banco de Dados** (migrações Alembic, alteração de tabelas no Supabase/PostgreSQL ou TiDB Cloud);

A ação correspondente deve **obrigatoriamente ser registrada** em `HISTORICO.md` na raiz do projeto com:
- Data (Mês/Ano ou DD/MM/AAAA);
- Categoria da mudança (`Adicionado`, `Modificado`, `Corrigido`, `Segurança`, `Infraestrutura`);
- Resumo conciso do que foi alterado e o impacto técnico.

---

## 3. READMEs Internos e Alinhamento Modular

Ao criar ou editar subpastas com módulos independentes (como `/backend`, `/frontend`, `/scripts`):
- O subdiretório deve conter um `README.md` exclusivo e conciso focado **apenas no escopo daquela pasta**.
- O README interno deve conter obrigatoriamente links de retorno:
  - Para o `[README Principal](../README.md)` (para orientações globais de execução e arquitetura);
  - Para o `[Histórico de Atualizações](../HISTORICO.md)` (para o changelog geral).
