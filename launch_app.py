"""
Launcher for the modular Social Innovation Diffusion Simulation Streamlit App
"""
from app.core import StreamlitDiffusionApp
import streamlit.runtime.scriptrunner
import streamlit as st


if __name__ == "__main__":
    try:
        check = streamlit.runtime.scriptrunner.get_script_run_ctx()
        if check:
            app = st.session_state.get('app_instance', None)
            if app is None:
                app = StreamlitDiffusionApp()
                st.session_state['app_instance'] = app
            app.run_app()
        else:
            print("Error: This script must be run with Streamlit.")
            print("Usage: streamlit run launch_app.py")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        print(traceback.format_exc())
        import sys
        sys.exit(1)
