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
    .mv-banner {
        display: flex;
        gap: 16px;
        align-items: center;
        padding: 8px 4px 14px;
    }
    .mv-banner h1 { margin: 0 !important; font-size: 1.7rem !important; }
    .mv-mark { flex: 0 0 auto; filter: drop-shadow(0 0 12px rgba(255, 45, 149, 0.55)); }
    .mv-lock-note {
        font-size: 0.92rem;
        line-height: 1.35;
        color: #e7c6ea;
        margin: 0.4rem 0 0.55rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def app_password() -> str:
    try:
        return str(st.secrets["APP_PASSWORD"]).strip()
    except Exception:
        return os.environ.get("APP_PASSWORD", "").strip()


_saved_password = app_password()
if not st.session_state.get("authed"):
    st.title("Address Variation Generator")
    st.caption("Created by Midnightvandal")
    if not _saved_password:
        st.error("This app is locked. Add APP_PASSWORD in Streamlit secrets, then reboot.")
        st.stop()
    entered = st.text_input("Password", type="password")
    if st.button("Unlock", type="primary"):
        if entered == _saved_password:
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Wrong password.")
    st.stop()

head_l, head_r = st.columns([1, 5])
with head_l:
    if IMAGE_PATH:
        st.image(IMAGE_PATH, width=80)
with head_r:
    st.markdown(
        """
        <div class="mv-banner">
          <svg class="mv-mark" width="74" height="74" viewBox="0 0 74 74" fill="none" aria-hidden="true">
            <circle cx="37" cy="37" r="34" stroke="#ff4db8" stroke-width="2"/>
            <path d="M18 32c4-12 34-12 38 0v8c-2 16-36 16-38 0v-8z" fill="#1a0b22" stroke="#ff7ac8"/>
            <path d="M22 30c3-8 27-8 30 0" stroke="#b026ff" stroke-width="2"/>
            <circle cx="29" cy="36" r="3" fill="#ff4db8"/>
            <circle cx="45" cy="36" r="3" fill="#ff4db8"/>
            <path d="M30 46h14" stroke="#ffd6f2" stroke-width="2"/>
          </svg>
          <div>
            <p class="mv-kicker">MIDNIGHTVANDAL</p>
            <h1>Address Variation Generator</h1>
            <p class="mv-kicker">TARGET · BEST BUY · AYCD · SHEET</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.sidebar:
    st.header("Name Settings")
    first_mode_label = st.radio(
        "First Name",
        ["Fixed", "Random (store item)", "Random (real 1st name)", "Blank"],
        index=1,
    )
    fixed_first = st.text_input("Fixed First Name", value="LAPTOP", disabled=(first_mode_label != "Fixed"))
    last_mode_label = st.radio(
        "Last Name",
        ["Fixed", "Random (One-Twenty)", "Random (real last name)", "Blank"],
        index=1,
    )
    fixed_last = st.text_input("Fixed Last Name", value="ONE", disabled=(last_mode_label != "Fixed"))
    st.header("Batch")
    count = st.selectbox("Number of variations", COUNTS, index=1)
    st.header("Export fields")
    st.caption("Blank until you type them. Generated name and address fill the shipping columns.")
    profile_prefix = st.text_input("Profile name starts with", value="Address")
    jig_names = st.checkbox("Jig each profile name", value=True)
    full_state = st.checkbox("Spell out state names", value=True)
    country = st.text_input("Country", value="United States")
    email = st.text_input("Email", value="")
    ship_email = st.text_input("Shipping email, if different", value="")
    phone = st.text_input("Phone", value="")
    size_value = st.text_input("Size (optional)", value="")
    notes = st.text_input("AYCD notes", value="")
    only_once = st.checkbox("Only one checkout", value=False)
    same_billing = st.checkbox("Same billing and shipping", value=False)
    match_card = st.checkbox("Match name on card and address", value=False)
    with st.expander("Billing and card, optional"):
        billing_name = st.text_input("Billing name", value="", key="bill-name")
        billing_phone = st.text_input("Billing phone", value="", key="bill-phone")
        billing_line1 = st.text_input("Billing address", value="", key="bill-line")
        billing_line2 = st.text_input("Billing address 2", value="", key="bill-line2")
        billing_city = st.text_input("Billing city", value="", key="bill-city")
        billing_state = st.text_input("Billing state", value="", key="bill-state")
        billing_zip = st.text_input("Billing ZIP", value="", key="bill-zip")
        card_name = st.text_input("Name on card", value="", key="card-name")
        card_type = st.selectbox(
            "Card type",
            ["", "Visa", "Mastercard", "AmericanExpress", "Discover"],
            key="card-type",
        )
        card_number = st.text_input("Card number", value="", key="card-number")
        card_month = st.text_input("Expiration month", value="", key="card-month")
        card_year = st.text_input("Expiration year", value="", key="card-year")
        card_cvv = st.text_input("CVV", value="", type="password", key="card-cvv")
    export_opts = {
        "prefix": profile_prefix,
        "jig_names": jig_names,
        "full_state": full_state,
        "country": country,
        "email": email.strip(),
        "ship_email": ship_email.strip(),
        "phone": phone.strip(),
        "size": size_value.strip(),
        "notes": notes.strip(),
        "only_once": only_once,
        "same_billing": same_billing,
        "match_card": match_card,
        "billing_name": billing_name.strip(),
        "billing_phone": billing_phone.strip(),
        "billing_line1": billing_line1.strip(),
        "billing_line2": billing_line2.strip(),
        "billing_city": billing_city.strip(),
        "billing_state": billing_state.strip(),
        "billing_zip": billing_zip.strip(),
        "card_name": card_name.strip(),
        "card_type": card_type,
        "card_number": card_number.strip(),
        "card_month": card_month.strip(),
        "card_year": card_year.strip(),
        "card_cvv": card_cvv.strip(),
    }
    st.divider()
    st.markdown(
        """
        <svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true">
          <rect x="6" y="12" width="16" height="12" rx="2" fill="#ff4db8"/>
          <path d="M9 12V9a5 5 0 0 1 10 0v3" stroke="#ffd6f2" stroke-width="2" fill="none"/>
        </svg>
        <p class="mv-lock-note">Lock signs this browser out and brings the password box back. The list on screen is cleared.</p>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Lock", use_container_width=True):
        st.session_state["authed"] = False
        st.session_state.pop("target_out", None)
        st.session_state.pop("bb_out", None)
        st.rerun()

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
        show_results("target", *st.session_state["target_out"], count, export_opts)

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
        show_results("bestbuy", *st.session_state["bb_out"], count, export_opts)
