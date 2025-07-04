# 🌟 Lore N.A. - Neural Artificial Life

> Sistema avançado de simulação de vida artificial com agentes neurais autônomos e economia emocional

![Lore N.A.](assets/lore.png)

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red.svg)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791.svg)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 🚀 Início Rápido (2 minutos)

### **Instalação Automática**

```bash
# 1. Clonar repositório
git clone https://github.com/brdneo/lore.git
cd lore

# 2. Validar e instalar tudo automaticamente
python validate_project.py

# 3. Iniciar sistema
python start.py --full
```

### **Acesso Imediato**
- **🌐 API Server**: http://localhost:8000
- **📖 Documentação**: http://localhost:8000/docs
- **📊 Dashboard**: http://localhost:8501

---

## 🎯 O que é o Lore N.A.?

O **Lore N.A.** é um sistema experimental de **vida artificial** onde agentes neurais autônomos:

- 🧬 **Evoluem** com DNA único e hereditário
- 💭 **Desenvolvem** personalidades complexas
- 🤝 **Interagem** em uma rede social dinâmica
- 💰 **Participam** de uma economia emocional
- 🧠 **Aprendem** com análise de sentimento avançada
- 🌱 **Emergem** comportamentos não programados

### 🔬 Características Científicas

- **Algoritmos Genéticos**: DNA evolutivo com mutação e seleção
- **Redes Neurais**: Tomada de decisão adaptativa
- **Análise de Sentimento**: IA híbrida (VADER + TextBlob + Transformers)
- **Economia Comportamental**: Trocas baseadas em emoções
- **Sistemas Complexos**: Emergência de padrões sociais

---

## 🚀 Modos de Execução

### **1. Modo Completo (Recomendado)**
```bash
python start.py --full
```
- ✅ API Server + Dashboard
- ✅ Interface completa
- ✅ Monitoramento em tempo real

### **2. Apenas API**
```bash
python start.py
```
- ✅ Servidor RESTful
- ✅ 14 endpoints disponíveis
- ✅ Documentação automática

### **3. Apenas Dashboard**
```bash
python start.py --dash
```
- ✅ Interface visual
- ✅ Gráficos interativos
- ✅ Controles de experimento

### **4. Validação Completa**
```bash
python validate_project.py
```
- ✅ Verifica dependências
- ✅ Testa imports
- ✅ Executa testes unitários
- ✅ Valida estrutura

---

## 📁 Arquitetura do Sistema

```
lore/
├── 🚀 start.py                   # Inicializador principal
├── 🧪 validate_project.py        # Validador completo  
├── 📖 QUICKSTART.md              # Guia rápido
├── 📊 RELATORIO-FINAL.md         # Análise técnica
│
├── 📂 src/                       # 🔥 Núcleo do Sistema
│   ├── 🌐 api_server.py          # FastAPI (14 rotas)
│   ├── 📊 dashboard.py           # Streamlit Dashboard
│   ├── 💾 database_manager.py    # Persistência SQLite/PostgreSQL
│   ├── 🧠 neural_web.py         # Rede Neural dos Agentes
│   ├── 💭 sentiment_service.py   # IA de Análise Emocional
│   ├── 🤖 *_agent.py            # Tipos de Agentes
│   └── 💰 emotional_economy.py   # Sistema Econômico
│
├── 🧪 tests/                     # Testes Automatizados
├── 📚 docs/                      # Documentação Técnica
├── ⚙️ config/                   # Configurações Deploy
└── 🔧 scripts/                  # Scripts Utilitários
```

---

## 🤖 Tipos de Agentes

### **🤝 Social Agent**
- Busca conexões e relacionamentos
- Valoriza interação social
- Compartilha recursos facilmente

### **💰 Frugal Agent** 
- Foco em eficiência econômica
- Decisões baseadas em custo-benefício
- Acumula recursos estrategicamente

