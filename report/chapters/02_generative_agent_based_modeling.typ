= Generative Agent-Based Modeling (GABM): From Task Automation to Simulation

Building on orchestration frameworks like AutoGen for multi-agent collaboration, GABM integrates LLM-driven cognition, memory and social interaction to study emergent behavior.

== Evolution from Traditional AI Agents to Generative Models

After the introduction of AI agents powered by large language models (LLMs), the landscape of artificial intelligence began to shift dramatically. These advanced models enabled agents to not only understand and generate human-like text but also to engage in more complex forms of reasoning and interaction. This evolution marked a departure from the earlier, more rigid frameworks of traditional AI agents, moving toward more flexible and adaptive systems capable of emergent behavior.

== The Emergence of Generative Agent-Based Models

Generative Agent-Based Modeling (GABM) represents a revolutionary approach that integrates large language models (LLMs) with traditional agent-based modeling methodologies. This fusion creates agents capable of exhibiting human-like reasoning, creativity and social behavior, fundamentally transforming how complex social systems and human interactions are simulated @park2023generativeagentsinteractivesimulacra.

== Technical Architecture of GABM

=== Large Language Model Integration
GABM agents utilize pre-trained language models (GPT-4, Claude, LLaMA) to enable generative agents that may be able to reason appropriately from premises to conclusions much of the time and can approximate intention modeling in some contexts @park2023generativeagentsinteractivesimulacra. These agents also possess substantial cultural knowledge and can be prompted to role-play effectively. The integration enables agents to:

- *Generate contextually appropriate responses* to novel situations beyond their training data
- *Maintain coherent personality traits* across extended interactions and time periods
- *Simulate theory of mind* by modeling other agents' mental states and intentions
- *Adapt communication styles* based on social context, relationships and cultural norms
- *Demonstrate emergent behaviors* that arise from the interaction of multiple agents

=== Memory and Reflection Systems
Advanced GABM implementations incorporate sophisticated memory architectures that mirror human cognitive processes:

- *Episodic Memory*: Storing and retrieving specific interaction experiences with temporal and contextual tags
- *Semantic Memory*: Maintaining general knowledge and learned patterns about the world and other agents
- *Reflection Mechanisms*: Periodic self-evaluation and behavior adjustment based on past experiences
- *Importance Weighting*: Prioritizing memories based on relevance, emotional significance and recency
- *Memory Consolidation*: Converting short-term experiences into long-term behavioral patterns

=== Behavioral Architecture
GABM agents implement complex behavioral models that include:

- *Goal-Directed Behavior*: Pursuing both short-term objectives and long-term aspirations
- *Social Cognition*: Understanding social hierarchies, relationships and cultural contexts
- *Emotional Processing*: Generating and responding to emotional states and social dynamics
- *Personality Consistency*: Maintaining stable personality traits while allowing for growth and change
- *Adaptive Learning*: Modifying behavior based on social feedback and environmental changes

== The Concordia Framework for Advanced GABM

Google DeepMind's Concordia framework represents one of the recent approaches to generative agent-based modeling, providing a comprehensive library for creating, configuring and studying generative agents in grounded physical, social or digital environments @vezhnevets2023generativeagentbasedmodelingactions. Concordia enables researchers and developers to build agents that can participate in complex social simulations with unprecedented realism and sophistication.

While this framework could have been used for the current project, because it is still under active development and not yet fully mature, I opted for a more established solution.

=== Concordia Architecture and Capabilities

Concordia implements a modular architecture that supports various types of generative agents and environmental simulations. The framework provides tools for creating agents that can interact in simulated physical spaces, social contexts or digital platforms with sophisticated multi-modal perception capabilities.

Key architectural components include:
- *Grounded Environments*: Agents can interact in simulated physical spaces, social contexts or digital platforms
- *Multi-Modal Perception*: Agents process visual, textual and social information from their environment
- *Social Interaction Engine*: Sophisticated systems for modeling conversations, relationships and group dynamics
- *Cultural Context Modeling*: Agents understand and express cultural norms, values and behaviors
- *Temporal Consistency*: Agents maintain consistent behavior and memory across extended time periods

=== Agent Configuration and Customization
The Concordia framework provides extensive customization options for creating diverse agent populations:

