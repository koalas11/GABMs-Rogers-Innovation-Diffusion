"""
Core StreamlitDiffusionApp class
Main application controller
"""

import json
import streamlit as st
import asyncio
import logging
import traceback
import pandas as pd
from typing import Dict

from social.config import ADOPTER_CATEGORIES, SimulationConfig

from app.utils import (
    calculate_adoption_metrics, cancel_simulation, setup_logging
)
from app.ui_components import (
    setup_page, create_sidebar_controls, create_sidebar_help, 
)
from app.visualizations import create_adoption_curve, create_category_adoption_rate_over_time, create_category_analysis, create_network_graph, display_simulation_summary
from social.simulation import get_simulation_with_config

class StreamlitDiffusionApp:
    """
    Streamlit application for interactive social innovation diffusion simulation
    """
    
    def __init__(self):
        self.progress_bar = None
        self.status_text = None
        self.network_container = None
        self.step_metrics_container = None
        self.live_network_placeholder = None
        self.live_metrics_placeholder = None
        
        # Setup logging and initialize session state
        setup_logging()
        self.initialize_session_state()
    
    def initialize_session_state(self):
        st.session_state.temp_simulation_config = SimulationConfig()
        st.session_state.auto_save_enabled = True
        st.session_state.live_visualization_enabled = True
        st.session_state.simulation_loaded = False
        self.reset_session_state()

    def reset_session_state(self):
        """Reset the session state to initial values"""
        st.session_state.simulation_running = False
        st.session_state.simulation_task = None
        st.session_state.simulation_cancelled = False
        st.session_state.simulation_starting = False
        st.session_state.simulation_started = False
        st.session_state.simulation_completed = False
        if st.session_state.simulation_loaded and st.session_state.old_config is not None:
            st.session_state.temp_simulation_config = st.session_state.old_config
        st.session_state.old_config = None
        st.session_state.simulation_loaded = False
        st.session_state.simulation = None

    def reset_state(self):
        self.reset_session_state()

    def start_simulation(self):
        st.session_state.simulation_running = True
        st.session_state.simulation_cancelled = False
        st.session_state.simulation_starting = True
        st.session_state.simulation_started = False

    def run_app(self):
        """Main application runner"""
        setup_page()
        create_sidebar_help()

        # --- Centralize session state keys ---
        session = st.session_state
        is_running = session.simulation_running
        is_cancelled = session.simulation_cancelled
        is_completed = session.simulation_completed

        # --- Sidebar controls ---
        create_sidebar_controls()

        # --- Main controls ---
        st.markdown("## 🎮 Simulation Controls")
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.button(
                "🚀 Run Simulation",
                disabled=is_running or session.simulation_loaded,
                use_container_width=True,
                type="primary",
                on_click=self.start_simulation
            )
        with col2:
            if st.checkbox(
                "📹 Live Updates",
                value=st.session_state.live_visualization_enabled,
                help="Show real-time network evolution during simulation",
                disabled=is_running
            ):
                st.session_state.live_visualization_enabled = True
            else:
                st.session_state.live_visualization_enabled = False
        with col3:
            if st.session_state.simulation_cancelled or is_completed or session.simulation_loaded:
                st.button(
                    "⚠️ Reset",
                    disabled=st.session_state.simulation_cancelled or (not is_running and not session.simulation_loaded),
                    use_container_width=True,
                    type="secondary",
                    on_click=self.reset_state
                )
            else:
                st.button(
                    "⚠️ Cancel",
                    disabled=not is_running and session.simulation_started,
                    use_container_width=True,
                    type="secondary",
                    on_click=cancel_simulation
                )
                    

        # --- State logic ---
        if is_cancelled:
            st.warning("⚠️ Simulation was cancelled. Click 'Reset' to start a new simulation.")
            return
        if st.session_state.get('wait_for_cancel', False):
            st.info("⏳ Wait for initialization to cancel the simulation...")

        if is_running and session.simulation_started:
            st.info("🔄 Simulation is currently running... Please wait for completion.")
            return
        
        if is_completed or session.simulation_loaded and not is_running:
            self._display_simulation_results()
            return

        # --- Start simulation after rerun ---
        if is_running and session.simulation_starting:
            logging.info("Starting simulation execution")
            st.info("🚀 Starting simulation execution...")
            self._execute_simulation()
    
    def _execute_simulation(self):
        """Execute simulation with proper error handling and UI updates"""

        # Setup live visualization if requested
        if st.session_state.live_visualization_enabled:
            self._setup_live_visualization()
        
        # Create progress indicators
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        
        try:            
            self.status_text.text("🚀 Initializing simulation...")
            self.progress_bar.progress(0.1)

            st.session_state.simulation_starting = False

            # Initialize simulation with callbacks
            simulation = get_simulation_with_config(
                st.session_state.temp_simulation_config,
                simulation_step_started_callback=self.step_started_callback,
                simulation_step_completed_callback=self.step_completed_callback,
                simulation_completed_callback=self.simulation_completed_callback,
                simulation_initialized_callback=self.simulation_initialized_callback
            )
            st.session_state.simulation = simulation
            simulation.initialize_simulation()
            asyncio.run(self.run_simulation())
            st.session_state.simulation_running = True
            st.session_state.simulation_started = True
        except Exception as e:
            error_msg = str(e)
            self.status_text.text(f"❌ Simulation failed to start: {error_msg}")
            logging.error(f"Simulation error: {error_msg}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            
            # Additional error context for debugging
            with st.expander("🔍 Error Details (for debugging)", expanded=False):
                st.code(traceback.format_exc())
            self.progress_bar = None
        st.rerun()

    def simulation_initialized_callback(self):
        """Callback when simulation is initialized"""
        self.status_text.text("📊 Initial network stored! Starting simulation...")
        self.progress_bar.progress(0.2)
        try:
            self._display_live_network(0)
        except Exception as e:
            logging.error(f"Error displaying initial live network: {str(e)}")
            pass
    
    def step_started_callback(self, step):
        """Callback when a simulation step starts"""
        progress = 0.3 + (step / st.session_state.temp_simulation_config.max_steps) * 0.6
        self.progress_bar.progress(progress)
        self.status_text.text(f"🏃‍♂️ Running step {step}/{st.session_state.temp_simulation_config.max_steps}...")

    def step_completed_callback(self, step):
        """Callback when a simulation step completes"""
        config = st.session_state.temp_simulation_config
        progress = 0.3 + ((step) / config.max_steps) * 0.6
        self.progress_bar.progress(progress)
        try:
            self._display_live_network(step)
        except Exception as e:
            logging.error(f"Error displaying live network: {e}")
            pass
    
    def simulation_completed_callback(self):
        # Auto-save if enabled
        if st.session_state.auto_save_enabled:
            try:
                config_name = st.session_state.simulation.config.name
                if config_name:
                    filename = f"results_{config_name}"
                else:
                    filename = "results"
                st.session_state.simulation.save_results(filename)
                st.sidebar.success(f"✅ Simulation saved as: '{filename}'")
            except Exception as e:
                st.sidebar.error(f"❌ Failed to save simulation: {str(e)}")
        self.status_text.text("📊 Analyzing results...")
        self.progress_bar.progress(0.95)

        st.session_state.simulation_running = False
        st.session_state.simulation_started = False
        st.session_state.simulation_completed = True

        if st.session_state.live_visualization_enabled and hasattr(self, 'live_network_placeholder') and self.live_network_placeholder:
            self.live_network_placeholder.empty()
        if st.session_state.live_visualization_enabled and hasattr(self, 'live_metrics_placeholder') and self.live_metrics_placeholder:
            self.live_metrics_placeholder.empty()

        self.status_text.text("✅ Simulation completed! Ready for analysis...")
        self.progress_bar.progress(1)
        st.rerun()


    def _display_live_network(self, step: int):
        """Display initial simulation state in live visualization"""
        # Show initial network state
        if self.live_network_placeholder:
            with self.live_network_placeholder.container():
                if step == 0:
                    st.markdown("### 🌐 Live Network Evolution - Initial State 🔴 LIVE")
                    st.caption("🚀 Starting simulation - network visualization will update in real-time!")
                else:
                    st.markdown(f"### 🌐 Live Network Evolution - Step {step} 🔴 LIVE")
                    st.caption("🎬 Watch the network evolve in real-time as agents adopt the innovation!")
            
                network_fig = create_network_graph(current_step=step)
                st.plotly_chart(network_fig, use_container_width=True, key=f"live_network_{step}")
        
        # Show initial metrics
        if self.live_metrics_placeholder:
            with self.live_metrics_placeholder.container():
                metrics = calculate_adoption_metrics(step)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Current Step", f"{step}" if step >= 1 else "Initial")
                with col2:
                    st.metric("Adoption Rate", f"{metrics['adoption_rate']:.1%}")
                with col3:
                    st.metric("New Adoptions", f"{metrics['new_adoptions']}")

    async def run_simulation(self):
        """Run simulation with progress updates and robust error handling"""
        try:
            st.session_state.simulation_task = asyncio.current_task()
            await st.session_state.simulation.run_simulation()
        except asyncio.CancelledError:
            self.status_text.text("⚠️ Simulation cancelled by user")
        except Exception as e:
            error_msg = str(e)
            self.status_text.text(f"❌ Simulation failed: {error_msg}")
            st.error(f"Error during simulation: {error_msg}")
            logging.error(f"Simulation error: {error_msg}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            st.session_state.simulation_running = False
            st.session_state.simulation_started = False
            st.session_state.simulation_task = None
            st.rerun()
        finally:
            st.session_state.simulation_running = False
            st.session_state.simulation_started = False
            st.session_state.simulation_task = None

    def _cleanup_ui_elements(self):
        """Clean up UI elements and temporary state safely"""
        # Clean up UI elements safely
        self.progress_bar.empty()
        self.status_text.empty()
    
    def _setup_live_visualization(self):
        """Setup live visualization containers"""
        st.markdown("## 🎬 Live Simulation Visualization")
        st.markdown("*Watch the network evolution in real-time as the simulation progresses*")
        
        # Create containers for live updates
        self.live_network_placeholder = st.empty()
        self.live_metrics_placeholder = st.empty()
    
    def _display_simulation_results(self):
        """Display comprehensive simulation results"""
        
        results = st.session_state.simulation.results
        if not results:
            st.error("❌ No simulation results data found")
            return
                    
        # Show loaded file info if available
        if hasattr(st.session_state, 'loaded_file_info'):
            st.caption(f"📂 Data source: {st.session_state.loaded_file_info}")
        
        # Display summary metrics
        display_simulation_summary(results)
        
        # Create tabs for different visualizations
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Adoption Curves", 
            "👥 Category Analysis", 
            "🌐 Network Graph",
            "🎬 Step-by-Step Network",
            "🧠 Agent Response Analysis"
        ])
        
        with tab1:
            st.markdown("### 📈 Innovation Adoption Over Steps")
            adoption_fig = create_adoption_curve(results)
            config = {
                'toImageButtonOptions': {
                    'format': 'svg', # one of png, svg, jpeg, webp
                    'filename': 'adoption_curves',
                    'height': 600,
                    'width': 1000,
                    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                }
            }
            st.plotly_chart(adoption_fig, use_container_width=True, key="results_adoption_curve", config=config)

        with tab2:
            st.markdown("### 👥 Rogers Category Analysis")
            category_fig = create_category_analysis(results)
            config = {
                'toImageButtonOptions': {
                    'format': 'svg', # one of png, svg, jpeg, webp
                    'filename': 'category_analysis',
                    'height': 600,
                    'width': 1000,
                    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                }
            }
            st.plotly_chart(category_fig, use_container_width=True, key="results_category_analysis", config=config)

            category_fig2 = create_category_adoption_rate_over_time(results)
            config = {
                'toImageButtonOptions': {
                    'format': 'svg', # one of png, svg, jpeg, webp
                    'filename': 'category_adoption_over_time',
                    'height': 500,
                    'width': 1000,
                    'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                }
            }
            st.plotly_chart(category_fig2, use_container_width=True, key="results_category_adoption_over_time", config=config)

        with tab3:
            st.markdown("### 🌐 Final Network State")
            st.caption("📊 This shows the final state after simulation completion. For step-by-step evolution, check the 'Step-by-Step Network' tab.")
            
            # Get agent states from results
            agent_states = results.get('agent_states', [])
            if agent_states:
                selected_agent = st.selectbox(
                    "Select Agent to Highlight",
                    options=[None] + [agent['agent_id'] for agent in agent_states],
                    help="View details for a specific agent",
                    key="selected_agent_network_final"
                )
                network_fig = create_network_graph(-1, selected_agent=selected_agent)
                config = {
                    'toImageButtonOptions': {
                        'format': 'svg', # one of png, svg, jpeg, webp
                        'filename': 'final_network_state',
                        'height': 550,
                        'width': 1000,
                        'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                    }
                }
                st.plotly_chart(network_fig, use_container_width=True, key="results_network_graph", config=config)

                # Show network statistics
                total_agents = len(agent_states)
                adopted_agents = sum(1 for state in agent_states if state.get('has_adopted', False))
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Agents", total_agents)
                with col2:
                    st.metric("Adopted Agents", adopted_agents)
                with col3:
                    adoption_rate = adopted_agents / total_agents if total_agents > 0 else 0
                    st.metric("Final Adoption Rate", f"{adoption_rate:.1%}")
                
                # Display comprehensive network statistics
                network_metrics = results.get('network_metrics', {})
                if network_metrics:
                    st.markdown("#### 🔗 Network Structure Analysis")
                    
                    # First row of network metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Edges", network_metrics.get('total_edges', 0))
                    with col2:
                        st.metric("Average Degree", f"{network_metrics.get('avg_degree', 0):.1f}")
                    with col3:
                        st.metric("Network Density", f"{network_metrics.get('density', 0):.3f}")
                    with col4:
                        st.metric("Avg Clustering", f"{network_metrics.get('avg_clustering', 0):.3f}")
                    
                    # Second row of network metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        is_connected = network_metrics.get('is_connected', False)
                        st.metric("Connected", "Yes" if is_connected else "No")
                    with col2:
                        st.metric("Components", network_metrics.get('num_components', 0))
                    with col3:
                        avg_path = network_metrics.get('avg_shortest_path', float('inf'))
                        avg_path_display = f"{avg_path:.2f}" if avg_path != float('inf') else "∞"
                        st.metric("Avg Path Length", avg_path_display)
                    with col4:
                        st.metric("Diameter", network_metrics.get('diameter', 0))
            else:
                st.error("❌ No agent state data available for network visualization")

        with tab4:
            st.markdown("### 🎬 Step-by-Step Network Evolution")
            
            # Get agent states and adoption history from results
            agent_states = results.get('agent_states', [])
            adoption_history = results.get('adoption_history', {})
            
            # Validate data integrity
            if not agent_states:
                st.error("❌ No agent state data available for step-by-step visualization")
                return
                
            if not adoption_history:
                st.error("❌ No adoption history data available for step-by-step visualization")
                return
                
            # Check for valid step data
            valid_steps = [k for k, v in adoption_history.items() if v and isinstance(v, dict)]
            if not valid_steps:
                st.error("❌ No valid step data found in adoption history")
                return
            
            if agent_states and adoption_history and valid_steps:
                # Create a slider to select simulation step
                max_step = len(valid_steps)
                if max_step >= 0:
                    selected_step = st.slider(
                        "Select Simulation Step",
                        min_value=0,
                        max_value=max_step,
                        value=max_step,
                        help=f"View network state at different simulation steps (0 to {max_step})"
                    )
                    
                    # Show step information with safe data access
                    step_data = adoption_history.get(selected_step, {})
                    
                    # Validate step data
                    if not step_data and selected_step > 0:
                        st.warning(f"⚠️ No data available for step {selected_step}")
                        step_data = {}  # Provide empty dict for safe access
                    
                    new_adoptions = step_data.get('new_adoptions', 0)
                    adoption_rate = step_data.get('total_adoption_rate', 0)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        text = selected_step if selected_step > 0 else "Initial"
                        st.metric("Current Step", text)
                    with col2:
                        st.metric("New Adoptions", new_adoptions)
                    with col3:
                        st.metric("Cumulative Adoption Rate", f"{adoption_rate:.1%}")

                    st.markdown("#### Evidence an Agent and it's Connections")
                    selected_agent = st.selectbox(
                        "Select Agent to Highlight",
                        options=[None] + [agent['agent_id'] for agent in agent_states],
                        help="View details for a specific agent",
                        key="selected_agent_network_step"
                    )

                    # Create network graph for the selected step
                    step_network_fig = create_network_graph(current_step=selected_step, selected_agent=selected_agent)
                    config = {
                        'toImageButtonOptions': {
                            'format': 'svg', # one of png, svg, jpeg, webp
                            'filename': f'step_network_{selected_step}',
                            'height': 600,
                            'width': 900,
                            'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
                        }
                    }
                    st.plotly_chart(step_network_fig, use_container_width=True, key=f"step_network_{selected_step}", config=config)
                else:
                    st.warning("No step data available for visualization")
            else:
                st.error("❌ No agent state or adoption history data available for step-by-step visualization")
            self.create_agents_analysis(results)

        with tab5:
            st.markdown("### 🧠 Agent Response Analysis")

            self.create_agents_analysis(results, "analysis")

    def create_agents_analysis(self, results: Dict, key: str = "network"):
            # Get agent states and adoption history from results
            agent_states = results.get('agent_states', [])
            adoption_history = results.get('adoption_history', {})
            
            # Validate data integrity
            if not agent_states:
                st.error("❌ No agent state data available for step-by-step visualization")
                return
                
            if not adoption_history:
                st.error("❌ No adoption history data available for step-by-step visualization")
                return
                
            # Check for valid step data
            valid_steps = [k for k, v in adoption_history.items() if v and isinstance(v, dict)]
            if not valid_steps:
                st.error("❌ No valid step data found in adoption history")
                return
            
            if agent_states and adoption_history and valid_steps:
                # Create a slider to select simulation step
                max_step = len(valid_steps)
                if max_step >= 0:
                    col1, col2 = st.columns([2, 2])
                    
                    with col1:
                        if max_step == 1:
                            st.warning("⚠️ Only one simulation step available. No slider needed.")
                            selected_step = 1
                        else:
                            selected_step = st.slider(
                                "Select Simulation Step",
                                min_value=1,
                                max_value=max_step,
                                value=max_step,
                                help=f"View agent response at different simulation steps (1 to {max_step})",
                                key="selected_step_" + key
                            )

                    with col2:
                        selected_agent = st.selectbox(
                            "Select Agent",
                            options=[agent['agent_id'] for agent in agent_states],
                            help="View details for a specific agent",
                            key="selected_agent_" + key
                        )

                if selected_step > 0 and selected_agent:
                    agents_results = adoption_history[selected_step]['agents_results']
                    agent_results = agents_results[selected_agent]

                    if not agent_results:
                        st.warning(f"⚠️ No data available for agent {selected_agent} at step {selected_step}")
                        return

                    if agent_results.get('adopted_before', False):
                        adopted_step = agent_results.get('adoption_time', 0)
                        st.success(f"✅ Agent {selected_agent} has adopted before step {selected_step} at step {adopted_step}.")
                        return

                    st.markdown("#### 🧠 Agent Response")
                    has_adopted = agent_results['has_adopted']
                    reasoning = agent_results.get('reasoning', "No reasoning provided")
                    thinking = agent_results.get('thinking', "No thinking provided")
                    network_influence_level = agent_results.get('network_influence_level', "N/A")
                    global_influence_level = agent_results.get('global_influence_level', "N/A")
                    confidence_level = agent_results.get('confidence_level', "N/A")

                    st.metric("##### Adopted", "Yes" if has_adopted else "No")

                    st.markdown("##### 🧠 Reasoning:")
                    st.write(reasoning)

                    st.markdown("##### 💭 Thinking:")
                    st.write(thinking)

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.write("Network Influence Level:")
                        st.write(network_influence_level)

                    with col2:
                        st.write("Global Influence Level:")
                        st.write(global_influence_level)

                    with col3:
                        st.write("Confidence Level:")
                        st.write(confidence_level)


                    full_output = agent_results.get('full_output', {})
                    try:
                        json_output = json.loads(full_output)
                        st.expander("🔍 Full Output (Json)", expanded=False).json(json_output)
                    except json.JSONDecodeError:
                        st.expander("🔍 Full Output", expanded=False).write(full_output)
                    