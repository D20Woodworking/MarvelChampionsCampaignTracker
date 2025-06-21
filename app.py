with st.expander("➕ Record New Scenario Outcome", expanded=True):
    st.subheader("Record Scenario Result")
    # Set the correct max allowed heroes based on players
    max_heroes_allowed = min(4, len(st.session_state.players)) if len(st.session_state.players) > 0 else 1
    # Clamp session value before drawing widget
    if st.session_state.num_heroes_input > max_heroes_allowed:
        st.session_state.num_heroes_input = max_heroes_allowed

    num_heroes_playing = st.number_input(
        "How many heroes played?",
        min_value=1,
        max_value=max_heroes_allowed,
        value=st.session_state.num_heroes_input,
        step=1,
        key="num_heroes_input"
    )

    selected_heroes_choices = []
    cols = st.columns(st.session_state.num_heroes_input)
    for i in range(st.session_state.num_heroes_input):
        hero_choice = cols[i].selectbox(
            f"Hero {i+1}", options=MARVEL_CHAMPIONS_HEROES, key=f"hero_select_{i}")
        selected_heroes_choices.append(hero_choice)
    # ... rest of your block
