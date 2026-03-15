# Contributing to Prompt Optimization Platform

Obrigado por se interessar em contribuir para o Prompt Optimization Platform! Aqui estão algumas diretrizes para facilitar o processo.

## Como Contribuir

### Reportando Bugs
- Use a aba de Issues do GitHub
- Descreva o problema claramente com:
  - Passos para reproduzir
  - Comportamento esperado vs. observado
  - Ambiente (OS, versão do Node/Python)
  - Screenshots se aplicável

### Sugerindo Melhorias
- Abra uma issue com o label `enhancement`
- Descreva o benefício e caso de uso
- Discuta a implementação esperada

### Enviando Pull Requests
1. **Fork o repositório**
2. **Crie uma branch** para sua feature: `git checkout -b feature/minha-feature`
3. **Commit suas mudanças**: `git commit -am 'Add minha feature'`
4. **Push para a branch**: `git push origin feature/minha-feature`
5. **Abra um Pull Request** com descrição clara

## Guidelines de Desenvolvimento

### Frontend (Next.js/TypeScript)
- Use TypeScript para type safety
- Siga o padrão de componentes funcional
- Mantenha os componentes focados e reutilizáveis
- Execute `npm run build` antes de fazer PR

### Backend (FastAPI/Python)
- Mantenha code style com PEP 8
- Adicione type hints nas funções
- Escreva testes para novas funcionalidades
- Execute testes com `pytest` antes de fazer PR

## Setup Local

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
pip install -r requirements.txt
python run.py
```

## Código de Conduta

- Seja respeitoso com outros contribuidores
- Forneça feedback construtivo
- Reporte problemas responsavelmente

Obrigado por contribuir! 🚀
