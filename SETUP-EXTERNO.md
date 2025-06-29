# 🚀 CADASTROS EXTERNOS - Passo a Passo Completo

## 📋 RESUMO DO PLANO

-   **💰 Custo Real**: $0 nos primeiros 100 meses (Railway dá $500 créditos)
-   **🔄 Depois**: $5/mês (apenas Railway, Neon continua grátis)
-   **⏱️ Tempo Setup**: ~10 minutos no total

---

## 1️⃣ NEON POSTGRESQL (GRÁTIS PARA SEMPRE)

### 🔗 Cadastro

1. **Acesse**: https://neon.tech/
2. **Clique**: "Sign Up" (canto superior direito)
3. **Escolha**: "Continue with GitHub" (recomendado)
4. **Autorize**: Conectar sua conta GitHub

### 🗄️ Criar Database

1. **Dashboard**: Após login, clique "Create Database"
2. **Configurações**:
    - **Project Name**: `lore-na-universe`
    - **Database Name**: `lore_agents`
    - **Region**: `US East (Ohio)` (melhor latência para Brasil)
    - **Postgres Version**: `15` (mais recente)
3. **Clique**: "Create Project"

### 📝 Copiar Connection String

1. **No Dashboard**: Clique no projeto criado
2. **Vá em**: "Connection Details"
3. **Copie**: A connection string completa (formato: `postgresql://user:pass@host/db`)
4. **Exemplo**:
    ```
    postgresql://username:password123@ep-cool-name-123456.us-east-1.aws.neon.tech/lore_agents?sslmode=require
    ```

### ✅ Neon Pronto!

-   **Status**: ✅ Database criado
-   **Custo**: $0 (0.5GB grátis, suficiente para 1M+ agentes)
-   **Uptime**: 24/7

---

## 2️⃣ RAILWAY (PRIMEIROS 100 MESES GRÁTIS!)

### 🔗 Cadastro

1. **Acesse**: https://railway.app/
2. **Clique**: "Login" (canto superior direito)
3. **Escolha**: "GitHub" (mesmo GitHub do Neon)
4. **Autorize**: Conectar Railway ao seu GitHub

### 🎯 Plano Hobby ($5/mês)

1. **No Dashboard**: Clique no seu perfil (canto superior direito)
2. **Vá em**: "Account Settings"
3. **Aba**: "Plans & Usage"
4. **Clique**: "Upgrade to Hobby Plan"
5. **Adicione**: Cartão de crédito (não será cobrado nos primeiros $500)

### 📊 Créditos Iniciais

-   **$500 grátis**: Equivale a ~100 meses de uso
-   **Consumption**: ~$5/mês depois dos créditos
-   **Billing**: Só depois de esgotar os $500

### 🚀 Deploy do Projeto

1. **Dashboard Railway**: Clique "New Project"
2. **Escolha**: "Deploy from GitHub repo"
3. **Selecione**: Repositório `lore` (autorizar acesso se necessário)
4. **Branch**: `main`
5. **Clique**: "Deploy"

### ⚙️ Configurar Variáveis de Ambiente

1. **No Projeto**: Clique na aba "Variables"
2. **Adicionar as seguintes variáveis**:

```bash
# Cole a connection string do Neon aqui
DATABASE_URL=postgresql://username:password123@ep-cool-name-123456.us-east-1.aws.neon.tech/lore_agents?sslmode=require

# Configurações Railway
PORT=8000
PYTHONPATH=/app/services/agent_runner
WEB_CONCURRENCY=1
RAILWAY_ENVIRONMENT=production
```

3. **Clique**: "Save" para cada variável

### 🔗 Configurar Domínio

1. **Aba "Settings"**: Do seu projeto
2. **Seção "Domains"**: Clique "Generate Domain"
3. **URL será**: `https://lore-na-production.up.railway.app` (ou similar)

### ✅ Railway Pronto!

-   **Status**: ✅ App deployed e rodando 24/7
-   **URL**: Sua URL personalizada do Railway
-   **Custo**: $0 (por ~100 meses)

---

## 3️⃣ GITHUB STUDENT PACK (OPCIONAL - MAIS CRÉDITOS)

### 📚 Se você é estudante

1. **Acesse**: https://education.github.com/pack
2. **Clique**: "Get student benefits"
3. **Verificação**: Upload de comprovante de matrícula
4. **Benefícios extras**:
    - **Railway**: +$500 créditos adicionais
    - **Neon**: Tier PRO grátis por 1 ano
    - **Outros**: 100+ ferramentas grátis

### ✅ GitHub Pack (Se aplicável)

-   **Status**: ✅ Créditos extras garantidos
-   **Duração**: Enquanto for estudante

---

## 4️⃣ VALIDAÇÃO FINAL

### 🧪 Testar Sistema

Após completar os passos acima:

1. **API Health Check**:

    ```bash
    curl https://sua-app.railway.app/health
    ```

2. **Resposta esperada**:

    ```json
    {
        "status": "healthy",
        "environment": "production",
        "agents_count": 0,
        "database": { "status": "healthy" },
        "version": "2.0.0"
    }
    ```

3. **Dashboard Railway**: Logs devem mostrar "🚀 Iniciando Lore N.A. API Server"

### ✅ Sistema 24/7 Ativo!

-   **API**: ✅ Online 24/7
-   **Database**: ✅ Persistente
-   **Monitoring**: ✅ Health checks automáticos
-   **Custo**: ✅ $0 por ~100 meses

---

## 📋 CHECKLIST FINAL

### Antes de começar:

-   [ ] Conta GitHub ativa
-   [ ] Cartão de crédito válido (para Railway Hobby)

### Neon PostgreSQL:

-   [ ] Conta criada via GitHub
-   [ ] Database `lore-na-universe` criado
-   [ ] Connection string copiada
-   [ ] Testado conexão

### Railway:

-   [ ] Conta criada via GitHub
-   [ ] Upgrade para Hobby Plan realizado
-   [ ] Repositório conectado
-   [ ] Variáveis de ambiente configuradas
-   [ ] Deploy realizado com sucesso
-   [ ] URL personalizada gerada

### Validação:

-   [ ] Health check respondendo
-   [ ] Logs showing startup success
-   [ ] Database conectado
-   [ ] Sistema 24/7 operacional

---

## 🆘 SUPORTE DURANTE SETUP

Se tiver algum problema durante o setup:

1. **Database Issues**: Verifique connection string no Neon
2. **Deploy Issues**: Verifique logs no Railway Dashboard
3. **Environment**: Confirme todas as variáveis estão corretas
4. **Help**: Railway tem chat support excellent 24/7

---

## 🎯 RESULTADO FINAL

**🚀 Sistema Lore N.A. rodando 24/7 na nuvem:**

-   **URL**: `https://sua-app.railway.app`
-   **Uptime**: 99.9%
-   **Latência**: <200ms global
-   **Capacity**: Milhões de agentes
-   **Cost**: $0/mês (100 meses)
-   **Backup**: Automático (Neon)
-   **Scaling**: Automático (Railway)

**🧬 Agentes neurais evoluindo 24/7! 🌐**
