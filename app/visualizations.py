"""
Visualization components for the Streamlit application
Includes charts, graphs, and network visualizations
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import networkx as nx
import pandas as pd
import logging
from typing import Dict, List
from scipy.stats import norm

from social.config import ADOPTER_CATEGORIES


def _create_empty_figure(message: str) -> go.Figure:
    """Create an empty figure with a message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16, color="gray")
    )
    return fig


def create_adoption_curve(results: Dict) -> go.Figure:
    """Create interactive adoption curve with Plotly based on step-by-step data"""
    
    if not results or not isinstance(results, dict):
        return _create_empty_figure("No results data provided")
    
    adoption_history = results.get("adoption_history", {})
    if not adoption_history:
        return _create_empty_figure("No adoption data available")
    
    # Build timeline from adoption_history with better error handling
    timeline = [{'step': 0, 'total_adoption_rate': 0, 'total_adoptions': 0, 'adoption_rate': 0, 'new_adoptions': 0}]

    for step_num in sorted(adoption_history.keys()):
        step_data = adoption_history[step_num]
        if not isinstance(step_data, dict):
            continue
            
        total_adoption_rate = step_data.get("total_adoption_rate", 0)
        total_adoptions = step_data.get("total_adoptions", 0)
        adoption_rate = step_data.get("adoption_rate", 0)
        new_adoptions = step_data.get("new_adoptions", 0)

        timeline_entry = {
            'step': step_num,
            'total_adoption_rate': total_adoption_rate,
            'total_adoptions': total_adoptions,
            'adoption_rate': adoption_rate,
            'new_adoptions': new_adoptions
        }
        timeline.append(timeline_entry)

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Cumulative Adoption Rate per Step', 'Cumulative Adoptions per Step', 'Adoption Rate per Step', 'Adoptions per Step'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]],
        vertical_spacing=0.3,
        horizontal_spacing=0.1,  
    )
    
    steps = [t["step"] for t in timeline]
    total_adoption_rates = [t["total_adoption_rate"] * 100 for t in timeline]
    total_adoptions = [t["total_adoptions"] for t in timeline]
    adoption_rates = [t["adoption_rate"] * 100 for t in timeline]
    new_adoptions = [t["new_adoptions"] for t in timeline]

    
    # Cumulative adoption curve
    fig.add_trace(
        go.Scatter(x=steps, y=total_adoption_rates, 
                  mode='lines+markers',
                  name='Cumulative Adoption Rate',
                  line=dict(color='blue', width=3, shape='spline'),
                  hovertemplate='Step: %{x}<br>Cumulative Adoption Rate: %{y:.1f}%<extra></extra>'),
        row=1, col=1
    )
    
    # Cumulative adoptions bar chart
    fig.add_trace(
        go.Bar(x=steps, y=total_adoptions,
              name='Cumulative Adoptions',
              marker_color='skyblue',
              hovertemplate='Step: %{x}<br>Cumulative Adoptions: %{y}<extra></extra>'),
        row=1, col=2
    )

    # adoption curve
    fig.add_trace(
        go.Scatter(x=steps, y=adoption_rates, 
                  mode='lines+markers',
                  name='Adoption Rate',
                  line=dict(color='blue', width=3, shape='spline'),
                  hovertemplate='Step: %{x}<br>Adoption Rate: %{y:.1f}%<extra></extra>'),
        row=2, col=1
    )
    
    # adoptions bar chart
    fig.add_trace(
        go.Bar(x=steps, y=new_adoptions,
              name='Adoptions',
              marker_color='skyblue',
              hovertemplate='Step: %{x}<br>Adoptions: %{y}<extra></extra>'),
        row=2, col=2
    )
    
    fig.update_xaxes(title_text="Simulation Step", row=1, col=1)
    fig.update_xaxes(title_text="Simulation Step", row=1, col=2)
    fig.update_xaxes(title_text="Simulation Step", row=2, col=1)
    fig.update_xaxes(title_text="Simulation Step", row=2, col=2)
    fig.update_yaxes(title_text="Cumulative Adoption Rate (%)", row=1, col=1)
    fig.update_yaxes(title_text="Cumulative Adoptions", row=1, col=2)
    fig.update_yaxes(title_text="Adoption Rate (%)", row=2, col=1)
    fig.update_yaxes(title_text="Adoptions", row=2, col=2)

    fig.update_layout(height=800, showlegend=False,
                     title="Innovation Adoption Progress Over Steps")

    return fig

