# 🚂 RAILWAY SETUP - Configuração Final

## 🎯 NEON ✅ CONCLUÍDO - AGORA É A VEZ DO RAILWAY

Suas credenciais Neon estão configuradas! Agora vamos ao Railway.

---

## 📋 PASSO A PASSO RAILWAY

### 1️⃣ **Cadastro Railway (2 min)**

1. **Acesse**: https://railway.app
2. **Clique**: "Login" (canto superior direito)
3. **Escolha**: "Continue with GitHub" (mesmo GitHub do Neon)
4. **Autorize**: Conectar Railway ao seu GitHub

### 2️⃣ **Upgrade para Hobby Plan (1 min)**

1. **Dashboard Railway**: Clique no seu avatar (canto superior direito)
2. **Menu**: "Account Settings"
3. **Aba**: "Plans & Usage"
4. **Clique**: "Upgrade to Hobby Plan"
5. **Adicione**: Cartão de crédito
6. **Confirme**: $5/mês (mas você tem $500 créditos = 100 meses grátis!)

### 3️⃣ **Deploy do Projeto (2 min)**

1. **Dashboard**: Clique "New Project"
2. **Escolha**: "Deploy from GitHub repo"
3. **Selecione**: Repositório `lore` (autorizar acesso se necessário)
4. **Branch**: `main`
5. **Clique**: "Deploy"

**⏳ Aguarde deploy (2-3 minutos)...**

### 4️⃣ **CONFIGURAR VARIÁVEL DE AMBIENTE (CRÍTICO!)**

1. **No projeto deployado**: Clique na aba "Variables"
2. **Clique**: "New Variable"
3. **Nome**: `DATABASE_URL`
4. **Valor**: Cole EXATAMENTE isto:
    ```
    postgresql://neondb_owner:npg_Il2RJN8hGwYb@ep-orange-fog-a5a3ol11-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require
    ```
5. **Clique**: "Add"

### 5️⃣ **Configurar Outras Variáveis**

Adicione essas variáveis também:

**PORT**:

```
8000
```

**PYTHONPATH**:

```
/app/services/agent_runner
```

**WEB_CONCURRENCY**:

```
1
```

**RAILWAY_ENVIRONMENT**:

```
production
```

### 6️⃣ **Redeploy (Importante!)**

1. **Aba "Deployments"**: Clique no deploy mais recente
2. **Clique**: "Redeploy" (para aplicar as variáveis)
3. **Aguarde**: 2-3 minutos

---

## 🔗 RESULTADO ESPERADO

Após o redeploy, você terá:

1. **URL da aplicação**: `https://lore-na-XXXXX.railway.app`
2. **Health check**: `https://lore-na-XXXXX.railway.app/health`
3. **Status**: Should return `{"status": "healthy"}`

---

## ✅ CHECKLIST RAILWAY

-   [ ] Conta Railway criada (GitHub)
-   [ ] Upgrade para Hobby Plan realizado
-   [ ] Repositório `lore` conectado
-   [ ] Deploy realizado com sucesso
-   [ ] Variável `DATABASE_URL` configurada ✨
-   [ ] Variáveis `PORT`, `PYTHONPATH`, etc configuradas
-   [ ] Redeploy realizado
-   [ ] URL gerada e funcionando
-   [ ] Health check respondendo `healthy`

---

## 🆘 SE DER PROBLEMA

### **Deploy Failed?**

-   Verifique se o repositório está público
-   Confirme que está na branch `main`

### **Health Check Failed?**

-   Verifique se `DATABASE_URL` está EXATAMENTE como mostrado
-   Confirme que todas as variáveis foram adicionadas
-   Faça redeploy após adicionar variáveis

### **Connection Error?**

-   Teste connection string Neon separadamente
-   Verifique se não há espaços extras na `DATABASE_URL`

---

## 🎯 QUANDO TERMINAR

Me envie:

1. ✅ **"Railway configurado"**
2. 🔗 **URL da aplicação** (https://lore-na-xxxxx.railway.app)
3. 🧪 **Resultado do health check** (teste acessando /health)

**Estamos a minutos do sistema 24/7 funcionando! 🚀**