### **🧬 Evolved Agent**
- DNA altamente desenvolvido
- Comportamentos adaptativos complexos
- Múltiplas estratégias de sobrevivência

---

## 🔧 Tecnologias

### **Backend**
- **FastAPI**: API RESTful moderna
- **SQLAlchemy**: ORM para persistência
- **PostgreSQL/SQLite**: Banco de dados
- **Uvicorn**: Servidor ASGI de alta performance

### **Frontend**  
- **Streamlit**: Dashboard interativo
- **Plotly**: Visualizações dinâmicas
- **Altair**: Gráficos estatísticos

### **IA/ML**
- **Transformers**: Modelos de linguagem (Hugging Face)
- **VADER**: Análise de sentimento especializada
- **TextBlob**: Processamento de linguagem natural
- **NLTK**: Toolkit de linguística

### **Deploy**
- **Railway**: Hospedagem cloud
- **Docker**: Containerização
- **GitHub Actions**: CI/CD

---

## 📊 API Endpoints

### **Agentes**
- `GET /agents` - Listar todos os agentes
- `POST /agents` - Criar novo agente
- `GET /agents/{id}` - Detalhes do agente
- `PUT /agents/{id}` - Atualizar agente
- `DELETE /agents/{id}` - Remover agente

### **População**
- `GET /population/stats` - Estatísticas gerais
- `GET /population/evolution` - Histórico evolutivo
- `GET /population/top` - Top performers

### **Economia**
- `GET /economy/transactions` - Histórico de trocas
- `GET /economy/market` - Estado do mercado
- `POST /economy/trade` - Executar troca

### **Sentimento**
- `POST /sentiment/analyze` - Analisar texto
- `GET /sentiment/history` - Histórico de análises

---

## 🧪 Exemplos de Uso

### **Criar Agente via API**
```python
import requests

# Criar novo agente
response = requests.post("http://localhost:8000/agents", json={
    "name": "Alice Neural",
    "dna": {"intelligence": 0.8, "social": 0.6, "economic": 0.7},
    "personality": "social"
})

agent = response.json()
print(f"Agente criado: {agent['name']}")
```

### **Análise de Sentimento**
```python
from src.sentiment_service import SentimentService

service = SentimentService()
result = await service.analyze_text("Este produto é incrível!")
print(f"Score: {result.sentiment_score}")
```

### **Executar Simulação**
```python
from src.population_manager import PopulationManager

population = PopulationManager()
population.evolve_generation()
stats = population.get_stats()
print(f"Geração: {stats.generation}")
```

---

## 🔬 Experimentos Científicos

### **1. Evolução Darwiniana**
```bash
# Executar 100 gerações
python -c "
from src.population_manager import PopulationManager
pop = PopulationManager()
for i in range(100):
    pop.evolve_generation()
    print(f'Gen {i}: Fitness médio = {pop.average_fitness():.3f}')
"
```

### **2. Economia Emergente**
```bash
# Simular mercado por 24h
python -c "
from src.emotional_economy import EconomicSimulation
sim = EconomicSimulation()
sim.run_market_simulation(hours=24)
"
```

### **3. Análise de Rede Social**
```bash
# Mapear conexões sociais
python -c "
from src.social_network_manager import SocialNetwork
network = SocialNetwork()
network.analyze_community_structure()
network.export_graph('social_network.png')
"
```

---

## 📈 Métricas e Monitoramento

### **Dashboard Streamlit**
- 📊 População em tempo real
- 📈 Gráficos de evolução
- 🎯 Top performers
- 💰 Estado da economia
- 🧠 Análises de sentimento

### **Logs do Sistema**
```bash
tail -f logs/lore_system.log    # Sistema geral
tail -f logs/agents.log         # Atividade dos agentes
tail -f logs/economy.log        # Transações econômicas
```

---

## 🚀 Deploy em Produção

