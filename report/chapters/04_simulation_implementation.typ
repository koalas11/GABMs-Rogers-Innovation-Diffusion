= Generative Agent-Based Modeling of Innovation Diffusion: Implementation and Methodology

This chapter presents the methodology used to integrate Rogers' diffusion of innovations theory with generative agent-based modeling, leveraging large language models (LLMs) to create more realistic simulations of innovation adoption decisions, with focus on the role of social networks and social pressure.

== Simplification of Rogers' Theory

To effectively simulate the diffusion of innovations, certain simplifications of Rogers' theory were necessary. The focus was primarily on the decision-making stage, with less emphasis on the pre-adoption and post-adoption phases. This approach allowed for a more manageable implementation while still capturing the essential dynamics of innovation adoption.

== Core Architecture

The simulation operates through discrete time steps, with non-adopter agents evaluating adoption decisions at each iteration. Once an agent adopts the innovation, it is no longer prompted further and becomes inactive in subsequent rounds, while the remaining agents continue to get prompted in the subsequent steps. The simulation stops either when all agents have adopted the innovation or when a predefined number of consecutive steps occur with no new adoptions, indicating that further diffusion is unlikely. Unlike traditional models where decisions emerge from threshold comparisons, the agents generate responses through prompting of large language models using the AutoGen framework. This approach enables the emergence of complex, context-dependent reasoning that better reflects the cognitive processes underlying real-world adoption decisions.

The methodological approach directly implements Rogers' four key elements of diffusion: 

- *Innovation characteristics* through structured attribute scoring
- *Communication channels* not directly implemented, as agents do not communicate with each other, partially implemented through agents observing adoption status in their network connections
- *Time dimension* through discrete simulation steps and temporal context provided by the LLM prompts
- *Social system effects* through agent behavioral profiles, network topology and global adoption information that all agents can observe

This integration addresses Rogers' emphasis on the complexity of the decision phase, where individuals transition from attitude formation to behavioral commitment through recursive evaluation, multi-criteria analysis and bounded rationality considerations.

A critical aspect is proper state management: before each simulation step, the state must be frozen to prevent agents from accessing network adoption information that reflects the current step, as it would bias their decision-making.

=== Core Decision-Making Process

The centerpiece of the methodology is the implementation of LLM-powered decision-making that transforms abstract agent profiles into concrete adoption choices. Each agent is implemented as an `AssistantAgent` from the AutoGen Chat library, receiving carefully constructed prompts combining their behavioral profile with current environmental information, enabling dynamic, context-sensitive responses aligned with Rogers' theory.

== Agent-Based Decision Making Architecture

=== Prompt Engineering and LLM Integration

==== Dual-Prompt Architecture

A central innovation of the simulation is the use of carefully engineered prompts implemented in the `DiffusionPrompts` class to guide agent decision-making via large language models. The prompt engineering process represents iterative development and testing to ensure theoretical alignment and behavioral consistency. Each agent receives two types of prompts:

*System Prompt*: Establishes the LLM's role and simulation context through the `create_agent_system_prompt()` method, ensuring consistent and theoretically grounded responses across all decision-making instances.

*Decision Prompt*: Dynamically constructed for each agent at every time step via `create_adoption_decision_prompt()`, combining the agent's behavioral profile, current adoption rates, innovation attributes and temporal context.

==== System Prompt Architecture

The system prompt is composed of three essential components that work together to establish the agent's decision-making context:

===== Agent Identity Component
The first component establishes the agent's role and identity:
```
You are a human, making an adoption decision about an innovation.

WHO YOU ARE:
{profile}

{innovation_context}

Each step you will be asked if you want to adopt this innovation. Think through this decision authentically based on your characteristics and situation. Consider what matters most to someone like you, but avoid predetermined responses.
```

This section grounds the agent in their specific adopter category by injecting the behavioral profile that defines their decision-making characteristics, risk tolerance and social influences.

===== Innovation Context Component
The second component provides structured information about the innovation being evaluated:
```
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

Interpret these scores through your own lens - what seems high, low or concerning to someone with your characteristics?
```

The system represent Rogers' five perceived attributes using a 0-10 scale for conditioning the prompts. This discrete scale was chosen because it allows agents to naturally interpret and integrate the innovation attributes into their reasoning processes. Through iterative testing, I found that the models interpret intuitive, discrete scales more reliably than continuous probability distributions, resulting in more consistent and meaningful agent responses.

While Rogers' theory describes these attributes as natural language constructs, I decided to use a numerical approach to avoid biases in describing the attributes and to facilitate more precise comparisons and evaluations.

===== Output Format Component
The final component ensures structured, analyzable responses:
```
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
```

This structured output enables quantitative analysis of decision factors while capturing the qualitative reasoning process underlying each adoption decision.

