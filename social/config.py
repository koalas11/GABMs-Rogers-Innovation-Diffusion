"""
Configuration and Constants for Social Innovation Diffusion Model
Based on Rogers' Diffusion of Innovation Theory
"""

from typing import Any, Dict
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Rogers' adopter categories with theoretical distributions
ADOPTER_CATEGORIES = [
    "Innovator",      # 2.5% - Risk-takers, well-connected
    "EarlyAdopter",   # 13.5% - Opinion leaders, respected  
    "EarlyMajority",  # 34% - Deliberate, follow early adopters
    "LateMajority",   # 34% - Skeptical, adopt due to social pressure
    "Laggard"         # 16% - Traditional, suspicious of change
]

# Default distribution based on Rogers (2003)
DEFAULT_ADOPTER_DISTRIBUTION = {
    "Innovator": 0.025,
    "EarlyAdopter": 0.135, 
    "EarlyMajority": 0.34,
    "LateMajority": 0.34,
    "Laggard": 0.16
}

# Rogers' 5 innovation attributes with default values
DEFAULT_INNOVATION_ATTRIBUTES = {
    "relative_advantage": 0.7,  # Perceived benefits vs current solution
    "compatibility": 0.6,       # Fit with existing values/practices
    "complexity": 0.4,          # Ease of understanding/use (0=very easy, 1=very difficult)
    "trialability": 0.8,        # Ability to experiment before adoption
    "observability": 0.5        # Visibility of results to others
}


