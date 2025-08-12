from collections.abc import Callable
import logging
import time
import pickle
from typing import List, Dict, Optional
from datetime import datetime

from social.config import SimulationConfig, SIMULATION_CONFIGS
from social.agent import SocialAgent
from social.network import NetworkGenerator
from social.orchestrator import AgentOrchestrator

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class SocialDiffusionSimulation:
    """
    Social Innovation Diffusion Simulation
    """

    def __init__(
            self,
            config: SimulationConfig = None,
            simulation_initialized_callback: Optional[Callable[[], None]] = None,
            simulation_step_started_callback: Optional[Callable[[int], None]] = None,
            simulation_step_completed_callback: Optional[Callable[[int], None]] = None,
            simulation_completed_callback: Optional[Callable[[], None]] = None,
            simulation_error_callback: Optional[Callable[[str], None]] = None,
        ):
        """
        Initialize simulation with scientific configuration
        
        Args:
            config: Simulation configuration (default if None)
        """
        self.config = config or SimulationConfig()
        self.simulation_initialized_callback = simulation_initialized_callback
        self.simulation_step_started_callback = simulation_step_started_callback
        self.simulation_step_completed_callback = simulation_step_completed_callback
        self.simulation_completed_callback = simulation_completed_callback
        self.simulation_error_callback = simulation_error_callback
        
        # Simulation state
        self.agents: List[SocialAgent] = []
        self.orchestrator: Optional[AgentOrchestrator] = None
        self.current_step = 0
        
        # Data tracking
        self.results = {
            "config": self.config.to_dict(),
        }
        self.results["adoption_history"] = {}
        
        # Performance metrics
        self.simulation_start_time = None
        self.total_llm_calls = 0
        
    def initialize_simulation(self):
        """Initialize all simulation components"""
        
        # Create agents
        self._create_agents()
        
        # Create social network
        network_stats = NetworkGenerator.create_network(self.agents, self.config)
        self.results["network_metrics"] = network_stats
        
        # Validate network
        validation = NetworkGenerator.validate_network(self.agents)
        if not validation["valid"]:
            logger.warning(f"Network validation issues: {validation['issues']}")
        
        # Initialize orchestrator for multi-agent coordination
        self.orchestrator = AgentOrchestrator(self.agents, self.config)
        
        logger.info(f"Enhanced Social Diffusion Simulation initialized")
        logger.info(f"Agents: {self.config.num_agents}, "
                   f"Network: {self.config.network_type}, "
                   f"Max steps: {self.config.max_steps}")
        
        if self.simulation_initialized_callback:
            self.simulation_initialized_callback()
    
    def _create_agents(self):
        """Create agents with configured distribution"""
        
        agents_per_category = self.config.get_agents_per_category()
        
        for category, count in agents_per_category.items():
            logger.debug(f"Creating {count} {category} agents")
            
            for i in range(1, count + 1):
                agent = SocialAgent(
                    agent_id=f"{category}_agent_{i:03d}",
                    adopter_category=category,
                    config=self.config
                )
                self.agents.append(agent)

        logger.info(f"Created {len(self.agents)} agents")
        for category, count in agents_per_category.items():
            percentage = (count / self.config.num_agents) * 100
            logger.info(f"  {category}: {count} agents ({percentage:.1f}%)")
    
    async def run_simulation(self):
        """
        Run complete simulation with orchestrated multi-agent decisions
        """
        self.simulation_start_time = time.time()
        logger.info(f"🚀 Starting enhanced social diffusion simulation")
        logger.info(f"📊 Using scientific formulas and improved LLM prompting")
        
        try:
            no_adoption_steps = 0
            # Run simulation steps
            for step in range(1, self.config.max_steps + 1):
                self.current_step = step  # Track current step
                
                if self.simulation_step_started_callback:
                    self.simulation_step_started_callback(step)

                logger.debug(f"Starting step {step}/{self.config.max_steps}")

                # Use orchestrator for complex multi-agent coordination
                step_results = await self.orchestrator.orchestrate_group_decision(step)

                self.results["adoption_history"][step] = step_results
                
                total_adoption_rate = step_results.get("total_adoption_rate", 0)
                if total_adoption_rate == 1.0:
                    logger.info(f"🏁 Simulation completed early at step {step}: all agents adopted")
                    if self.simulation_step_completed_callback:
                        self.simulation_step_completed_callback(step)
                    break

                # Check early stopping condition - high adoption rate
                if total_adoption_rate >= self.config.early_stop_threshold:
                    logger.info(f"🏁 Early stopping at step {step}: "
                               f"adoption rate {total_adoption_rate} >= {self.config.early_stop_threshold}")
                    if self.simulation_step_completed_callback:
                        self.simulation_step_completed_callback(step)
                    break
                
                # Check early stopping condition - no new adoptions
                new_adoptions = step_results.get("new_adoptions", 0)

                if new_adoptions > 0:
                    no_adoption_steps = 0
                else:
                    no_adoption_steps += 1

                if self.config.early_stop_no_adoption_steps is not None and no_adoption_steps >= self.config.early_stop_no_adoption_steps:
                    logger.info(f"🛑 Early stopping at step {step}: "
                               f"no new adoptions in this iteration ({no_adoption_steps} consecutive steps)")
                    if self.simulation_step_completed_callback:
                        self.simulation_step_completed_callback(step)
                    break

                adoption_rate = step_results.get("adoption_rate", 0)
                logger.info(f"📈 Step {step}: {adoption_rate:.1%} adoption rate ({total_adoption_rate:.1%} total), "
                            f"{new_adoptions} new adoptions")
                
                if self.simulation_step_completed_callback:
                    self.simulation_step_completed_callback(step)

            simulation_time = time.time() - self.simulation_start_time
            self.results["total_adoption_rate"] = step_results.get("total_adoption_rate", 0)
            self.results["total_adoptions"] = step_results.get("total_adoptions", 0)
            self.results["final_step"] = step
            self.results["simulation_time"] = simulation_time

            # Add agent states for visualization
            agent_states = []
            for agent in self.agents:
                agent_state = agent.get_state()
                agent_states.append(agent_state)

            self.results["agent_states"] = agent_states

            # Ensure config is properly included
            self.results["config"] = self.config.to_dict()

            logger.info(f"🎯 Simulation completed in {simulation_time:.2f}s")
            if self.simulation_completed_callback:
                self.simulation_completed_callback()
        except Exception as e:
            logger.error(f"❌ Simulation failed: {e}")
            if self.simulation_error_callback:
                self.simulation_error_callback(str(e))    
    
    def save_results(self, filename_prefix: str = None):
        """Save simulation results to a single comprehensive file"""
        if filename_prefix is None:
            filename_prefix = "simulation_results"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Ensure results directory exists
        import os
        results_dir = "results"
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        results = self.results.copy()
        
        # Add simulation metadata
        results["metadata"] = {
            'save_date': datetime.now().isoformat(),
            'app_version': '1.0.0',
            'description': 'Social Innovation Diffusion Simulation Results',
            'simulation_time': results.get('simulation_time', 0),
            'total_agents': len(self.agents),
            'config_name': getattr(self.config, 'name', 'custom')
        }

        results_file = os.path.join(results_dir, f"{filename_prefix}_{timestamp}.pkl")
        
        try:
            with open(results_file, 'wb') as f:
                pickle.dump(results, f)
            logger.info(f"Complete simulation results saved to {results_file}")
            return results_file
            
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise
    
    @staticmethod
    def load_simulation(filepath: str) -> 'SocialDiffusionSimulation':
        """Load simulation results from file"""
        try:
            with open(filepath, 'rb') as f:
                results = pickle.load(f)
            logger.info(f"Simulation results loaded from {filepath}")
            simulation = SocialDiffusionSimulation(
                config=SimulationConfig.from_dict(results.get("config", {})),
            )
            simulation.results = results
            return simulation
        except Exception as e:
            logger.error(f"Failed to load results from {filepath}: {e}")
            raise
    
    @staticmethod
    def get_saved_simulations(results_dir: str = "results") -> List[str]:
        """Get list of saved simulation files"""
        import os
        if not os.path.exists(results_dir):
            return []
        
        saved_files = []
        for file in os.listdir(results_dir):
            if file.endswith('.pkl'):
                saved_files.append(file)
        
        return sorted(saved_files, reverse=True)  # Most recent first


