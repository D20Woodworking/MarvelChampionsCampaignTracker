# app.py
import streamlit as st
import pandas as pd
import datetime
import json # Import the json module for saving/loading data

# --- Constants and Initial Setup ---
# Define specific campaigns and their 5 associated scenarios/villains
MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS = {
    "--- Select a Campaign ---": [], # Default empty state
    "Rise of Red Skull": [
        "Crossbones",
        "Absorbing Man",
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
        "Tower Defense",
        "Thanos",
        "Hela",
        "Loki"
    ],
    "Sinister Motives": [
        "Sandman",
        "Venom",
        "Mysterio",
        "Sinister Six",
        "Venom Goblin"
    ],
    "Mutant Genesis": [
        "Sabretooth",
        "Project Wideawake",
        "Master Mold",
        "Mansion Attack",
        "Magneto"
    ],
    "Next Evolution": [
        "Morlock Siege",
        "On the Run",
        "Juggernaut",
        "Mister Sinister",
        "Stryfe"
    ],
    "Age of Apocalypse": [
        "Unus",
        "Four Horseman",
        "Apocalypse",
        "Dark Beast",
        "En Sabah Nur"
    ],
    "Agents of S.H.I.E.L.D.": [
        "Black Widow",
        "Batroc",
        "M.O.D.O.K.",
        "Thunderbolts",
        "Baron Zero"
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
    "Rocket Racoon", "Rogue", "Ronin", "Scarlet Witch", "Shadowcat", "She-Hulk",
    "Silk", "Silver Surfer", "SP//dr", "Spider-Ham", "Spider-Man (Peter Parker)",
    "Spider-Woman", "Spectrum", "Star-Lord", "Storm", "Thor", "Valkyrie",
    "Venom (Flash Thompson)", "Vision", "War Machine", "Wasp", "Winter Soldier", "Wolverine", "X-23"
]
MARVEL_CHAMPIONS_HEROES = ["--- Select a Hero ---"] + sorted(MARVEL_CHAMPIONS_HEROES_RAW)

# --- Constants for Data Persistence ---
# Internal file format remains JSON for ease of serialization, but users won't see "JSON" in the UI
DEFAULT_DATA_FILE_NAME = "marvel_champions_campaign_data.json"

# --- Helper Functions ---
def initialize_campaign_state():
    """Initializes the campaign state in session_state."""
    if 'selected_campaign' not in st.session_state:
        st.session_state.selected_campaign = "--- Select a Campaign ---"
    if 'players' not in st.session_state:
        st.session_state.players = []
    if 'scenarios_played' not in st.session_state:
        # A list of dictionaries to store scenario outcomes, including heroes played and their health
        st.session_state.scenarios_played = []
    if 'campaign_boons' not in st.session_state:
        # Stores campaign-specific boons/notes as a dictionary of lists
        st.session_state.campaign_boons = {}
    if 'num_heroes_selected_count' not in st.session_state: # Use a distinct key for the count
        st.session_state.num_heroes_selected_count = 1 # Default to 1 hero


def add_scenario_outcome(campaign_name, scenario_name, heroes_played_data, outcome, notes, date_played):
    """Adds a new scenario outcome to the campaign log."""
    st.session_state.scenarios_played.append({
        "campaign": campaign_name,
        "scenario": scenario_name,
        "heroes_played": heroes_played_data,
        "outcome": outcome,
        "notes": notes,
        "date": date_played.strftime("%Y-%m-%d") # Format date for display
    })
    hero_names = ", ".join([h["hero"] for h in heroes_played_data if h["hero"] != "N/A (Not Selected)"])
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

# --- Helper Functions for Data Persistence ---
def get_campaign_data_for_download():
    """Prepares the current session state data for download as a JSON string."""
    data_to_save = {
        "players": st.session_state.players,
        "scenarios_played": st.session_state.scenarios_played,
        "campaign_boons": st.session_state.campaign_boons
    }
    # Use indent for pretty-printing the JSON
    return json.dumps(data_to_save, indent=4)

def load_campaign_data(uploaded_file):
    """Loads data from an uploaded file into the session state."""
    try:
        data = json.loads(uploaded_file.read().decode("utf-8"))

        # Update session state with loaded data, providing defaults if keys are missing
        st.session_state.players = data.get("players", [])
        st.session_state.scenarios_played = data.get("scenarios_played", [])
        st.session_state.campaign_boons = data.get("campaign_boons", {})
        # Reset selected campaign after loading, or try to select a default/first one
        st.session_state.selected_campaign = list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys())[0]

        st.success("Campaign data loaded successfully! Reloading application...")
        # Use st.rerun() for stable rerun behavior
        st.rerun()
    except json.JSONDecodeError:
        st.error("Error: The uploaded file is not a valid campaign data file. Please check the file format.")
    except Exception as e:
        st.error(f"An unexpected error occurred while loading data: {e}")


