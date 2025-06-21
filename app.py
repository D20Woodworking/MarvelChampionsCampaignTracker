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
        "Absorbing Man", # Corrected
        "Taskmaster",
        "Zola",
        "Red Skull"
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
        "Tower Defense", # Corrected
        "Thanos",
        "Hela",
        "Loki" # Corrected
    ],
    "Sinister Motives": [
        "Sandman",
        "Venom",
        "Mysterio",
        "Sinister Six", # Corrected
        "Venom Goblin"
    ],
    "Mutant Genesis": [
        "Sabretooth",
        "Project Wideawake", # Corrected
        "Master Mold",
        "Mansion Attack", # Corrected
        "Magneto" # Corrected
    ],
    "Next Evolution": [
        "Morlock Siege", # Corrected
        "On the Run", # Corrected
        "Juggernaut",
        "Mister Sinister",
        "Stryfe" # Corrected
    ],
    "Age of Apocalypse": [
        "Unus", # Corrected
        "Four Horseman", # Corrected
        "Apocalypse",
        "Dark Beast",
        "En Sabah Nur" # Corrected
    ],
    "Agents of S.H.I.E.L.D.": [
        "Black Widow", # Corrected
        "Batroc", # Corrected
        "M.O.D.O.K.", # Corrected
        "Thunderbolts", # Corrected
        "Baron Zero" # Corrected
    ]
    # Add more campaigns as needed
}