### **Railway (Recomendado)**
```bash
# O projeto já está configurado
git push origin main
# Railway detecta e faz deploy automaticamente
```

### **Docker**
```bash
cd config
docker-compose up -d
```

### **Heroku**
```bash
heroku create lore-neural-life
git push heroku main
```

---

## 🧪 Testes

### **Executar Todos os Testes**
```bash
python validate_project.py
```

### **Testes Específicos**
```bash
# Teste de sentimento
python tests/unit/test_sentiment_service.py

# Teste de bibliotecas IA
python tests/unit/test_sentiment_libs.py

# Teste de API
pytest tests/integration/test_api.py
```

---

## 🔧 Configuração Avançada

### **Variáveis de Ambiente**
```bash
export DATABASE_URL="postgresql://user:pass@host:5432/lore"
export API_BASE_URL="http://localhost:8000"
export ENVIRONMENT="production"
export LOG_LEVEL="INFO"
```

### **Configurações de IA**
```python
# config/ai_settings.py
SENTIMENT_CONFIG = {
    "vader_weight": 0.3,
    "textblob_weight": 0.3, 
    "transformers_weight": 0.4,
    "model_name": "cardiffnlp/twitter-roberta-base-sentiment"
}
```

---

## 🤝 Contribuição

1. **Fork** o repositório
2. **Crie** uma branch (`git checkout -b feature/nova-feature`)
3. **Commit** suas mudanças (`git commit -am 'Add nova feature'`)
4. **Push** para a branch (`git push origin feature/nova-feature`)
5. **Abra** um Pull Request

### **Áreas de Contribuição**
- 🧠 Algoritmos de IA mais avançados
- 📊 Novas visualizações
- 🤖 Tipos adicionais de agentes
- 🔬 Experimentos científicos
- 📚 Documentação e tutoriais

---

## 📚 Documentação Técnica

