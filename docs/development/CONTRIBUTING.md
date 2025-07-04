# Guia de Contribuição - Lore N.A. 🧠

Obrigado pelo interesse em contribuir com o Lore N.A.! Este projeto é um experimento fascinante sobre vida artificial e comportamentos emergentes.

## 🎯 Como Contribuir

### 🐛 Reportando Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/seu-usuario/lore/issues)
2. Use o template de bug report
3. Inclua logs e informações do sistema
4. Execute `./check-system.sh` e anexe o resultado

### ✨ Sugerindo Features

-   **Novos tipos de agentes**: Diferentes personalidades e comportamentos
-   **Análises de sentimento**: Melhorias na IA emocional
-   **Métricas**: Novas formas de observar o sistema
-   **Visualizações**: Dashboards e gráficos
-   **Performance**: Otimizações de código

### 🔧 Desenvolvendo

#### Setup do Ambiente de Desenvolvimento

```bash
# Clone e configure
git clone https://github.com/seu-usuario/lore.git
cd lore
./install.sh

# Verifique se tudo funciona
./check-system.sh
```

#### Estrutura de Branches

-   `main`: Código estável em produção
-   `develop`: Branch de desenvolvimento
-   `feature/nome-da-feature`: Novas funcionalidades
-   `bugfix/nome-do-bug`: Correções de bugs
-   `hotfix/nome-do-hotfix`: Correções urgentes

#### Workflow de Desenvolvimento

1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie uma branch** para sua feature:
    ```bash
    git checkout -b feature/minha-nova-feature
    ```
4. **Desenvolva** seguindo os padrões do projeto
5. **Teste** suas mudanças:
    ```bash
    ./check-system.sh
    cd services/agent_runner
    python test_sentiment_service.py
    ```
6. **Commit** com mensagens descritivas:
    ```bash
    git commit -m "feat: adiciona novo tipo de agente aventureiro"
    ```
7. **Push** para seu fork:
    ```bash
    git push origin feature/minha-nova-feature
    ```
8. **Abra um Pull Request** com descrição detalhada

## 📝 Padrões de Código

### Python

-   **PEP 8**: Siga as convenções de estilo Python
-   **Type Hints**: Use tipagem quando possível
-   **Docstrings**: Documente funções e classes
-   **Tests**: Inclua testes para novas funcionalidades

```python
from typing import Dict, Optional

class NovoAgente:
    """
    Agente neural com comportamento específico.

    Args:
        agent_id: Identificador único do agente
        personality: Tipo de personalidade ('conservative', 'adventurous', etc.)
    """

    def __init__(self, agent_id: str, personality: str = 'neutral'):
        self.agent_id = agent_id
        self.personality = personality

    async def make_decision(self, products: Dict) -> Optional[str]:
        """
        Toma decisão de compra baseada na personalidade.

        Returns:
            ID do produto escolhido ou None se nenhum interesse
        """
        # Sua lógica aqui
        pass
```

### Docker & DevOps

-   **Multi-stage builds** para otimização
-   **Health checks** em todos os services
-   **Logs estruturados** (JSON quando possível)
-   **Secrets** gerenciados via variáveis de ambiente

### SQL

-   **Migrations** versionadas
-   **Índices** apropriados para performance
-   **Constraints** para integridade de dados
-   **Comentários** em estruturas complexas

## 🧪 Testando

### Testes Unitários

```bash
cd services/agent_runner
python -m pytest tests/
```

### Testes de Integração

```bash
# Testar análise de sentimento
python test_sentiment_service.py

# Testar conectividade
./check-system.sh

# Testar APIs
curl http://localhost:8080/api/agents
```

### Testes de Performance

```bash
# Monitorar recursos
docker stats

# Logs de performance
docker-compose logs agent_runner | grep -i "performance\|time"
```

## 📋 Tipos de Contribuição

### 🤖 Novos Agentes

Crie agentes com personalidades únicas:

-   **Econômico**: Só compra com desconto
-   **Impulsivo**: Compra rapidamente
-   **Social**: Influenciado por outros agentes
-   **Analítico**: Pesquisa muito antes de comprar

### 🧠 Melhorias de IA

-   **Novos modelos** de análise de sentimento
-   **Fine-tuning** para português brasileiro
-   **Análise de aspectos** (ABSA)
-   **Classificação de emoções** mais granular

### 📊 Observabilidade

-   **Métricas** de comportamento dos agentes
-   **Dashboards** para visualização
-   **Alertas** para anomalias
-   **Exportadores** para ferramentas de monitoramento

### 🔧 Infraestrutura

-   **Otimizações** de performance
-   **Escalabilidade** horizontal
-   **Backup** e recuperação
-   **CI/CD** pipelines

## 🏆 Reconhecimento

Contribuidores ativos serão reconhecidos:

-   **README**: Listagem na seção de agradecimentos
-   **Releases**: Créditos nas notas de versão
-   **Issues**: Badge de contribuidor ativo
-   **Community**: Acesso ao servidor Discord privado

## 🤝 Code of Conduct

-   **Seja respeitoso** com outros contribuidores
-   **Seja construtivo** em feedbacks e reviews
-   **Seja paciente** com iniciantes
-   **Seja inclusivo** e acolhedor

## 🐛 Debugging

### Logs Úteis

```bash
# Logs de todos os serviços
docker-compose logs -f

# Logs específicos
docker-compose logs postgres
docker-compose logs kong
docker-compose logs agent_runner

# Logs de um agente específico
docker-compose logs agent_runner | grep "agent_001"
```

### Problemas Comuns

1. **Containers não iniciam**: Verifique `.env` e `secrets.json`
2. **API não responde**: Verifique Kong config
3. **Database inacessível**: Verifique PostgreSQL health
4. **IA falha**: Verifique dependências Python
5. **Permissões**: Verifique `chmod +x` nos scripts

## 📞 Suporte

-   **Issues**: Para bugs e sugestões
-   **Discussions**: Para dúvidas gerais
-   **Discord**: Para chat em tempo real (em breve)
-   **Email**: Para questões sensíveis

## 🎉 Obrigado!

Sua contribuição ajuda a criar um dos experimentos mais interessantes sobre vida artificial! Cada linha de código nos aproxima de entender melhor os padrões emergentes da vida digital.

**Que os agentes evoluam! 🧠✨**

---

_Para mais informações, consulte [README.md](README.md) e [MIGRACAO-SENTIMENTO.md](MIGRACAO-SENTIMENTO.md)_
