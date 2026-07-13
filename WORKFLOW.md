# 🚀 Git Workflow - Task Manager API

## Estrutura de Branches

```
main (produção)
  ↑
  └─ Pull Request (revisão)
dev (desenvolvimento)
  ↑
  └─ Merge (feature branch)
    ├─ feature/nome-funcionalidade-1
    ├─ feature/nome-funcionalidade-2
    └─ feature/nome-funcionalidade-3
```

## 📋 Processo para Novas Features

### 1️⃣ Criar Branch da Feature

```bash
# Sincronize com a branch dev
git checkout dev
git pull origin dev

# Crie a branch da feature
git checkout -b feature/nome-da-feature
```

### 2️⃣ Trabalhar na Feature

- Faça todos os commits **nesta branch**
- Siga o padrão de commits (veja abaixo)
- Faça push regularmente

```bash
git add .
git commit -m "feat: descrição da mudança"
git push origin feature/nome-da-feature
```

### 3️⃣ Fazer Merge com Dev

```bash
# Sincronize a branch dev
git checkout dev
git pull origin dev

# Faça merge da feature
git merge feature/nome-da-feature

# Faça push da dev
git push origin dev
```

### 4️⃣ Apagar a Branch da Feature

```bash
# Apague localmente
git branch -d feature/nome-da-feature

# Apague no remoto
git push origin --delete feature/nome-da-feature
```

## 📝 Convenção de Nomes de Branches

| Tipo | Padrão | Exemplo |
|------|--------|---------|
| Nova Feature | `feature/` | `feature/user-authentication` |
| Bug Fix | `fix/` | `fix/login-error` |
| Documentação | `docs/` | `docs/api-endpoints` |
| Refatoração | `refactor/` | `refactor/database-connection` |
| Testes | `test/` | `test/auth-endpoints` |

## ✍️ Padrão de Commits (Conventional Commits)

### Formato
```
<tipo>(<escopo>): <descrição breve>

<descrição detalhada (opcional)>

<footer (opcional)>
```

### Tipos Disponíveis

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Nova feature | `feat: add JWT token refresh` |
| `fix` | Correção de bug | `fix: handle null pointer exception` |
| `docs` | Documentação | `docs: update API endpoints` |
| `style` | Formatação/Estilo | `style: remove console logs` |
| `refactor` | Refatoração | `refactor: simplify auth logic` |
| `test` | Testes | `test: add unit tests for auth` |
| `chore` | Tarefas administrativas | `chore: update dependencies` |
| `perf` | Performance | `perf: optimize database queries` |

### Exemplos de Commits Bons

```bash
feat: add task completion endpoint
feat(auth): implement password reset functionality
fix: prevent duplicate user registration
fix(tasks): correct task filter logic
docs: add setup instructions for PostgreSQL
refactor: extract authentication logic to utils
test: add integration tests for task CRUD
chore: update FastAPI to 0.140.0
```

## 🔄 Fluxo Completo de Uma Feature

```bash
# 1. Criar feature branch
git checkout dev
git pull origin dev
git checkout -b feature/user-profile

# 2. Fazer alterações e commits
# ... editar arquivos ...
git add .
git commit -m "feat: add user profile endpoint"
git push origin feature/user-profile

# 3. Fazer mais commits conforme necessário
# ... mais edições ...
git add .
git commit -m "feat: add profile validation"
git push origin feature/user-profile

# 4. Fazer merge com dev
git checkout dev
git pull origin dev
git merge feature/user-profile
git push origin dev

# 5. Apagar branch
git branch -d feature/user-profile
git push origin --delete feature/user-profile
```

## 🎯 Fluxo ao Final do Dia

1. **Features prontas** → Merge para `dev`
2. **Branch dev** → Pull Request para `main`
3. **PR aprovado** → Merge para `main`

```bash
# Exemplo: fazer PR de dev para main
git checkout dev
git pull origin dev
# Abra PR via GitHub ou CLI
# gh pr create --base main --head dev --title "Release v1.0.1"
```

## ⚠️ Regras Importantes

- ✅ **SEMPRE** criar uma branch para cada feature
- ✅ **NUNCA** commitar diretamente em `dev` ou `main`
- ✅ **SEMPRE** sincronizar com `dev` antes de criar nova feature branch
- ✅ **SEMPRE** deletar branch de feature após merge
- ✅ **SEMPRE** fazer push regularmente
- ✅ **SEMPRE** escrever mensagens de commit claras
- ❌ **NUNCA** fazer rebase em branches públicas
- ❌ **NUNCA** force push

## 🆘 Situações Comuns

### Sincronizar feature branch com dev mais recente

```bash
git checkout dev
git pull origin dev
git checkout feature/nome
git merge dev
git push origin feature/nome
```

### Desfazer último commit

```bash
git reset --soft HEAD~1  # Manter mudanças
git reset --hard HEAD~1  # Descartar mudanças
```

### Renomear branch local

```bash
git branch -m feature/nome-antigo feature/nome-novo
git push origin --delete feature/nome-antigo
git push origin feature/nome-novo
```

### Ver status

```bash
# Branch atual
git branch

# Branches remotas
git branch -r

# Log de commits
git log --oneline -10
```

---

**Última atualização:** 2026-07-13  
**Mantido por:** DBCBR