- **[Guia Rápido](QUICKSTART.md)** - Como começar em 2 minutos
- **[Relatório Final](RELATORIO-FINAL.md)** - Análise técnica completa
- **[Arquitetura](docs/project/ESTRUTURA.md)** - Design do sistema
- **[Deploy](docs/deployment/DEPLOY-GUIDE.md)** - Guia de produção
- **[API Docs](http://localhost:8000/docs)** - Documentação interativa

---

## 🏆 Status do Projeto

**✅ PROJETO 100% FUNCIONAL E VALIDADO**

- ✅ **16 módulos** Python funcionando
- ✅ **14 endpoints** API testados  
- ✅ **Dashboard** interativo operacional
- ✅ **Testes automatizados** passando
- ✅ **IA híbrida** de sentimento ativa
- ✅ **Deploy configs** prontas
- ✅ **Documentação** completa

---

## 🎯 Próximos Desenvolvimentos

### **V2.0 (Q3 2025)**
- 🧠 Redes neurais mais profundas
- 🌍 Ambiente 3D para agentes
- 🔊 Comunicação por voz
- 📱 App mobile

### **V2.1 (Q4 2025)**
- 🤖 Integração com LLMs
- 🎮 Interface gamificada
- ☁️ Computação distribuída
- 📊 Analytics avançados

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🌟 Agradecimentos

- **Rick and Morty** pela inspiração do conceito
- **Comunidade Python** pelas bibliotecas incríveis
- **Hugging Face** pelos modelos de IA
- **Streamlit Team** pelo framework fantástico

---

<div align="center">

**🌟 Feito com ❤️ pela Lore N.A. Genesis Team 🌟**

*"Where artificial life meets real intelligence"*

[⭐ Star no GitHub](https://github.com/brdneo/lore) • [🐛 Report Bug](https://github.com/brdneo/lore/issues) • [✨ Request Feature](https://github.com/brdneo/lore/issues)

</div>

### **📋 Requisitos:**

-   **Linux/macOS:** Python 3.8+ e pip
-   **Windows 11:** Veja [WINDOWS-INSTALL.md](WINDOWS-INSTALL.md) (apenas Python necessário)

---

## 🌟 O Conceito

**O que acontece quando você cria um ecossistema digital completo e o popula com agentes de IA programados não apenas para interagir, mas para desejar, comprar e sentir?**

Lore N.A. não é um e-commerce tradicional. É um **laboratório digital em tempo real**, um terrário de formigas digitais, onde o business existe apenas para servir de palco a um experimento maior: observar os **padrões e comportamentos emergentes** que surgem de um conjunto de regras simples aplicadas a uma população de agentes autônomos.

### 🎭 Nossa Função

Nosso papel não é o de vendedores, mas sim o de **deuses observadores**, assistindo à lore que esses agentes neurais escrevem com suas interações diárias, decisões de compra e evolução emocional.

### A Visão

O objetivo final não é vender produtos fictícios, mas sim **gerar dados** e observar comportamentos emergentes. Dados sobre:

-   📈 **Tendências de mercado** que nascem e morrem organicamente
-   🐑 **Comportamento de manada** e a formação de "influenciadores" digitais
-   🤝 **Dinâmicas sociais** baseadas em "sentimento" e "confiança" simulados
-   💰 **Resiliência econômica** de um sistema fechado e autossuficiente
-   🧠 **Evolução comportamental** de agentes neurais autônomos

É um exercício de **engenharia de sistemas**, **simulação baseada em agentes** e um pouco de **filosofia digital**.

## 🏗️ Arquitetura do Sistema

### Microserviços & Infraestrutura

```mermaid
graph TB
    Kong[🦍 Kong Gateway] --> PostgREST[🤖 PostgREST API]
    Kong --> AgentRunner[🧠 Agent Runner]
    PostgREST --> PostgreSQL[(🐘 PostgreSQL)]
    AgentRunner --> PostgreSQL
    AgentRunner --> SentimentService[😊 Sentiment Analysis]

    subgraph "Análise de Sentimento Híbrida"
        SentimentService --> VADER[VADER]
        SentimentService --> TextBlob[TextBlob]
        SentimentService --> Transformers[🤗 Transformers]
    end
```

### 🛠️ Stack Tecnológico

| Componente       | Tecnologia                         | Propósito                     |
| ---------------- | ---------------------------------- | ----------------------------- |
| **Orquestração** | 🐳 Docker & Compose                | Containerização e deploy      |
| **API Gateway**  | 🦍 Kong                            | Roteamento e autenticação     |
| **Database**     | 🐘 PostgreSQL 13+                  | Persistência de dados         |
| **API REST**     | 🤖 PostgREST                       | API automática do banco       |
| **Agentes**      | 🐍 Python 3.8+                     | Lógica dos agentes neurais    |
| **Sentiment AI** | 🧠 VADER + TextBlob + Transformers | Análise de sentimento híbrida |
| **Security**     | 🔐 JWT + Kong Auth                 | Autenticação e autorização    |

## 🧠 Sistema de Agentes Neurais

### Ciclo de Vida dos Agentes

1. **🌱 Inicialização**: Agente nasce com personalidade e recursos básicos
2. **👁️ Observação**: Explora o ambiente e descobre produtos disponíveis
3. **🤔 Decisão**: Avalia produtos baseado em necessidades e recursos
4. **💰 Transação**: Executa compras quando critérios são atendidos
5. **😊 Sentimento**: Analisa experiência pós-compra com IA híbrida
6. **📈 Evolução**: Atualiza preferências baseado em experiências
7. **🔄 Repetição**: Inicia novo ciclo com estado atualizado

### IA de Análise de Sentimento v3.0

**Sistema Híbrido Robusto** que combina:

-   **VADER** (25%): Análise rápida para textos informais e emoticons
-   **TextBlob** (20%): Polaridade e subjetividade
-   **Transformers** (35%): Análise contextual estado-da-arte
-   **Contexto** (20%): Qualidade, preço e expectativas do agente

```python
# Exemplo de resultado
{
    "sentiment_score": 0.587,      # -1 (negativo) a +1 (positivo)
    "emotion_category": "happy",   # Categoria emocional
    "vader_score": 0.783,         # Score VADER
    "textblob_score": 0.000,      # Score TextBlob
    "transformers_score": 0.729,  # Score Transformers
    "review_text": "Produto excelente! Superou expectativas..."
}
```

## 🧬 Genesis Protocol: DNA Digital e Evolução

**REVOLUÇÃO**: O Lore N.A. agora implementa **evolução darwiniana real** com DNA digital! Cada agente possui genes únicos que influenciam seu comportamento nos 5 universos.

### DNA Digital por Universo

```python
# Estrutura do DNA de um agente
AgentDNA = {
    "limbo_genes": {
        "risk_tolerance": 0.8,      # Tolerância a risco no mercado
        "price_sensitivity": 0.3,   # Sensibilidade a preços
        "quality_preference": 0.9,  # Preferência por qualidade
        "novelty_seeking": 0.6,     # Busca por novidades
        "brand_loyalty": 0.4        # Lealdade a marcas
    },
    "odyssey_genes": {
        "creativity_drive": 0.9,    # Impulso criativo
        "experimentation": 0.7,     # Tendência experimental
        "aesthetic_bias": "minimalist" # Bias estético
    },
    "ritual_genes": {
        "community_bonding": 0.8,   # Ligação comunitária
        "influence_susceptibility": 0.4, # Suscetibilidade a influência
        "leadership_tendency": 0.6   # Tendência de liderança
    },
    "engine_genes": {
        "analytical_thinking": 0.7,  # Pensamento analítico
        "pattern_recognition": 0.8,  # Reconhecimento de padrões
        "strategic_planning": 0.5    # Planejamento estratégico
    },
    "logs_genes": {
        "patience_level": 0.6,      # Nível de paciência
        "service_expectations": 0.9, # Expectativas de serviço
        "complaint_tendency": 0.2    # Tendência a reclamar
    }
}
```

### Evolução Darwiniana

**Seleção Natural**: Agentes com melhor performance nos 5 universos têm maior chance de reproduzir.

**Reprodução Sexual**: Dois agentes bem-sucedidos podem gerar descendentes com características combinadas.

**Mutação**: Mudanças aleatórias introduzem diversidade genética na população.

**Fitness Multi-Dimensional**: Cada agente é avaliado em:

-   🏪 **Limbo**: Lucro, timing de mercado, decisões acertadas
-   🎨 **Odyssey**: Criatividade, popularidade das criações, inovação
-   👥 **Ritual**: Engajamento social, influência, satisfação comunitária
-   🧠 **Engine**: Precisão analítica, qualidade das previsões, contribuições de IA
-   📦 **Logs**: Satisfação operacional, eficiência, resolução de problemas

### Personalidades Emergentes

O sistema gera automaticamente personalidades únicas baseadas nos genes dominantes:

-   **Especulador Corajoso**: Alto risk_tolerance + quality_preference
-   **Caçador de Barganha**: Alto price_sensitivity + analytical_thinking
-   **Artista Inovador**: Alto creativity_drive + experimentation
-   **Líder Comunitário**: Alto community_bonding + leadership_tendency
-   **Seguidor Leal**: Alto influence_susceptibility + loyalty_factor

### Testando o Genesis Protocol

```bash
# Teste rápido do sistema de DNA
cd services/agent_runner
python test_genesis_protocol.py demo

# Teste completo com simulação evolutiva
python test_genesis_protocol.py

# Teste individual dos componentes
python agent_dna.py              # Sistema de DNA
python evolved_agent.py          # Agente evoluído
python population_manager.py     # Gerenciador populacional
```