- *Personality Modeling*: Detailed personality profiles based on psychological frameworks
- *Cultural Background*: Agents with specific cultural identities, languages and worldviews
- *Skill and Knowledge Domains*: Specialized expertise areas and professional backgrounds
- *Social Roles and Relationships*: Family structures, professional hierarchies and community positions
- *Individual Histories*: Personal backstories that influence behavior and decision-making

== Complex Networks and Social Dynamics in GABM

Recent research has demonstrated how GABMs can model complex network formation and social dynamics. An example is the paper that explored the self-organization of generative agents in forming complex network structures, where nodes represented generative agents whose behavior was controlled by GPT-3.5-turbo. The agents were initialized using specific prompts, simulating the growth of an online social network. @demarzo2023emergencescalefreenetworkssocial

The LLM created a network with a hub-and-spoke structure that does not resemble the classical results obtained from preferential attachment algorithms. Interestingly, the researchers found that this was a consequence of a bias in the selection of nodes by the LLM that depended on their name. This study highlights both the potential and limitations of these models, demonstrating the importance of careful experimental design and bias mitigation.

Similarly, in another paper, 10 artificial agents based on the LLM Claude-2.1 were deployed and allowed to freely interact without specific priors. The agents showed a tendency to interact repeatedly with the same peers rather than exploring new connections and an analysis of their conversations indicated homophily, a common characteristic of human social networks. @lai2024evolvingaicollectivesenhance

== GABM Applications in Game Theory and Strategic Interaction

One of the most compelling applications of GABM has been in the study of game theory and strategic interaction, where LLM-driven agents can mimic intricate internal features of human cognition. Researchers have successfully deployed GABMs in various classic game theory scenarios, revealing both similarities and differences with human behavior patterns @lu2024generativeagentbasedmodelscomplex.

=== Game Theory Experiments with LLMs

LLM-driven agents have been extensively tested in various economic games, including the Dictator Game, Ultimatum Game, Prisoner's Dilemma and Public Goods Games. These experiments illustrate the feasibility of simulating individuals with a wide range of characteristics and traits, unlike traditional rule-based agents.

In the Ultimatum Game, LLMs demonstrated behavior that closely aligned with human decision trends, but also revealed biases related to gender and social roles. For instance, agents with male identifiers were more likely to accept unfair offers from agents with female identifiers, while female agents were less inclined to accept unfair offers from male agents @aher2023usinglargelanguagemodels.

The Prisoner's Dilemma experiments showed that LLMs exhibited cooperation rates of 65.4% on average, significantly higher than the 37% found in meta-analyses of human participants. This suggests that LLMs may have different risk and cooperation preferences compared to humans, potentially reflecting their training on cooperative and helpful interactions @lu2024generativeagentbasedmodelscomplex.

=== Strategic Behavior and Adaptation

Research has shown that this type of modeling can be conditioned to follow certain strategic behaviors, modifying their cooperative profiles based on specific prompts. However, this conditioning revealed the complexity of prompting these models, as some initial hypotheses had to be discarded. For instance, prompting for "selfish behavior" sometimes led to more cooperation than competitive scenarios, indicating the nuanced relationship between prompt design and behavioral outcomes. @lu2024generativeagentbasedmodelscomplex

== Epidemic Modeling and Public Health Applications

One of the most promising applications of GABM lies in epidemic modeling, where traditional approaches struggle to capture the complexity of human behavior during outbreaks. Current epidemic models, even those using traditional agent-based modeling, must make certain assumptions about how humans react during an outbreak. GABMs can transfer the decision-making process directly to LLMs without having to introduce these assumptions.

Williams et al. explored these possibilities using a simple GABM epidemic model, simulating virus propagation in a population where ChatGPT decided whether individual agents would exit home at each timestep. The agents received varying levels of information: baseline scenarios with no virus information, self-health feedback scenarios including symptom information and full feedback scenarios including information about the virus and infection rates in the community. @williams2023epidemicmodelinggenerativeagents

The results demonstrated the potential of GABMs for epidemic modeling:
- *Baseline Model*: Reproduced SIR-like model results with all agents exiting homes daily
- *Self-Health Feedback*: Agents with symptoms usually decided to stay home
- *Full Feedback*: Even asymptomatic agents decided to stay home when informed about community infection rates, greatly diminishing outbreak size

These results show the potential of applying GABMs for epidemic modeling and open many interesting questions about the alignment between LLM decisions and actual human behavior during health crises.

== GABM Applications in Social Simulation