=== Agent Behavioral Profiles and Category Implementation

Each agent is characterized by detailed behavioral profiles that encapsulate decision-making tendencies, risk tolerance, information processing patterns and social influence sensitivity associated with their adopter category. These profiles synthesize Rogers' theoretical descriptions with practical considerations for LLM interpretation and response generation.

A key characteristic of the prompt design is that it avoids explicitly telling agents which adopter category they belong to. Instead, agents receive behavioral descriptions that naturally guide their decision-making without creating artificial constraints or biases that might arise from category labels.

The following profiles represent operationalizations of Rogers' adopter categories, rewritten as prompt personas:

==== Innovator Profile
```
You're naturally drawn to cutting-edge possibilities and breakthrough potential. You have the financial resources and risk tolerance to experiment with uncertain outcomes. You maintain diverse networks that span beyond your local community and actively seek information from experts, researchers and technical sources, but not to follow others' choices. You get excited about transformative innovations and are comfortable being first to try something, even without social validation or widespread proof of success. You are willing to adopt promising innovations early, relying on your own judgment and expert information, even if no one else has adopted yet. While you consider practical uses and tangible value, your openness to risk and future potential often leads you to act before others.
```

==== Early Adopter Profile  
```
You're well-respected in your community and others often seek your opinion on new developments. You have established social status and resources that you want to protect while staying ahead of important trends. You carefully balance being forward-thinking with maintaining your reputation for sound judgment. You value clear benefits and accessible solutions, prefer innovations you can test thoroughly and pay attention to both expert opinions and market signals. You're comfortable being early when you see genuine promise and validation.
```

==== Early Majority Profile
```
You represent practical, mainstream thinking and are successful with established methods but open to proven improvements. You highly value social proof and peer experiences-especially when several trusted people in your immediate network have succeeded. You feel most comfortable adopting when you see substantial, widespread success among people in similar situations, not just a small number of initial users. You prefer methodical decision-making with clear evidence of practical benefits. You want innovations that integrate smoothly into your existing routines and have been demonstrated to work reliably by others you trust.
```

==== Late Majority Profile
```
You're naturally cautious about change and prefer stability over novelty. You have limited resources that make you risk-averse and very concerned about potential complications or problems. You need to see widespread success in your trusted network and substantial global adoption before feeling safe to proceed. You're motivated more by necessity and avoiding disadvantages than by seeking opportunities. You require extensive proof that innovations work smoothly without causing the problems that earlier users often experience.
```

==== Laggard Profile
```
You strongly value traditional approaches that have proven reliable over time. You have established methods that work well for you and see little reason to change unless absolutely necessary. You're comfortable being different from trend-followers and aren't influenced by popular movements. Your information comes primarily from family and close local contacts rather than external sources. You change only when current methods fail or create concrete problems in your daily life, not because others are succeeding with alternatives.
```

==== Decision Prompt Construction

The decision prompt dynamically integrates current environmental information with a critical reflection component designed to enhance decision quality and realism:

```
You are deciding {"again" if adoption_attempts > 1 else ""} if you want to adopt this innovation.

CURRENT CONTEXT:
{global_context}
{network_context}

{reflection_prompt}
```

The context information is carefully formatted to avoid interpretation bias. The global and network contexts are generated as follows:

```python
if global_adoption_rate == 0.0:
    global_context = "No one has adopted this innovation globally yet."
else:
    percentage = global_adoption_rate * 100
    if int(percentage) == percentage:
        global_context = f"Global adoption rate: {percentage}%"
    else:
        global_context = f"Global adoption rate: {percentage:.1f}%"

if total_connections == 0:
    network_context = "You have no network connections to observe."
else:
    network_context = f"Your network: {adopted_connections}/{total_connections} connections have adopted"
```

A critical design decision was to round percentages like 4.0% to 4%, as agents sometimes confused "4.0%" with "40%", leading to significant decision-making errors. This formatting ensures agents correctly interpret adoption rates without introducing computational artifacts.

This approach addresses Rogers' emphasis on the complex, recursive nature of the decision phase by providing neutral, quantitative information that allows agents to interpret data through their own behavioral lens while maintaining consistency. The prompt design deliberately avoids specifying fixed constraints or biasing language that might override the natural decision-making tendencies encoded in the behavioral profiles.

The reflection component implements the "Devil's Advocate" approach, which addresses Rogers' recognition that decision-making involves bounded rationality and emotional influences:

This approach is based on a paper where researchers found that self-reflection in AI Agents before a task improved their performance @wang2024devilsadvocateanticipatoryreflection.