class SimulationConfig:
    """
    Configuration class for simulation parameters
    """
    
    def __init__(
        self,
        name: str = None,
        # Agent population
        num_agents: int = 100,
        adopter_distribution: Dict[str, float] = None,
        
        # Innovation characteristics
        innovation_attributes: Dict[str, float] = None,

        # Network structure
        network_type: str = "small_world",  # "small_world", "scale_free", "random"
        network_params: Dict = None,
        network_seed: int = None,
        network_shuffle: bool = True,

        # Simulation parameters
        max_steps: int = 25,
        early_stop_threshold: float = 1.0,
        early_stop_no_adoption_steps: int = 2,
        enable_devils_advocate: bool = False,
        speed_up: bool = True
    ):
        self.name = name or "unnamed_simulation"
        self.num_agents = num_agents
        self.adopter_distribution = adopter_distribution or DEFAULT_ADOPTER_DISTRIBUTION.copy()
        self.innovation_attributes = innovation_attributes or DEFAULT_INNOVATION_ATTRIBUTES.copy()
        
        self.network_type = network_type
        self.network_params = network_params or self._get_default_network_params()
        self.network_seed = network_seed
        self.network_shuffle = network_shuffle

        self.max_steps = max_steps
        self.early_stop_threshold = early_stop_threshold
        self.early_stop_no_adoption_steps = early_stop_no_adoption_steps
        self.enable_devils_advocate = enable_devils_advocate
        self.speed_up = speed_up
        
        # Validate configuration
        self._validate_config()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "num_agents": self.num_agents,
            "adopter_distribution": self.adopter_distribution,
            "innovation_attributes": self.innovation_attributes,
            "network_type": self.network_type,
            "network_params": self.network_params,
            "network_seed": self.network_seed,
            "network_shuffle": self.network_shuffle,
            "max_steps": self.max_steps,
            "early_stop_threshold": self.early_stop_threshold,
            "early_stop_no_adoption_steps": self.early_stop_no_adoption_steps,
            "enable_devils_advocate": self.enable_devils_advocate,
            "speed_up": self.speed_up
        }
    
    @staticmethod
    def from_dict(config_dict: Dict[str, Any]) -> 'SimulationConfig':
        """Create SimulationConfig from dictionary"""
        return SimulationConfig(
            num_agents=config_dict.get("num_agents", 100),
            adopter_distribution=config_dict.get("adopter_distribution", DEFAULT_ADOPTER_DISTRIBUTION),
            innovation_attributes=config_dict.get("innovation_attributes", DEFAULT_INNOVATION_ATTRIBUTES),
            network_type=config_dict.get("network_type", "small_world"),
            network_params=config_dict.get("network_params", None),
            network_seed=config_dict.get("network_seed", None),
            network_shuffle=config_dict.get("network_shuffle", True),
            max_steps=config_dict.get("max_steps", 25),
            early_stop_threshold=config_dict.get("early_stop_threshold", 1),
            early_stop_no_adoption_steps=config_dict.get("early_stop_no_adoption_steps", 2),
            enable_devils_advocate=config_dict.get("enable_devils_advocate", False),
            speed_up=config_dict.get("speed_up", True)
        )

    def _get_default_network_params(self) -> Dict:
        """Get default network parameters by type"""
        defaults = {
            "small_world": {"k": 4, "rewiring_prob": 0.3},
            "scale_free": {"m": 2, "alpha": 2.5},
            "random": {"p": 0.1}
        }
        return defaults.get(self.network_type, defaults["small_world"])
    
    def _validate_config(self):
        """Validate configuration parameters"""
        # Validate adopter distribution
        total = sum(self.adopter_distribution.values())
        if abs(total - 1.0) > 0.01:
            raise ValueError(f"Adopter distribution must sum to 1.0, got {total}")

        
        # Validate innovation attributes are in [0,1]
        for attr, value in self.innovation_attributes.items():
            if not 0 <= value <= 1:
                raise ValueError(f"Innovation attribute {attr} must be in [0,1], got {value}")
        
        # Validate network parameters based on type
        self._validate_network_params()
        
        # Validate positive parameters
        if self.num_agents <= 0:
            raise ValueError(f"num_agents must be positive, got {self.num_agents}")
        if self.max_steps <= 0:
            raise ValueError(f"max_steps must be positive, got {self.max_steps}")
        if not 0 <= self.early_stop_threshold <= 1:
            raise ValueError(f"early_stop_threshold must be in [0,1], got {self.early_stop_threshold}")
    
    def _validate_network_params(self):
        """Validate network-specific parameters"""
        params = self.network_params
        
        if self.network_type == "small_world":
            k = params.get("k", 4)
            rewiring_prob = params.get("rewiring_prob", 0.3)
            if k < 1 or k >= self.num_agents:
                raise ValueError(f"Small-world k must be between 1 and {self.num_agents-1}, got {k}")
            if not 0 <= rewiring_prob <= 1:
                raise ValueError(f"Small-world rewiring_prob must be in [0,1], got {rewiring_prob}")
                
        elif self.network_type == "scale_free":
            m = params.get("m", 2)
            alpha = params.get("alpha", 2.5)
            if m < 1 or m >= self.num_agents:
                raise ValueError(f"Scale-free m must be between 1 and {self.num_agents-1}, got {m}")
            if alpha <= 1:
                raise ValueError(f"Scale-free alpha must be > 1, got {alpha}")
                
        elif self.network_type == "random":
            p = params.get("p", 0.1)
            if not 0 <= p <= 1:
                raise ValueError(f"Random network p must be in [0,1], got {p}")
        
        # Validate positive parameters
        if self.num_agents <= 0:
            raise ValueError("Number of agents must be positive")
        if self.max_steps <= 0:
            raise ValueError("Max steps must be positive")
    
    def get_agents_per_category(self) -> Dict[str, int]:
        """Calculate number of agents per category based strictly on distribution"""
        agents_per_category = {}
        total_assigned = 0
        categories = list(self.adopter_distribution.keys())
        # Assign agents by rounding down, last category gets the remainder
        for i, (category, proportion) in enumerate(self.adopter_distribution.items()):
            if i == len(categories) - 1:
                count = self.num_agents - total_assigned
            else:
                count = int(round(self.num_agents * proportion))
                total_assigned += count
            agents_per_category[category] = count
        return agents_per_category