Generative agent-based models are opening new possibilities in social simulation, helping researchers explore how people behave in complex, dynamic environments. Unlike traditional rule-based systems, these models can reflect the unpredictability and nuance of real human interactions.

=== Information Propagation in Social Networks

Gao et al. created a simulated social media platform to study how ideas and rumors spread. Each agent powered using ChatGLM made independent choices: whether to share a post, write something new or stay quiet, based on patterns observed in real-life behavior. By tuning the model with data on sharing habits, follower networks and attention spans, they were able to recreate familiar patterns of information spread. They also pinpointed key moments when a message shifts from grassroots sharing to viral influence driven by popular accounts @gao2025s3socialnetworksimulationlarge.

=== Simulating Collective Decision-Making with Multi-Agent Debates <self_reflection_degenerative>

Liang et al. explored group cognition by orchestrating debates among heterogeneous LLM agents: GPT-4, Vicuna and GPT-3.5. They found that isolated self-reflection often led individual models into degenerative loops of circular reasoning. In contrast, structured argumentation among multiple agents produced richer and more accurate conclusions, reducing logical errors and enhancing consistency. This multi-LLM debate paradigm illustrates how GABMs can emulate real-world deliberative forums, providing a sandbox for testing policy proposals, design concepts or strategic plans under diverse social dynamics @liang2024encouragingdivergentthinkinglarge.

== Methodological Advantages and Challenges

While the precedent sections explored the potential of GABMs, it is important to acknowledge the methodological advantages and challenges that come with this approach. GABMs offer a unique blend of capabilities that traditional agent-based models (ABMs) struggle to achieve, but they also introduce new complexities that must be addressed.

=== Enhanced Realism and Behavioral Authenticity

- *Cognitive Biases and Heuristics*: Realistic decision-making flaws including confirmation bias, anchoring effects and availability heuristics
- *Cultural Competency and Context*: Understanding and expressing cultural norms, values and communication styles
- *Individual Personality Variation*: Diverse personalities, backgrounds and capabilities that reflect real human variation
- *Moral and Ethical Reasoning*: Complex ethical decision-making processes that reflect human moral reasoning

=== Technical and Computational Limitations

- *Computational Resource Requirements*: Large-scale GABM simulations require substantial computational resources, with API costs potentially reaching thousands of dollars for comprehensive studies
- *Scalability Constraints*: Hardware requirements for running multiple agents simultaneously can be prohibitive, limiting the number of agents that can be effectively simulated
- *Model Validation Complexity*: Difficulty in validating agent behavior against real-world data, particularly for novel social scenarios where ground truth is unavailable
- *Behavioral Consistency Issues*: Maintaining consistent agent behavior across different contexts and extended time periods remains challenging

=== Methodological and Reproducibility Concerns <method_reprod_concerns>
A main concern is the reproducibility of GABM simulations, which can be affected by various factors @lu2024generativeagentbasedmodelscomplex:

- *Prompt Sensitivity and Engineering*: LLMs are highly sensitive to word ordering, formatting and non-semantic features of prompts, making results difficult to replicate
- *Training and Fine-Tuning Biases*: Models may propagate biases from training data and posterior fine-tuning processes, affecting simulation validity
- *Hallucination and Factual Accuracy*: Models may generate plausible but factually incorrect responses that compromise simulation integrity
- *Cross-Model Behavioral Variation*: Different LLMs exhibit distinct behavioral patterns and preferences that can significantly affect study outcomes
- *Version Dependency*: LLM updates can alter agent behavior mid-study, compromising longitudinal research validity

=== Interpretability and Control Limitations

- *Black Box Decision-Making*: The reasoning process behind agent decisions is often opaque, making it difficult to understand why specific behaviors emerge
- *Limited Behavioral Control*: There is minimal control over specific agent responses, unlike traditional ABMs where behaviors are explicitly programmed
- *Emergent Behavior Unpredictability*: Complex interactions between agents can produce unexpected emergent behaviors that are difficult to anticipate or control

== Simplified GABM Approach for Innovation Diffusion

The project aims to explore a more streamlined application of GABM principles to study Rogers' innovation diffusion theory explained in the next chapter. Rather than implementing the full complexity of advanced GABM frameworks and Rogers' diffusion theory, this approach focuses on the core capability of LLMs to make context-aware decisions that reflect human-like reasoning about the decision-making process.
