import asyncio
import json
import logging
import re
from typing import List, Dict, Optional
import time

import autogen_agentchat
import autogen_core
from autogen_core import CancellationToken
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage

from social.config import SimulationConfig
from social.prompts import DiffusionPrompts
from social.model import create_llm_client

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logging.getLogger(autogen_agentchat.EVENT_LOGGER_NAME).setLevel(logging.ERROR)
logging.getLogger(autogen_agentchat.TRACE_LOGGER_NAME).setLevel(logging.ERROR)
logging.getLogger(autogen_core.EVENT_LOGGER_NAME).setLevel(logging.ERROR)
logging.getLogger(autogen_core.TRACE_LOGGER_NAME).setLevel(logging.ERROR)
logging.getLogger(autogen_core.ROOT_LOGGER_NAME).setLevel(logging.ERROR)
logging.getLogger(autogen_core.JSON_DATA_CONTENT_TYPE).setLevel(logging.ERROR)
logging.getLogger(autogen_core.PROTOBUF_DATA_CONTENT_TYPE).setLevel(logging.ERROR)
logging.getLogger("httpx").setLevel(logging.ERROR)


class ReasoningError(Exception):
    """Custom exception for reasoning errors in social agents"""
    pass


class SocialAgent(AssistantAgent):
    """
    Social Agent for Innovation Diffusion Simulation
    """
    
    def __init__(
            self,
            agent_id: str,
            adopter_category: str,
            config: SimulationConfig
        ):
        """
        Initialize social agent with scientific behavioral modeling
        
        Args:
            agent_id: Unique agent identifier
            adopter_category: Rogers' adopter category
            config: Simulation configuration
        """
        
        # Create scientifically-informed system message
        system_message = DiffusionPrompts.create_agent_system_prompt(
            agent_id, adopter_category, config
        )

        llm_client = create_llm_client()

        # Initialize parent AssistantAgent
        super().__init__(
            name=agent_id,
            model_client=llm_client,
            description="Social Agent for Innovation Diffusion",
            system_message=system_message,
        )
        
        # Agent identity and characteristics
        self.agent_id = agent_id
        self.adopter_category = adopter_category
        self.config = config

        # Network connections
        self.connections: List['SocialAgent'] = []
        
        # Adoption state
        self.has_adopted = False
        self.adoption_time: Optional[int] = None
        self.adoption_attempts = 0

        # Step State
        self.current_step_state: Optional[Dict] = None
        
        logger.debug(f"Created agent {agent_id}: {adopter_category}")
    
    def add_connection(self, agent: 'SocialAgent'):
        """Add bidirectional social network connection"""
        if agent not in self.connections and agent.agent_id != self.agent_id:
            self.connections.append(agent)

    def get_connections(self) -> List['SocialAgent']:
        """Get list of connected agents"""
        return self.connections.copy()

    def freeze_state(self, global_adoption_rate: float):
        """Freeze current state for multi-phase decision making"""

        self.current_step_state = {
            "global_adoption_rate": global_adoption_rate,
            "has_adopted": self.has_adopted,
            "connections_count": len(self.connections),
            "adopted_connections": sum(1 for agent in self.connections if agent.has_adopted),
        }

    async def decide_adoption(self, current_step: int = None, last_attempt: bool = False) -> Optional[Dict]:
        """
        Make adoption decision using LLM reasoning
        
        Args:
            current_step: Current simulation step for setting adoption_time

        Returns:
            Dict with adoption decision or None if already adopted
        """

        # Skip if already adopted
        if self.has_adopted:
            return {
                "decision_time": 0,
                "has_adopted": self.has_adopted,
                "adoption_time": self.adoption_time,
                "adopted_before": True
            }
        
        cancellation_token = CancellationToken()
        try:
            decision_start = time.time()

            reasoning_output = await self._get_llm_reasoning(cancellation_token)

            decision_time = time.time() - decision_start
        except asyncio.CancelledError:
            cancellation_token.cancel()
            logger.debug(f"LLM reasoning cancelled for {self.agent_id}")
            return None
        except Exception as e:
            logger.debug(f"Error getting LLM reasoning for {self.agent_id}: {e}")
            raise e

        try:
            reasoning_str = reasoning_output.replace("\n", " ").strip()
            reasoning_str = re.sub(r',\s*(\}|])', r'\1', reasoning_str)
            json_obj_start = reasoning_str.find('{')
            json_obj_end = reasoning_str.rfind('}') + 1
            reasoning_json: dict = json.loads(reasoning_str[json_obj_start:json_obj_end])
            if reasoning_json.keys() != DiffusionPrompts.EXPECTED_DECISION_KEYS:
                logger.error(f"LLM Output: {reasoning_output}")
                logger.error(f"Invalid LLM reasoning format. Expected: {DiffusionPrompts.EXPECTED_DECISION_KEYS}, Got: {reasoning_json.keys()}")
                if last_attempt and ["decision", "reasoning"] in reasoning_json.keys():
                    logger.warning(f"Continuing with missing keys in reasoning: {reasoning_json.keys()}")
                else:
                    raise ReasoningError("Invalid LLM reasoning format")
            if not isinstance(reasoning_json["decision"], str) or reasoning_json["decision"] not in ["ADOPT", "NOT_ADOPT"]:
                logger.error(f"LLM Output: {reasoning_output}")
                logger.error(f"Invalid 'decision' type in reasoning: {reasoning_json['decision']}")
                raise ReasoningError("Invalid 'decision' type in LLM reasoning")
            if not isinstance(reasoning_json["reasoning"], str):
                logger.error(f"LLM Output: {reasoning_output}")
                logger.error(f"Invalid 'reasoning' type in reasoning: {reasoning_json['reasoning']}")
                raise ReasoningError("Invalid 'reasoning' type in LLM reasoning")
        except json.JSONDecodeError as e:
            logger.error(f"LLM Output: {reasoning_output}")
            logger.error(f"Failed to decode LLM reasoning JSON: {reasoning_str}")
            raise ReasoningError("Failed to decode LLM reasoning JSON") from e

        # Process adoption decision
        self.adoption_attempts += 1

        adopted = reasoning_json["decision"]
        reasoning_msg = reasoning_json["reasoning"]

        logger.debug(json.dumps(reasoning_json, indent=2, ensure_ascii=False))

        if adopted == "ADOPT":
            self.has_adopted = True
            self.adoption_time = current_step  # Set adoption time when adopting
            logger.info(f"🎉 Agent {self.agent_id} ({self.adopter_category}) ADOPTED in step {current_step}! ")
        else:
            logger.info(f"❌ Agent {self.agent_id} ({self.adopter_category}) did NOT adopt.")
        logger.info(f"🧠 Reasoning: {reasoning_msg}")
        
        # Record decision
        decision_record = {
            "decision_time": decision_time,
            "has_adopted": True if adopted == "ADOPT" else False,
            "adoption_time": current_step if adopted == "ADOPT" else None,
            "full_output": reasoning_output,
            **reasoning_json,
        }
        
        logger.debug(f"Agent {self.agent_id} decision completed in {decision_time:.3f}s")
        return decision_record

    async def _get_llm_reasoning(self, cancellation_token) -> str:
        """Get LLM reasoning for adoption decision"""

        prompt = DiffusionPrompts.create_adoption_decision_prompt(
            self.current_step_state.get("global_adoption_rate", 0.0),
            self.current_step_state.get("adopted_connections", 0),
            self.current_step_state.get("connections_count", 0),
            self.adoption_attempts,
            self.config
        )
        
        response = await self.on_messages(
            [TextMessage(content=prompt, source="system")], 
            cancellation_token=cancellation_token
        )
        
        return response.chat_message.content.strip()
    
    def get_state(self) -> Dict:
        return {
            "agent_id": self.agent_id,
            "adopter_category": self.adopter_category,
            "has_adopted": self.has_adopted,
            "adoption_time": self.adoption_time,
            "adoption_attempts": self.adoption_attempts,
        }
