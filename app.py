import streamlit as st
import pandas as pd
import datetime
import json

# --- App Config and CSS ---
st.set_page_config(
    page_title="Marvel Champions Campaign Tracker",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .main-title {
        font-size:2.2rem;
        font-weight:900;
        color:#0072B1;
        letter-spacing:0.02em;
        margin-bottom:0.2em;
        text-shadow:0 2px 6px #11223311;
    }
    .subtitle {
        color:#e8431d;
        font-size:1.08em;
        letter-spacing:0.01em;
        margin-bottom:2rem;
    }
    .stDataFrame {border-radius:10px; box-shadow:0 0 16px #0072B133;}
    </style>
    <h1 class='main-title'>🛡️ Marvel Champions Campaign Tracker</h1>
    <p class='subtitle'>Track, save, and celebrate your Marvel Champions campaign adventures!</p>
    """,
    unsafe_allow_html=True
)

# --- Data Constants ---
MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS = {
    "--- Select a Campaign ---": [],
    "Rise of Red Skull": [
        "Crossbones", "Absorbing Man", "Taskmaster", "Zola", "Red Skull"
    ],
    "Galaxy's Most Wanted": [
        "Drang", "Collector (Museum)", "Collector (Ship)", "Nebula", "Ronan"
    ],
    "Mad Titan's Shadow": [
        "Ebony Maw", "Tower Defense", "Thanos", "Hela", "Loki"
    ],
    "Sinister Motives": [
        "Sandman", "Venom", "Mysterio", "Sinister Six", "Venom Goblin"
    ],
    "Mutant Genesis": [
        "Sabretooth", "Project Wideawake", "Master Mold", "Mansion Attack", "Magneto"
    ],
    "Next Evolution": [
        "Morlock Siege", "On the Run", "Juggernaut", "Mister Sinister", "Stryfe"
    ],
    "Age of Apocalypse": [
        "Unus", "Four Horseman", "Apocalypse", "Dark Beast", "En Sabah Nur"
    ],
    "Agents of S.H.I.E.L.D.": [
        "Black Widow", "Batroc", "M.O.D.O.K.", "Thunderbolts", "Baron Zero"
    ]
}

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
DEFAULT_DATA_FILE_NAME = "marvel_champions_campaign_data.mchamp"

# --- Helper Functions ---
def initialize_campaign_state():
    st.session_state.setdefault('selected_campaign', "--- Select a Campaign ---")
    st.session_state.setdefault('players', [])
    st.session_state.setdefault('scenarios_played', [])
    st.session_state.setdefault('campaign_boons', {})
    st.session_state.setdefault('num_heroes_input', 1)

def get_campaign_data_for_download():
    data_to_save = {
        "players": st.session_state.players,
        "scenarios_played": st.session_state.scenarios_played,
        "campaign_boons": st.session_state.campaign_boons
    }
    return json.dumps(data_to_save, indent=4)

def load_campaign_data(uploaded_file):
    try:
        data = json.loads(uploaded_file.read().decode("utf-8"))
        st.session_state.players = data.get("players", [])
        st.session_state.scenarios_played = data.get("scenarios_played", [])
        st.session_state.campaign_boons = data.get("campaign_boons", {})
        st.session_state.selected_campaign = list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys())[0]
        st.success("Campaign data loaded successfully! Reloading application...")
        st.rerun()
    except Exception as e:
        st.error(f"Error loading data: {e}")

def add_scenario_outcome(campaign_name, scenario_name, heroes_played_data, outcome, notes, date_played):
    st.session_state.scenarios_played.append({
        "campaign": campaign_name,
        "scenario": scenario_name,
        "heroes_played": heroes_played_data,
        "outcome": outcome,
        "notes": notes,
        "date": date_played.strftime("%Y-%m-%d")
    })
    hero_names = ", ".join([h["hero"] for h in heroes_played_data if h["hero"] != "N/A (Not Selected)"])
    st.success(f"'{scenario_name}' played with '{hero_names}' recorded as {outcome} in {campaign_name}!")

def add_campaign_note(campaign_name, note, date):
    if campaign_name not in st.session_state.campaign_boons:
        st.session_state.campaign_boons[campaign_name] = []
    st.session_state.campaign_boons[campaign_name].append({
        "date": date.strftime("%Y-%m-%d"),
        "note": note
    })
    st.success(f"Note added to {campaign_name} campaign log!")

# --- Main App Function ---
def main():
    initialize_campaign_state()

    # Sidebar
    with st.sidebar:
        st.image(
            "https://raw.githubusercontent.com/D20Woodworking/MarvelChampionsCampaignTracker/main/assets/mc-logo.png",
            width=110,
        )
        st.header("👤 Player Management")
        new_player_name = st.text_input("Add Player Name:")
        if st.button("Add Player", use_container_width=True):
            if new_player_name and new_player_name not in st.session_state.players:
                st.session_state.players.append(new_player_name)
                st.success(f"Player '{new_player_name}' added!")
            elif new_player_name:
                st.warning("Player already exists or name is empty.")

        st.markdown("**Current Players:**")
        if st.session_state.players:
            st.markdown("\n".join([f"- {p}" for p in st.session_state.players]))
        else:
            st.info("No players added yet.")

        st.markdown("---")
        st.header("💾 Save / Load Data")
        st.download_button(
            label="💾 Save Campaign Progress",
            data=get_campaign_data_for_download(),
            file_name=DEFAULT_DATA_FILE_NAME,
            mime="application/json",
            help="Download your current campaign data as a backup."
        )
        uploaded_file = st.file_uploader(
            "",
            type=["mchamp"],
            label_visibility='collapsed',
            help="Upload a previously saved .mchamp campaign file."
        )
        st.caption("Accepted file type: .MCHAMP")
        if uploaded_file:
            load_campaign_data(uploaded_file)
        st.markdown("---")
        if st.button("Reset All Data", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Main Content
    st.markdown("## 🎲 Select Your Campaign")
    st.session_state.selected_campaign = st.selectbox(
        "Choose a Campaign:",
        options=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()),
        index=list(MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.keys()).index(st.session_state.selected_campaign),
    )
    is_campaign_selected = st.session_state.selected_campaign != "--- Select a Campaign ---"
    are_players_added = len(st.session_state.players) > 0
    if not is_campaign_selected or not are_players_added:
        if not is_campaign_selected:
            st.warning("Please select a campaign to begin tracking.")
        if not are_players_added:
            st.warning("Add at least one player in the sidebar.")
        st.stop()

    st.info(f"**Currently Tracking:** `{st.session_state.selected_campaign}`")
    st.markdown(f"**Players:** {' | '.join(st.session_state.players)}")
    st.markdown("---")

    # Record New Scenario
    with st.expander("➕ Record New Scenario Outcome", expanded=True):
        st.subheader("Record Scenario Result")
        num_heroes_playing = st.number_input(
            "How many heroes played?", min_value=1, max_value=4, value=st.session_state.num_heroes_input, step=1, key="num_heroes_input"
        )
        st.session_state.num_heroes_input = max(1, min(num_heroes_playing, len(st.session_state.players)))
        selected_heroes_choices = []
        cols = st.columns(st.session_state.num_heroes_input)
        for i in range(st.session_state.num_heroes_input):
            hero_choice = cols[i].selectbox(
                f"Hero {i+1}", options=MARVEL_CHAMPIONS_HEROES, key=f"hero_select_{i}")
            selected_heroes_choices.append(hero_choice)
        outcome = st.radio("Outcome", ("Win", "Loss"), horizontal=True, key="scenario_outcome")
        hero_health_inputs_for_submission = []
        if outcome == "Win":
            st.markdown("**Hero Health Remaining (for Win):**")
            cols_health = st.columns(st.session_state.num_heroes_input)
            for i, hero_name in enumerate(selected_heroes_choices):
                if hero_name != "--- Select a Hero ---":
                    health = cols_health[i].number_input(
                        f"{hero_name}", min_value=0, value=0, key=f"hero_health_{i}")
                    hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": health})
                else:
                    hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})
        else:
            for hero_name in selected_heroes_choices:
                if hero_name != "--- Select a Hero ---":
                    hero_health_inputs_for_submission.append({"hero": hero_name, "health_remaining": "N/A (Loss)"})
                else:
                    hero_health_inputs_for_submission.append({"hero": "N/A (Not Selected)", "health_remaining": "N/A"})
        with st.form("scenario_form"):
            current_campaign_scenarios = MARVEL_CHAMPIONS_CAMPAIGNS_AND_SCENARIOS.get(st.session_state.selected_campaign, [])
            selected_scenario = st.selectbox(
                "Scenario Played:",
                options=["--- Select a Scenario ---"] + current_campaign_scenarios,
                index=0,
                key="scenario_select_in_form"
            )
            scenario_notes = st.text_area("Scenario Notes (Optional)")
            scenario_date_played = st.date_input("Date Played:", datetime.date.today(), key="scenario_date")
            submit_scenario_button = st.form_submit_button("Record Scenario Outcome", type="primary")
            if submit_scenario_button:
                if selected_scenario == "--- Select a Scenario ---":
                    st.error("Select a scenario to record its outcome.")
                elif any(h == "--- Select a Hero ---" for h in selected_heroes_choices):
                    st.error("Please select all heroes used for the scenario.")
                else:
                    add_scenario_outcome(
                        st.session_state.selected_campaign,
                        selected_scenario,
                        hero_health_inputs_for_submission,
                        outcome,
                        scenario_notes,
                        scenario_date_played
                    )

    # Scenario Log
    st.markdown("## 📜 Scenario Log")
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
                else:
                    heroes_str.append(hero_info['hero'])
            display_data.append({
                "Scenario": record["scenario"],
                "Heroes Used": ", ".join(heroes_str),
                "Outcome": record["outcome"],
                "Notes": record["notes"],
                "Date": record["date"]
            })
        df_scenarios = pd.DataFrame(display_data)
        df_scenarios['Date'] = pd.to_datetime(df_scenarios['Date'])
        df_scenarios = df_scenarios.sort_values(by='Date', ascending=False).reset_index(drop=True)
        st.dataframe(df_scenarios, use_container_width=True, hide_index=True)
    else:
        st.info(f"No scenarios recorded yet for {st.session_state.selected_campaign}.")

    # Campaign Boons & Notes
    st.markdown("## 📝 Campaign Boons & Notes")
    with st.form("campaign_notes_form"):
        new_campaign_note = st.text_area("Add Campaign Note/Boon (Optional)")
        note_date = st.date_input("Date (Note):", datetime.date.today(), key="note_date_form")
        submit_note_button = st.form_submit_button("Add Campaign Note", type="secondary")
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
        df_boons['date'] = pd.to_datetime(df_boons['date'])
        df_boons = df_boons.sort_values(by='date', ascending=False).reset_index(drop=True)
        st.dataframe(df_boons, use_container_width=True, hide_index=True)
    else:
        st.info(f"No special boons or notes recorded yet for {st.session_state.selected_campaign}.")

if __name__ == "__main__":
    main()
