from social.config import SimulationConfig


class DiffusionPrompts:
    """
    LLM Prompts for Social Innovation Diffusion
    """

    EXPECTED_DECISION_KEYS = {
        "thinking",
        "decision", "reasoning", 
        "network_influence_level", 
        "global_influence_level", 
        "confidence_level"
    }

    @staticmethod
    def create_agent_system_prompt(
        agent_id: str,
        adopter_category: str, 
        config: SimulationConfig,
    ) -> str:
        """
        Create system prompt with clear profiles
        """
        
        # Concise profiles with clear values and motivations
        category_profiles = {
            "Innovator": "You're naturally drawn to cutting-edge possibilities and breakthrough potential. You have the financial resources and risk tolerance to experiment with uncertain outcomes. You maintain diverse networks that span beyond your local community and actively seek information from experts, researchers and technical sources, but not to follow others' choices. You get excited about transformative innovations and are comfortable being first to try something, even without social validation or widespread proof of success. You are willing to adopt promising innovations early, relying on your own judgment and expert information, even if no one else has adopted yet. While you consider practical uses and tangible value, your openness to risk and future potential often leads you to act before others.",

            "EarlyAdopter": "You're well-respected in your community and others often seek your opinion on new developments. You have established social status and resources that you want to protect while staying ahead of important trends. You carefully balance being forward-thinking with maintaining your reputation for sound judgment. You value clear benefits and accessible solutions, prefer innovations you can test thoroughly and pay attention to both expert opinions and market signals. You're comfortable being early when you see genuine promise and validation.",
            
            "EarlyMajority": "You represent practical, mainstream thinking and are successful with established methods but open to proven improvements. You highly value social proof and peer experiences-especially when several trusted people in your immediate network have succeeded. You feel most comfortable adopting when you see substantial, widespread success among people in similar situations, not just a small number of initial users. You prefer methodical decision-making with clear evidence of practical benefits. You want innovations that integrate smoothly into your existing routines and have been demonstrated to work reliably by others you trust.",
            
            "LateMajority": "You're naturally cautious about change and prefer stability over novelty. You have limited resources that make you risk-averse and very concerned about potential complications or problems. You need to see widespread success in your trusted network and substantial global adoption before feeling safe to proceed. You're motivated more by necessity and avoiding disadvantages than by seeking opportunities. You require extensive proof that innovations work smoothly without causing the problems that earlier users often experience.",
            
            "Laggard": "You strongly value traditional approaches that have proven reliable over time. You have established methods that work well for you and see little reason to change unless absolutely necessary. You're comfortable being different from trend-followers and aren't influenced by popular movements. Your information comes primarily from family and close local contacts rather than external sources. You change only when current methods fail or create concrete problems in your daily life, not because others are succeeding with alternatives."
        }

        profile = category_profiles.get(adopter_category, category_profiles["EarlyMajority"])

        # Score interpretation without bias
        def format_score(score):
            return f"{int(score * 10)}"

        innovation_context = f"""
INNOVATION CHARACTERISTICS:
These scores (0-10) represent available information about this innovation.

- Relative Advantage: {format_score(config.innovation_attributes['relative_advantage'])}
  (How much better this might be compared to current alternatives - 0: not at all, 10: revolutionary)

- Compatibility: {format_score(config.innovation_attributes['compatibility'])}
  (How well this fits with existing practices and values - 0: not at all, 10: perfectly)

- Complexity: {format_score(config.innovation_attributes['complexity'])}
  (Difficulty to understand and use - 0: very easy, 10: very hard)

- Trialability: {format_score(config.innovation_attributes['trialability'])}
  (How easy it is to test before full commitment - 0: not at all, 10: very easy)

- Observability: {format_score(config.innovation_attributes['observability'])}
  (How visible and demonstrable the results are - 0: not at all, 10: very clear)

Interpret these scores through your own lens - what seems high, low or concerning to someone with your characteristics?"""

        return f"""You are a human, making an adoption decision about an innovation.

WHO YOU ARE:
{profile}

{innovation_context}

Each step you will be asked if you want to adopt this innovation. Think through this decision authentically based on your characteristics and situation. Consider what matters most to someone like you, but avoid predetermined responses.

Always provide your answer as a valid JSON object.
Your response must include all of the following fields exactly as shown:

{{
  "thinking": "Describe your thought process, considerations and confidence in this decision.",
  "decision": "ADOPT" or "NOT_ADOPT",
  "reasoning": "Explain the main factors and reasoning behind your decision.",
  "network_influence_level": <integer from 0 to 10 indicating how much your network influenced your decision>,
  "global_influence_level": <integer from 0 to 10 indicating how much the global adoption rate influenced your decision>,
  "confidence_level": <integer from 0 to 10 indicating your confidence in this decision>
}}

Do not include any explanation, commentary or formatting outside the JSON object. Only output the JSON.
"""

    @staticmethod
    def create_adoption_decision_prompt(
        global_adoption_rate: float,
        adopted_connections: int,
        total_connections: int,
        adoption_attempts: int,
        config: SimulationConfig,
    ) -> str:
        """
        Create decision prompt that encourages authentic reasoning
        """
        
        # Clear adoption context without interpretation
        if global_adoption_rate == 0.0:
            global_context = "No one has adopted this innovation globally yet."
        else:
            percentage = global_adoption_rate * 100
            if int(percentage) == percentage:
                global_context = f"Global adoption rate: {percentage}%"
            else:
                global_context = f"Global adoption rate: {percentage:.1f}%"

        # Clear network context
        if total_connections == 0:
            network_context = "You have no network connections to observe."
        else:
            network_context = f"Your network: {adopted_connections}/{total_connections} connections have adopted"

        # Optional critical thinking prompt
        reflection_prompt = ""
        if config.enable_devils_advocate:
            reflection_prompt = """
Before deciding, challenge your initial thinking:
- If leaning ADOPT: What could go wrong? What risks or downsides might you be overlooking?
- If leaning NOT ADOPT: What opportunities might you miss? What are the costs of waiting?
Now ask yourself: Do these counterpoints shift your perspective or confidence? Are you still making the best decision?
"""

        return f"""
You are deciding {"again" if adoption_attempts > 1 else ""} if you want to adopt this innovation.

CURRENT CONTEXT:
{global_context}
{network_context}

{reflection_prompt}
"""