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
    "Rocket Racoon", "Rogue", "Ronin", "Scarlet Witch", "Shadowcat", "She-Hulk",
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
        # Each scenario outc
