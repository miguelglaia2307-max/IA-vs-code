# Workflow de Desenvolvimento - Atualizações Automáticas

## 📋 Padrão de Commits

Todas as atualizações devem seguir este padrão:

```
<tipo>(<escopo>): <descrição>

<corpo detalhado>

<referências>
```

### Tipos de Commit:
- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Apenas documentação
- **style**: Alterações de formatação/estilo
- **refactor**: Refatoração de código
- **perf**: Melhorias de performance
- **test**: Testes
- **chore**: Atualizações de build, dependências, etc

### Exemplo:
```
feat(backend): adicionar endpoint de otimização de prompts

- Implementar novo endpoint POST /api/optimizations
- Integração com serviço de otimização
- Validação de entrada com Pydantic

Closes #1
```

## 🚀 Processo de Atualização

### 1. **Desenvolvimento Local**
```powershell
# Criar branch para a feature
git checkout -b feature/nova-funcionalidade

# Fazer as alterações no código
# ...
```

### 2. **Documentação**
- Atualizar [README.md](./README.md) se for feature importante
- Atualizar [API_REFERENCE.md](./API_REFERENCE.md) se houver mudanças na API
- Adicionar changelog em [CHANGELOG.md](./CHANGELOG.md)
- Atualizar [FULL_ARCHITECTURE.md](./FULL_ARCHITECTURE.md) se houver mudanças na arquitetura

### 3. **Commit e Push**
```powershell
# Adicionar alterações
git add .

# Fazer commit com mensagem clara
git commit -m "feat(frontend): adicionar componente de visualização"

# Push para o repositório
git push origin feature/nova-funcionalidade
```

### 4. **GitHub**
- Criar Pull Request
- Adicionar descrição da mudança
- Aguardar revisão
- Merge para main

## 📝 Arquivos de Documentação a Manter Atualizados

| Arquivo | Quando Atualizar |
|---------|-----------------|
| [README.md](./README.md) | Features principais, instruções gerais |
| [CHANGELOG.md](./CHANGELOG.md) | **Toda** mudança importante |
| [API_REFERENCE.md](./API_REFERENCE.md) | Novos endpoints ou mudanças na API |
| [FULL_ARCHITECTURE.md](./FULL_ARCHITECTURE.md) | Mudanças na arquitetura do sistema |
| [GETTING_STARTED.md](./GETTING_STARTED.md) | Mudanças nas instruções de início |
| [USER_GUIDE.md](./USER_GUIDE.md) | Novos recursos do usuário |
| [DEVELOPMENT.md](./DEVELOPMENT.md) | Mudanças na configuração de dev |

## 🔄 Checklist para Cada Atualização

- [ ] Código implementado e testado
- [ ] Documentação principal atualizada (README)
- [ ] CHANGELOG atualizado
- [ ] Documentação específica atualizada (API, Arquitetura, etc)
- [ ] Commit com mensagem clara
- [ ] Push para branch
- [ ] Pull Request criado com descrição
- [ ] Revisar e fazer merge

## 📊 Monitoramento

Use este comando para verificar o status:
```powershell
git status
git log --oneline -10
```

## 🔐 Permissões e Segurança

- Nunca commit credenciais ou tokens
- Use `.env.example` para variáveis de ambiente
- Revisar `.gitignore` antes de cada push