```
Before deciding, challenge your initial thinking:
- If leaning ADOPT: What could go wrong? What risks or downsides might you be overlooking?
- If leaning NOT ADOPT: What opportunities might you miss? What are the costs of waiting?
Now ask yourself: Do these counterpoints shift your perspective or confidence? Are you still making the best decision?
```

While research has shown that self-reflection can lead to degeneration of thought in some contexts as explained in @self_reflection_degenerative, I incorporated and tested these ideas within the simulation environment to evaluate their effects on decision-making quality, making it optional to use.

=== Prompts Characteristics

A fundamental aspect of the prompt design in this simulation is the deliberate avoidance of any explicit mention of Rogers' adopter categories. Nowhere in the prompts is the agent told which class it belongs to (for example, "you are an innovator" or "you are a laggard"). Instead, each agent receives a detailed behavioral description that synthesizes psychological traits, risk attitudes, information sources and sensitivity to social influence typical of its category.

This design choice serves two main purposes: first, it prevents the language model from simply reproducing stereotypes associated with explicit labels ("innovator", "early adopter", etc.); second, it encourages the emergence of more natural and theory-consistent behaviors, allowing the differences in behavioral profiles to guide the decision process. As a result, agent responses reflect a variety of reasoning patterns and sensitivities, without being constrained by rigid instructions or biases induced by explicit labels.

== NetworkX - Network Implementation

The simulation employs the NetworkX library to generate realistic social network structures using the Watts-Strogatz model for small-world networks @NetworkX. The small-world network parameters include the number of nodes, the number of nearest neighbors each node connects to (typically 4-6) and the rewiring probability (typically 0.1-0.3) that controls the balance between local clustering and long-range connections.

The simulation environment also supports scale-free networks (using the Barabási-Albert model) and random networks (using the Erdős-Rényi model) for comparative analysis, as detailed in previous chapters. The implementation includes:

*Configurable Parameters*: The rewiring probability parameter allows adjustment of the balance between local clustering and long-range connections, enabling exploration of how different degrees of "small-worldness" affect diffusion outcomes.

*Agent Distribution Controls*: Agent shuffling capabilities prevent systematic biases that might arise from deterministic agent-to-node assignments based on adopter categories. This ensures that network position effects are independent of adopter category characteristics.

*Reproducible Generation*: Configurable random seeds enable identical network structures and agents shuffling across multiple simulation runs, facilitating controlled experimentation and result validation.

=== LLM Response Processing and Validation

A crucial problem in the development of the simulation was ensuring that LLM responses were correctly formatted and contained all required fields. The following sections detail the robust mechanisms implemented to handle this challenge.

==== JSON Extraction and Parsing
The response processing begins with JSON extraction, handling various formatting inconsistencies that may emerge from LLM outputs:

- Removal of extraneous whitespace and newlines
- Correction of common formatting issues (e.g., misplaced commas, brackets)
- Ensuring proper JSON structure (e.g., matching braces)
- Ensuring all required fields are present

==== Retry Mechanism with Context Cleanup
A big challenge was handling LLM failures while maintaining conversation context integrity:

```python
for attempt in range(max_retries + 1):
    try:
        result = await agent.decide_adoption(step, last_attempt=(attempt == max_retries))
        return result
    except ReasoningError as e:
        if agent.model_context._messages:
            agent.model_context._messages.pop()  # Clean up decision prompt message
            agent.model_context._messages.pop()  # Clean up failed message
        if attempt == max_retries:
            break
raise last_exception # Raise the last encountered exception
```

To achieve this, I implemented a retry mechanism that allows the system to reattempt LLM calls while preserving the context of the conversation, removing failed messages from the context.

== Technology Stack and LLM Choice

Due to hardware limitations, I use Ollama, a software that allows running LLMs locally, avoiding the costs of cloud-based solutions. The simulation uses the `llama3.1 8B` model, which is a smaller model compared to the latest ones but still capable of generating coherent and contextually relevant responses for the simulation's needs and it's multilingual and can handle large contexts @grattafiori2024llama3herdmodels.

Using the AutoGen framework extensions, I integrated the Ollama model easily through its flexible model interface, enabling seamless local LLM deployment without requiring cloud API access. This integration allows the simulation to maintain consistent performance while operating entirely offline.

Before `llama3.1 8B`, I explored `Mistral`, another local LLM option, but ultimately chose `llama3.1 8B` for its ease of use and integration capabilities, as `Mistral` was more likely to go out of role and produce less reliable outputs.

== Configuration Management and Simulation Control

=== Comprehensive Configuration System

The simulation environment is highly configurable through the `SimulationConfig` class, which manages all aspects of the simulation including:

