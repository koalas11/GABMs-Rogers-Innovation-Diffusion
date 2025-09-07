= Simulation Results and Analysis

This chapter presents comprehensive results from simulations conducted using the proposed Generative Agent-Based Model (GABM) methodology. The analysis focuses on key decision-making dynamics, behavioral patterns across agent categories and the interplay between innovation attributes and network effects in driving adoption diffusion.

Complete simulation data, including detailed agent responses and network visualizations, are available in the project repository for further analysis.

== Premises

=== Simulation Scope and Design Choices

This research focuses specifically on the *decision stage* of Rogers' innovation adoption process, intentionally excluding implementation and post-adoption satisfaction feedback. This approach enables targeted analysis of decision-making factors, though it introduces certain behavioral artifacts discussed later.

Given the complexity of Rogers's Diffusion theory and hardware limitations, several simplifications were necessary:

- *Network Awareness Without Satisfaction Feedback:* Agents observe adoption patterns within their network but cannot assess actual adopter satisfaction. This may lead to decisions based on incomplete or perceived information, potentially diverging from real-world outcomes.
- *Scale Constraints:* Simulations were limited to a maximum of 100 agents due to computational requirements. While this allows for an analysis of individual decisions, it may not capture emergent behaviors present in larger populations or varying network densities.
- *Single Network Topology:* All simulations used a small-world network structure (k=4, p=0.3), ensuring internal consistency but limiting generalizability to other configurations such as scale-free or random networks.

=== Prompt Engineering and Decision Consistency

Extensive testing revealed that LLM-based agent behavior is highly sensitive to prompt design, necessitating iterative refinement to achieve theoretical alignment. A key limitation identified was *reasoning-decision inconsistency*, where agents occasionally made adoption choices that contradicted their stated reasoning or thinking. Due to the black-box nature of LLMs, it is not possible to determine whether the decision or the reasoning is at fault. This highlights one of the main challenges when using GABMs: the lack of transparency makes it difficult to fully understand or correct such inconsistencies.

=== Response inconsistencies

Another problem that was observed was that agents sometimes provided inconsistent responses with the data provided in the prompt. For example, an agent could say in their *Thinking* that 1 of its connections adopted the innovation, while in reality, none of them did as shown in the example below of an Innovator agent from the simulation B1 at step 1 with no one in the simulation having adopted yet:

- *Decision:* ADOPT
- *Reasoning:* 'As someone who naturally seeks cutting-edge possibilities and is willing to take calculated risks, this innovation aligns well with my values. The fact that no one has adopted globally yet actually increases its appeal since I can establish myself as a pioneer in my field.'
- *Thinking:* 'Considering this is a cutting-edge possibility with high potential for breakthroughs, I'm drawn to the prospect of being an early adopter. With no global adoption and only 1 out of 3 connections having adopted in my network, it's unlikely anyone will be able to offer guidance or feedback on actual results. I'll have to rely on expert information and my own judgment.'

Similarly to the reasoning-decision inconsistency discussed earlier, it is not possible to determine whether the decision is correct and why the thinking is flawed or vice versa.

=== Computational Constraints

Due to the computational intensity (4-6 hours per full simulation), the project prioritized prompt refinement and behavioral validation over extensive replication, resulting in a limited number of final simulations. This trade-off was necessary to ensure meaningful analysis within available resources.

=== Network and Global Influence Levels

While agents in the simulations reported their perceived levels of network and global influence, these metrics were ultimately excluded from the main results. Upon analysis, it became clear that the way these influence levels were generalized in the prompts could lead to misinterpretation. As a result, presenting them would have been misleading, so they were excluded.

This is an example of how easy it is to introduce unintended behaviors. In this particular case, it shouldn't have introduced bias in the decision-making process, as it only affected the interpretation of agents' influence and not their actual choices.

== Devil's Advocate Prompt Evaluation

To enhance critical thinking and decision-making diversity, preliminary testing evaluated the Devil's Advocate prompt designed to encourage agents to consider counterarguments before making adoption decisions.

=== Experimental Design

*Configuration Parameters:*
- *Test Scope:* Single-step simulations with 20 Early Adopter agents
- *Innovation Profile:* Favorable attributes (Relative Advantage: 7, Compatibility: 6, Complexity: 4, Trialability: 8, Observability: 5)
- *Control Conditions:* Prompt enabled vs. disabled across three simulation rounds each

=== Findings and Implications

*Prompt Enabled Results:*
- 4 of 20 agents adopted (20% adoption rate)
- Enhanced reasoning complexity with explicit consideration of both benefits and risks
- Balanced decision processes reflecting nuanced cost-benefit analysis

*Prompt Disabled Results:*
- 0 of 20 agents adopted (0% adoption rate)  
- More conservative, risk-averse reasoning patterns
- Simpler decision logic focused primarily on uncertainty avoidance
- More decisive language with less hedging

*Full-Scale Validation:*
When tested with 100 agents across all adopter categories, the Devil's Advocate prompt produced an unexpected outcome: rather than increasing decision-making rigor, it appeared to bias agents toward adoption through elaborate rationalization processes, especially for Late Majority and Laggards. Agents generated reasoning that ultimately justified adoption even for marginal innovations, suggesting that the prompt inadvertently encouraged confirmation bias rather than critical evaluation.

==== Representative Agent Response Comparison

*With Devil's Advocate Prompt:*

