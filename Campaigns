# app.py
import streamlit as st
import pandas as pd
import datetime

# --- Constants and Initial Setup ---
# Define the default scenarios for Marvel Champions (can be expanded)
# This is just a starting point, you'll want to add more as you play through campaigns.
MARVEL_CHAMPIONS_SCENARIOS = [
    "Rhino",
    "Klaw",
    "Ultron",
    "Mutagen Formula", # Example from a campaign box
    "Green Goblin (Risky Business)",
    "Green Goblin (Goblin Golem)",
    "Crossbones",
    "Taskmaster",
    "Zola",
    "Red Skull",
    "Nebula",
    "Ronan",
    "Thanos",
    "Collector (Museum)",
    "Collector (Ship)",
    "The Hood",
    "Drang",
    "Collector 1",
    "Collector 2",
    "Grandmaster 1",
    "Grandmaster 2",
    "Venom Goblin",
    "Mysterio",
    "Sandman",
    "Venom",
    "Kraven the Hunter",
    "Lizard",
    "Shocker",
    "Electro",
    "Vulture",
    "Doc Ock",
    "Rhino (Expert)",
    "Klaw (Expert)",
    "Ultron (Expert)",
]

# --- Helper Functions ---
def initialize_campaign():
    """Initializes the campaign state in session_state."""
    if 'campaign_name' not in st.session_state:
        st.session_state.campaign_name = ""
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'scenarios_played' not in st.session_state:
        # A list of dictionaries to store scenario outcomes
        st.session_state.scenarios_played = []
    if 'campaign_initialized' not in st.session_state:
        st.session_state.campaign_initialized = False

def add_scenario_outcome(scenario_name, outcome, notes, date_played):
    """Adds a new scenario outcome to the campaign log."""
    st.session_state.scenarios_played.append({
        "scenario": scenario_name,
        "outcome": outcome,
        "notes": notes,
        "date": date_played.strftime("%Y-%m-%d") # Format date for display
    })
    st.success(f"'{scenario_name}' outcome recorded as {outcome}!")

# --- Main Streamlit Application ---
def main():
    st.set_page_config(
        page_title="Marvel Champions Campaign Tracker",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("🛡️ Marvel Champions Campaign Tracker")

    initialize_campaign()

    # --- Sidebar for Campaign Setup and Navigation ---
    with st.sidebar:
        st.header("Campaign Setup")
        if not st.session_state.campaign_initialized:
            st.session_state.campaign_name = st.text_input("Campaign Name:", value=st.session_state.campaign_name)
            new_player_name = st.text_input("Add Player Name:")
            if st.button("Add Player"):
                if new_player_name and new_player_name not in st.session_state.players:
                    st.session_state.players.append(new_player_name)
                    st.success(f"Player '{new_player_name}' added!")
                elif new_player_name:
                    st.warning("Player already exists or name is empty.")

            st.write("Current Players:")
            if st.session_state.players:
                for player in st.session_state.players:
                    st.write(f"- {player}")
            else:
                st.info("No players added yet.")

            if st.session_state.campaign_name and st.session_state.players:
                if st.button("Start Campaign"):
                    st.session_state.campaign_initialized = True
                    st.success(f"Campaign '{st.session_state.campaign_name}' started!")
                    st.experimental_rerun() # Rerun to update the main page content
            else:
                st.warning("Please enter a campaign name and add at least one player to start.")
        else:
            st.write(f"**Current Campaign:** {st.session_state.campaign_name}")
            st.write(f"**Players:** {', '.join(st.session_state.players)}")
            if st.button("Reset Campaign"):
                # Clear all session state variables to restart
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.experimental_rerun() # Rerun to show the initial setup state

    # --- Main Content Area ---
    if st.session_state.campaign_initialized:
        st.header(f"Campaign: {st.session_state.campaign_name}")

        st.subheader("Record New Scenario")
        with st.form("scenario_form"):
            selected_scenario = st.selectbox(
                "Scenario Played:",
                options=["--- Select a Scenario ---"] + MARVEL_CHAMPIONS_SCENARIOS,
                index=0
            )
            outcome = st.radio("Outcome:", ("Win", "Loss"), horizontal=True)
            notes = st.text_area("Notes (e.g., heroes used, specific challenges):")
            date_played = st.date_input("Date Played:", datetime.date.today())

            submit_button = st.form_submit_button("Record Scenario Outcome")

            if submit_button:
                if selected_scenario != "--- Select a Scenario ---":
                    add_scenario_outcome(selected_scenario, outcome, notes, date_played)
                else:
                    st.error("Please select a scenario to record its outcome.")

        st.subheader("Campaign Log")
        if st.session_state.scenarios_played:
            # Convert list of dicts to DataFrame for better display
            df = pd.DataFrame(st.session_state.scenarios_played)
            # Ensure date column is datetime objects for proper sorting if needed later
            df['date'] = pd.to_datetime(df['date'])
            # Sort by date in descending order
            df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
            st.table(df) # Using st.table for a simple, fixed-width display
        else:
            st.info("No scenarios recorded yet. Start playing!")

    else:
        st.info("Set up your campaign in the sidebar to get started!")

# --- Run the app ---
if __name__ == "__main__":
    main()
