# services/agent_runner/base_agent.py
# Contém a classe mãe para todos os agentes, encapsulando a comunicação com a API.

import logging
import os
import time
import requests
import jwt
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configura o logger para este módulo.
logger = logging.getLogger(__name__)

class BaseAgent:
    """
    A classe base para todos os Agentes Neurais do Lore N.A.
    
    Responsabilidades:
    - Gerenciar a comunicação segura e resiliente com a API.
    - Manter o estado interno do agente (ID, saldo, etc.).
    - Fornecer métodos para perceber o ambiente e atuar sobre ele.
    - Definir um ciclo de vida que pode ser executado.
    """
    
    def __init__(self, name: str, api_base_url: str):
        """
        Inicializa o agente.
        
        Args:
            name (str): O nome único do agente, usado para buscar seu estado.
            api_base_url (str): A URL base da API do Lore (ex: http://kong:8000).
        """
        self.name = name
        self.api_base_url = api_base_url
        self.agent_data = None  # Armazena os dados do agente vindos da API.
        
        # Configuração JWT do Kong
        self.kong_jwt_iss = os.getenv("KONG_JWT_ISS", "agent_genesis")
        self.kong_jwt_secret = os.getenv("KONG_JWT_SECRET")
        
        if not self.kong_jwt_secret:
            raise ValueError("KONG_JWT_SECRET deve ser definido nas variáveis de ambiente")
        
        # Adiciona o nome do agente aos logs para fácil rastreamento.
        self.logger = logging.LoggerAdapter(logger, {'agent_name': self.name})

        # Configura a sessão de requisições com resiliência.
        self.session = self._create_resilient_session()
        self.headers = {
            "Authorization": f"Bearer {self._generate_jwt_token()}",
            "Prefer": "return=representation,resolution=merge-duplicates"
        }
        
        self.initialize()

    def _generate_jwt_token(self) -> str:
        """
        Gera um token JWT para autenticação no Kong.
        O token expira em 1 hora.
        """
        payload = {
            "iss": self.kong_jwt_iss,
            "exp": int(time.time()) + 60 * 60  # expira em 1h
        }
        token = jwt.encode(payload, self.kong_jwt_secret, algorithm="HS256")
        self.logger.info(f"Novo token JWT gerado para issuer: {self.kong_jwt_iss}")
        return token

    def _refresh_jwt_if_needed(self):
        """
        Verifica se o token JWT está próximo de expirar e o renova se necessário.
        """
        try:
            current_token = self.headers["Authorization"].split("Bearer ")[1]
            decoded = jwt.decode(current_token, self.kong_jwt_secret, algorithms=["HS256"])
            
            # Se restam menos de 5 minutos, renova o token
            if decoded['exp'] - time.time() < 300:
                self.logger.info("Token JWT próximo de expirar, renovando...")
                new_token = self._generate_jwt_token()
                self.headers["Authorization"] = f"Bearer {new_token}"
                
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token JWT expirado, gerando novo...")
            new_token = self._generate_jwt_token()
            self.headers["Authorization"] = f"Bearer {new_token}"
        except Exception as e:
            self.logger.error(f"Erro ao verificar token JWT: {e}")

    def _create_resilient_session(self) -> requests.Session:
        """
        Cria uma sessão de requisições com uma estratégia de reintentos.
        Isso torna o agente robusto a falhas de rede transitórias.
        (Implementa a Recomendação nº 4 da Revisão Arquitetônica)
        """
        session = requests.Session()
        retry_strategy = Retry(
            total=5,  # Número total de reintentos.
            backoff_factor=1,  # Fator de espera (ex: 1s, 2s, 4s, 8s).
            status_forcelist=[500, 502, 503, 504],  # Códigos de erro que disparam o reintento.
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def initialize(self):
        """Busca o estado inicial do agente na API pelo seu nome."""
        self.logger.info("Inicializando e buscando estado na API...")
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?name=eq.{self.name}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Estado inicial carregado: ID={self.agent_data['id']}, Saldo={self.agent_data['wallet_balance']}")
            else:
                self.logger.error(f"Não foi possível encontrar o agente com o nome '{self.name}'.")
                self.agent_data = None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro de comunicação ao inicializar: {e}")
            self.agent_data = None

    def _update_local_state(self):
        """Atualiza o estado local do agente buscando os dados mais recentes da API."""
        if not self.agent_data:
            return
        try:
            self._refresh_jwt_if_needed()
            response = self.session.get(f"{self.api_base_url}/agents?id=eq.{self.agent_data['id']}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Estado local atualizado. Novo saldo: {self.agent_data['wallet_balance']}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Não foi possível atualizar o estado local: {e}")

    def decide_and_act(self):
        """
        Método abstrato para a lógica de decisão.
        As classes filhas DEVEM implementar este método.
        """
        raise NotImplementedError("A subclasse do agente deve implementar o método 'decide_and_act'.")

    def run_life_cycle(self, tick_interval: int):
        """
        O ciclo de vida principal que orquestra o agente.
        
        Args:
            tick_interval (int): O número de segundos a esperar entre cada ciclo.
        """
        self.logger.info(f"Iniciando ciclo de vida com intervalo de {tick_interval} segundos.")
        while True:
            self.logger.info("--- Novo Ciclo (Tick) ---")
            if self.agent_data:
                self.decide_and_act()
            else:
                self.logger.warning("Agente não inicializado. Tentando reinicializar...")
                self.initialize()
            
            time.sleep(tick_interval)

    def _update_local_state(self):
        """Atualiza o estado local do agente buscando os dados mais recentes da API."""
        if not self.agent_data:
            return
        try:
            response = self.session.get(f"{self.api_base_url}/agents?id=eq.{self.agent_data['id']}", headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data:
                self.agent_data = data[0]
                self.logger.info(f"Estado local atualizado. Novo saldo: {self.agent_data['wallet_balance']}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Não foi possível atualizar o estado local: {e}")

    def decide_and_act(self):
        """
        Método abstrato para a lógica de decisão.
        As classes filhas DEVEM implementar este método.
        """
        raise NotImplementedError("A subclasse do agente deve implementar o método 'decide_and_act'.")

    def run_life_cycle(self, tick_interval: int):
        """
        O ciclo de vida principal que orquestra o agente.
        
        Args:
            tick_interval (int): O número de segundos a esperar entre cada ciclo.
        """
        self.logger.info(f"Iniciando ciclo de vida com intervalo de {tick_interval} segundos.")
        while True:
            self.logger.info("--- Novo Ciclo (Tick) ---")
            if self.agent_data:
                self.decide_and_act()
            else:
                self.logger.warning("Agente não inicializado. Tentando reinicializar...")
                self.initialize()
            
            time.sleep(tick_interval)

