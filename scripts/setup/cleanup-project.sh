#!/bin/bash
# Script de Limpeza Completa do Projeto Lore N.A.
# =================================================

echo "🧹 INICIANDO LIMPEZA COMPLETA DO PROJETO LORE N.A."
echo "=================================================="

# 1. Backup de segurança
echo "1️⃣ Criando backup de segurança..."
cp -r /home/brendo/lore /home/brendo/lore-backup-$(date +%Y%m%d-%H%M%S) 2>/dev/null || true

# 2. Remover estruturas antigas e duplicadas
echo "2️⃣ Removendo estruturas duplicadas..."
rm -rf services/ 2>/dev/null || true
rm -rf infra/ 2>/dev/null || true

# 3. Organizar documentos duplicados
echo "3️⃣ Organizando documentos..."
mkdir -p docs/archive
mv *-SUCESSO.md docs/archive/ 2>/dev/null || true
mv NEON-*.md docs/archive/ 2>/dev/null || true
mv RAILWAY-*.md docs/archive/ 2>/dev/null || true
mv RESPOSTA-*.md docs/archive/ 2>/dev/null || true
mv SETUP-*.md docs/archive/ 2>/dev/null || true
mv SECURITY-*.md docs/archive/ 2>/dev/null || true
mv SESSAO-*.md docs/archive/ 2>/dev/null || true

# 4. Organizar scripts
echo "4️⃣ Organizando scripts..."
mkdir -p scripts/setup scripts/deployment scripts/maintenance
mv *.sh scripts/setup/ 2>/dev/null || true
mv scripts/setup/check-system.sh scripts/maintenance/ 2>/dev/null || true
mv scripts/setup/test-jwt.sh scripts/maintenance/ 2>/dev/null || true

# 5. Organizar configurações
echo "5️⃣ Organizando configurações..."
mkdir -p config
mv app.json config/ 2>/dev/null || true
mv railway.json config/ 2>/dev/null || true
mv docker-compose.yml config/ 2>/dev/null || true

# 6. Limpar arquivos temporários
echo "6️⃣ Removendo arquivos temporários..."
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
rm -f security-audit-report.json 2>/dev/null || true
rm -f token_generator.py 2>/dev/null || true
rm -f wait-for-postgrest.sh 2>/dev/null || true

# 7. Reorganizar arquivos principais
echo "7️⃣ Reorganizando arquivos principais..."
mkdir -p docs/deployment
mv DEPLOY-GUIDE.md docs/deployment/ 2>/dev/null || true
mv WINDOWS-INSTALL.md docs/deployment/ 2>/dev/null || true

mkdir -p docs/project
mv GENESIS-PROTOCOL.md docs/project/ 2>/dev/null || true
mv COMO-USAR.md docs/project/ 2>/dev/null || true
mv ESTRUTURA.md docs/project/ 2>/dev/null || true

mkdir -p docs/strategy
mv PUBLIC-STRATEGY.md docs/strategy/ 2>/dev/null || true
mv REPOSITORY-STRATEGY.md docs/strategy/ 2>/dev/null || true
mv RESUMO-ESTRATEGIA.md docs/strategy/ 2>/dev/null || true

# 8. Criar estrutura final limpa
echo "8️⃣ Criando estrutura final..."
mkdir -p src/{core,api,web,utils,models}
mkdir -p docs/{setup,deployment,project,strategy,internal}
mkdir -p tests/{unit,integration,e2e}
mkdir -p scripts/{setup,deployment,maintenance}
mkdir -p config
mkdir -p examples
mkdir -p data

# 9. Criar arquivos __init__.py necessários
echo "9️⃣ Criando arquivos de inicialização..."
touch src/__init__.py
touch src/core/__init__.py
touch src/api/__init__.py
touch src/web/__init__.py
touch src/utils/__init__.py
touch src/models/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

echo "✅ LIMPEZA CONCLUÍDA!"
echo "📊 Estrutura organizada e pronta para desenvolvimento"
