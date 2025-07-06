# 🐳 Configuração Docker para CI/CD

## 📋 Status Atual

O workflow de CI/CD está configurado para **build** automático do Docker, mas o **push** para registry está desabilitado por padrão para evitar erros de secrets não configurados.

## 🔧 Como Habilitar Docker Push

### 1. **Configurar Secrets no GitHub**

No seu repositório GitHub:

1. Vá em **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione os secrets:

```
DOCKER_USERNAME: seu_usuario_dockerhub
DOCKER_PASSWORD: sua_senha_dockerhub
```

### 2. **Ativar Workflow de Push**

Renomeie o arquivo:

```bash
mv .github/workflows/docker-push.yml.disabled .github/workflows/docker-push.yml
```

### 3. **Alternativa: Dockerfile Seguro**

Para reduzir vulnerabilidades, use o Dockerfile distroless:

```bash
mv Dockerfile.distroless Dockerfile
```

## 🚀 Como Funciona

### **Workflow Principal (ci.yml)**

-   ✅ **Build Docker**: Sempre executa
-   ❌ **Push Docker**: Desabilitado por padrão
-   ✅ **Testes**: Rust + Python completos
-   ✅ **Segurança**: Audit de dependências

### **Workflow Docker Push (opcional)**

-   🔒 **Só executa se**: Secrets configurados
-   🎯 **Trigger**: Após CI principal passar
-   🐳 **Resultado**: Imagem no Docker Hub

## 📊 Comparação de Segurança

| Dockerfile              | Vulnerabilidades | Tamanho | Recomendação    |
| ----------------------- | ---------------- | ------- | --------------- |
| `Dockerfile`            | 5 high/critical  | ~500MB  | Desenvolvimento |
| `Dockerfile.distroless` | 0-1 high         | ~150MB  | **Produção**    |

## 🛡️ Melhores Práticas

### **Para Desenvolvimento:**

```yaml
# Manter workflow atual (build only)
push: false
```

### **Para Produção:**

```yaml
# Configurar secrets + ativar push
push: true
tags: lore-na/core:latest
```

### **Para Máxima Segurança:**

1. Usar `Dockerfile.distroless`
2. Configurar scanning de vulnerabilidades
3. Implementar signed images

## 🔗 Links Úteis

-   [Docker Hub](https://hub.docker.com)
-   [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
-   [Distroless Images](https://github.com/GoogleContainerTools/distroless)

---

**Status**: Build funcional ✅ | Push opcional 🔧 | Segurança configurada 🛡️
