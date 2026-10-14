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

import streamlit.components.v1 as components

_prefs_component = components.declare_component(
    "mv_prefs",
    path=os.path.join(SCRIPT_DIR, "mv_prefs"),
)
_hidden_jig = load_hidden_jig()
PREF_DEFAULTS = {
    "first_mode": "Random (store item)",
    "fixed_first": "",
    "last_mode": "Random (One-Twenty)",
    "fixed_last": "",
    "batch_count": 100,
    "jig-initial": bool(_hidden_jig["name_initial"]),
    "jig-suffix": bool(_hidden_jig["name_suffix"]),
    "jig-unit": bool(_hidden_jig["unit_line"]),
    "jig-zip4": bool(_hidden_jig["zip_plus4"]),
    "profile_prefix": "Address",
    "jig_names": True,
    "full_state": True,
    "country": "United States",
    "email": "",
    "ship_email": "",
    "phone": "",
    "size_value": "",
    "notes": "",
    "only_once": False,
    "same_billing": False,
    "match_card": False,
    "bill-name": "",
    "bill-phone": "",
    "bill-line": "",
    "bill-line2": "",
    "bill-city": "",
    "bill-state": "",
    "bill-zip": "",
    "t-addr": "",
    "b-addr": "",
    "t-junk": 2,
    "t-dash": True,
    "t-space": False,
    "t-case": "mixed",
    "b-code": True,
    "b-letters": 4,
    "b-digits": 4,
    "b-regular": True,
    "b-vowel": True,
}
_loaded_prefs = _prefs_component(action="load", payload={}, key="mv_prefs_load", default=None)
if isinstance(_loaded_prefs, dict) and "data" in _loaded_prefs and not st.session_state.get("prefs_applied"):
    _saved = _loaded_prefs.get("data") or {}
    if isinstance(_saved, dict) and _saved:
        for _key, _value in _saved.items():
            if _key in PREF_DEFAULTS:
                st.session_state[_key] = _value
        if "batch_count" in st.session_state:
            st.session_state["batch_count"] = max(1, min(int(st.session_state["batch_count"]), MAX_VARIATIONS))
        st.session_state["prefs_applied"] = True
        st.rerun()
    else:
        st.session_state["prefs_applied"] = True
for _key, _default in PREF_DEFAULTS.items():
    if _key not in st.session_state:
        st.session_state[_key] = _default

with st.sidebar:
    st.header("Saved fields")
    st.caption("Save once in this browser. Next visit fills the addresses and contact fields back in. Card numbers are not saved.")
    _prefs_now = {key: st.session_state.get(key) for key in PREF_DEFAULTS}
    save_col, clear_col = st.columns(2)
    with save_col:
        if st.button("Save my fields", use_container_width=True):
            _prefs_component(action="save", payload=_prefs_now, key="mv_prefs_save")
            st.success("Saved in this browser.")
    with clear_col:
        if st.button("Clear saved", use_container_width=True):
            _prefs_component(action="clear", payload={}, key="mv_prefs_clear")
            st.info("Cleared. This visit stays as it is.")
    st.download_button(
        "Download fields file",
        json.dumps(_prefs_now, indent=2),
        file_name="my_fields.json",
        mime="application/json",
        use_container_width=True,
        key="prefs-download",
    )
    fields_file = st.file_uploader("Load a fields file", type=["json"], key="fields-json")
    if fields_file is not None:
        token = f"{fields_file.name}:{getattr(fields_file, 'size', 0)}"
        if st.session_state.get("fields_token") != token:
            loaded_fields = json.loads(fields_file.getvalue().decode("utf-8-sig"))
            if isinstance(loaded_fields, dict):
                for key, value in loaded_fields.items():
                    if key in PREF_DEFAULTS:
                        st.session_state[key] = value
                st.session_state["fields_token"] = token
                st.session_state["prefs_applied"] = True
                st.rerun()
    st.header("Name Settings")
    first_mode_label = st.radio(
        "First Name",
        ["Fixed", "Random (store item)", "Random (real 1st name)", "Blank"],
        key="first_mode",
    )
    fixed_first = st.text_input(
        "Fixed First Name",
        placeholder="Input name here",
        key="fixed_first",
        disabled=(first_mode_label != "Fixed"),
    )
    last_mode_label = st.radio(
        "Last Name",
        ["Fixed", "Random (One-Twenty)", "Random (real last name)", "Blank"],
        key="last_mode",
    )
    fixed_last = st.text_input(
        "Fixed Last Name",
        placeholder="Input name here",
        key="fixed_last",
        disabled=(last_mode_label != "Fixed"),
    )
    st.header("Batch")
    count = st.number_input(
        "Number of variations",
        min_value=1,
        max_value=MAX_VARIATIONS,
        step=1,
        help="Any number from 1 to 20,000. Each line is unique.",
        key="batch_count",
    )
    with st.expander("Jig options"):
        st.caption("Off unless you turn them on. Starting values come from hidden/jig_options.json.")
        jig_initial = st.checkbox("First name as an initial", key="jig-initial")
        jig_suffix = st.checkbox("Add a name suffix (Jr, Sr, II, III)", key="jig-suffix")
        jig_unit = st.checkbox("Add a unit line (Apt, Unit, Suite, #)", key="jig-unit")
        jig_zip4 = st.checkbox("Add ZIP+4", key="jig-zip4")
    jig = {
        "name_initial": jig_initial,
        "name_suffix": jig_suffix,
        "unit_line": jig_unit,
        "zip_plus4": jig_zip4,
    }
    st.header("Export fields")
    st.caption("Blank until you type them. Generated name and address fill the shipping columns.")
    profile_prefix = st.text_input("Profile name starts with", key="profile_prefix")
    jig_names = st.checkbox("Jig each profile name", key="jig_names")
    full_state = st.checkbox("Spell out state names", key="full_state")
    country = st.text_input("Country", key="country")
    email = st.text_input("Email", key="email")
    ship_email = st.text_input("Shipping email, if different", key="ship_email")
    phone = st.text_input("Phone", key="phone")
    size_value = st.text_input("Size (optional)", key="size_value")
    notes = st.text_input("AYCD notes", key="notes")
    only_once = st.checkbox("Only one checkout", key="only_once")
    same_billing = st.checkbox("Same billing and shipping", key="same_billing")
    match_card = st.checkbox("Match name on card and address", key="match_card")
    with st.expander("Billing and card, optional"):
        billing_name = st.text_input("Billing name", key="bill-name")
        billing_phone = st.text_input("Billing phone", key="bill-phone")
        billing_line1 = st.text_input("Billing address", key="bill-line")
        billing_line2 = st.text_input("Billing address 2", key="bill-line2")
        billing_city = st.text_input("Billing city", key="bill-city")
        billing_state = st.text_input("Billing state", key="bill-state")
        billing_zip = st.text_input("Billing ZIP", key="bill-zip")
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
        card_file = st.file_uploader(
            "Upload cards CSV",
            type=["csv"],
            key=f"card-file-{st.session_state.get('upload_nonce', 0)}",
            help="Columns: Name on Card, Card Number, Expiration Month, Expiration Year, Card CVV, Card Type, Card State.",
        )
    uploaded_cards = []
    if card_file is not None:
        try:
            parsed_cards = parse_card_csv(card_file.getvalue().decode("utf-8-sig", errors="replace"))
            uploaded_cards = unique_cards(parsed_cards)
            skipped = len(parsed_cards) - len(uploaded_cards)
            st.caption(
                f"{len(uploaded_cards)} unique cards. Each profile gets the next card, once. "
                "Full numbers are only in the download."
            )
            if skipped:
                st.caption(f"{skipped} duplicate card numbers were skipped.")
            for card in uploaded_cards[:8]:
                st.text(f"{card['type'] or 'Card'} ····{card['number'][-4:]}  {card['name']}")
            if len(uploaded_cards) > 8:
                st.caption(f"and {len(uploaded_cards) - 8} more")
        except Exception as exc:
            st.error(str(exc))
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
        "cards": uploaded_cards,
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
        st.session_state["upload_nonce"] = st.session_state.get("upload_nonce", 0) + 1
        st.rerun()