# Simulation runner functions
def get_simulation_with_config(
        config: SimulationConfig,
        simulation_initialized_callback: Optional[Callable[[], None]] = None,
        simulation_step_started_callback: Optional[Callable[[int], None]] = None,
        simulation_step_completed_callback: Optional[Callable[[int], None]] = None,
        simulation_completed_callback: Optional[Callable[[], None]] = None,
        simulation_error_callback: Optional[Callable[[str], None]] = None
    ) -> SocialDiffusionSimulation:
    """
    Run simulation with specific configuration
    
    Args:
        config: Simulation configuration
        
    Returns:
        Dict with simulation results
    """
    sim = SocialDiffusionSimulation(
        config,
        simulation_initialized_callback=simulation_initialized_callback,
        simulation_step_started_callback=simulation_step_started_callback,
        simulation_step_completed_callback=simulation_step_completed_callback,
        simulation_completed_callback=simulation_completed_callback,
        simulation_error_callback=simulation_error_callback
    )

    return sim


def get_predefined_simulation(config_name: str = "default") -> SocialDiffusionSimulation:
    """
    Run simulation with predefined configuration
    
    Args:
        config_name: Name of predefined configuration
        
    Returns:
        Dict with simulation results
    """
    if config_name not in SIMULATION_CONFIGS:
        raise ValueError(f"Unknown configuration: {config_name}. "
                        f"Available: {list(SIMULATION_CONFIGS.keys())}")
    
    config = SIMULATION_CONFIGS[config_name]
    config.name = config_name  # Add name for file saving
    
    logger.info(f"Running predefined simulation: {config_name}")
    return get_simulation_with_config(config)
