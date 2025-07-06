# python/lore_na/agents/frugal_agent.py
# Implements decision logic for the "Frugal Buyer" archetype.

import logging
from .base_agent import BaseAgent
import requests

# Configure logger for this module
logger = logging.getLogger(__name__)


class FrugalBuyerAgent(BaseAgent):
    """
    An agent with simple decision logic: buy the cheapest artifact
    it can afford.
    """

    def __init__(self, name: str, api_base_url: str, dna=None):
        # Call parent constructor to set up communication
        super().__init__(name, api_base_url, dna)
        self.logger.info("Frugal Buyer archetype instantiated.")

    def decide_and_act(self):
        """
        Implements the Perception -> Decision -> Action cycle.
        """
        try:
            # Refresh JWT token if needed
            self._refresh_jwt_if_needed()

            # 1. PERCEPTION: Observe the market
            self.logger.info("Observing the market...")
            response = self.session.get(f"{self.api_base_url}/artifacts", headers=self.headers)
            response.raise_for_status()
            artifacts = response.json()
            self.logger.info(f"Perceived {len(artifacts)} artifact(s).")

            if not artifacts:
                self.logger.info("Empty market. Nothing to do.")
                return

            # 2. DECISION: "Frugal Buyer" logic with genetic influence
            # Filter artifacts that are active and affordable
            current_balance = float(self.agent_data['wallet_balance'])
            affordable_artifacts = [
                a for a in artifacts
                if a['status'] == 'ACTIVE' and float(a['current_price']) <= current_balance
            ]

            if not affordable_artifacts:
                self.logger.info("No affordable artifacts with current balance. Saving money.")

                # Update performance based on frugal behavior
                self.update_performance("limbo", {
                    "decision_accuracy": 0.6,  # Conservative but safe
                    "market_timing": 0.5
                })
                return

            # 🧬 GENETIC DECISION: Use DNA to influence decision
            decision_factors = {
                "products": [
                    {
                        "id": a['id'],
                        "name": a['name'],
                        "price": float(a['current_price']),
                        "quality": 0.5,  # Default quality estimate
                        "is_new": False  # Could be enhanced with actual data
                    }
                    for a in affordable_artifacts
                ]
            }

            # Let genetics influence the decision
            influenced_factors = self.make_decision_with_genes(decision_factors, "limbo")

            # Sort by genetic score if available, otherwise by price
            if influenced_factors["products"] and "genetic_score" in influenced_factors["products"][0]:
                # Use genetic scoring
                best_artifact_data = influenced_factors["products"][0]
                cheapest_artifact = next(
                    a for a in affordable_artifacts
                    if a['id'] == best_artifact_data['id']
                )
                self.logger.info(
    f"Genetic decision: Buying artifact with genetic score {
        best_artifact_data['genetic_score']:.3f}")
            else:
                # Fallback to original frugal logic
                cheapest_artifact = min(affordable_artifacts, key=lambda a: float(a['current_price']))
                self.logger.info("Using fallback frugal logic: cheapest available.")

            self.logger.info(
    f"Decision: Attempting to buy artifact: '{
        cheapest_artifact['name']}' for {
            cheapest_artifact['current_price']}.")

            # 3. ACTION: Execute the purchase
            success = self._buy_artifact(cheapest_artifact['id'])

            # Update performance based on action
            if success:
                # Calculate profit potential (simplified)
                price_paid = float(cheapest_artifact['current_price'])
                profit_ratio = max(0.1, (current_balance - price_paid) / current_balance)

                self.update_performance("limbo", {
                    "profit_ratio": profit_ratio,
                    "decision_accuracy": 0.8,  # Successful purchase
                    "market_timing": 0.7  # Reasonable timing
                })
            else:
                self.update_performance("limbo", {
                    "decision_accuracy": 0.3,  # Failed purchase
                    "market_timing": 0.4
                })

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error in perception/action cycle: {e}")
            self.update_performance("limbo", {
                "decision_accuracy": 0.2,
                "market_timing": 0.3
            })
        except Exception as e:
            self.logger.error(f"Unexpected error in cycle: {e}")
            self.update_performance("limbo", {
                "decision_accuracy": 0.1,
                "market_timing": 0.2
            })

    def _buy_artifact(self, artifact_id: str) -> bool:
        """Call the API RPC function to make the purchase."""
        self.logger.info(f"Action: Sending purchase request for artifact {artifact_id}.")
        try:
            self._refresh_jwt_if_needed()
            payload = {
                "p_agent_id": self.agent_data['id'],
                "p_artifact_id": artifact_id
            }
            response = self.session.post(f"{self.api_base_url}/rpc/buy_artifact", json=payload, headers=self.headers)
            response.raise_for_status()

            self.logger.info("Purchase action successful! Updating local state.")
            # If purchase is successful, update our internal state
            self._update_local_state()
            return True

        except requests.exceptions.RequestException as e:
            if e.response is not None:
                self.logger.error(f"API failure when trying to buy: {e.response.status_code} - {e.response.text}")
            else:
                self.logger.error(f"Communication failure when trying to buy: {e}")
            return False