Example 1:
- *Decision:* NOT_ADOPT
- *Reasoning:* 'While the innovation has some promising features, I believe its potential risks outweigh the benefits at this time. Given the lack of global adoption and relatively low compatibility score, I think it's better to wait until more information becomes available or others have tested its long-term effectiveness.'
- *Thinking:* 'I initially thought that with a relative advantage score of 7 and high trialability, this innovation could be a good fit. However, I'm now considering potential risks such as compatibility issues (score: 6) which might affect my ability to integrate it seamlessly into my existing practices. Additionally, the complexity score of 4 makes me question whether others will find it easy to use or understand. Furthermore, with no global adoption yet and only a few connections adopting, I'm concerned that this could be an early adopter's risk.'

Example 2:
- *Decision:* ADOPT
- *Reasoning:* 'Based on the characteristics provided, this innovation shows promise with a high relative advantage and ease of trialability. While compatibility and observability are lower, they're not deal-breakers for me. I'm willing to take calculated risks and adapt as needed.'
- *Thinking:* 'I've been considering this innovation, and while it's promising with a relatively high relative advantage (7) and ease of trialability (8), I'm concerned about its compatibility (6) and observability (5). I need to weigh the potential benefits against the potential risks. If I adopt, what if others don't see the value in this innovation? It might become a niche solution that's hard to scale or maintain. On the other hand, if I wait, I might miss out on early mover advantages and be left behind by my peers. Considering these counterpoints, I'm still leaning towards ADOPT. While there are risks, I believe the potential rewards outweigh them. The innovation's relative advantage is significant enough to justify exploring it further. However, I need to carefully evaluate its implementation and be prepared to adapt or adjust if necessary.'

*Without Devil's Advocate Prompt:*

Example 1:
- *Decision:* NOT_ADOPT
- *Reasoning:* 'At this stage, I need more convincing evidence of the innovation's value proposition and ease of implementation before adopting it myself.'
- *Thinking:* 'Given the current lack of global adoption and low rate among my network, I'm cautious about adopting this innovation. The scores show some promising aspects, such as relative advantage (7) and trialability (8), but also some red flags like complexity (4) and observability (5). These seem to indicate a potential learning curve and unclear results. Considering my preference for clear benefits and accessible solutions, I'm not convinced yet.'

Example 2:
- *Decision:* NOT_ADOPT
- *Reasoning:* 'Given that no one has adopted this innovation globally yet and none of my connections have adopted it either, I'm hesitant to be the first mover. The relatively low Compatibility score also makes me worry about potential disruptions to our operations.'
- *Thinking:* 'Considering the Relative Advantage score of 7, I think this innovation might offer significant benefits over current alternatives. However, its Compatibility score of 6 raises some concerns about how well it will fit with our existing practices and values.'

=== Decision Impact

The Devil's Advocate prompt was disabled for main simulations to avoid introducing systematic adoption bias. This experience highlights the delicate balance required in prompt engineering for behavioral simulations and the potential for well-intentioned modifications to create unintended systemic effects. This finding underscores the importance of extensive validation when using LLM-based agents for behavioral research.

== Categories Initial Responses

Targeted tests were conducted to observe how agents respond to innovations with both unfavorable and favorable attributes in the absence of network influence (e.g., high complexity or low relative advantage). The goal was to assess whether agents would behave in accordance with their designated adopter categories.

Each simulation consisted of a single step, activating only one adopter category at a time.

Across all tests, results confirmed that the prompts effectively guided agents to make decisions aligned with their category roles, providing a solid foundation for more realistic and theory-consistent simulations.

For example, Early Adopters avoided adopting new innovations, even when they appeared beneficial, demonstrating their greater risk aversion compared to Innovators and their reluctance to try innovations that have not yet been adopted by anyone.

== Network Structure and Simulation Environment

All main simulations utilized a small-world network topology designed to model realistic social influence patterns in innovation diffusion contexts.

*Network Specifications:*
- *Type:* Small-world with k=4 nearest neighbors and p=0.3 rewiring probability
- *Agents:* 100 total (Rogers' Default Distribution) (Innovators rounded to 2, Early Adopters rounded to 14)
  - 2 Innovators (2.5%)
  - 14 Early Adopters (13.5%)
  - 34 Early Majority (34%)
  - 34 Late Majority (34%)
  - 16 Laggards (16%)
- *Edges:* 200 total connections
- *Average Degree:* 4.0 connections per agent
- *Clustering Coefficient:* 0.199
- *Average Path Length:* 3.81 steps
- *Network Diameter:* 7 steps

#figure(
    caption: [Small-World Network Structure - Initial State],
    image("../images/simulation_result/successful_1/step_network_0.svg")
)

*Strategic Properties:*
The small-world structure creates a balance between local clustering (enabling rapid within-group diffusion) and long-range connections (allowing adoption to bridge distant network regions).

*Network Topology Justification:*
Small-world networks represent realistic social structures where individuals maintain close local connections while having occasional long-distance ties, making them appropriate for modeling innovation diffusion in communities, organizations and professional networks. Additionally, they are one of the types of networks usually used in diffusion research as discussed in @diffusion_research.

== Simulation of Unsuccessful Innovations

Preliminary tests examined agent responses to clearly unsuccessful innovations with extremely poor attributes across all dimensions.

*Innovation Scores:*
- Relative Advantage: 1
- Compatibility: 1  
- Complexity: 9
- Trialability: 1
- Observability: 1

