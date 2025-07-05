# Estrutura Final da Raiz do Projeto Lore N.A.

## Arquivos que DEVEM ficar na raiz

### Documentação Principal

-   `README.md` - Documentação principal do projeto (único arquivo .md permitido na raiz)

### Configuração do Projeto

-   `LICENSE` - Licença do projeto
-   `Makefile` - Comandos de build e automação
-   `Dockerfile` - Configuração do container Docker
-   `Cargo.toml` - Configuração do workspace Rust
-   `Cargo.lock` - Lock file do Cargo (gerado automaticamente)

### Configuração de Ambiente

-   `.gitignore` - Arquivos ignorados pelo Git
-   `.env.example` - Exemplo de variáveis de ambiente
-   `.github/` - Configurações do GitHub Actions

### Scripts Principais

-   `start.py` - Script principal de inicialização
-   `validate_project.py` - Script de validação do projeto

## Estrutura de Diretórios na Raiz

```
/home/brendo/lore/
├── README.md              # Documentação principal
├── LICENSE                # Licença
├── Makefile              # Comandos de build
├── Dockerfile            # Container Docker
├── Cargo.toml            # Workspace Rust
├── .gitignore            # Arquivos ignorados
├── .env.example          # Exemplo de variáveis
├── start.py              # Script principal
├── validate_project.py   # Validação
├── .github/              # GitHub Actions
├── assets/               # Recursos estáticos
├── backup/               # Backups e arquivos antigos
├── config/               # Configurações (Procfile, runtime.txt, etc.)
├── crates/               # Código Rust
├── data/                 # Dados e bases de dados
├── docs/                 # TODA A DOCUMENTAÇÃO
├── examples/             # Exemplos de uso
├── python/               # Código Python
├── scripts/              # Scripts de automação
├── tests/                # Testes
└── tools/                # Ferramentas auxiliares
```

## Arquivos REMOVIDOS da raiz

Todos os seguintes arquivos foram movidos para `docs/`:

### Movidos para `docs/guides/`

-   `COMANDOS.md` → `docs/guides/COMANDOS.md`

### Movidos para `docs/getting-started/`

-   `QUICKSTART.md` → `docs/getting-started/QUICKSTART.md`

### Movidos para `docs/reports/`

-   `HYBRID_IMPLEMENTATION_REPORT.md`
-   `RELATORIO-FINAL.md` → `RELATORIO-FINAL-ROOT.md`
-   `RUST-IMPLEMENTATION-FINAL-REPORT.md`
-   `RUST-IMPLEMENTATION-SUCCESS.md`
-   `SISTEMA-HIBRIDO-SUCESSO-FINAL.md`

### Movidos para `docs/internal/`

-   `REORGANIZACAO-ESTRUTURA.md`
-   `REORGANIZACAO-CONCLUIDA.md`
-   `REORGANIZACAO-FINAL-CONCLUIDA.md`
-   `MISSAO-CUMPRIDA-REORGANIZACAO-FINAL.md`

### Movidos para outras pastas

-   `reactivate_railway.sh` → `scripts/deployment/`
-   `requirements-dev.txt` → `python/`
-   `runtime.txt` → `config/`
-   `Procfile` → `config/`
-   `Cargo.toml.old` → `backup/`

## Regras do .gitignore

O `.gitignore` foi atualizado para:

1. **Permitir apenas README.md na raiz**: `/*.md` + `!README.md`
2. **Ignorar arquivos temporários na raiz**: `*.tmp`, `*.bak`, etc.
3. **Manter organização**: Scripts, dados, logs em suas pastas específicas

## Princípios da Organização

1. **Clareza**: A raiz contém apenas arquivos essenciais
2. **Modularidade**: Cada tipo de arquivo tem sua pasta específica
3. **Manutenibilidade**: Estrutura previsível e bem documentada
4. **Padrões**: Segue best practices de projetos open source

## Validação

Para validar a estrutura:

```bash
make validate
# ou
python validate_project.py
```

Isso verificará se:

-   Apenas arquivos permitidos estão na raiz
-   Todas as dependências estão corretas
-   A estrutura está seguindo os padrões definidos
