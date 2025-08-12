"""
Utility functions for the Streamlit application
"""

import os
import logging
from typing import List, Dict
import streamlit as st

from social.simulation import SocialDiffusionSimulation


def setup_logging():
    """Setup logging configuration for cleaner Streamlit interface"""
    logging.getLogger('PIL').setLevel(logging.WARNING)

def has_completed_simulation():
    """Check if there's a completed simulation available"""
    if 'simulation_data' not in st.session_state:
        return False
    return (st.session_state.simulation_data.get('simulation_completed', False) and 
            st.session_state.simulation_data.get('simulation_object', None) is not None)

def cancel_simulation():
    """Cancel the currently running simulation task"""    
    # Cancel the actual task
    if st.session_state.simulation_task is not None:
        logging.info("Cancelling simulation task...")
        # Set cancellation flag first
        st.session_state.simulation_cancelled = True
        st.session_state.simulation_running = False
        st.session_state.simulation_started = False
        st.session_state.simulation_task.cancel()
        
        # Clear task reference
        st.session_state.simulation_task = None
    
        logging.info("Simulation cancellation requested by user")
    else:
        st.session_state.wait_for_cancel = True

def calculate_adoption_metrics(step: int) -> Dict:
    """Calculate adoption metrics for a given step"""
    simulation = st.session_state.simulation
    if simulation is None:
        raise ValueError("No simulation object found in session state")

    if step == 0:
        return {
            'total_agents': simulation.agents,
            'total_adopted': 0,
            'adoption_rate': 0.0,
            'new_adoptions': 0
        }
    
    simulation = st.session_state.simulation
    if step == -1:
        step = sorted(simulation.results['adoption_history'].keys())[-1]

    total_agents = len(simulation.agents)
    total_adopted = sum(1 for agent in simulation.agents if agent.has_adopted)
    adoption_rate = total_adopted / total_agents if total_agents > 0 else 0
    new_adoptions = sum(1 for agent in simulation.agents 
                      if agent.has_adopted and agent.adoption_time == step)
    
    return {
        'total_agents': total_agents,
        'total_adopted': total_adopted,
        'adoption_rate': adoption_rate,
        'new_adoptions': new_adoptions
    }