*Key Findings:*
Despite the unfavorable profile, some agents still adopted the innovation, revealing limitations in the decision-only simulation approach. The absence of post-adoption satisfaction feedback created unrealistic adoption persistence, as agents could not learn from negative experiences or observe others' dissatisfaction.

Therefore, unsuccessful innovation simulations were excluded from the main analysis to maintain theoretical validity due to the simplifications made in the model.

== Comparative Analysis

To ensure robustness and identify consistent behavioral patterns, 3 simulation runs were conducted for both successful and balanced innovation scenarios. This comparative analysis examines three simulation runs for each innovation type to understand how innovation attributes fundamentally alter diffusion dynamics.

=== Methodology

*Innovation Profiles:*
- *Successful Innovation:* High performance across key attributes
  - Relative Advantage: 7
  - Compatibility: 6
  - Complexity: 4
  - Trialability: 8
  - Observability: 5

- *Balanced Innovation:* Neutral performance across all dimensions
  - Relative Advantage: 5
  - Compatibility: 5
  - Complexity: 5
  - Trialability: 5
  - Observability: 5

*Strategy:*
Three independent runs per innovation type (S1-S3 for successful, B1-B3 for balanced) with identical network topology but allowing natural variation in agent decision-making processes due to the LLM involvement. Each simulation used the same 100-agent network with small-world topology (k=4, p=0.3) and Rogers' standard adopter distribution.

=== Cross-Run Analysis and Results Summary

#let set-global-style() = {
  import "../packages.typ": cetz.draw.set-style
  set-style(
    legend: (fill: white.transparentize(15%)),
    axes: (
      x: (
        tick: (label: (angle: 45deg, offset: 1.25em, anchor: "east")),
        label: (offset: 1.5em),
      ),
      y: (
        label: (angle: 90deg, anchor: "east", offset: 3.5em),
      ),
    ),
  )
}

#let make-rainbow-color(lightness: 80%, chroma: 60%, division: 1, offset: 0deg) = {
  assert(division > 0, message: "division must be positive")
  range(0, division).map(i => oklch(lightness, chroma, (360deg * i / division) + offset))
}

#import "../packages.typ": cetz
#let cetz-color-palette = cetz.palette.new(
  colors: make-rainbow-color(chroma: 100%, lightness: 80%, division: 3, offset: 30deg)
    .zip(make-rainbow-color(division: 3, offset: 40deg))
    .flatten(),
)

#let create_comparison_plot(data_type, y_label, y_max, legend_pos: "inner-south-east") = {
  import "../packages.typ": cetz-plot, cetz

  cetz.canvas({
    import cetz-plot: plot
    import cetz.draw: set-style

    let palette = cetz-color-palette
    
    // Data for successful runs
    let S1 = if data_type == "cumulative" {
      (0, 2, 3, 8, 17, 32, 44, 57, 70, 88, 97, 100)
    } else {
      (0, 2, 1, 5, 9, 15, 12, 13, 13, 18, 9, 3)
    }
    
    let S2 = if data_type == "cumulative" {
      (0, 2, 3, 12, 22, 29, 45, 58, 70, 88, 97, 99, 100)
    } else {
      (0, 2, 1, 9, 10, 7, 16, 13, 12, 18, 9, 2, 1)
    }
    
    let S3 = if data_type == "cumulative" {
      (0, 2, 3, 6, 12, 20, 26, 38, 51, 67, 84, 97, 100)
    } else {
      (0, 2, 1, 3, 6, 8, 6, 12, 13, 16, 17, 13, 3)
    }

    set-global-style()

    plot.plot(
      size: (12, 6),
      plot-style: palette.with(stroke: true),
      mark-style: palette.with(stroke: true, fill: false),
      legend: legend_pos,
      x-label: [Simulation Steps],
      y-label: y_label,
      y-max: y_max,
      y-min: if data_type == "rate" { -1 } else { -5 },
      y-tick-step: if data_type == "rate" { 5 } else { 10 },
      x-min: -1,
      x-max: 21,
      x-tick-step: none,
      x-ticks: range(0, 20).map(i => (i, str(i))),
      axis-style: "left",
      x-grid: true,
      y-grid: true,
      {
        plot.add(S1.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "S1")
        plot.add(S2.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "S2")
        plot.add(S3.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "S3")
      },
    )
  })
}

#let create_balanced_comparison_plot(data_type, y_label, y_max, legend_pos: "inner-south-east") = {
  import "../packages.typ": cetz-plot, cetz

  cetz.canvas({
    import cetz-plot: plot
    import cetz.draw: set-style

    let palette = cetz-color-palette
    
    // Data for balanced runs
    let B1 = if data_type == "cumulative" {
      (0, 2, 2, 5, 9, 19, 27, 32, 41, 55, 72, 81, 95, 97, 99, 99, 99)
    } else {
      (0, 2, 0, 3, 4, 10, 8, 5, 9, 14, 17, 9, 14, 2, 2, 0, 0)
    }
    
    let B2 = if data_type == "cumulative" {
      (0, 2, 2, 4, 6, 11, 19, 21, 28, 40, 48, 59, 70, 81, 86, 93, 98, 99, 100)
    } else {
      (0, 2, 0, 2, 2, 5, 8, 2, 7, 12, 8, 11, 11, 11, 5, 7, 5, 1, 1)
    }
    
    let B3 = if data_type == "cumulative" {
      (0, 2, 2, 2)
    } else {
      (0, 2, 0, 0)
    }

    set-global-style()

    plot.plot(
      size: (12, 6),
      plot-style: palette.with(stroke: true),
      mark-style: palette.with(stroke: true, fill: false),
      legend: legend_pos,
      x-label: [Simulation Steps],
      y-label: y_label,
      y-max: y_max,
      y-min: if data_type == "rate" { -1 } else { -5 },
      y-tick-step: if data_type == "rate" { 5 } else { 10 },
      x-min: -1,
      x-max: 21,
      x-tick-step: none,
      x-ticks: range(0, 20).map(i => (i, str(i))),
      axis-style: "left",
      x-grid: true,
      y-grid: true,
      {
        plot.add(B1.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "B1")
        plot.add(B2.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "B2")
        plot.add(B3.enumerate(), line: "spline", mark: "o", mark-size: .125, label: "B3")
      },
    )
  })
}

