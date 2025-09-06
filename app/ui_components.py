"""
UI Components for the Streamlit application
Sidebar controls, help sections, and UI utilities
"""

import streamlit as st
import os
from typing import List

from social.config import SIMULATION_CONFIGS, SimulationConfig
from social.simulation import SocialDiffusionSimulation


def setup_page():
    """Setup Streamlit page configuration"""
    st.set_page_config(
        page_title="Social Innovation Diffusion Simulation",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🧪 Social Innovation Diffusion Simulation")
    st.markdown("*Based on Rogers (2003) Diffusion of Innovations")
    
    st.sidebar.title("🔬 Simulation Controls")
    

def create_sidebar_controls():
    """Create sidebar controls for simulation parameters with improved validation"""
    
    # Get current simulation state
    is_running = st.session_state.simulation_running
    is_cancelled = st.session_state.simulation_cancelled
    is_loaded = st.session_state.simulation_loaded
    is_completed = st.session_state.simulation_completed

    disable_sidebar = is_running or is_loaded or is_completed
    
    # Display simulation status at the top
    """Display current simulation status in sidebar"""
    st.sidebar.markdown("#### 🎯 Current Status")
    
    if is_running:
        st.sidebar.info("🔄 **Simulation Running**")
        st.sidebar.caption("⏱️ Simulation is currently executing...")
    elif is_cancelled:
        st.sidebar.warning("⚠️ **Simulation Cancelled**")
        st.sidebar.caption("🛑 Last simulation was cancelled by user")
    elif is_loaded:
        st.sidebar.info("📂 **Simulation Loaded**")
        st.sidebar.caption("🔄 Loaded a previous simulation state")
    elif is_completed:
        st.sidebar.success("✅ **Simulation Complete**")
        st.sidebar.caption("📊 Results are ready for analysis")
    else:
        st.sidebar.info("🎯 **Ready to Start**")
        st.sidebar.caption("📝 Configure parameters and run simulation")
    
    st.sidebar.markdown("---")
    
    # Load/Save section
    st.sidebar.markdown("### 💾 Save/Load Simulations")
    
    # Show success messages if they exist
    for msg_key in ['load_success_message', 'delete_success_message', 'config_success_message']:
        if hasattr(st.session_state, msg_key):
            st.sidebar.success(getattr(st.session_state, msg_key))
            delattr(st.session_state, msg_key)
    
    # Load existing simulation
    try:
        saved_simulations = SocialDiffusionSimulation.get_saved_simulations()
    except Exception as e:
        st.sidebar.error(f"❌ Error loading saved simulations: {str(e)}")
        saved_simulations = []
        
    if saved_simulations:
        selected_file = st.sidebar.selectbox(
            "Load saved simulation",
            ["None"] + saved_simulations,
            help="Load a previously saved simulation",
            disabled=disable_sidebar
        )
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("📂 Load", use_container_width=True, key="load_sim", disabled=disable_sidebar or selected_file == "None"):
                if selected_file != "None":
                    try:
                        filepath = os.path.join("results", selected_file)
                        simulation = SocialDiffusionSimulation.load_simulation(filepath)

                        # Update session state with loaded simulation data
                        st.session_state.simulation = simulation
                        st.session_state.old_config = st.session_state.temp_simulation_config
                        st.session_state.temp_simulation_config = simulation.config
                        st.session_state.simulation_loaded = True

                        # Show success message with metadata
                        save_date = simulation.results['metadata'].get('save_date', 'Unknown')
                        st.session_state.load_success_message = f"✅ Loaded '{selected_file}' (saved: {save_date[:10]})"
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"❌ Failed to load simulation: {str(e)}")
                        import logging
                        logging.error(f"Load error for {selected_file}: {e}")
                else:
                    st.sidebar.warning("⚠️ Please select a simulation file to load")
        
        with col2:
            if st.button("🗑️ Delete", use_container_width=True, key="delete_sim", disabled=disable_sidebar or selected_file == "None"):
                if selected_file != "None":
                    try:
                        filepath = os.path.join("results", selected_file)
                        os.remove(filepath)
                        st.session_state.delete_success_message = f"✅ File '{selected_file}' deleted!"
                        st.rerun()
                    except Exception as e:
                        st.sidebar.error(f"❌ Failed to delete file: {str(e)}")
                else:
                    st.sidebar.warning("⚠️ Please select a file to delete")
    else:
        st.sidebar.info("📁 No saved simulations found")
    
    # Show storage info
    if saved_simulations:
        total_files = len(saved_simulations)
        st.sidebar.caption(f"📊 {total_files} saved simulation{'s' if total_files != 1 else ''}")
        
    if is_completed and not is_running:
        save_col1, save_col2 = st.sidebar.columns([3, 1])
        with save_col1:
            if st.sidebar.button("💾 Save Current Simulation", 
                                use_container_width=True, key="save_sim", disabled=is_running):
                if st.session_state.simulation is not None:
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
                else:
                    st.sidebar.warning("⚠️ No simulation to save")
        with save_col2:
            # Show save indicator
            st.sidebar.caption("✅")
    else:
        save_reason = ""
        if is_running:
            save_reason = "Simulation is running... Save will be available when complete"
        elif not is_completed:
            save_reason = "Complete a simulation first to enable saving"
        st.sidebar.info(f"ℹ️ {save_reason}")
        
        # Still show the disabled button for consistency
        st.sidebar.button("💾 Save Current Simulation", 
                         disabled=True, use_container_width=True, key="save_sim_disabled")
    
    # Auto-save settings
    st.sidebar.markdown("### 🔧 Auto-Save Settings")
    if st.sidebar.checkbox(
        "💾 Auto-save completed simulations",
        value=st.session_state.auto_save_enabled,
        help="Automatically save simulation results when simulation completes",
        disabled=disable_sidebar
    ):
        st.session_state.auto_save_enabled = True
    else:
        st.session_state.auto_save_enabled = False
    auto_save = st.session_state.auto_save_enabled

    if auto_save:
        st.sidebar.caption("✅ Simulations will be saved automatically")
    else:
        st.sidebar.caption("⚠️ Remember to save manually")
    
    st.sidebar.markdown("---")
    
    # Predefined configurations
    st.sidebar.markdown("### 🎯 Predefined Configurations")
    config_names = list(SIMULATION_CONFIGS.keys())
    selected_preset = st.sidebar.selectbox(
        "Choose configuration",
        config_names,
        index=0,
        help="Predefined configurations with optimized parameters",
        disabled=disable_sidebar
    )

    if st.sidebar.button("📋 Load Configuration", use_container_width=True, key="load_config", disabled=disable_sidebar):
        # Load selected configuration
        preset_config = SIMULATION_CONFIGS[selected_preset]
        
        # Update session state with configuration values
        st.session_state.temp_simulation_config = preset_config
        st.session_state.config_success_message = f"✅ Configuration '{selected_preset}' loaded!"
        st.rerun()
    
    st.sidebar.markdown("---")
    
    # Main configuration section - these controls create the actual simulation config
    st.sidebar.markdown("### 👥 Population Settings")
    num_agents = st.sidebar.slider("Number of Agents", 10, 500, 
                                  st.session_state.temp_simulation_config.num_agents, 5, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.num_agents = num_agents
    max_steps = st.sidebar.slider("Maximum Steps", 2, 50, 
                                 st.session_state.temp_simulation_config.max_steps, 1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.max_steps = max_steps

    innovators_distribution = st.sidebar.slider("Distribution of Innovators", 0.0, 100.0,
                                  st.session_state.temp_simulation_config.adopter_distribution['Innovator'] * 100.0, 0.1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.adopter_distribution['Innovator'] = innovators_distribution / 100.0
    early_adopters_distribution = st.sidebar.slider("Distribution of Early Adopters", 0.0, 100.0,
                                  st.session_state.temp_simulation_config.adopter_distribution['EarlyAdopter'] * 100.0, 0.1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.adopter_distribution['EarlyAdopter'] = early_adopters_distribution / 100.0
    early_majority_distribution = st.sidebar.slider("Distribution of Early Majority", 0.0, 100.0,
                                  st.session_state.temp_simulation_config.adopter_distribution['EarlyMajority'] * 100.0, 0.1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.adopter_distribution['EarlyMajority'] = early_majority_distribution / 100.0
    late_majority_distribution = st.sidebar.slider("Distribution of Late Majority", 0.0, 100.0,
                                  st.session_state.temp_simulation_config.adopter_distribution['LateMajority'] * 100.0, 0.1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.adopter_distribution['LateMajority'] = late_majority_distribution / 100.0
    laggards_distribution = st.sidebar.slider("Distribution of Laggards", 0.0, 100.0,
                                  st.session_state.temp_simulation_config.adopter_distribution['Laggard'] * 100.0, 0.1, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.adopter_distribution['Laggard'] = laggards_distribution / 100.0

    st.sidebar.markdown("### 🌐 Network Configuration")
    network_type = st.sidebar.selectbox(
        "Network Type",
        ["small_world", "scale_free", "random"],
        index=["small_world", "scale_free", "random"].index(st.session_state.temp_simulation_config.network_type),
        disabled=disable_sidebar
    )
    st.session_state.temp_simulation_config.network_type = network_type
    
    if network_type == "small_world":
        # Get saved network params or defaults
        saved_params = st.session_state.temp_simulation_config.network_params
        k = st.sidebar.slider("Neighbors (k)", 2, 10, saved_params.get('k', 4), disabled=disable_sidebar)
        rewiring_prob = st.sidebar.slider("Rewiring Probability", 0.0, 1.0, saved_params.get('rewiring_prob', 0.3), 0.1, disabled=disable_sidebar)
        network_params = {"k": k, "rewiring_prob": rewiring_prob}
    elif network_type == "scale_free":
        saved_params = st.session_state.temp_simulation_config.network_params
        m = st.sidebar.slider("Edges per new node (m)", 1, 5, saved_params.get('m', 2), disabled=disable_sidebar)
        network_params = {"m": m}
    else:  # random
        saved_params = st.session_state.temp_simulation_config.network_params
        p = st.sidebar.slider("Connection Probability", 0.05, 0.5, saved_params.get('p', 0.1), 0.05, disabled=disable_sidebar)
        network_params = {"p": p}
    st.session_state.temp_simulation_config.network_params = network_params
    
    st.sidebar.markdown("### 💡 Innovation Attributes")
    st.sidebar.markdown("*Rogers' 5 characteristics (0=low, 1=high)*")
    
    relative_advantage = st.sidebar.slider("Relative Advantage", 0.0, 10.0, 
                                          st.session_state.temp_simulation_config.innovation_attributes['relative_advantage'] * 10.0, 1.0, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.innovation_attributes['relative_advantage'] = relative_advantage / 10.0
    compatibility = st.sidebar.slider("Compatibility", 0.0, 10.0, 
                                     st.session_state.temp_simulation_config.innovation_attributes['compatibility'] * 10.0, 1.0, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.innovation_attributes['compatibility'] = compatibility / 10.0
    complexity = st.sidebar.slider("Complexity (lower=easier)", 0.0, 10.0, 
                                  st.session_state.temp_simulation_config.innovation_attributes['complexity'] * 10.0, 1.0, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.innovation_attributes['complexity'] = complexity / 10.0
    trialability = st.sidebar.slider("Trialability", 0.0, 10.0, 
                                    st.session_state.temp_simulation_config.innovation_attributes['trialability'] * 10.0, 1.0, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.innovation_attributes['trialability'] = trialability / 10.0
    observability = st.sidebar.slider("Observability", 0.0, 10.0, 
                                     st.session_state.temp_simulation_config.innovation_attributes['observability'] * 10.0, 1.0, disabled=disable_sidebar)
    st.session_state.temp_simulation_config.innovation_attributes['observability'] = observability / 10.0


def create_sidebar_help():
    """Create help section in sidebar"""
    st.sidebar.markdown("---")
    
    with st.sidebar.popover("❓ Help & Tutorial"):
        
        tab1, tab2, tab3 = st.tabs([
            "🚀 Quick Start", 
            "🔬 Scientific Base", 
            "🎮 Interface Guide"
        ])
        
        with tab1:
            st.markdown("""
            ### 🚀 How to Start
            
            1. **Choose Configuration**: Use predefined configurations or customize parameters
            2. **Run Simulation**: Click "🚀 Run Simulation" 
            3. **Observe Results**: View adoption charts and network analysis
            
            ### 🎯 Predefined Configurations
            - **default**: Balanced configuration for general use
            - **innovation_heavy**: Innovation with high benefits
            - **conservative**: Conservative environment 
            - **scale_free**: Scale-free network (central hubs)
            """)
        
        with tab2:
            st.markdown("""
            ### 🔬 Theoretical Base
            
            **Rogers Model (2003)**
            - 5 adopter categories: Innovators → Early Adopters → Early Majority → Late Majority → Laggards
            - 5 innovation attributes: relative advantage, compatibility, complexity, trialability, observability
            
            **Social Graph Theory**
            - Small-world networks (Watts-Strogatz)
            - Scale-free networks (Barabási-Albert)
            - Social influence through connections
            """)
        
        with tab3:
            st.markdown("""
            ### 🎮 Interface Guide
            
            **Controls**
            - **Load/Save**: Manage simulation results
            - **Parameters**: Adjust population and network settings
            - **Live Mode**: Watch simulation progress in real-time
            
            **Visualizations**
            - **Network Graph**: Interactive network with adoption states
            - **Adoption Curve**: Progress over steps with Rogers benchmarks
            - **Category Analysis**: Breakdown by adopter categories
            """)