target_tab, bestbuy_tab = st.tabs(["Target", "Best Buy"])

with target_tab:
    st.markdown('<p class="mv-kicker">TARGET</p>', unsafe_allow_html=True)
    st.caption("One address per line, up to 10. Word+digit house number, junk letters, spelled-out street type.")
    junk_len = st.slider("Junk letter length", 1, 4, key="t-junk")
    include_dash = st.checkbox("Include dash separator", key="t-dash")
    extra_spaces = st.checkbox("Extra spaces in the street line", key="t-space")
    case_style = st.selectbox("Case style", ["mixed", "upper", "lower"], key="t-case")
    target_address = st.text_area(
        "Enter address", height=140,
        placeholder="Enter address\nOne per line, up to 10",
        key="t-addr",
    )
    if st.button("GENERATE VARIATIONS", type="primary", use_container_width=True, key="t-go"):
        if not target_address.strip():
            st.error("Please enter an address.")
        else:
            try:
                chosen = split_addresses(target_address)
                addresses = generate_target(
                    chosen, int(count), junk_len, include_dash, extra_spaces, case_style, jig,
                )
                names = [
                    apply_name_jig(name, jig)
                    for name in generate_names(
                        len(addresses), name_mode(first_mode_label), name_mode(last_mode_label),
                        fixed_first, fixed_last,
                    )
                ]
                st.session_state["target_out"] = (names, addresses)
            except Exception as exc:
                st.error(str(exc))
    if "target_out" in st.session_state:
        show_results("target", *st.session_state["target_out"], count, export_opts)

with bestbuy_tab:
    st.markdown('<p class="mv-kicker">BEST BUY</p>', unsafe_allow_html=True)
    st.caption("One address per line, up to 10. Junk prefix, nudged street, spelled-out type.")
    code_on = st.checkbox("Include extra code line", key="b-code")
    code_letters = st.slider("Code letters", 0, 8, key="b-letters", disabled=not code_on)
    code_digits = st.slider("Code digits", 0, 8, key="b-digits", disabled=not code_on)
    use_regular_city = st.checkbox("Regular city spelling", key="b-regular")
    use_doubled_city = st.checkbox("Extra vowel in the city", key="b-vowel")
    if use_regular_city and use_doubled_city:
        city_mode = "both"
    elif use_doubled_city:
        city_mode = "doubled"
    else:
        city_mode = "regular"
    bb_address = st.text_area(
        "Enter address", height=140,
        placeholder="Enter address\nOne per line, up to 10",
        key="b-addr",
    )
    if st.button("GENERATE VARIATIONS", type="primary", use_container_width=True, key="b-go"):
        if not bb_address.strip():
            st.error("Please enter an address.")
        else:
            try:
                chosen = split_addresses(bb_address)
                addresses = generate_bestbuy(
                    chosen, int(count), code_on, int(code_letters), int(code_digits), city_mode, jig,
                )
                names = [
                    apply_name_jig(name, jig)
                    for name in generate_names(
                        len(addresses), name_mode(first_mode_label), name_mode(last_mode_label),
                        fixed_first, fixed_last,
                    )
                ]
                st.session_state["bb_out"] = (names, addresses)
            except Exception as exc:
                st.error(str(exc))
    if "bb_out" in st.session_state:
        show_results("bestbuy", *st.session_state["bb_out"], count, export_opts)