#figure(
    caption: [Cumulative Adoption Rate Comparison - Successful Runs],
    create_comparison_plot("cumulative", [Cumulative Adoption Rate (%)], 105)
) <s_runs_cumulative>

#figure(
    caption: [Cumulative Adoption Rate Comparison - Balanced Runs],
    create_balanced_comparison_plot("cumulative", [Cumulative Adoption Rate (%)], 105)
) <b_runs_cumulative>

#figure(
    caption: [Adoption Rate Comparison - Successful Runs],
    create_comparison_plot("rate", [Adoption Rate (%)], 19, legend_pos: "inner-north-east")
) <s_runs_rate>

#figure(
    caption: [Adoption Rate Comparison - Balanced Runs],
    create_balanced_comparison_plot("rate", [Adoption Rate (%)], 19, legend_pos: "inner-north-east")
) <b_runs_rate>

=== Successful Innovation Runs (S1-S3)

The three successful innovation simulations demonstrate high consistency in their overall diffusion patterns (@s_runs_cumulative), though with some variation in acceleration phases:

- *Completion Time:* 11-12 steps across all runs (S1: 11 steps, S2: 12 steps, S3: 12 steps)
- *Final Adoption Rate:* 100% in all cases
- *Critical Mass Point*: Steps 4-5 for S1 and S2, step 6-7 for S3
- *Peak Adoption Rate*: S1 shows peaks around steps 5 and 9 (15-18%), S2 around steps 6 and 9, S3 more gradual with peak around step 10

The adoption rate analysis (@s_runs_rate) reveals peak periods around steps 5, 6 and 9, where maximum single-step adoption occurs. This consistency suggests that when innovators and some early adopters adopt, it influences others to follow as social pressure and network effects come into play, though network position variations still play an important role. However, even successful innovations may find diffusion challenging, as demonstrated by S3.

The successful innovation adoption curves (@s_runs_cumulative) appear to align with Rogers' classic S-curve model and bell shape (@rogers_s_curve), exhibiting the characteristic three-phase progression (with S3 showing a slightly more gradual initiation phase):

*Phase 1 - Slow Initial Growth (Steps 1-3):* The curves show gradual initiation with 2-15% adoption, corresponding to Rogers' innovator and early adopter phases. This matches the theoretical expectation of limited initial uptake among risk-tolerant individuals.

*Phase 2 - Rapid Acceleration (Steps 4-8):* All three runs display steep acceleration phases reaching peak adoption rates of 15-18% per step, representing the critical mass breakthrough as early and late majority populations adopt. This phase closely aligns with Rogers' prediction of exponential growth once social proof mechanisms activate.

*Phase 3 - Saturation and Plateau (Steps 9-12):* The curves level off as remaining agents complete adoption, matching Rogers' saturation phase where diminishing returns occur as the innovation reaches market limits.

It's important to note that the fact that only the decision stage was considered may have influenced the observed diffusion patterns, as the initial stage could be slower due to the need for knowledge of the innovation's existence. Additionally, the missing media influence could have played a role in shaping the adoption dynamics.

=== Balanced Innovation Runs (B1-B3)

The balanced innovation scenarios exhibit significantly greater variability and extended timelines (@b_runs_cumulative):

- *Completion Time:* 16 steps for B1 (early stopping), 18 steps for B2
- *Final Adoption Rate:* 99% for B1 (stopped at 16 due to no adoptions since step 14); 100% for B2; 2% for B3 (early stopping)
- *Critical Mass Point:* Steps 9-12 (requiring 40-50% adoption threshold)
- *Peak Adoption Rate:* 11-17% per step, occurring around steps 3 and 6-9 depending on the run

The early stopping of B3 at only 2% demonstrates that neutral innovations might face genuine diffusion risk. Unlike successful innovations that create intrinsic adoption motivation, balanced innovations rely heavily on network cascade effects, making them vulnerable to early adoption failures, particularly when considering only the decision stage and assuming everyone knows the innovation exists.

The Balanced Innovation runs exhibited greater variability and uncertainty, highlighting the challenges of achieving widespread adoption for innovations with neutral attributes.

The balanced innovation curves (@b_runs_cumulative) reveal significant departures from Rogers' classic S-curve model (@rogers_s_curve):

*Flattened Initiation Phase (Steps 1-3):* Extended slow-growth period with minimal adoption beyond innovators, suggesting that neutral innovation attributes create adoption barriers that delay the transition to rapid growth phases.

*Multiple Acceleration Phases:* Rather than a single steep acceleration, the curves show multiple smaller growth spurts (visible in B1 around steps 3 and 9, in B2 around steps 6-8), indicating that network effects must accumulate gradually when intrinsic innovation appeal is limited.