def create_category_analysis(results: Dict) -> go.Figure:
    """Create category analysis visualization (fixed adoption rates)"""

    agent_states = results['agent_states']

    categories = []
    categories_count = []
    categories_adopted = []
    for agent in agent_states:
        adopter_category = agent['adopter_category']
        if adopter_category in categories:
            idx = categories.index(adopter_category)
            categories_count[idx] += 1
            categories_adopted[idx] += 1 if agent['has_adopted'] else 0
        else:
            categories.append(adopter_category)
            categories_count.append(1)
            categories_adopted.append(1 if agent['has_adopted'] else 0)

    # Calculate adoption rates as percentages
    categories_adoption_rate = [
        (adopted / count * 100) if count > 0 else 0
        for adopted, count in zip(categories_adopted, categories_count)
    ]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Adoption Rates by Category', 'Population Distribution'),
        specs=[[{"type": "bar"}, {"type": "pie"}]]
    )

    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
    # Adoption rates bar chart (now correct)
    fig.add_trace(
        go.Bar(
            x=categories,
            y=categories_adoption_rate,
            name='Adoption Rate (%)',
            marker_color=colors[:len(categories)],
            text=[f'{rate:.1f}%' for rate in categories_adoption_rate],
            textposition='outside'
        ),
        row=1, col=1
    )

    # Population distribution pie chart
    fig.add_trace(
        go.Pie(
            labels=categories,
            values=categories_count,
            name="Population",
            marker_colors=colors[:len(categories)]
        ),
        row=1, col=2
    )

    fig.update_xaxes(title_text="Adopter Category", row=1, col=1)
    fig.update_yaxes(title_text="Adoption Rate (%)", row=1, col=1)

    fig.update_layout(
        height=500,
        showlegend=False,
        title="Category Analysis"
    )

    return fig

def create_category_adoption_rate_over_time(results: Dict) -> go.Figure:
    """Show, for each category, the % of adopters over time (per step)."""

    agent_states = results['agent_states']
    adoption_history = results.get('adoption_history', {})

    # Map agent_id to category
    agent_category = {agent['agent_id']: agent['adopter_category'] for agent in agent_states}
    # Count total agents per category
    category_total = {cat: 0 for cat in ADOPTER_CATEGORIES}
    for cat in agent_category.values():
        if cat in category_total:
            category_total[cat] += 1

    # Get all categories in order
    categories = [cat for cat in ADOPTER_CATEGORIES if category_total[cat] > 0]

    # Prepare: for each step, count cumulative adopted per category
    steps = sorted(int(s) for s in adoption_history.keys())
    category_cumulative = {cat: [] for cat in categories}

    # For each step, get set of adopted agent_ids
    adopted_per_step = []
    for step in steps:
        agents_results = adoption_history[step]['agents_results']
        adopted_ids = {aid for aid, state in agents_results.items() if state.get('has_adopted', False)}
        adopted_per_step.append(adopted_ids)

    # Cumulative adopted per category (as %)
    cumulative_adopted = {cat: set() for cat in categories}
    for idx, step in enumerate(steps):
        for aid in adopted_per_step[idx]:
            cat = agent_category.get(aid)
            if cat:
                cumulative_adopted[cat].add(aid)
        for cat in categories:
            total = category_total[cat]
            percent = (len(cumulative_adopted[cat]) / total * 100) if total > 0 else 0
            category_cumulative[cat].append(percent)

    # Plot
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeaa7']
    fig = go.Figure()
    for i, cat in enumerate(categories):
        fig.add_trace(go.Scatter(
            x=steps,
            y=category_cumulative[cat],
            mode='lines+markers',
            name=cat,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(symbol='circle', size=8)
        ))

    fig.update_layout(
        title="Adoption Rate Over Steps by Category",
        xaxis_title="Simulation Step",
        yaxis_title="Cumulative Adoption Rate (%)",
        height=500,
        yaxis=dict(range=[0, 100])
    )
    return fig

