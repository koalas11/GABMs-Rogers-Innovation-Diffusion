import logging
import time
from typing import Any, List, Dict
from social.agent import ReasoningError, SocialAgent  
from social.config import SimulationConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AgentOrchestrator:
    """
    Orchestrator for coordinating multi-agent interactions
    """

    def __init__(self, agents: List[SocialAgent], config: SimulationConfig):
        """
        Initialize orchestrator
        
        Args:
            agents: List of social agents
            config: Simulation configuration
        """
        self.agents = agents
        self.config = config
        
        # Build agent lookup
        self.agent_lookup = {agent.agent_id: agent for agent in agents}
        self.message_history = []
        
        logger.debug(f"Orchestrator initialized for {len(agents)} agents")
    
    async def orchestrate_group_decision(self, step: int) -> Dict[str, Any]:
        """
        Orchestrate multi-phase group decision process
        
        Phases:
        1. Information sharing - influential agents share thoughts
        2. Individual decisions - agents decide with full context and network messages
        
        Args:
            step: Current simulation step
            
        Returns:
            List of agent decision results
        """
        logger.info(f"🎭 Orchestrating group decision for step {step}")

        # Log frozen state summary for debugging
        adopted_before = sum(1 for agent in self.agents if agent.has_adopted)
        logger.debug(f"Info: {adopted_before}/{len(self.agents)} agents adopted before step {step}")

        global_adoption_rate = sum(agent.has_adopted for agent in self.agents) / len(self.agents)

        orchestration_start = time.time()

        for agent in self.agents:
            # Freeze state for multi-phase decision making
            agent.freeze_state(global_adoption_rate)
        
        # Phase 1: Information sharing (using frozen states)
        #for agent in self.agents:
            #self._create_influence_message_with_frozen_state(agent)
        
        # Phase 2: Individual decisions with message context
        agents_results = await self._individual_decision_phase(step)

        orchestration_time = time.time() - orchestration_start
        
        # Log adoption changes for debugging
        adopted_after = sum(1 for agent in self.agents if agent.has_adopted)
        new_adoptions = adopted_after - adopted_before
        logger.info(f"📊 Step {step} results: {new_adoptions} new adoptions ({adopted_before} → {adopted_after})")
        
        logger.info(f"🎭 Group decision orchestration completed in {orchestration_time:.3f}s")

        results = {
            "new_adoptions": new_adoptions,
            "total_adoptions": adopted_after,
            "total_adoption_rate": adopted_after / len(self.agents),
            "total_adoption_rate_per_category": {
                category: sum(1 for agent in self.agents if agent.adopter_category == category and agent.has_adopted)
                for category in self.config.adopter_distribution.keys()
            },
            "adoption_rate": new_adoptions / len(self.agents),
            "adoption_rate_per_category": {
                category: sum(1 for agent in self.agents if agent.adopter_category == category and agent.has_adopted and agent.current_step_state["has_adopted"])
                for category in self.config.adopter_distribution.keys()
            },
            "agents_results": agents_results,
            "orchestration_time": orchestration_time,
        }

        return results

    async def _individual_decision_phase(self, step: int) -> Dict[str, Dict]:
        """
        Phase 2: Individual agents make adoption decisions with full context
        
        Uses frozen states and message context for realistic decisions
        """
        logger.debug("Phase 2: Individual decisions with message context")

        results = {}
        
        for agent in self.agents:
            if self.config.speed_up and step == 1 and agent.adopter_category == "LateMajority":
                break
            results[agent.agent_id] = await self._decide_adoption_with_retry(agent, step)

        return results
    
    async def _decide_adoption_with_retry(self, agent: SocialAgent, step: int, max_retries: int = 3) -> Dict[str, Any]:
        """
        Execute agent adoption decision with robust retry mechanism
        
        Args:
            agent: The agent making the decision
            step: Current simulation step
            max_retries: Maximum number of retry attempts
            
        Returns:
            Agent decision result
            
        Raises:
            Exception: After all retry attempts are exhausted
        """        
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                logger.debug(f"Agent {agent.agent_id} decision attempt {attempt + 1}/{max_retries + 1}")
                result = await agent.decide_adoption(step, last_attempt=(attempt == max_retries))
                
                if attempt > 0:
                    logger.info(f"✅ Agent {agent.agent_id} succeeded on attempt {attempt + 1}")
                
                return result
                
            except ReasoningError as e:
                logger.warning(f"Before pop: {len(agent.model_context._messages)} messages")
                if agent.model_context._messages:
                    # Pop agent reasoning messages
                    agent.model_context._messages.pop()
                    # Pop system messages
                    agent.model_context._messages.pop()
                    logger.warning(f"After pop: {len(agent.model_context._messages)} messages")
                else:
                    logger.warning("No messages to pop from model context!")
                last_exception = e
                attempt_type = "initial" if attempt == 0 else f"retry {attempt}"
                
                logger.warning(f"⚠️ Agent {agent.agent_id} failed on {attempt_type} attempt: {type(e).__name__}: {e}")
                
                # If this was the last attempt, we'll raise the exception
                if attempt == max_retries:
                    break
            except Exception as e:
                logger.error(f"❌ Agent {agent.agent_id} failed with a non-recoverable error: {type(e).__name__}: {e}")
                raise e
        
        # All attempts failed
        logger.error(f"❌ Agent {agent.agent_id} failed after {max_retries + 1} attempts. Last error: {last_exception}")
        raise last_exception