- *Population parameters*: Number of agents and adopter category distributions which defaults on Rogers' empirical proportions (2.5% Innovators, 13.5% Early Adopters, 34% Early Majority, 34% Late Majority, 16% Laggards)
- *Innovation characteristics*: All five Rogers attributes scored on a 0-10 scale
- *Network topology*: Type, parameters and structural properties
- *Simulation controls*: Step limits, early stopping conditions and performance optimizations
- *Prompt engineering*: Devil's advocate reflection toggle

=== Predefined Configuration Scenarios

The system includes several predefined configurations designed for specific research scenarios aligned with diffusion theory:

- *"successful"*: Innovations with strong relative advantage and high trialability, expected to achieve rapid diffusion
- *"unsuccessful"*: Innovations with poor compatibility and high complexity, expected to face adoption barriers
- *"balanced"*: Neutral innovations with moderate characteristics across all dimensions
- *Category-specific scenarios*: Configurations isolating individual adopter categories for behavioral analysis

These predefined scenarios enable researchers to quickly conduct targeted experiments while maintaining the ability to create custom configurations for specialized research questions.

=== Streamlit Application Interface

A comprehensive Streamlit application provides an intuitive web-based interface for running simulations and analyzing results. The application features:

- *Interactive configuration*: Sliders and controls for all simulation parameters
- *Real-time monitoring*: Live updates of adoption progress and agent decisions
- *Comprehensive visualization*: Network diagrams, adoption curves and decision analysis

== Agent Response Capture and Data Collection

=== Comprehensive Decision Recording

The system captures rich data about agent decision-making processes, going beyond simple adoption/rejection outcomes to record:

- *Reasoning patterns*: Full natural language explanations of decision logic
- *Influence metrics*: Quantified levels of network and global adoption influence
- *Confidence assessments*: Agent self-reported confidence in their decisions
- *Temporal dynamics*: How reasoning evolves across multiple decision points
- *Category-specific patterns*: Behavioral differences across adopter types

This comprehensive data collection enables detailed analysis of how different factors influence adoption decisions and how these patterns vary across Rogers' adopter categories, supporting the theory's emphasis on heterogeneous decision-making approaches.

== Problems during the developments

Several challenges emerged throughout the development process, some of which have been discussed in previous sections. For example, the implementation of a robust retry mechanism was necessary to handle LLM failures and prevent simulation interruptions, as detailed earlier. Additionally, issues arose from the LLM's inconsistent interpretation of floating point numbers, such as confusing "4.0%" with "40%", which required careful prompt formatting and rounding strategies to ensure reliable agent decision-making.

Another significant challenge was the risk of prompt-induced biases. Since LLMs are sensitive to subtle wording and context, even minor changes in prompt phrasing could lead to systematic shifts in agent behavior, undermining the theoretical validity of the simulation. To address this, I iteratively refined the prompt engineering process, focusing on neutral, quantitative language and avoiding leading or suggestive statements. Behavioral profiles were carefully rewritten to reflect Rogers' categories without explicitly labeling them, reducing the risk of agents simply mimicking category stereotypes. Furthermore, I tested multiple prompt variants and analyzed agent outputs to identify and minimize any persistent biases, ensuring that decision-making patterns emerged organically from the agents' profiles and environmental context rather than from prompt artifacts.

A further limitation encountered was the simulation runtime, which was significantly affected by hardware constraints. Since the system was limited to a single GPU, the overall speed of agent decision-making and simulation progression was much slower than would be possible with parallelized or multi-GPU setups, taking around 4 hours. This required management of simulation parameters to keep runtimes reasonable and limited the scale of experiments that could be conducted efficiently.

== Validation

Since Rogers' theory represents a complex socio-psychological framework, the validation leverages the rich reasoning data captured in agent JSON outputs to examine *how* agents make decisions rather than just *what* they decide.

=== Process-Based Validation Through Agent Reasoning

Unlike traditional agent-based models that only produce binary adoption decisions, the GABM captures detailed reasoning through the structured output shown before.

By analyzing these reasoning patterns alongside adoption timing, I can validate whether agents exhibit theoretically consistent behavior.

=== Validation Framework

*Category Behavior Validation*: Verify each adopter category demonstrates reasoning consistent with Rogers' descriptions - Innovators focusing on breakthrough potential regardless of social proof, Early Majority emphasizing peer experiences and widespread validation, Laggards prioritizing traditional approaches.

*Innovation Attribute Sensitivity*: Analyze how different categories respond to the five innovation characteristics, expecting theoretically consistent patterns (e.g., Laggards showing greater complexity concerns than Innovators).

*Temporal Reasoning Consistency*: Correlate reasoning content with adoption timing to validate that early adopters cite appropriate motivations while later adopters reference increasing social pressure.

*Reasoning-Decision Alignment*: Validate that agents' stated reasoning logically supports their adoption decisions, identifying contradictions between reasoning and final choices.