*Extended Timeline with Incomplete Adoption Risk:* The 16-18 step timelines represent 45-60% longer diffusion periods compared to successful innovations, with B3's complete failure demonstrating that not all innovations manage to achieve adoption.

*Linear Progression Tendency:* The balanced curves approximate linear growth more than exponential acceleration, suggesting that when innovation attributes are neutral, diffusion becomes primarily dependent on network cascade effects rather than intrinsic appeal (considering the simplifications made).

=== Category-Specific Adoption Patterns

#figure(
    caption: [Categories Adoption Rate - Run S1],
    image("../images/simulation_result/successful_1/category_adoption_over_time.svg")
) <s1_categories_rate>

#figure(
    caption: [Categories Adoption Rate - Run S2],
    image("../images/simulation_result/successful_2/category_adoption_over_time.svg")
) <s2_categories_rate>

#figure(
    caption: [Categories Adoption Rate - Run S3],
    image("../images/simulation_result/successful_3/category_adoption_over_time.svg")
) <s3_categories_rate>

==== Category-Specific Adoption Patterns - Successful Innovations

The category progression analysis (@s1_categories_rate, @s2_categories_rate, @s3_categories_rate) aligns with Rogers' theoretical sequence while revealing important behavioral nuances:

*Innovators:* Consistent first adoption within steps 1-2 across all runs, establishing multiple diffusion seed points simultaneously.

*Early Adopters:* Achieve 100% adoption by steps 5-6 across runs, demonstrating their role as opinion leaders in this simulation context. Their rapid adoption appears to contribute to triggering critical mass.

*Early Majority:* Initially show resistance even when few others have adopted, but their resistance diminishes due to network position and their profile characteristics.

*Late Majority:* Similar to Early Majority, they adopt later, but their adoption is more influenced by network pressure and the actions of the Early Majority.

*Laggards:* Latest to adopt due to their strong aversion to change and reliance on established norms. In this case, network position played a significant role in their adoption timing, while the innovation's attributes acted as a secondary influence.

#figure(
    caption: [Categories Adoption Rate - Run B1],
    image("../images/simulation_result/balanced_1/category_adoption_over_time.svg")
) <b1_categories_rate>

#figure(
    caption: [Categories Adoption Rate - Run B2],
    image("../images/simulation_result/balanced_2/category_adoption_over_time.svg")
) <b2_categories_rate>

==== Category-Specific Adoption Patterns - Balanced Innovations

The balanced innovation category analysis (@b1_categories_rate, @b2_categories_rate) reveals markedly different dynamics:

*Extended Evaluation Periods:* All categories except innovators require additional evaluation time, with early adopters not completing adoption until steps 6-8 compared to steps 4-5 in successful scenarios.

*Heightened Threshold Sensitivity:* Early and late majority groups demonstrate much stronger dependence on network adoption signals before committing.

*Category Override Phenomena:* More frequent instances where network position overrides categorical tendencies, particularly laggards adopting before late majority members.

*Persistent Resistance Risk:* Evidence of permanent non-adoption even under strong network pressure, as demonstrated in B1 where one laggard never adopts despite 99% global adoption.

=== Agents Response Analysis

Since it's not possible to show all agent responses, selected examples from key decision points in the simulations are provided, with a general summary of their behavior.

==== Successful Innovation Responses

Agent responses in successful innovation scenarios consistently acknowledge positive innovation attributes even when deciding not to adopt, while using network signals as confirmatory evidence rather than primary drivers. The following examples illustrate this pattern:

*Early Adopter Response (Step 4 - S1):*
- *Decision:* ADOPT
- *Reasoning:* "With the relatively high relative advantage score (7) and the increasing global adoption rate, I feel more confident in adopting this innovation. The trialability is still high (8), which allows me to test it without major commitment risks."
- *Thinking:* "The global adoption rate is now at 8%, which suggests that it's gaining traction and showing promise. Although my network hasn't adopted it yet, I'm starting to see more validation of its value proposition."
- *Confidence Level:* 8

*Early Majority Response (Step 4 - S1):*
- *Decision:* NOT_ADOPT
- *Reasoning:* "While the relative advantage (7) and trialability (8) are still promising, I'm concerned about the complexity (4) and observability (5). I need to see more evidence that it will integrate smoothly into my existing routines before committing."
- *Thinking:* "The global adoption rate has increased significantly, but it's still not at the level where I feel comfortable adopting without more information. Although my network hasn't adopted it yet, the growing number of users suggests there may be some benefits."
- *Confidence Level:* 6

*Late Majority Response (Step 4 - S1):*
- *Decision:* NOT_ADOPT
- *Reasoning:* "While the relative advantage (7/10) is more compelling with higher global adoption, I'm still concerned about compatibility issues (6/10) and complexity (4/10). Without any adopters in my network to provide firsthand experience and guidance, I'm not yet ready to take on this innovation."
- *Thinking:* "The global adoption rate has increased significantly, but it's still not at a level that makes me feel entirely confident in its success and stability. I'm starting to consider the potential benefits of adopting this innovation."
- *Confidence Level:* 5

*Key Pattern:* Even when not adopting, agents consistently frame innovation attributes in positive terms (e.g., "promising," "compelling," "attractive features") and use network adoption patterns as validation of the innovation's inherent value rather than as the primary decision driver.

==== Balanced Innovation Responses

In balanced innovation scenarios, network influence becomes the crucial factor driving adoption decisions, with agents expressing uncertainty about innovation value and relying heavily on social proof mechanisms:

