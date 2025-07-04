# 🌟 Lore N.A. - Neural Artificial Life

> Sistema de simulação de vida artificial com agentes neurais autônomos

![Lore N.A.](assets/lore.png)

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
# Usando pip
pip install -r requirements.txt

# OU usando o script de validação
python validate_project.py
```

### 2. Executar o Sistema

```bash
# 🎯 API Server apenas (recomendado para início)
python start.py

# 📊 Dashboard apenas
python start.py --dash

# 🔥 Sistema completo (API + Dashboard)
python start.py --full
```

### 3. Acessar

-   **API Server**: http://localhost:8000
-   **Documentação**: http://localhost:8000/docs
-   **Dashboard**: http://localhost:8501

## 📁 Estrutura do Projeto

```
lore/
├── 🚀 start.py              # Script de inicialização simples
├── 🧪 validate_project.py   # Validador completo
├── 📜 main.py               # Entry point principal
├── 📋 requirements.txt      # Dependências
│
├── 📂 src/                  # Código fonte principal
│   ├── 🌐 api_server.py     # Servidor FastAPI
│   ├── 📊 dashboard.py      # Dashboard Streamlit
│   ├── 💾 database_manager.py # Persistência
│   ├── 🧠 neural_web.py     # Rede neural
│   ├── 🤖 *_agent.py        # Tipos de agentes
│   └── 💭 sentiment_service.py # Análise de sentimento
│
├── 🧪 tests/               # Testes automatizados
├── 📚 docs/                # Documentação
├── ⚙️ config/             # Configurações
└── 📊 data/               # Dados persistentes
```

## 🛠️ Funcionalidades

### 🤖 Agentes Neurais

-   **DNA Evolutivo**: Cada agente possui DNA único que evolui
-   **Personalidades**: Diferentes tipos (Social, Frugal, Evolved)
-   **Economia Emocional**: Sistema de trocas baseado em sentimentos
-   **Rede Social**: Agentes interagem entre si

### 📊 Dashboard Interativo

-   Visualização em tempo real da população
-   Gráficos de evolução e fitness
-   Análise de comportamentos emergentes
-   Controles para experimentos

### 🌐 API RESTful

-   Endpoints para CRUD de agentes
-   Estatísticas da população
-   Histórico de evolução
-   Documentação automática (Swagger)

### 💾 Persistência

-   SQLite (desenvolvimento)
-   PostgreSQL (produção)
-   Backup automático
-   Migração de dados

## 🧪 Testes

```bash
# Executar validação completa
python validate_project.py

# Testes específicos
python tests/unit/test_sentiment_service.py
python tests/unit/test_sentiment_libs.py
```

## 🚀 Deploy

### Local

```bash
python start.py --full
```

### Railway (Produção)

```bash
# O projeto está configurado para Railway
# Procfile e configurações já incluídas
```

### Docker

```bash
# Usando docker-compose
cd config
docker-compose up
```

## 📖 Comandos Úteis

```bash
# 🧹 Limpar projeto
./cleanup-project.sh

# ✅ Validar tudo
python validate_project.py

# 🚀 Iniciar modo desenvolvimento
python start.py --full

# 📊 Apenas dashboard
python start.py --dash

# 🌐 Apenas API
python start.py
```

## 🎯 Exemplo de Uso

```python
# Importar agente
from src.social_agent import SocialAgent

# Criar agente
agent = SocialAgent("Alice")

# Executar ciclo de vida
agent.live_cycle()

# Ver estatísticas
print(agent.get_stats())
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
export DATABASE_URL="postgresql://..."  # PostgreSQL (produção)
export API_BASE_URL="http://localhost:8000"
export ENVIRONMENT="development"
```

### Arquivos de Config

-   `config/app.json` - Configurações da aplicação
-   `config/railway.json` - Deploy Railway
-   `config/docker-compose.yml` - Containerização

## 🎨 Características Técnicas

-   **Framework**: FastAPI + Streamlit
-   **Database**: SQLAlchemy (SQLite/PostgreSQL)
-   **AI/ML**: Transformers, NLTK, TextBlob
-   **Visualization**: Plotly, Altair
-   **Deploy**: Railway, Docker
-   **Tests**: Pytest, unittest

## 📚 Documentação

-   **API**: `/docs` (Swagger UI automático)
-   **Arquitetura**: `docs/project/ESTRUTURA.md`
-   **Deploy**: `docs/deployment/DEPLOY-GUIDE.md`
-   **Como Usar**: `docs/project/COMO-USAR.md`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Add nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🌟 Status do Projeto

✅ **Projeto Validado e Funcionando**

-   ✅ Estrutura organizada
-   ✅ Dependências instaladas
-   ✅ Testes passando
-   ✅ API funcionando
-   ✅ Dashboard operacional
-   ✅ Database configurado
-   ✅ Deploy pronto

---

**Feito com ❤️ pela Lore N.A. Genesis Team**
