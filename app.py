# app.py
import streamlit as st
import pandas as pd
import datetime

# --- Constants and Initial Setup ---
# Define specific campaigns and their 5 associated scenarios/villains
MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS = {
    "--- Select a Campaign ---": [], # Default empty state
    "Rise of Red Skull": [
        "Crossbones",
        "Taskmaster",
        "Zola",
        "Red Skull",
        "Ultron (from RoRS)"
    ],
    "Galaxy's Most Wanted": [
        "Drang",
        "Collector (Museum)",
        "Collector (Ship)",
        "Nebula",
        "Ronan"
    ],
    "Mad Titan's Shadow": [
        "Ebony Maw",
        "Corvus Glaive",
        "Proxima Midnight",
        "Thanos",
        "Hela" # Assuming Hela is the 5th for MTS
    ],
    "Sinister Motives": [
        "Sandman",
        "Venom",
        "Mysterio",
        "Venom Goblin",
        "Iron Spider (from SM)" # Assuming a placeholder or key encounter
    ],
    "Mutant Genesis": [
        "Sabretooth",
        "Brotherhood of Mutants (Blob, Pyro, Avalanche)",
        "Magneto (Mystique)",
        "Sentinel Base Assault (Master Mold)",
        "Juggernaut" # Assuming a placeholder or key encounter
    ],
    "Next Evolution": [
        "Dominus",
        "Mojo",
        "Spiral",
        "Shadow King",
        "Proteus" # Assuming a placeholder or key encounter
    ],
    "Age of Apocalypse": [
        "Mr. Sinister",
        "Apocalypse (Early)",
        "Dark Beast",
        "Holocaust",
        "Apocalypse (Final)"
    ],
    "Agents of S.H.I.E.L.D.": [
        "Gabe Jones",
        "Agent Brand",
        "Nick Fury",
        "Maria Hill",
        "Phil Coulson" # Assuming 5 specific Agents for the campaign feel
    ]
    # Add more campaigns as needed
}

# Define a list of Marvel Champions heroes (placeholder - expand as needed)
MARVEL_CHAMPIONS_HEROES = [
    "--- Select a Hero ---",
    "Captain America", "Iron Man", "Spider-Man (Peter Parker)", "Black Panther",
    "Captain Marvel", "She-Hulk", "Thor", "Doctor Strange", "Ant-Man", "Wasp",
    "Quicksilver", "Scarlet Witch", "Star-Lord", "Gamora", "Drax", "Groot",
    "Rocket Racoon", "Venom (Flash Thompson)", "Spectrum", "Adam Warlock",
    "Vision", "Sp-Dr", "Cyclops", "Phoenix", "Wolverine", "Storm", "Colossus",
    "Kitty Pryde", "Nightcrawler", "Domino", "Cable", "Deadpool", "Angel",
    "Psylocke", "Gambit", "Rogue", "X-23", "Nova", "Ironheart", "War Machine",
    "Valkyrie", "Dazzler", "Shadowcat", "Mister Sinister", "Jean Grey", "Iceman",
    "Bishop", "Hawkeye", "Ms. Marvel", "Hulk", "Black Widow", "Ronin",
    "Goliath", "Spider-Ham", "Doctor Voodoo", "Cloak & Dagger", "Spider-Man (Miles Morales)",
    "Ghost-Spider", "Silver Surfer", "Kitty Pryde" # Added some more for a decent list
]

# --- Helper Functions ---
def initialize_campaign_state():
    """Initializes the campaign state in session_state."""
    if 'selected_campaign' not in st.session_state:
        st.session_state.selected_campaign = "--- Select a Campaign ---"
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'scenarios_played' not in st.session_state:
        # A list of dictionaries to store scenario outcomes
        st.session_state.scenarios_played = []

def add_scenario_outcome(campaign_name, scenario_name, hero_used, outcome, notes, date_played):
    """Adds a new scenario outcome to the campaign log."""
    st.session_state.scenarios_played.append({
        "campaign": campaign_name,
        "scenario": scenario_name,
        "hero_used": hero_used,
        "outcome": outcome,
        "notes": notes,
        "date": date_played.strftime("%Y-%m-%d") # Format date for display
    })
    st.success(f"'{scenario_name}' played with '{hero_used}' recorded as {outcome} in {campaign_name}!")

# --- Main Streamlit Application ---
def main():
    st.set_page_config(
        page_title="Marvel Champions Campaign Tracker",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("🛡️ Marvel Champions Campaign Tracker")

    initialize_campaign_state()

    # --- Sidebar for Player Setup and Reset ---
    with st.sidebar:
        st.header("Player Management")
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

        st.markdown("---")
        if st.button("Reset All Data"):
            # Clear all session state variables to restart the entire app
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun() # Rerun to show the initial setup state
            st.success("All campaign data has been reset.")


    # --- Main Content Area ---

    # Campaign Selection
    st.subheader("Select Campaign")
    st.session_state.selected_campaign = st.selectbox(
        "Choose a Campaign:",
        options=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()),
        index=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()).index(st.session_state.selected_campaign)
    )

    is_campaign_selected = st.session_state.selected_campaign != "--- Select a Campaign ---"
    are_players_added = len(st.session_state.players) > 0

    if not is_campaign_selected or not are_players_added:
        if not is_campaign_selected:
            st.warning("Please select a campaign to begin tracking.")
        if not are_players_added:
            st.warning("Please add at least one player in the sidebar.")
    else:
        st.write(f"**Tracking Campaign:** {st.session_state.selected_campaign}")
        st.write(f"**Players:** {', '.join(st.session_state.players)}")

        st.subheader("Record New Scenario Outcome")
        with st.form("scenario_form"):
            selected_hero = st.selectbox(
                "Hero Used:",
                options=MARVEL_CHAMPIONS_HEROES,
                index=0
            )

            # Dynamically populate scenarios based on selected campaign
            current_campaign_scenarios = MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.get(
                st.session_state.selected_campaign, []
            )
            selected_scenario = st.selectbox(
                "Scenario Played:",
                options=["--- Select a Scenario ---"] + current_campaign_scenarios,
                index=0
            )
            outcome = st.radio("Outcome:", ("Win", "Loss"), horizontal=True)
            notes = st.text_area("Notes (e.g., specific challenges, campaign choices):")
            date_played = st.date_input("Date Played:", datetime.date.today())

            submit_button = st.form_submit_button("Record Scenario Outcome")

            if submit_button:
                if selected_scenario == "--- Select a Scenario ---":
                    st.error("Please select a scenario to record its outcome.")
                elif selected_hero == "--- Select a Hero ---":
                    st.error("Please select the hero used.")
                else:
                    add_scenario_outcome(
                        st.session_state.selected_campaign,
                        selected_scenario,
                        selected_hero,
                        outcome,
                        notes,
                        date_played
                    )

        st.subheader("Campaign Log")
        if st.session_state.scenarios_played:
            df = pd.DataFrame(st.session_state.scenarios_played)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False).reset_index(drop=True)
            st.dataframe(df) # Using st.dataframe for more interactive table
        else:
            st.info("No scenarios recorded yet for any campaign.")

# --- Run the app ---
if __name__ == "__main__":
    main()