*Early Adopter Response (Step 4 - B1):*
- *Decision:* ADOPT
- *Reasoning:* "With a growing number of adopters globally, I believe there's increasing evidence that this innovation is worth considering. While I still can't rely on my network for guidance, the trend suggests that others are starting to see value in it, which increases my confidence."
- *Thinking:* "The global adoption rate has increased from 2% to 5%, which suggests that more people are starting to see value in the innovation. Although no one in my network has adopted it yet, I'm beginning to consider its potential benefits."
- *Confidence Level:* 7

*Early Adopter Response (Step 3 - B1):*
- *Decision:* NOT_ADOPT
- *Reasoning:* "The lack of growth in global adoption raises concerns about the innovation's value and sustainability. Given that no one in my network has adopted, I'm hesitant to take on the risk of being an early adopter."
- *Thinking:* "The global adoption rate has stayed the same, which might indicate a plateau or some underlying issues. My network's hesitation is still present, but I'm starting to question whether I should be an early adopter if others in my social circle aren't"
- *Confidence Level:* 6

*Early Majority Response (Step 3 - B1):*
- *Decision:* NOT_ADOPT
- *Reasoning:* "The absence of peer experiences and success stories makes it difficult for me to trust this innovation. I need to see more widespread adoption, even if it's just from people outside my immediate network, before considering its value."
- *Thinking:* "I'm still not seeing any adoption among my network, and the global adoption rate is extremely low at only 2%. This lack of social proof is a significant concern for me."
- *Confidence Level:* 6

*Key Pattern:* Network adoption patterns become the primary consideration, with agents expressing uncertainty about innovation benefits and making decisions primarily based on social validation rather than intrinsic innovation appeal. The absence of network adoption signals creates significant adoption barriers.

=== Comparison

The simulations reveal substantial differences between scenarios (considering only the decision stage):

- *Diffusion Speed:*
  - *Successful:* Completed in 11-12 steps, with a sharp acceleration phase.
  - *Balanced:* 16-18 steps in successful runs, with more linear progression, a risk of early stalling (e.g., B3) and a less predictable trajectory.

- *Role of the Network:*
  - *Successful:* Intrinsic attributes drive adoption even without strong network pressure; the network acts as an amplifier.
  - *Balanced:* Network influence is the primary driver; adoption is heavily dependent on position and connections.

- *Category Behavior:*
  - *Successful:* Theoretical patterns mostly preserved, with rare overrides due to advantageous positioning.
  - *Balanced:* Greater variability, more frequent category overrides (e.g., well-connected Laggards adopting before some Late Majority agents).

In summary, successful innovations demonstrate more predictable diffusion patterns that align closely with Rogers' theoretical framework, while balanced innovations reveal the complex interplay between network structure and individual decision-making.

=== Network Positioning Effects

The small-world structure created several notable dynamics that influenced adoption patterns:

- *Bridge Agents:* Individuals connecting otherwise separate clusters wield disproportionate influence on global diffusion patterns
- *Hub Effects:* While not scale-free, agents with above-average connectivity become influential regardless of their adopter category as other agents perceived their adoption as successful
- *Peripheral Resistance:* Agents with fewer connections show greater resistance to adoption, requiring stronger local influence

These effects will be highlighted in the detailed case studies below.

== Detailed Single-Run Analysis

The following sections present detailed examination of representative runs to understand the micro-dynamics driving the observed macro-patterns.

=== Successful Innovation Case Study (Run S1)

#figure(
    caption: [Successful Innovation - Representative Adoption Curve (Run S1)],
    image("../images/simulation_result/successful_1/adoption_curves.svg")
) <adoption_progress_1>

#let create_network_stages_visualization(indexes, type, caption) = {
  for i in indexes {
    let file = "../images/simulation_result/" + type + "/step_network_" + str(i) + ".svg"
    [#figure(
      caption: [#caption (Step #str(i))],
      image(file, format: "svg", height: 46%),
    ) #label("net-"+ type + "-step-" + str(i))]
  }
}

#create_network_stages_visualization((2, 4, 6, 8, 10, 11), "successful_1", "Successful Simulation - Network State")

==== Network Evolution Analysis

*Steps 1-2 - Distributed Initiation:* Both innovators adopt simultaneously in separate network regions (@net-successful_1-step-2), creating distributed innovation sources. This multi-seed pattern accelerates diffusion compared to single-origin models.

*Steps 3-4 - Bridge Activation:* Early adopters in strategic bridge positions begin connecting adoption islands (@net-successful_1-step-4). Notably, some early majority agents adopt despite minimal local network exposure, indicating strong innovation appeal overcoming typical social proof requirements.

*Steps 5-6 - Critical Mass Formation:* Rapid expansion creates distinct adoption clusters (@net-successful_1-step-6). Late majority agents begin adopting around step 5-6, with the critical mass phase evident as multiple categories adopt simultaneously.

*Steps 7-8 - Cascade Acceleration:* Network pressure intensifies with even some laggards adopting before late majority counterparts (@net-successful_1-step-8), illustrating how network position can override categorical tendencies under favorable innovation conditions.

*Steps 9-11 - Complete Saturation:* Final phases show systematic elimination of remaining resistance (@net-successful_1-step-10, @net-successful_1-step-11), with the small-world topology ensuring no agent remains permanently isolated from adoption influences.

==== General Observations

