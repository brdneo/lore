import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Pega a URL e a chave do Supabase a partir das variáveis de ambiente
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Verifica se as variáveis foram carregadas
if not url or not key:
    raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser definidos no arquivo .env")

# Cria o cliente de conexão com o Supabase
print("Conectando ao universo de Lore N.A....")
supabase: Client = create_client(url, key)
print("Conexão estabelecida.")

# --- O GÊNESIS: A Lista dos Primeiros Produtos do Limbo ---
# Cada dicionário representa um produto a ser inserido na nossa tabela 'products'
produtos_inaugurais = [
    {
        "name": "Unidade de Contenção Quântica",
        "description": "Uma bateria portátil que dobra o espaço-tempo para armazenar energia infinita. Pequenos vazamentos são esperados.",
        "base_price": 9999.99,
        "category": "Energia",
        "status": "ACTIVE",
        "volatility_index": 0.9,
        "lifespan_days": 365,
    },
    {
        "name": "Nano-Enxame Reparador 'A Colmeia'",
        "description": "Libere um enxame de nanorobôs para consertar qualquer coisa, de um motor de fusão a um coração partido. Não nos responsabilizamos por senciência emergente.",
        "base_price": 2499.50,
        "category": "Nanotecnologia",
        "status": "ACTIVE",
        "volatility_index": 0.75,
        "lifespan_days": 180,
    },
    {
        "name": "Sintetizador de Matéria Portátil",
        "description": "Transforma lixo doméstico em qualquer item pré-programado. A versão 1.0 só sintetiza 'Bolo de Chocolate'.",
        "base_price": 750.00,
        "category": "Utilitários",
        "status": "ACTIVE",
        "volatility_index": 0.3,
        "lifespan_days": 730,
    },
    {
        "name": "Óculos de Realidade Consensual",
        "description": "Veja o mundo como ele realmente é. Ou como nós queremos que você veja. A escolha é sua. Mais ou menos.",
        "base_price": 1250.00,
        "category": "Vestíveis",
        "status": "ACTIVE",
        "volatility_index": 0.6,
        "lifespan_days": 500,
    },
    {
        "name": "Pingente de Tradução Universal 'Babel-17'",
        "description": "Entenda e seja entendido em mais de 7 milhões de dialetos galácticos. Efeitos colaterais incluem desejo incontrolável por poesia Vogon.",
        "base_price": 542.99,
        "category": "Comunicação",
        "status": "ACTIVE",
        "volatility_index": 0.4,
        "lifespan_days": 1095,
    },
    # Adicione mais 5 produtos aqui se quiser, seguindo o mesmo formato
]

print("\nIniciando a população do Limbo...")
for i, produto in enumerate(produtos_inaugurais):
    try:
        print(f"Criando produto {i+1}/10: '{produto['name']}'...")
        # Insere o produto na tabela 'products'
        data, count = supabase.table("products").insert(produto).execute()
        
        # A API retorna um erro em 'data' se algo der errado
        if data[1]: # O segundo elemento da tupla contém o registro inserido
             print(f"  -> SUCCESS: Produto '{data[1][0]['name']}' criado no Limbo com ID: {data[1][0]['product_id']}")
        else:
            # Tratamento de erro se a inserção não retornar dados, mas não lançar exceção
            print(f"  -> WARNING: Inserção do produto '{produto['name']}' não retornou dados.")

    except Exception as e:
        print(f"  -> FAILED: Erro ao criar o produto '{produto['name']}'. Razão: {e}")

print("\nPopulação do Limbo concluída.")