# Predefined simulation configurations
SIMULATION_CONFIGS = {
    "default": SimulationConfig(name="default"),

    "successful": SimulationConfig(
        name="successful",
        innovation_attributes={
            "relative_advantage": 0.7,
            "compatibility": 0.6, 
            "complexity": 0.4,
            "trialability": 0.8,
            "observability": 0.5
        },
        network_seed=314,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=True
    ),

    "all_balanced_no_dap": SimulationConfig(
        name="all_balanced_no_dap",
        innovation_attributes={
            "relative_advantage": 0.5,
            "compatibility": 0.5, 
            "complexity": 0.5,
            "trialability": 0.5,
            "observability": 0.5
        },
        network_seed=314,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=False
    ),

    "successful_no_dap": SimulationConfig(
        name="successful_no_dap",
        innovation_attributes={
            "relative_advantage": 0.7,
            "compatibility": 0.6, 
            "complexity": 0.4,
            "trialability": 0.8,
            "observability": 0.5
        },
        network_seed=314,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=False
    ),

    "unsuccessful_no_dap": SimulationConfig(
        name="unsuccessful_no_dap",
        innovation_attributes={
            "relative_advantage": 0.1,
            "compatibility": 0.1,
            "complexity": 0.9,
            "trialability": 0.1,
            "observability": 0.1
        },
        network_seed=314,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=False,
        early_stop_no_adoption_steps=2
    ),

    "bad_innovation_innovators_only": SimulationConfig(
        name="bad_innovation_innovators_only",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 1.0,
            "EarlyAdopter": 0.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.2,
            "compatibility": 0.1,
            "complexity": 0.9,
            "trialability": 0.1,
            "observability": 0.2
        },
        network_seed=41,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=True
    ),

    "decent_innovation_innovators_only": SimulationConfig(
        name="decent_innovation_innovators_only",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 1.0,
            "EarlyAdopter": 0.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.6,
            "compatibility": 0.5,
            "complexity": 0.4,
            "trialability": 0.5,
            "observability": 0.5
        },
        network_seed=41,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=True
    ),

    "early_adopters_devils_prompt_on": SimulationConfig(
        name="early_adopters_devils_prompt_on",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 0.0,
            "EarlyAdopter": 1.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.7,
            "compatibility": 0.6, 
            "complexity": 0.4,
            "trialability": 0.8,
            "observability": 0.5
        },
        network_seed=41,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=True
    ),

    "early_adopters_devils_prompt_off": SimulationConfig(
        name="early_adopters_devils_prompt_off",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 0.0,
            "EarlyAdopter": 1.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.7,
            "compatibility": 0.6, 
            "complexity": 0.4,
            "trialability": 0.8,
            "observability": 0.5
        },
        network_seed=41,
        network_shuffle=True,
        enable_devils_advocate=False,
        speed_up=False
    ),

    "early_adopters_bad_innovation_devils_prompt_on": SimulationConfig(
        name="early_adopters_bad_innovation_devils_prompt_on",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 0.0,
            "EarlyAdopter": 1.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.2,
            "compatibility": 0.1,
            "complexity": 0.7,
            "trialability": 0.3,
            "observability": 0.2
        },
        network_seed=41,
        network_shuffle=True,
        speed_up=False,
        enable_devils_advocate=True
    ),

    "early_adopters_bad_innovation_devils_prompt_off": SimulationConfig(
        name="early_adopters_bad_innovation_devils_prompt_off",
        num_agents=20,
        max_steps=1,
        adopter_distribution={
            "Innovator": 0.0,
            "EarlyAdopter": 1.0,
            "EarlyMajority": 0.0,
            "LateMajority": 0.0,
            "Laggard": 0.0
        },
        innovation_attributes={
            "relative_advantage": 0.2,
            "compatibility": 0.1,
            "complexity": 0.7,
            "trialability": 0.3,
            "observability": 0.2
        },
        network_seed=41,
        network_shuffle=True,
        enable_devils_advocate=False,
        speed_up=False
    ),
}