The S1 simulation (@adoption_progress_1) shows favorable diffusion conditions with its compressed 11-step timeline and smooth acceleration pattern. The cumulative adoption curve demonstrates classic S-curve characteristics: gradual initiation (steps 1-2), rapid acceleration (steps 3-7) and final saturation (steps 8-11).

The successful innovation simulation demonstrates several key patterns:

- *Rapid Cascade Dynamics:* The favorable innovation attributes created a "pull effect" where agents were intrinsically motivated to adopt, leading to faster diffusion across all categories. The innovation achieved complete adoption by Step 11, with the network structure serving as an amplifier rather than a primary driver.

- *Category Behavior Validation:* While agents generally followed their prescribed adoption tendencies, network positioning occasionally overrode categorical preferences. Notably, some Laggards adopted before Late Majority agents when positioned in high-influence network locations, demonstrating the power of local social pressure.

- *Network Structure Impact:* The small-world topology facilitated rapid diffusion through both local clustering (enabling rapid local spread) and long-range connections (allowing adoption to "jump" across network regions). Bridge agents connecting different clusters showed disproportionate influence on overall adoption patterns.

#pagebreak()

==== Specific Behavioral Observations

*Observation 1: Early Majority Premature Adoption*

#figure(
    caption: [Early Majority Network State at Step 2],
    image("../images/simulation_result/successful_1/step_network_2_early_majority.svg")
)

*Observation:* An Early Majority agent adopted in Step 3 despite minimal network exposure (connected to only 1 Innovator).

*Agent Response on Step 3:*
- *Reasoning:* 'I still have concerns about the compatibility (6) and complexity (4) of this innovation. However, the relative advantage (7) and trialability (8) are attractive features that could provide a competitive edge if I were to adopt. I'll wait for a bit more traction from my network or other early adopters before making a decision.'
- *Thinking:* 'The global adoption rate is slowly increasing, and it's now over 2%. While my network remains unaffected, I'm starting to see some early signs of potential value in this innovation.'
- *Confidence Level:* 7

*Analysis:* This response highlights an important limitation in LLM-based agents: the disconnect between expressed reasoning and final decision. The agent's reasoning suggests caution and waiting, yet ultimately adopted. This inconsistency suggests possible LLM bias toward adoption or insufficient constraint between reasoning and decision-making processes. While this doesn't necessarily mean the decision to adopt was incorrect, it does indicate a need for improved alignment between cognitive processes and final choices.

*Observation 2: Late Majority Social Influence Sensitivity*

#figure(
    caption: [Late Majority Network State at Step 4],
    image("../images/simulation_result/successful_1/step_network_4_late_majority.svg")
)

*Observation:* A Late Majority agent adopted in Step 5 after observing multiple connections adopting, despite initial hesitancy.

*Agent Response on Step 5:*
- *Reasoning:* 'While the innovation has some drawbacks (low compatibility and observability), its advantages seem substantial enough to outweigh them. The fact that many others have adopted it without major issues is reassuring, and I can now see some potential benefits for my organization.'
- *Thinking:* 'The global adoption rate is now significant, and having one of my connections adopt it successfully gives me more confidence. However, I still need to be cautious about potential complications or problems.'
- *Confidence Level:* 7

*Analysis:* This response demonstrates appropriate Late Majority behavior, balancing innovation attributes with social proof from network connections and global adoption rates.

#pagebreak()

*Observation 3: Laggard Network Pressure Response*

#figure(
    caption: [Laggard Network State at Step 6],
    image("../images/simulation_result/successful_1/step_network_6_laggard.svg")
)

*Observation:* A Laggard agent adopted in Step 7 after observing significant network adoption, despite initial resistance.

*Agent Response on Step 7:*
- *Reasoning:* 'While I still have some reservations about the innovation's complexity, its trialability and observability make it easier to try out without too much risk. And with more than a third of the global community already using it, I think it's time for me to give it a go.'
- *Thinking:* 'The global adoption rate is really taking off now, and it's hard not to feel like I'm missing out on something if everyone else is adopting it. Two of my close connections are already using it, so that's giving me some confidence.'
- *Confidence Level:* 9

*Analysis:* This demonstrates how network positioning can overcome inherent category resistance. The Laggard's high confidence level and FOMO (fear of missing out) reasoning reflects realistic social pressure dynamics.

=== Balanced Innovation Case Study (Run B1)

#figure(
    caption: [Balanced Innovation - Adoption Progress Analysis],
    image("../images/simulation_result/balanced_1/adoption_curves.svg")
) <adoption_progress_2>

#create_network_stages_visualization((2, 3, 6, 8, 9, 10, 12, 14), "balanced_1", "Balanced Simulation - Network State")

==== Network Evolution Analysis

*Steps 1-2 - Conservative Initiation:* Single innovator adoption in step 1 with no additional adoptions in step 2 (@net-balanced_1-step-2), contrasting sharply with successful scenario multi-seed patterns.

*Step 3 - Strategic Breakthrough:* Simultaneous adoption by strategically positioned early adopter and early majority agents (@net-balanced_1-step-3) represents critical transition from innovation appeal to network-driven adoption.

*Steps 4-6 - Gradual Expansion:* Slow cluster growth with clear spatial boundaries between adopted and non-adopted network regions (@net-balanced_1-step-6). Adoption concentrates in high-connectivity areas while peripheral regions remain resistant.

*Steps 7-8 - Network Pressure Emergence:* Late majority activation begins as local network pressure reaches threshold levels (@net-balanced_1-step-8). Some laggards adopt due to favorable positioning, demonstrating network override effects.

