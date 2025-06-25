# services/agent_runner/frugal_agent.py
# Implementa a lógica de decisão para o arquétipo "Comprador Frugal".

import logging
from base_agent import BaseAgent
import requests

# Configura o logger para este módulo.
logger = logging.getLogger(__name__)

class FrugalBuyerAgent(BaseAgent):
    """
    Um agente com uma lógica de decisão simples: comprar o artefato mais barato
    que ele pode pagar.
    """
    
    def __init__(self, name: str, api_base_url: str):
        # Chama o construtor da classe pai para configurar a comunicação.
        super().__init__(name, api_base_url)
        self.logger.info("Arquétipo 'Comprador Frugal' instanciado.")

    def decide_and_act(self):
        """
        Implementa o ciclo de Percepção -> Decisão -> Ação.
        """
        try:
            # Refresh JWT token if needed
            self._refresh_jwt_if_needed()
            
            # 1. PERCEPÇÃO: Observar o mercado.
            self.logger.info("Observando o mercado...")
            response = self.session.get(f"{self.api_base_url}/artifacts", headers=self.headers)
            response.raise_for_status()
            artifacts = response.json()
            self.logger.info(f"Percebeu {len(artifacts)} artefato(s).")
            
            if not artifacts:
                self.logger.info("Mercado vazio. Nada a fazer.")
                return

            # 2. DECISÃO: Lógica do "Comprador Frugal".
            # Filtrar artefatos que estão ativos e que posso pagar.
            current_balance = float(self.agent_data['wallet_balance'])
            affordable_artifacts = [
                a for a in artifacts 
                if a['status'] == 'ACTIVE' and float(a['current_price']) <= current_balance
            ]
            
            if not affordable_artifacts:
                self.logger.info("Nenhum artefato acessível com o saldo atual. Economizando.")
                return

            # Encontrar o mais barato entre os acessíveis.
            cheapest_artifact = min(affordable_artifacts, key=lambda a: float(a['current_price']))
            
            self.logger.info(f"Decisão: Tentar comprar o artefato mais barato: '{cheapest_artifact['name']}' por {cheapest_artifact['current_price']}.")

            # 3. AÇÃO: Executar a compra.
            self._buy_artifact(cheapest_artifact['id'])

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro no ciclo de percepção/ação: {e}")
        except Exception as e:
            self.logger.error(f"Erro inesperado no ciclo: {e}")

    def _buy_artifact(self, artifact_id: str):
        """Chama a função RPC da API para realizar a compra."""
        self.logger.info(f"Ação: Enviando requisição de compra para o artefato {artifact_id}.")
        try:
            self._refresh_jwt_if_needed()
            payload = {
                "p_agent_id": self.agent_data['id'],
                "p_artifact_id": artifact_id
            }
            response = self.session.post(f"{self.api_base_url}/rpc/buy_artifact", json=payload, headers=self.headers)
            response.raise_for_status()

            self.logger.info("Ação de compra bem-sucedida! Atualizando estado local.")
            # Se a compra for bem-sucedida, atualizamos nosso estado interno.
            self._update_local_state()

        except requests.exceptions.RequestException as e:
            if e.response is not None:
                self.logger.error(f"Falha na API ao tentar comprar: {e.response.status_code} - {e.response.text}")
            else:
                self.logger.error(f"Falha de comunicação ao tentar comprar: {e}")
