import os
import random
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

AGENT_NAME = "Agente 001"

def connect_to_universe() -> Client:
    """Carrega as variáveis de ambiente e cria uma conexão com o Supabase."""
    load_dotenv()
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser definidos no arquivo .env")

    print(f"{AGENT_NAME}: Conectando ao universo de Lore N.A....")
    client = create_client(url, key)
    print(f"{AGENT_NAME}: Conexão estabelecida.")
    return client

def get_agent_state(supabase: Client, agent_name: str) -> dict:
    """Busca o estado atual do agente no banco de dados."""
    print(f"\n{AGENT_NAME}: Acessando registros internos... buscando estado atual...")
    try:
        response = supabase.table("agents").select("*").eq("name", agent_name).single().execute()
        if response.data:
            print(f"{AGENT_NAME}: Estado encontrado. Saldo em carteira: {response.data.get('wallet_balance')}")
            return response.data
        else:
            print(f"{AGENT_NAME}: ERRO CRÍTICO - Não foi possível encontrar o próprio estado no universo.")
            return None
    except Exception as e:
        print(f"{AGENT_NAME}: Falha ao acessar registros. Razão: {e}")
        return None

def observe_limbo(supabase: Client) -> list:
    """Busca todos os produtos existentes na tabela 'products'."""
    print(f"\n{AGENT_NAME}: Observando o Limbo... buscando artefatos...")
    try:
        response = supabase.table("products").select("*").execute()
        if response.data:
            print(f"{AGENT_NAME}: {len(response.data)} artefatos encontrados.")
            return response.data
        else:
            print(f"{AGENT_NAME}: O Limbo está vazio.")
            return []
    except Exception as e:
        print(f"{AGENT_NAME}: Erro ao observar o Limbo. Razão: {e}")
        return []

def agent_logic(products: list, current_state: dict):
    """A lógica de 'pensamento' do agente, agora consciente de seu estado."""
    if not products or not current_state:
        print(f"{AGENT_NAME}: Dados insuficientes para processar. Desligando.")
        return

    print("\n--- Relatório de Observação do Agente 001 ---")
    for product in products:
        print(f"  - Artefato detectado: {product['name']} (Preço base: {product['base_price']})")

    produto_favorito = max(products, key=lambda p: p['base_price'])

    print("\n--- Conclusão do Agente 001 ---")
    print(f"Analisando com base no meu estado atual (Saldo: {current_state['wallet_balance']}), o artefato de maior valor percebido é a '{produto_favorito['name']}'.")

def update_agent_state(supabase: Client, agent_id: str):
    """Atualiza o estado do agente no banco, usando sua chave primária (agent_id)."""
    try:
        current_timestamp = datetime.now().isoformat()
        data, count = supabase.table("agents").update({"last_seen": current_timestamp}).eq("agent_id", agent_id).execute()
        print(f"\n{AGENT_NAME}: Registro de atividade atualizado ({current_timestamp}). Retornando ao modo de espera.")
    except Exception as e:
        print(f"{AGENT_NAME}: Falha ao atualizar registro de atividade. Razão: {e}")


if __name__ == "__main__":
    supabase_client = connect_to_universe()
    state = get_agent_state(supabase_client, AGENT_NAME)

    if state:
        lista_de_produtos = observe_limbo(supabase_client)
        agent_logic(lista_de_produtos, state)

        agent_uuid = state.get("agent_id")
        update_agent_state(supabase_client, agent_uuid)