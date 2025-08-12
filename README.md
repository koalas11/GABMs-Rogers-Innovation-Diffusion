# Simulating Rogers' Innovation Diffusion with Generative Agent-Based Models (GABMs)

This repository presents a novel simulation framework that integrates **Rogers' Diffusion of Innovations theory** with **Generative Agent-Based Modeling (GABM)**, leveraging Large Language Models (LLMs) to emulate realistic, heterogeneous decision-making in social networks.

## Project Overview

The simulation explores how innovations spread through complex social systems, focusing on the nuanced interplay between individual behavioral profiles, network topology and the perceived attributes of innovations. By employing advanced prompt engineering and modular agent design, the system enables in-depth analysis of adoption dynamics across different adopter categories—**Innovators, Early Adopters, Early Majority, Late Majority and Laggards**—without ever explicitly revealing these categories to the agents, with focus on the decision stage of Rogers' theory.

Key features include:

- **LLM-Driven Agents:** Each agent is powered by a local LLM (e.g., Llama 3.1 8B via Ollama), receiving detailed behavioral prompts that synthesize psychological traits, risk attitudes and social influence sensitivity.
- **Configurable Simulation Environment:** The [`SimulationConfig`](app/core.py) class allows for fine-grained control over population parameters, innovation characteristics, network structure and simulation logic.
- **Prompt Engineering:** The [`DiffusionPrompts`](app/core.py) class implements sophisticated system and decision prompts, including optional "Devil's Advocate" reflection to encourage critical reasoning and mitigate bias.
- **Network Topologies:** Supports small-world, scale-free and random networks, enabling the study of structural effects on diffusion.
- **Comprehensive Data Capture:** Records not only adoption outcomes but also agent reasoning, confidence and influence metrics for rich post-simulation analysis.
- **Streamlit Interface:** An interactive web app ([`launch_app.py`](launch_app.py)) for configuring, running and visualizing simulations in real time.

## Scientific Foundations

- **Rogers' Theory:** The simulation operationalizes Rogers' five perceived innovation attributes (relative advantage, compatibility, complexity, trialability, observability) and empirically grounded adopter category proportions.
- **Generative Agent-Based Modeling:** Inspired by recent advances in GABM and frameworks like AutoGen and Concordia, the project demonstrates how LLMs can be harnessed for social simulation, memory and reflection.
- **Prompt Design:** Prompts are meticulously crafted to avoid category leakage, instead providing agents with rich, psychologically plausible personas.

## Usage

1. **Install Requirements**
    ```sh
    pip install -r requirements.txt
    ```

2. **Run the Streamlit App**
    ```sh
    streamlit run launch_app.py
    ```

3. Configure and Launch Simulations
    - Use the web interface to select predefined or custom scenarios.
    - Monitor adoption curves, network evolution and agent-level decision logs.
