import streamlit as st
import pandas as pd
import datetime
import json

# =========================
# --- App Configuration ---
# =========================
st.set_page_config(
    page_title="Marvel Champions Campaign Tracker",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ================
# --- CONSTANTS ---
# ================
MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS = {
    "--- Select a Campaign ---": [],
    "Rise of Red Skull": ["Crossbones", "Absorbing Man", "Taskmaster", "Zola", "Red Skull"],
    "Galaxy's Most Wanted": ["Drang", "Collector (Museum)", "Collector (Ship)", "Nebula", "Ronan"],
    "Mad Titan's Shadow": ["Ebony Maw", "Tower Defense", "Thanos", "Hela", "Loki"],
    "Sinister Motives": ["Sandman", "Venom", "Mysterio", "Sinister Six", "Venom Goblin"],
    "Mutant Genesis": ["Sabretooth", "Project Wideawake", "Master Mold", "Mansion Attack", "Magneto"],
    "Next Evolution": ["Morlock Siege", "On the Run", "Juggernaut", "Mister Sinister", "Stryfe"],
    "Age of Apocalypse": ["Unus", "Four Horseman", "Apocalypse", "Dark Beast", "En Sabah Nur"],
    "Agents of S.H.I.E.L.D.": ["B]()
