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
    if 'num_heroes_input' not in st.session_state: # Initialize the num_heroes_input state
        st.session_state.num_heroes_input = 1 # Default to 1 hero


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
        new_player_name = st.text_in