def _update_graph_with_agent_attributes(graph: nx.Graph, step: int) -> None:
    """
    Update NetworkX graph nodes with current agent attributes.
    
    Args:
        graph: NetworkX graph to update
        step: Current simulation step
    """
    # Create a mapping from agent_id to agent state for quick lookup
    simulation = st.session_state.simulation
    if step != 0:
        adoption_history = simulation.results['adoption_history']
        agents_results = adoption_history[step]['agents_results']

    # Update each node with agent attributes
    for node_idx in graph.nodes():
        node_data = graph.nodes[node_idx]
        agent_id = node_data.get('agent_id')

        if step != 0:
            agent_state = agents_results.get(agent_id, {})
            if agent_state is not None:
                adoption_time = agent_state.get('adoption_time')
                has_adopted = agent_state.get('has_adopted', False)
            else:
                adoption_time = None
                has_adopted = False
        else:
            adoption_time = None
            has_adopted = False

        # Update node attributes
        graph.nodes[node_idx]['category'] = node_data.get('adopter_category')
        graph.nodes[node_idx]['adoption_time'] = adoption_time
        graph.nodes[node_idx]['adopted'] = has_adopted


def create_network_graph(current_step: int, selected_agent: str = None) -> go.Figure:
    """Create interactive network graph using Plotly with step-by-step visualization"""
    
    simulation = st.session_state.simulation
    if simulation is None:
        raise ValueError("No simulation data available")
    results = simulation.results
    # Check if we have saved network edges from network creation
    network_metrics = results.get("network_metrics", {}) if results else {}
    graph: nx.Graph = network_metrics.get("networkx_graph", None)

    if graph is None:
        raise ValueError("No network graph data available in results")

    # Create NetworkX graph - use saved network data
    G = graph.copy()  # Create a copy to avoid modifying the original
    
    if current_step == -1:
        current_step = simulation.results['final_step'] or sorted(simulation.results['adoption_history'])[-1]
    # Update graph nodes with current agent attributes
    _update_graph_with_agent_attributes(G, current_step)
    
    # Calculate layout - use circular layout for small world networks as requested
    if G.number_of_nodes() > 1:
        pos = nx.circular_layout(G)
    else:
        pos = {0: (0, 0)} if G.number_of_nodes() == 1 else {}
    
    # --- Highlight logic ---
    selected_node = None
    if selected_agent is not None:
        for node_idx, node_data in G.nodes(data=True):
            if node_data.get('agent_id') == selected_agent:
                selected_node = node_idx
                break

    highlight_nodes = set()
    highlight_edges = set()
    if selected_node is not None and selected_node in G.nodes:
        # Mark the selected node and its neighbors for highlighting
        highlight_nodes.add(selected_node)
        highlight_nodes.update(G.neighbors(selected_node))
        # Mark edges connecting the selected node to its neighbors for highlighting
        for neighbor in G.neighbors(selected_node):
            highlight_edges.add(frozenset((selected_node, neighbor)))

    # Category colors and symbols
    category_colors = {
        'Innovator': '#ff4757',        
        'EarlyAdopter': '#3742fa',     
        'EarlyMajority': '#2ed573',    
        'LateMajority': '#ffa502',     
        'Laggard': '#747d8c'           
    }
    
    category_symbols = {
        'Innovator': 'star',           
        'EarlyAdopter': 'diamond',     
        'EarlyMajority': 'circle',     
        'LateMajority': 'square',      
        'Laggard': 'triangle-up'       
    }
    
    # Create edge traces by category for proper show/hide functionality
    node_traces = []
    
    for edge in G.edges():
        node1, node2 = edge
        cat1 = G.nodes[node1]['category']
        cat2 = G.nodes[node2]['category']
        
        # Determine edge color based on category priority (Innovators > EarlyAdopter > etc.)
        category_priority = ['Innovator', 'EarlyAdopter', 'EarlyMajority', 'LateMajority', 'Laggard']
        
        if cat1 == cat2:
            # Same category - use that category's color
            edge_category = cat1
        else:
            # Different categories - use the higher priority category
            if category_priority.index(cat1) <= category_priority.index(cat2):
                edge_category = cat1
            else:
                edge_category = cat2
        
        x0, y0 = pos[node1]
        x1, y1 = pos[node2]
        is_highlighted = frozenset((node1, node2)) in highlight_edges
        edge_color = "#e17055" if is_highlighted else category_colors[edge_category]
        edge_width = 4 if is_highlighted else 1
        edge_opacity = 1.0 if is_highlighted else 0.4

        edge_trace = go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=edge_width, color=edge_color),
            opacity=edge_opacity,
            hoverinfo='none',
            mode='lines',
            showlegend=False,
            legendgroup=edge_category,
            visible=True
        )
        node_traces.append(edge_trace)
    
    for category in ADOPTER_CATEGORIES:
        # Adopted nodes
        adopted_x, adopted_y, adopted_text = [], [], []
        adopted_size, adopted_opacity, adopted_line_width = [], [], []
        for node_idx in G.nodes():
            node_data = G.nodes[node_idx]
            if node_data['category'] != category or not node_data.get('adopted', False):
                continue
            x, y = pos[node_idx]
            adopted_x.append(x)
            adopted_y.append(y)
            agent_id = node_data['agent_id']
            adoption_step = node_data.get('adoption_time', None)
            if adoption_step is not None:
                if adoption_step == current_step:
                    status = f"✅ Status: JUST ADOPTED!<br>⏰ Adoption Step: {adoption_step}<br>🎉 NEW in this step!"
                elif adoption_step < current_step:
                    status = f"✅ Status: ADOPTED<br>⏰ Adoption Step: {adoption_step}<br>✔️ Adopted {current_step - adoption_step} step(s) ago"
                else:
                    status = f"✅ Status: ADOPTED<br>⏰ Adoption Step: {adoption_step}<br>🔥 Innovation Adopted!"
            else:
                status = "✅ Status: ADOPTED<br>⏰ Adoption time unknown"
            adopted_text.append(f"🎯 Agent {agent_id}<br>📊 Category: {category}<br>{status}")

            # Highlight logic
            if node_idx in highlight_nodes:
                adopted_size.append(22)
                adopted_opacity.append(1.0)
                adopted_line_width.append(6)
            else:
                adopted_size.append(18)
                adopted_opacity.append(0.9 if selected_node is None else 0.2)
                adopted_line_width.append(3)

        if adopted_x:
            node_traces.append(go.Scatter(
                x=adopted_x, y=adopted_y,
                mode='markers',
                hoverinfo='text',
                text=adopted_text,
                marker=dict(
                    size=adopted_size,
                    color=category_colors[category],
                    symbol=category_symbols[category],
                    line=dict(width=adopted_line_width, color='#00ff00'),
                    opacity=adopted_opacity
                ),
                name=f"{category} (✅ Adopted)",
                showlegend=True,
                legendgroup=category,
                visible=True
            ))

        # Not adopted nodes
        notadopted_x, notadopted_y, notadopted_text = [], [], []
        notadopted_size, notadopted_opacity, notadopted_line_width = [], [], []
        for node_idx in G.nodes():
            node_data = G.nodes[node_idx]
            if node_data['category'] != category or node_data.get('adopted', False):
                continue
            x, y = pos[node_idx]
            notadopted_x.append(x)
            notadopted_y.append(y)
            agent_id = node_data['agent_id']
            adoption_step = node_data.get('adoption_time', None)
            if current_step is not None and adoption_step is not None and adoption_step > current_step:
                steps_until_adoption = adoption_step - current_step
                status = f"⏳ Status: WILL ADOPT<br>⏰ Will adopt in step: {adoption_step}<br> - {steps_until_adoption} step(s) to go"
            else:
                status = "❌ Status: NOT ADOPTED<br>⏳ Still Evaluating..."
            notadopted_text.append(f"👤 Agent {agent_id}<br>📊 Category: {category}<br>{status}")

            # Highlight logic
            if node_idx in highlight_nodes:
                notadopted_size.append(22)
                notadopted_opacity.append(1.0)
                notadopted_line_width.append(6)
            else:
                notadopted_size.append(14)
                notadopted_opacity.append(0.8 if selected_node is None else 0.2)
                notadopted_line_width.append(3)

        if notadopted_x:
            node_traces.append(go.Scatter(
                x=notadopted_x, y=notadopted_y,
                mode='markers',
                hoverinfo='text',
                text=notadopted_text,
                marker=dict(
                    size=notadopted_size,
                    color='white',
                    symbol=category_symbols[category],
                    line=dict(width=notadopted_line_width, color=category_colors[category]),
                    opacity=notadopted_opacity
                ),
                name=f"{category} (❌ Not Adopted)",
                showlegend=True,
                legendgroup=category,
                visible=True
            ))
    
    # Create title with step information
    title_text = 'Social Network: Innovation Diffusion Visualization'
    if current_step != 0:
        if results.get('final_step', None) is not None and current_step == results['final_step']:
            title_text += f' (Final Step)'
        else:
            title_text += f' (Step {current_step})'
    else:
        title_text += f' (Initial Step)'
    
    # Create figure
    fig = go.Figure(data=node_traces,
                   layout=go.Layout(
                       title=dict(
                           text=title_text,
                           font=dict(size=18, color='#2c3e50')
                       ),
                       showlegend=True,
                       hovermode='closest',
                       margin=dict(b=40,l=20,r=20,t=80),
                       annotations=None,
                       xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                       height=800,
                       legend=dict(
                           orientation="v",
                           yanchor="top",
                           y=0.98,
                           xanchor="left",
                           x=1.01,
                           font=dict(size=9),
                           itemclick="toggle",
                           itemdoubleclick="toggleothers",
                           title=dict(
                               text="<b>Categories</b>",
                               font=dict(size=10)
                           ),
                           groupclick="toggleitem",
                           bgcolor="rgba(255,255,255,0.9)",
                           bordercolor="rgba(0,0,0,0.1)",
                           borderwidth=1,
                           itemsizing="constant",
                           itemwidth=30,
                           tracegroupgap=2
                       )
                   ))
    return fig

def display_simulation_summary(results: Dict):
    """Display simulation summary metrics"""

    col1, col2, col4 = st.columns(3)

    if not 'total_adoption_rate' in results or not 'total_adoptions' in results or not 'simulation_time' in results:
        st.warning("Missing adoption data available for summary.")

    with col1:
        st.metric(
            "Final Adoption Rate",
            f"{results.get('total_adoption_rate', 0):.1%}",
            delta=None
        )
    
    with col2:
        st.metric(
            "Total Adoptions",
            results.get('total_adoptions', 0),
            delta=None
        )
    
    with col4:
        st.metric(
            "Simulation Time",
            f"{results.get('simulation_time', 0):.2f}s",
            delta=None
        )
