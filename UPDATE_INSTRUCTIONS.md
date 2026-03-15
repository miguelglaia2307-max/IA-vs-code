# 📋 Instruções para Atualizações do Projeto

## ✅ Status Atual

O repositório **IA-vs-code** foi configurado e está pronto para receber atualizações documentadas.

- **Repositório**: https://github.com/miguelglaia2307-max/IA-vs-code
- **Branch**: main
- **Commits**: 2 (inicial + workflow)
- **Status**: ✅ Sincronizado com GitHub

## 🚀 Como Proceder com Atualizações

### Passo 1: Fazer Alterações no Código
```powershell
cd c:\Users\User1\.vscode\my-web-app

# Editar arquivos conforme necessário
# Exemplo: adicionar nova feature, corrigir bug, etc
```

### Passo 2: Atualizar Documentação
Dependendo do tipo de mudança, atualize:

1. **Para novas features**: Atualize [README.md](./README.md)
2. **Para mudanças na API**: Atualize [API_REFERENCE.md](./API_REFERENCE.md)
3. **Para mudanças na arquitetura**: Atualize [FULL_ARCHITECTURE.md](./FULL_ARCHITECTURE.md)
4. **Sempre**: Atualize [CHANGELOG.md](./CHANGELOG.md)

### Passo 3: Fazer Commit
```powershell
# Ver o que mudou
git status

# Adicionar as mudanças
git add .

# Fazer commit com mensagem clara (veja WORKFLOW.md para convenções)
git commit -m "feat(componente): descrição da mudança"

# Exemplo:
git commit -m "feat(frontend): adicionar novo componente de dashboard"
git commit -m "fix(backend): corrigir erro na otimização"
git commit -m "docs: atualizar documentação de API"
```

### Passo 4: Fazer Push
```powershell
# Enviar para o GitHub
git push origin main
```

## 📁 Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| **WORKFLOW.md** | Guia completo de workflow de desenvolvimento |
| **CHANGELOG.md** | Histórico de todas as mudanças |
| **README.md** | Visão geral do projeto |
| **.github/PULL_REQUEST_TEMPLATE.md** | Template para pull requests |

## 🔑 Convenções de Commit

Use um destes prefixos:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação/Estilo
- `refactor:` - Refatoração de código
- `perf:` - Melhorias de performance
- `test:` - Testes
- `chore:` - Atualizações de build/dependências

**Exemplo de bom commit:**
```
feat(backend): adicionar validação de entrada em otimizações

- Implementar schema Pydantic para validação
- Adicionar testes automatizados
- Atualizar documentação da API

Closes #5
```

## 💡 Dicas

1. **Commits pequenos e focados** são melhores que commits grandes
2. **Sempre atualize a documentação** junto com o código
3. **Use CHANGELOG.md** para rastrear mudanças
4. **Verifique git status** antes de fazer push
5. **Se errar um commit**, use `git revert` (não `git reset` em main)

## 🔗 Links Úteis

- Ver histórico: `git log --oneline -10`
- Ver mudanças: `git diff`
- Ver remote: `git remote -v`
- Ver status: `git status`

## 🆘 Precisa de Ajuda?

Se precisar desfazer um push para main:
```powershell
# NÃO USE RESET! Use revert:
git revert HEAD
git push origin main
```

---

**Próxima etapa**: Comece a fazer atualizações seguindo este processo! 🎉
