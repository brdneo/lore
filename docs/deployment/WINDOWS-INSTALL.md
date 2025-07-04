# 🪟 Instruções para Windows 11

## ⚠️ PRÉ-REQUISITOS NECESSÁRIOS

**Para Windows 11 "zerado", você precisa instalar APENAS:**

### 1. **Python 3.8 ou superior** ⭐ OBRIGATÓRIO

```powershell
# Baixar do site oficial:
# https://www.python.org/downloads/

# OU via Microsoft Store:
# Buscar "Python" na Microsoft Store
```

**✅ IMPORTANTE**: Marcar a opção "Add Python to PATH" durante a instalação!

### 2. **Git** (Opcional, mas recomendado)

```powershell
# Baixar do site oficial:
# https://git-scm.com/download/win

# OU usar GitHub Desktop:
# https://desktop.github.com/
```

## 🚀 Instalação no Windows 11

### **Opção 1: Com Git (Recomendado)**

```powershell
# Abrir PowerShell ou CMD
# Clonar repositório
git clone https://github.com/your-username/lore.git
cd lore

# Navegar para o sistema
cd services\agent_runner

# Executar (instala tudo automaticamente)
python advanced_launcher.py
```

### **Opção 2: Download ZIP**

```powershell
# 1. Baixar ZIP do GitHub
# 2. Extrair em qualquer pasta
# 3. Abrir PowerShell na pasta extraída
cd lore-main\services\agent_runner

# Executar sistema
python advanced_launcher.py
```

### **Opção 3: Via GitHub Desktop**

```powershell
# 1. Instalar GitHub Desktop
# 2. Clonar repositório pela interface
# 3. Abrir pasta no explorador
# 4. Shift + Clique direito > "Abrir PowerShell aqui"
cd services\agent_runner
python advanced_launcher.py
```

## 🔧 Solução de Problemas Windows

### Se aparecer "python não é reconhecido":

```powershell
# Tentar com py:
py advanced_launcher.py

# OU verificar instalação:
py --version
```

### Se der erro de execução de scripts:

```powershell
# Executar como Administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Se der erro de dependências:

```powershell
# Instalar manualmente:
pip install -r requirements.txt

# OU:
py -m pip install -r requirements.txt
```

## ✅ Verificação Rápida

**Teste se Python está instalado:**

```powershell
python --version
# OU
py --version
```

**Deve mostrar algo como:**

```
Python 3.11.x
```

## 🎯 Resumo para Windows 11 Zerado:

1. **Instalar Python** (site oficial ou Microsoft Store)
2. **Baixar projeto** (Git clone ou ZIP)
3. **Executar** `python advanced_launcher.py`
4. **Pronto!** 🎉

**Tempo total: ~5-10 minutos**

## 🌐 URLs que funcionarão:

-   **Dashboard**: http://localhost:8501
-   **API**: http://localhost:8000/docs

## 💡 Dicas Windows:

-   Use **PowerShell** (mais moderno que CMD)
-   **Shift + Clique direito** na pasta = menu "Abrir PowerShell aqui"
-   **Windows Terminal** é ainda melhor (disponível na Microsoft Store)
-   Firewall do Windows pode perguntar sobre as portas 8501/8000 = **Permitir**
