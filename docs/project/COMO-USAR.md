# 🚀 Como Usar o Lore N.A.

## Para Novos Usuários

### 1. **Clone do Repositório**

```bash
git clone https://github.com/your-username/lore.git
cd lore
```

### 2. **Instalação Automática**

```bash
# Navegar para o diretório do sistema
cd services/agent_runner

# Executar o launcher (faz setup automático na primeira vez)
python3 advanced_launcher.py
```

### 3. **Primeira Execução**

-   O sistema detecta automaticamente se é a primeira vez
-   Verifica Python 3.8+ e pip
-   Instala todas as dependências automaticamente
-   Configura o ambiente

### 4. **Usar o Sistema**

-   **Opção 1**: 🌐 API Server - http://localhost:8000
-   **Opção 2**: 📊 Dashboard - http://localhost:8501
-   **Opção 4**: 🎭 Demo Completo (recomendado para primeira vez)

## Solução de Problemas

### Se der erro de dependências:

```bash
pip install -r requirements.txt
```

### Se der erro de Python:

-   Certifique-se de ter Python 3.8 ou superior
-   Use `python3` no lugar de `python` se necessário

### Se der erro de permissão:

```bash
chmod +x setup.sh
```

## 🎯 O que cada opção faz:

1. **API Server**: Inicia API REST para integração externa
2. **Dashboard**: Interface web com gráficos e visualizações
3. **Economia Emocional**: Teste do sistema de tokens emocionais
4. **Demo Completo**: Demonstração de todos os recursos (RECOMENDADO)
5. **Teste Rápido**: Validação rápida do sistema
6. **Status**: Informações sobre o estado atual
7. **Neural Web**: Menu avançado de redes neurais
8. **Documentação**: Este guia e outros documentos

## 🌟 Pronto!

Você agora tem um sistema de vida artificial funcionando!

**Próximos passos:**

-   Execute a **Demonstração Completa** (opção 4)
-   Explore o **Dashboard** (opção 2)
-   Leia a documentação no **GENESIS-PROTOCOL.md**