*Steps 9-12 - Network Pressure Peak:* Sustained adoption activity with late majority completing adoption and most laggards adopting by step 12 (@net-balanced_1-step-12). The network effects become clearly visible as social pressure drives remaining adoptions.

*Steps 13-16 - Early Stopping Trigger:* By step 14, adoption reaches 99% with one persistent holdout (@net-balanced_1-step-14). No additional adoptions occur in steps 15-16, triggering the early stopping mechanism. This illustrates that neutral innovations may face genuine adoption ceilings where even sustained network pressure cannot overcome individual resistance.

==== General Observations

The B1 simulation (@adoption_progress_2) represents network-dependent diffusion dynamics, reaching 99% adoption by step 14 before triggering early stopping at step 16 due to no new adoptions. The adoption pattern shows more linear progression with multiple smaller acceleration phases rather than a single dramatic surge.

The balanced innovation simulation revealed fundamentally different dynamics:

- *Network-Dependent Diffusion:* With neutral innovation attributes, network influence became the primary adoption driver. This created a more linear, gradual adoption pattern requiring more steps compared to the successful scenario.

- *Enhanced Category Sensitivity:* Agent categories displayed heightened adherence to their risk profiles. Early Adopters became more selective, requiring stronger network signals before adopting, while Majority groups showed clear threshold behaviors, requiring more local network adoption before committing.

- *Incomplete Diffusion Risk:* Unlike the successful innovation that achieved universal adoption, the balanced innovation reached 99% adoption with one Laggard holdout by Step 14. This suggests that neutral innovations face inherent adoption ceilings in realistic scenarios.

- *Temporal Dependency:* The extended 14-step timeline revealed how network effects accumulate over time. Initial hesitancy (steps 1-2 with minimal adoption) gave way to sudden adoption clusters (step 3), demonstrating non-linear network influence patterns.

- *Spatial Clustering Patterns:* Adoption concentrated in network regions with high connectivity, creating distinct adopter and non-adopter clusters. This spatial heterogeneity persisted throughout the simulation, indicating that network topology significantly shapes diffusion patterns for marginal innovations.

==== Specific Behavioral Observations

*Observation 1: Delayed Early Adoption*

*Observation:* In Step 1, only Innovators adopted; in Step 2, there were no adoptions; and in Step 3, only a few Early Adopters decided to adopt.

*Analysis:* This temporal pattern highlights the non-linear effects of network influence. After an initial period of inertia, the accumulation of previous adoption decisions can suddenly trigger uptake among previously hesitant categories. Such delayed responses underscore how network structure and local thresholds can create tipping points, leading to abrupt shifts in adoption dynamics.

Of course due to the nature of LLM this is not always the case and it might be just a coincidence, but it is an interesting observation nonetheless.

#pagebreak()

*Observation 2: Laggard Social Pressure*

#figure(
    caption: [Laggard Network State in Step 7],
    image("../images/simulation_result/balanced_1/step_network_7_laggard.svg")
)

*Observation:* Laggards exhibited a delayed response to social pressure, ultimately adopting after observing significant uptake among their peers.

*Agent Response on Step 8:*
- *Reasoning:* 'While I still have some reservations about the innovation's complexity, its trialability and observability make it easier to try out without too much risk. And with more than a third of the global community already using it, I think it's time for me to give it a go.'
- *Thinking:* 'The global adoption rate is really taking off now, and it's hard not to feel like I'm missing out on something if everyone else is adopting it. Two of my close connections are already using it, so that's giving me some confidence.'
- *Confidence Level:* 9

*Analysis:* This demonstrates how network connections become primary drivers for neutral innovations, with social influence overcoming individual skepticism.

#pagebreak()

*Observation 3: Persistent Resistance*

#figure(
    caption: [Laggard Network State at Steps 14-16],
    image("../images/simulation_result/balanced_1/step_network_14_laggard.svg")
)

*Observation:* One Laggard displayed persistent resistance to adopting the innovation, even as social pressure mounted.

*Agent Responses across Steps 14-16:*

*Step 14:*
- *Reasoning:* 'At this point, the vast majority of people are using this innovation, which makes me wonder if there's something I'm missing. However, I've yet to see any concrete evidence that it offers significant advantages over my current methods.'
- *Thinking:* 'The global adoption is almost complete, and two of my connections have adopted it, but I'm still hesitant due to the lack of clear benefits.'
- *Confidence Level:* 5

*Step 15:*
- *Reasoning:* 'While the majority of people are using this innovation, I've yet to see any compelling reasons to switch from what I'm already doing. I'll continue with my current methods until there's more concrete evidence or a significant problem arises that this innovation can solve.'
- *Thinking:* 'The global adoption is almost universal, and all of my connections have adopted it, but I'm still not convinced that it's worth adopting.'
- *Confidence Level:* 4

*Step 16:*
- *Reasoning:* 'I'm not convinced that adopting this innovation is necessary at this time. My current methods are still working fine, and I'd rather wait until there's a compelling reason to change.'
- *Thinking:* 'It's clear that this innovation has been widely adopted and seems to be working well for others, but I still need to see a specific problem or issue that it can solve.'
- *Confidence Level:* 5

*Analysis:* This demonstrates that for some agents (especially laggards), even overwhelming social influence cannot overcome lack of perceived benefit when innovation attributes are neutral. The declining then stabilizing confidence levels reflect realistic skepticism persistence.