# --- Main Streamlit Application ---
def main():
    st.set_page_config(
        page_title="Marvel Champions Campaign Tracker",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    st.title("🛡️ Marvel Champions Campaign Tracker")
    st.markdown("Welcome, True Believer! Track your Marvel Champions campaign progress here.")

    initialize_campaign_state()

    # --- Sidebar for Player Management and Data Operations ---
    with st.sidebar:
        st.header("Player Management")
        new_player_name = st.text_input("Add Player Name:", help="Enter a name and click 'Add Player' to add them to this campaign's roster.")
        if st.button("Add Player"):
            if new_player_name and new_player_name not in st.session_state.players:
                st.session_state.players.append(new_player_name)
                st.success(f"Player '{new_player_name}' added!")
            elif new_player_name:
                st.warning("Player already exists or name is empty.")

        st.markdown("**Current Players:**")
        if st.session_state.players:
            for player in st.session_state.players:
                st.write(f"- {player}")
        else:
            st.info("No players added yet. Please add at least one player to start.")

        st.divider() # Visual separator

        st.header("Save/Load Data")
        st.caption("Manage your campaign progress files.")

        # Save Data Button
        st.download_button(
            label="💾 Save Campaign Progress", # Added icon
            data=get_campaign_data_for_download(),
            file_name=DEFAULT_DATA_FILE_NAME,
            mime="application/json",
            help="Download your current campaign data to your computer. You can upload this file later to continue your progress."
        )

        # Upload Data Button
        uploaded_file = st.file_uploader(
            "⬆️ Load Campaign Progress", # Added icon
            type=["json"],
            help=f"Upload a previously saved campaign data file (e.g., '{DEFAULT_DATA_FILE_NAME}')."
        )
        if uploaded_file is not None:
            load_campaign_data(uploaded_file)

        st.divider() # Visual separator

        if st.button("🚨 Reset All Data", help="This will permanently clear all current campaign data in the app."):
            # Clear all session state variables to restart the entire app
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
            st.success("All campaign data has been reset.")


    # --- Main Content Area ---

    # Campaign Selection
    main_content_container = st.container()
    with main_content_container:
        st.subheader("Choose Your Campaign")
        st.session_state.selected_campaign = st.selectbox(
            "Select the campaign you are currently playing:",
            options=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()),
            index=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()).index(st.session_state.selected_campaign)
        )

        is_campaign_selected = st.session_state.selected_campaign != "--- Select a Campaign ---"
        are_players_added = len(st.session_state.players) > 0

        if not is_campaign_selected or not are_players_added:
            if not is_campaign_selected:
                st.warning("Please select a campaign from the dropdown above to proceed.")
            if not are_players_added:
                st.warning("Please add at least one player in the sidebar to get started.")
        else:
            st.info(f"You are currently tracking **{st.session_state.selected_campaign}** with players: **{', '.join(st.session_state.players)}**")

            st.divider() # Visual separator

            # --- Record New Scenario Outcome Section ---
            st.subheader("Record New Scenario Outcome")
            st.write("Fill in the details of your latest scenario play.")

            # Calculate initial value for num_heroes_selected_count, clamping as needed
            initial_num_heroes_value = st.session_state.num_heroes_selected_count
            if 'players' in st.session_state and len(st.session_state.players) > 0:
                initial_num_heroes_value = min(initial_num_heroes_value, len(st.session_state.players))
                if initial_num_heroes_value == 0:
                    initial_num_heroes_value = 1
            else:
                initial_num_heroes_value = 1 # Default to 1 if no players


            # Input for number of heroes playing (outside the form for immediate reactivity)
            num_heroes_playing_current = st.number_input(
                "Number of Heroes Playing:",
                min_value=1,
                max_value=4, # Typically 1-4 players in Marvel Champions
                value=initial_num_heroes_value, # Use the calculated initial value
                step=1,
                key="num_heroes_input_main" # Widget key
            )
            # Update session state with the current value from the widget
            st.session_state.num_heroes_selected_count = num_heroes_playing_current


            selected_heroes_choices = []
            # Dynamically create hero selection dropdowns (outside the form for immediate reactivity)
            # Use the value from st.session_state.num_heroes_selected_count for the loop range
            for i in range(st.session_state.num_heroes_selected_count):
                hero_choice = st.selectbox(
                    f"Hero {i+1} Used:",
                    options=MARVEL_CHAMPIONS_HEROES,
                    key=f"hero_select_{i}"
                )
                selected_heroes_choices.append(hero_choice) # Store the selected hero for validation/processing later

            outcome = st.radio("Scenario Outcome:", ("Win", "Loss"), horizontal=True, key="scenario_outcome")

            hero_health_inputs_for_submission = [] # This will store the final data for adding to scenarios_played

            # Conditional health input for winning scenarios - displayed immediately if outcome is 'Win'
            if outcome == "Win":
                st.markdown("---")
                st.subheader("Hero Health Remaining (After Win)")
                st.write("Enter the health remaining for each hero that played.")
                for i, hero_name in enumerate(selected_heroes_choices):
                    if hero_name != "--- Select a Hero ---":
                        health = st.number_input(
                            f"Health Remaining for **{hero_name}**:", # Bold hero name
                            min_value=0,
                            value=0,
                            key=f"hero_health_{i}"
                        )
                        hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": health})
                    else:
                        hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})
            else: # If outcome is Loss, populate with N/A
                for hero_name in selected_heroes_choices:
                    if hero_name != "--- Select a Hero ---":
                        hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": "N/A (Loss)"})
                    else:
                        hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})

            # The form now only contains the fields that need to be submitted together
            with st.form("scenario_submit_form"): # Changed form key to prevent conflicts
                st.divider()
                st.write("Final details for this scenario:")
                # Dynamically populate scenarios based on selected campaign
                current_campaign_scenarios = MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.get(
                    st.session_state.selected_campaign, []
                )
                selected_scenario = st.selectbox(
                    "Scenario Played:",
                    options=["--- Select a Scenario ---"] + current_campaign_scenarios,
                    index=0,
                    key="scenario_select_in_form"
                )

                scenario_notes = st.text_area("Notes for this scenario (e.g., specific challenges, campaign choices, defeated villain):")
                scenario_date_played = st.date_input("Date Played:", datetime.date.today(), key="scenario_date")

                submit_scenario_button = st.form_submit_button("➕ Record Scenario Outcome")

                if submit_scenario_button:
                    if selected_scenario == "--- Select a Scenario ---":
                        st.error("❌ Please select a scenario to record its outcome.")
                    elif any(h == "--- Select a Hero ---" for h in selected_heroes_choices):
                        st.error("❌ Please select all heroes used for the scenario.")
                    else:
                        add_scenario_outcome(
                            st.session_state.selected_campaign,
                            selected_scenario,
                            hero_health_inputs_for_submission,
                            outcome,
                            scenario_notes,
                            scenario_date_played
                        )

            st.divider()

            # --- Campaign Log Section (Scenarios) ---
            st.subheader("Scenario Log 📜")
            st.write(f"All recorded scenarios for **{st.session_state.selected_campaign}**.")

            # Filter scenarios played by the currently selected campaign
            current_campaign_scenarios_played = [
                s for s in st.session_state.scenarios_played
                if s["campaign"] == st.session_state.selected_campaign
            ]

            if current_campaign_scenarios_played:
                display_data = []
                for record in current_campaign_scenarios_played:
                    heroes_str = []
                    for hero_info in record["heroes_played"]:
                        if hero_info["health_remaining"] != "N/A" and hero_info["health_remaining"] != "N/A (Loss)":
                            heroes_str.append(f"{hero_info['hero']} ({hero_info['health_remaining']} HP)")
                        elif hero_info["health_remaining"] == "N/A (Loss)":
                            heroes_str.append(f"{hero_info['hero']} (Defeated)")
                        else:
                            heroes_str.append(hero_info['hero'])
                    display_data.append({
                        "Campaign": record["campaign"],
                        "Scenario": record["scenario"],
                        "Heroes Used": ", ".join(heroes_str),
                        "Outcome": record["outcome"],
                        "Notes": record["notes"],
                        "Date Played": record["date"]
                    })

                df_scenarios = pd.DataFrame(display_data)
                df_scenarios['Date Played'] = pd.to_datetime(df_scenarios['Date Played'])
                df_scenarios = df_scenarios.sort_values(by='Date Played', ascending=False).reset_index(drop=True)
                st.dataframe(df_scenarios, use_container_width=True)
            else:
                st.info(f"No scenarios recorded yet for **{st.session_state.selected_campaign}**. Time to play!")

            st.divider()

            # --- Campaign Boons & Notes Section ---
            st.subheader("Campaign Boons & Notes 📝")
            st.write(f"Important ongoing effects or notes for **{st.session_state.selected_campaign}**.")
            with st.form("campaign_notes_form"):
                new_campaign_note = st.text_area("Add a new campaign note or boon:", help="e.g., 'Permanent +1 HP for Captain America', 'Obligation: Betrayal added to deck'.")
                note_date = st.date_input("Date (Note Added):", datetime.date.today(), key="note_date_form")
                submit_note_button = st.form_submit_button("➕ Add Campaign Note")

                if submit_note_button:
                    if new_campaign_note:
                        add_campaign_note(st.session_state.selected_campaign, new_campaign_note, note_date)
                    else:
                        st.warning("Please enter a note to add.")

            current_campaign_boons = st.session_state.campaign_boons.get(
                st.session_state.selected_campaign, []
            )
            if current_campaign_boons:
                df_boons = pd.DataFrame(current_campaign_boons)
                df_boons.rename(columns={"date": "Date Added", "note": "Note/Boon"}, inplace=True)
                df_boons['Date Added'] = pd.to_datetime(df_boons['Date Added'])
                df_boons = df_boons.sort_values(by='Date Added', ascending=False).reset_index(drop=True)
                st.dataframe(df_boons, use_container_width=True)
            else:
                st.info(f"No special boons or notes recorded yet for **{st.session_state.selected_campaign}**.")


# --- Run the app ---
if __name__ == "__main__":
    main()