# Define a list of Marvel Champions heroes.
# This list has been updated and alphabetized based on available online resources.
MARVEL_CHAMPIONS_HEROES_RAW = [
    "Adam Warlock", "Angel", "Ant-Man", "Bishop", "Black Panther",
    "Black Widow", "Cable", "Captain America", "Captain Marvel", "Cloak & Dagger",
    "Colossus", "Cyclops", "Dazzler", "Deadpool", "Doctor Strange",
    "Doctor Voodoo", "Domino", "Drax", "Falcon", "Gambit", "Gamora",
    "Ghost-Spider", "Goliath", "Groot", "Hawkeye", "Hulk", "Iceman", "Iron Man",
    "Ironheart", "Jean Grey", "Jubilee", "Kitty Pryde", "Magik", "Magneto",
    "Maria Hill", "Miles Morales", "Mister Sinister", "Ms. Marvel", "Nebula",
    "Nick Fury", "Nightcrawler", "Nova", "Phoenix", "Psylocke", "Quicksilver",
    "Rocket Raccoon", "Rogue", "Ronin", "Scarlet Witch", "Shadowcat", "She-Hulk",
    "Silk", "Silver Surfer", "SP//dr", "Spider-Ham", "Spider-Man (Peter Parker)",
    "Spider-Woman", "Spectrum", "Star-Lord", "Storm", "Thor", "Valkyrie",
    "Venom (Flash Thompson)", "Vision", "War Machine", "Wasp", "Winter Soldier", "Wolverine", "X-23"
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
        # Each scenario outcome will now include a list of heroes played and their health if applicable
        st.session_state.scenarios_played = []
    if 'campaign_boons' not in st.session_state:
        # Stores campaign-specific boons/notes as a dictionary of lists
        # e.g., {"Campaign Name": [{"date": "YYYY-MM-DD", "note": "..."}]}
        st.session_state.campaign_boons = {}


def add_scenario_outcome(campaign_name, scenario_name, heroes_played_data, outcome, notes, date_played):
    """Adds a new scenario outcome to the campaign log.
    heroes_played_data is a list of dictionaries, e.g.,
    [{"hero": "Captain America", "health_remaining": 5}, {"hero": "Iron Man", "health_remaining": 10}]
    """
    st.session_state.scenarios_played.append({
        "campaign": campaign_name,
        "scenario": scenario_name,
        "heroes_played": heroes_played_data, # Now a list of hero dicts
        "outcome": outcome,
        "notes": notes,
        "date": date_played.strftime("%Y-%m-%d") # Format date for display
    })
    hero_names = ", ".join([h["hero"] for h in heroes_played_data])
    st.success(f"'{scenario_name}' played with '{hero_names}' recorded as {outcome} in {campaign_name}!")

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
            # Input for number of heroes playing
            num_heroes_playing = st.number_input(
                "Number of Heroes Playing:",
                min_value=1,
                max_value=4, # Typically 1-4 players in Marvel Champions
                value=1 if len(st.session_state.players) == 0 else min(len(st.session_state.players), 1),
                step=1,
                key="num_heroes_input"
            )

            selected_heroes_choices = []
            # Dynamically create hero selection dropdowns
            for i in range(num_heroes_playing):
                hero_choice = st.selectbox(
                    f"Hero {i+1} Used:",
                    options=MARVEL_CHAMPIONS_HEROES,
                    key=f"hero_select_{i}"
                )
                selected_heroes_choices.append(hero_choice) # Store the selected hero for validation/processing later

            # Dynamically populate scenarios based on selected campaign
            current_campaign_scenarios = MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.get(
                st.session_state.selected_campaign, []
            )
            selected_scenario = st.selectbox(
                "Scenario Played:",
                options=["--- Select a Scenario ---"] + current_campaign_scenarios,
                index=0
            )
            outcome = st.radio("Outcome:", ("Win", "Loss"), horizontal=True, key="scenario_outcome")

            hero_health_inputs_for_submission = [] # This will store the final data for adding to scenarios_played

            # Conditional health input for winning scenarios - now displayed immediately if outcome is 'Win'
            if outcome == "Win":
                st.markdown("---") # Separator for health inputs
                st.subheader("Hero Health Remaining (for Win)")
                for i, hero_name in enumerate(selected_heroes_choices):
                    if hero_name != "--- Select a Hero ---":
                        health = st.number_input(
                            f"Health Remaining for {hero_name}:",
                            min_value=0,
                            value=0, # Default to 0, user can change
                            key=f"hero_health_{i}"
                        )
                        hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": health})
                    else:
                        # If a hero is not selected, add a placeholder indicating so
                        hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})
            else: # If outcome is Loss, populate with N/A
                for hero_name in selected_heroes_choices:
                    if hero_name != "--- Select a Hero ---":
                        hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": "N/A (Loss)"})
                    else:
                        hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})


            scenario_notes = st.text_area("Scenario Notes (e.g., challenges, hero performance):")
            scenario_date_played = st.date_input("Date Played (Scenario):", datetime.date.today(), key="scenario_date")

            submit_scenario_button = st.form_submit_button("Record Scenario Outcome")

            if submit_scenario_button:
                # Validate selected scenario and heroes
                if selected_scenario == "--- Select a Scenario ---":
                    st.error("Please select a scenario to record its outcome.")
                elif any(h == "--- Select a Hero ---" for h in selected_heroes_choices):
                    st.error("Please select all heroes used for the scenario.")
                else:
                    add_scenario_outcome(
                        st.session_state.selected_campaign,
                        selected_scenario,
                        hero_health_inputs_for_submission, # Pass the collected list of hero data
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
            # Flatten the 'heroes_played' list for better display in DataFrame
            # Create a list of dictionaries where each dict represents a row for the DataFrame
            display_data = []
            for record in current_campaign_scenarios_played:
                heroes_str = []
                for hero_info in record["heroes_played"]:
                    if hero_info["health_remaining"] != "N/A" and hero_info["health_remaining"] != "N/A (Loss)":
                        heroes_str.append(f"{hero_info['hero']} ({hero_info['health_remaining']} HP)")
                    else:
                        heroes_str.append(hero_info['hero'])
                display_data.append({
                    "campaign": record["campaign"],
                    "scenario": record["scenario"],
                    "heroes_used": ", ".join(heroes_str), # Display combined hero and health info
                    "outcome": record["outcome"],
                    "notes": record["notes"],
                    "date": record["date"]
                })

            df_scenarios = pd.DataFrame(display_data)
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
