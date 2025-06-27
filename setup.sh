#!/bin/bash
"""
Setup Script - Lore N.A.
========================

Script de instalação rápida para o sistema Lore N.A.

Autor: Lore N.A. Genesis Team
Data: 27 de Junho de 2025
"""

echo "🌟============================================================🌟"
echo "🚀                LORE N.A. - SETUP AUTOMÁTICO               🚀"
echo "🌟============================================================🌟"
echo ""
echo "🧬 Sistema de Vida Artificial Neural"
echo "🎯 Agentes autônomos com DNA digital e evolução genética"
echo ""

# Verificar Python
echo "🔍 Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 não encontrado!"
    echo "💡 Instale Python 3.8+ primeiro"
    exit 1
fi
echo "✅ Python OK"

# Verificar pip
echo ""
echo "🔍 Verificando pip..."
python3 -m pip --version
if [ $? -ne 0 ]; then
    echo "❌ pip não encontrado!"
    echo "💡 Instale pip primeiro"
    exit 1
fi
echo "✅ pip OK"

# Navegar para diretório correto
echo ""
echo "📁 Navegando para services/agent_runner..."
cd services/agent_runner

# Instalar dependências
echo ""
echo "📦 Instalando dependências..."
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro na instalação de dependências"
    echo "💡 Tente instalar manualmente: pip install -r requirements.txt"
    exit 1
fi

# Executar launcher
echo ""
echo "🚀 Iniciando sistema..."
echo "🎯 Execute: python3 advanced_launcher.py"
echo ""
echo "🌐 URLs que estarão disponíveis:"
echo "   • Dashboard: http://localhost:8501"
echo "   • API: http://localhost:8000/docs"
echo ""
echo "🎉 SETUP CONCLUÍDO!"
echo "🚀 Para iniciar: cd services/agent_runner && python3 advanced_launcher.py"
