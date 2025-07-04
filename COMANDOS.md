# 🎯 Comandos Essenciais - Lore N.A.

> Referência rápida para usar o projeto

## 🚀 Início Imediato

```bash
# Clone e execute em 30 segundos
git clone https://github.com/brdneo/lore.git
cd lore
python start.py --full
```

## 📋 Comandos Principais

### **Validação e Setup**
```bash
python validate_project.py    # Validar tudo
python start.py --help        # Ver opções
```

### **Execução**
```bash
python start.py              # API apenas
python start.py --dash       # Dashboard apenas
python start.py --full       # Sistema completo
```

### **Desenvolvimento**
```bash
python tests/unit/test_sentiment_service.py    # Testar IA
python -m pytest tests/                        # Todos os testes
python src/api_server.py                       # API direta
streamlit run src/dashboard.py                 # Dashboard direto
```

### **Monitoramento**
```bash
curl http://localhost:8000/health             # Status API
curl http://localhost:8000/agents             # Listar agentes
tail -f logs/lore_system.log                  # Ver logs
```

## 🔧 Solução de Problemas

### **Dependências**
```bash
pip install -r requirements.txt               # Instalar deps
python -c "import fastapi; print('OK')"       # Testar FastAPI
python -c "import streamlit; print('OK')"     # Testar Streamlit
```

### **Database**
```bash
rm -f lore_universe.db                        # Reset database
python -c "from src.database_manager import LoREDatabase; db=LoREDatabase(); print('DB OK')"
```

### **Reset Completo**
```bash
./cleanup-project.sh                          # Limpar projeto
python validate_project.py                    # Revalidar
python start.py --full                        # Reiniciar
```

## 🌐 URLs de Acesso

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs  
- **Dashboard**: http://localhost:8501
- **Health**: http://localhost:8000/health

## 📊 Status Esperado

Se tudo estiver funcionando, você deve ver:

```
✅ API Server funcionando (14 rotas)
✅ Database conectado (SQLite/PostgreSQL)
✅ Dashboard carregado
✅ Testes passando
✅ IA de sentimento ativa
```

## 🆘 Ajuda Rápida

- **Issues**: https://github.com/brdneo/lore/issues
- **Docs**: Veja `docs/` ou `QUICKSTART.md`
- **Status**: Execute `python validate_project.py`

---

**Projeto 100% validado e funcionando! 🌟**
