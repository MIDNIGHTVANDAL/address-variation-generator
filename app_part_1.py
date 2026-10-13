
    return {
        "house": house,
        "street_name": street_name,
        "street_type": street_type,
        "city": city,
        "state": state,
        "zip": zipcode,
    }

def format_variation(parts: dict, junk1: str, junk2: str,
                     include_dash: bool = True,
                     extra_spaces: bool = False,
                     case_style: str = "mixed") -> str:
    house_word = number_to_word_digit(parts["house"])
    street_name = parts["street_name"].replace(" ", "")
    stype = expand_street_type(parts["street_type"])

    sep = " - " if include_dash else " "
    space = "  " if extra_spaces else " "

    line = f"{house_word}{sep}{junk1}{street_name}{space}{junk2}{stype} {parts['city']}, {parts['state']}, {parts['zip']}"

    if case_style == "upper":
        line = line.upper()
    elif case_style == "lower":
        line = line.lower()
    return line

def generate_address_variations(address: str, count: int,
                                junk_len: int = 2,
                                include_dash: bool = True,
                                extra_spaces: bool = False,
                                case_style: str = "mixed") -> list[str]:
    parts = parse_address(address)
    results = []
    used = set()
    attempts = 0
    max_attempts = count * 30
    while len(results) < count and attempts < max_attempts:
        attempts += 1
        j1 = random_junk(junk_len)
        j2 = random_junk(junk_len)
        key = (j1, j2)
        if key in used and len(used) < (26 ** max(junk_len, 1)):
            continue
        used.add(key)
        results.append(format_variation(parts, j1, j2, include_dash, extra_spaces, case_style))
    return results

def get_first_name(mode: str, fixed: str = "") -> str:
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    elif mode == "random":
        return random.choice(STORE_ITEMS).upper()
    else:
        return ""

def get_last_name(mode: str, fixed: str = "") -> str:
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    elif mode == "random":
        base = random.choice(NUMBER_WORDS)
        if random.random() < 0.3:
            return base + str(random.randint(1, 9))
        return base
    else:
        return ""

def generate_names(count: int, first_mode: str, last_mode: str,
                   fixed_first: str = "", fixed_last: str = "") -> list[str]:
    names = []
    for _ in range(count):
        f = get_first_name(first_mode, fixed_first)
        l = get_last_name(last_mode, fixed_last)
        if f and l:
            names.append(f"{f} {l}")
        elif f:
            names.append(f)
        elif l:
            names.append(l)
        else:
            names.append("")
    return names

st.set_page_config(page_title="Address Variation Generator", layout="wide", page_icon="MV")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;800&family=Rajdhani:wght@500;600;700&display=swap');

    .stApp {
        background:
            radial-gradient(1200px 500px at 10% -10%, rgba(255, 30, 140, 0.22), transparent 55%),
            radial-gradient(900px 420px at 100% 0%, rgba(110, 40, 255, 0.22), transparent 50%),
            linear-gradient(180deg, #07040c 0%, #100814 45%, #07040c 100%);
        color: #f4e9f7;
        font-family: 'Rajdhani', sans-serif;
    }
    h1, h2, h3, [data-testid="stSidebar"] h2 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 0.06em;
    }
    h1 { color: #ff4db8 !important; text-shadow: 0 0 18px rgba(255, 45, 149, 0.45); }
    [data-testid="stCaptionContainer"] { color: #c9a6d4 !important; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #120816 0%, #09060e 100%);
        border-right: 1px solid rgba(255, 45, 149, 0.28);
    }
    [data-testid="stSidebar"] * { color: #f3e7f6; }

    .stTextArea textarea, .stTextInput input, [data-baseweb="select"] > div {
        background: #140a18 !important;
        color: #fff !important;
        border: 1px solid rgba(255, 45, 149, 0.45) !important;
        border-radius: 12px !important;
        box-shadow: inset 0 0 12px rgba(255, 45, 149, 0.08);
    }

    .stButton > button, .stDownloadButton > button,
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-secondary"] {
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 77, 184, 0.7) !important;
        padding: 0.85rem 1.2rem !important;
        min-height: 3.4rem !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, filter 0.18s ease !important;
        box-shadow:
            0 0 0 1px rgba(255, 45, 149, 0.15),
            0 8px 24px rgba(0, 0, 0, 0.45),
            0 0 22px rgba(255, 45, 149, 0.28) !important;
    }
    .stButton > button, button[data-testid="stBaseButton-primary"] {
        background: linear-gradient(120deg, #ff2d95 0%, #b026ff 55%, #6a1bff 100%) !important;
        color: #fff !important;
    }
    .stDownloadButton > button, button[data-testid="stBaseButton-secondary"] {
        background: linear-gradient(160deg, #1a0d22 0%, #2a1038 100%) !important;
        color: #ffd6f2 !important;
    }
    .stButton > button:hover, .stDownloadButton > button:hover,
    button[data-testid="stBaseButton-primary"]:hover,
    button[data-testid="stBaseButton-secondary"]:hover {
