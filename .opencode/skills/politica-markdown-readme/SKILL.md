---
name: Política de Markdown do Projeto
description: "Regra exclusiva deste projeto: apenas o README.md da raiz pode ser commitado como .md. Todos os demais .md ficam no .gitignore e só saem com solicitação explícita do usuário."
---

# Política de Markdown do Projeto

## Escopo
Esta regra vale **somente** para este repositório. Ela tem **precedência** sobre qualquer instrução global que peça para versionar arquivos `.md` (PRD, ADRs, relatórios, CHANGELOG, AGENTS.md, READMEs internos etc.).

## Regra inviolável
1. O **único** arquivo com extensão `.md` que pode ser rastreado/commitado é o **`README.md` da raiz**.
2. Todos os outros `.md` — em qualquer pasta, incluindo `docs/`, `.opencode/`, `notebooks/`, subpastas e arquivos como `AGENTS.md` e `CHANGELOG.md` — são **ignorados pelo Git**.
3. Um `.md` só sai da lista de ignorados se o **usuário solicitar explicitamente**, informando o caminho exato. A exceção deve ser registrada no `.gitignore` com `!<caminho>` e comentário com data e autorização.
4. É proibido usar `git add -f` (ou `--force`) para incluir `.md` ignorado sem a autorização explícita acima.
5. Sem autorização, não criar arquivos `.md` novos esperando que sejam versionados. Se forem necessários como artefato local, mantenha-os ignorados.

## Regra no `.gitignore`
```gitignore
# Política do projeto: apenas o README.md da raiz é versionado como Markdown.
*.md
!/README.md
```
- `*.md` ignora Markdown em qualquer nível.
- `!/README.md` reabilita **somente** o README da raiz; READMEs internos continuam ignorados.

## Onde registrar artefatos
Como PRD, ADRs, relatórios e reviews não são versionados:
- O conteúdo obrigatório vai para a **issue** ou o **PR** no GitHub (descrição/comentário).
- Se precisar de arquivo local, ele fica no disco **ignorado**, sem `git add`.
- `CHANGELOG.md` não é versionado neste projeto: notas de release vão na **GitHub Release**.
- `AGENTS.md` não é versionado: regras do projeto ficam nesta skill e nas issues.

## Verificação antes de todo commit
```bash
# 1. Nenhum .md além do README.md pode aparecer
git ls-files '*.md'
# esperado: README.md

# 2. Nada .md fora do README debe entrar no staging
git diff --cached --name-only | grep -E '\.md$' | grep -v '^README\.md$' && echo "BLOQUEADO: .md indevido no staging"

# 3. Arquivos .md devem estar ignorados
git status --porcelain | grep -E '^\?\? .*\.md$' && echo "BLOQUEADO: .md não ignorado"
```

Se qualquer verificação acusar um `.md` indevido:
1. `git restore --staged <arquivo>` (se estiver no staging).
2. Garantir a regra no `.gitignore`.
3. Não commitar até a verificação passar.

## Checklist
- [ ] `git ls-files '*.md'` retorna apenas `README.md`.
- [ ] Nenhum `.md` no `git diff --cached`.
- [ ] Nenhum `.md` como untracked (todos ignorados).
- [ ] Exceções, se houver, foram autorizadas explicitamente pelo usuário e estão no `.gitignore` com `!caminho`.
- [ ] Artefatos de processo foram registrados em issue/PR, não em arquivos versionados.

## Proibições
- Commitar qualquer `.md` que não seja o `README.md` da raiz.
- Criar exceções por conta própria.
- Usar `git add -f` para burlar a regra.
- Alterar esta política sem pedido explícito do usuário.
