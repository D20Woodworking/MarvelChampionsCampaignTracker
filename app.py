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

# Define a list of Marvel Champions heroes.
# The list is sorted alphabetically after removing the initial placeholder.
MARVEL_CHAMPIONS_HEROES_RAW = [
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
    "Ghost-Spider", "Silver Surfer"
]
MARVEL_CHAMPIONS_HEROES = ["--- Select a Hero ---"] + sorted(MARVEL_CHAMPIONS_HEROES_RAW)


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
    if 'campaign_boons' not in st.session_state:
        # Stores campaign-specific boons/notes as a dictionary of lists
        # e.g., {"Campaign Name": [{"date": "YYYY-MM-DD", "note": "..."}]}
        st.session_state.campaign_boons = {}


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

def add_campaign_note(campaign_name, note, date):
    """Adds a campaign-specific note or boon."""
    if campaign_name not in st.session_state.campaign_boons:
        st.session_state.campaign_boons[campaign_name] = []
    st.session_state.campaign_boons[campaign_name].append({
        "date": date.strftime("%Y-%m-%d"),
        "note": note
    })
    st.success(f"Note added to {campaign_name} campaign log!")


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

        # --- Record New Scenario Outcome Section ---
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
            scenario_notes = st.text_area("Scenario Notes (e.g., challenges, hero performance):")
            scenario_date_played = st.date_input("Date Played (Scenario):", datetime.date.today(), key="scenario_date")

            submit_scenario_button = st.form_submit_button("Record Scenario Outcome")

            if submit_scenario_button:
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
                        scenario_notes,
                        scenario_date_played
                    )

        # --- Campaign Log Section (Scenarios) ---
        st.subheader("Scenario Log")
        # Filter scenarios played by the currently selected campaign
        current_campaign_scenarios_played = [
            s for s in st.session_state.scenarios_played
            if s["campaign"] == st.session_state.selected_campaign
        ]

        if current_campaign_scenarios_played:
            df_scenarios = pd.DataFrame(current_campaign_scenarios_played)
            df_scenarios['date'] = pd.to_datetime(df_scenarios['date'])
            df_scenarios = df_scenarios.sort_values(by='date', ascending=False).reset_index(drop=True)
            st.dataframe(df_scenarios)
        else:
            st.info(f"No scenarios recorded yet for {st.session_state.selected_campaign}.")

        # --- Campaign Boons & Notes Section ---
        st.subheader("Campaign Boons & Notes")
        with st.form("campaign_notes_form"):
            new_campaign_note = st.text_area("Add Campaign Note/Boon (e.g., 'Permanent +1 HP for Captain America', 'Obligation: Betrayal added'):")
            note_date = st.date_input("Date (Note):", datetime.date.today(), key="note_date")
            submit_note_button = st.form_submit_button("Add Campaign Note")

            if submit_note_button:
                if new_campaign_note:
                    add_campaign_note(st.session_state.selected_campaign, new_campaign_note, note_date)
                else:
                    st.warning("Please enter a note to add.")

        # Display campaign boons/notes for the current campaign
        current_campaign_boons = st.session_state.campaign_boons.get(
            st.session_state.selected_campaign, []
        )
        if current_campaign_boons:
            df_boons = pd.DataFrame(current_campaign_boons)
            df_boons['date'] = pd.to_datetime(df_boons['date'])
            df_boons = df_boons.sort_values(by='date', ascending=False).reset_index(drop=True)
            st.dataframe(df_boons)
        else:
            st.info(f"No special boons or notes recorded yet for {st.session_state.selected_campaign}.")


# --- Run the app ---
if __name__ == "__main__":
    main()
