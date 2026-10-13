# ---------- UI ----------
st.set_page_config(page_title="Address Variation Generator", layout="wide", page_icon="MV")
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@500;600;700&display=swap');
    .stApp {
        background:
            radial-gradient(1200px 500px at 10% -10%, rgba(255, 30, 140, 0.22), transparent 55%),
            radial-gradient(900px 420px at 100% 0%, rgba(110, 40, 255, 0.18), transparent 50%),
            linear-gradient(180deg, #07040c 0%, #100814 45%, #07040c 100%);
        color: #f4e9f7;
        font-family: 'Rajdhani', sans-serif;
    }
    h1, h2, h3, [data-testid="stSidebar"] h2 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.06em;
    }
    h1 { color: #ff4db8 !important; text-shadow: 0 0 18px rgba(255, 45, 149, 0.45); }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #120816 0%, #09060e 100%);
        border-right: 1px solid rgba(255, 45, 149, 0.28);
    }
    .stTextArea textarea, .stTextInput input, [data-baseweb="select"] > div {
        background: #140a18 !important;
        color: #fff !important;
        border: 1px solid rgba(255, 45, 149, 0.45) !important;
        border-radius: 12px !important;
    }
    .stButton > button, .stDownloadButton > button,
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-secondary"] {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        border-radius: 16px !important;
        min-height: 3.2rem !important;
        border: 1px solid rgba(255, 77, 184, 0.7) !important;
    }
    .stButton > button, button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(120deg, #ff2d95 0%, #b026ff 55%, #6a1bff 100%) !important;
        color: #fff !important;
    }
    .stDownloadButton > button, button[data-testid="stBaseButton-secondary"] {
        background: linear-gradient(160deg, #1a0d22 0%, #2a1038 100%) !important;
        color: #ffd6f2 !important;
    }
    .mv-kicker {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        color: #ff7ac8;
        margin: 0 0 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

head_l, head_r = st.columns([1, 5])
with head_l:
    if IMAGE_PATH:
        st.image(IMAGE_PATH, width=80)
with head_r:
    st.title("Address Variation Generator")
    st.caption("Created by Midnightvandal")

with st.sidebar:
    st.header("Name Settings")
    first_mode_label = st.radio("First Name", ["Fixed", "Random (store item)", "Blank"], index=1)
    fixed_first = st.text_input("Fixed First Name", value="LAPTOP", disabled=(first_mode_label != "Fixed"))
    last_mode_label = st.radio("Last Name", ["Fixed", "Random (One-Twenty)", "Blank"], index=1)
    fixed_last = st.text_input("Fixed Last Name", value="ONE", disabled=(last_mode_label != "Fixed"))
    st.header("Batch")
    count = st.selectbox("Number of variations", COUNTS, index=1)

target_tab, bestbuy_tab = st.tabs(["Target", "Best Buy"])

with target_tab:
    st.markdown('<p class="mv-kicker">TARGET</p>', unsafe_allow_html=True)
    st.caption("Word+digit house number, junk letters on the street name and spelled-out street type.")
    junk_len = st.slider("Junk letter length", 1, 4, 2, key="t-junk")
    include_dash = st.checkbox("Include dash separator", value=True, key="t-dash")
    extra_spaces = st.checkbox("Extra spaces in the street line", value=False, key="t-space")
    case_style = st.selectbox("Case style", ["mixed", "upper", "lower"], index=0, key="t-case")
    target_address = st.text_area("Enter address", value="", height=80, placeholder="Enter address", key="t-addr")
    if st.button("GENERATE VARIATIONS", type="primary", use_container_width=True, key="t-go"):
        if not target_address.strip():
            st.error("Please enter an address.")
        else:
            try:
                addresses = generate_target(
                    target_address.strip(), count, junk_len, include_dash, extra_spaces, case_style,
                )
                names = generate_names(len(addresses), name_mode(first_mode_label), name_mode(last_mode_label), fixed_first, fixed_last)
                st.session_state["target_out"] = (names, addresses)
            except Exception as exc:
                st.error(str(exc))
    if "target_out" in st.session_state:
        show_results("target", *st.session_state["target_out"], count)

with bestbuy_tab:
    st.markdown('<p class="mv-kicker">BEST BUY</p>', unsafe_allow_html=True)
    st.caption("Junk prefix on the house number, nudged street name, spelled-out type with one inserted letter, extra code line, doubled vowel in the city.")
    bb_address = st.text_area("Enter address", value="", height=80, placeholder="Enter address", key="b-addr")
    if st.button("GENERATE VARIATIONS", type="primary", use_container_width=True, key="b-go"):
        if not bb_address.strip():
            st.error("Please enter an address.")
        else:
            try:
                addresses = generate_bestbuy(bb_address.strip(), count)
                names = generate_names(len(addresses), name_mode(first_mode_label), name_mode(last_mode_label), fixed_first, fixed_last)
                st.session_state["bb_out"] = (names, addresses)
            except Exception as exc:
                st.error(str(exc))
    if "bb_out" in st.session_state:
        show_results("bestbuy", *st.session_state["bb_out"], count)
