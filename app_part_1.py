def _title_word(word: str) -> str:
    if not word:
        return word
    return word[0].upper() + word[1:].lower()


def mutate_street_name(name: str) -> str:
    """Cirillo -> CiRyllo: keep ends, capitalize one interior letter, swap another."""
    chars = list(_title_word(name))
    if len(chars) < 3:
        return "".join(chars)
    interior = list(range(1, len(chars) - 1))
    cap_at = random.choice(interior)
    chars[cap_at] = chars[cap_at].upper()
    others = [i for i in interior if i != cap_at]
    if others:
        swap_at = random.choice(others)
        current = chars[swap_at].lower()
        chars[swap_at] = LETTER_SWAPS.get(current, "x" if current != "x" else "z")
    return "".join(chars)


def mutate_street_type(stype: str) -> str:
    """Cir -> Circle -> CirRcle. Spell it out, insert one capital after the first 3 letters."""
    word = _title_word(expand_street_type(stype).lower())
    if len(word) < 4:
        word = (word + "xx")[:4]
    return word[:3] + random_junk(1) + word[3:]


def double_first_vowel(word: str) -> str:
    """New -> Neew, Castle -> Caastle."""
    for i, ch in enumerate(word):
        if ch.lower() in "aeiou":
            return word[: i + 1] + ch.lower() + word[i + 1 :]
    return word


def format_bestbuy(parts) -> str:
    street = mutate_street_name(parts["street_name"])
    stype = mutate_street_type(parts["street_type"])
    city = " ".join(double_first_vowel(w) for w in parts["city"].split())
    line1 = f"{random_junk(3, 'abcdefghijklmnopqrstuvwxyz')}{parts['house']} {street} {stype}"
    line2 = f"{random_junk(4)} {random.randint(1000, 9999)}"
    line3 = f"{city}, {parts['state']} {parts['zip']}"
    return f"{line1}\n{line2}\n{line3}"


def generate_bestbuy(address, count):
    parts = parse_address(address)
    return [format_bestbuy(parts) for _ in range(count)]


def get_first_name(mode, fixed=""):
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    if mode == "random":
        return random.choice(STORE_ITEMS).upper()
    return ""


def get_last_name(mode, fixed=""):
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    if mode == "random":
        base = random.choice(NUMBER_WORDS)
        if random.random() < 0.3:
            return base + str(random.randint(1, 9))
        return base
    return ""


def generate_names(count, first_mode, last_mode, fixed_first, fixed_last):
    names = []
    for _ in range(count):
        first = get_first_name(first_mode, fixed_first)
        last = get_last_name(last_mode, fixed_last)
        names.append(" ".join(p for p in (first, last) if p))
    return names


def name_mode(label):
    if label == "Fixed":
        return "fixed"
    if "Random" in label:
        return "random"
    return "blank"


def pack_lines(names, addresses):
    lines = []
    for name, addr in zip(names, addresses):
        lines.append(f"{name}\n{addr}" if name else addr)
    return lines


def to_csv(names, addresses):
    rows = ["Name,Address"]
    for name, addr in zip(names, addresses):
        rows.append(f'"{name.replace(chr(34), chr(34)*2)}","{addr.replace(chr(34), chr(34)*2)}"')
    return "\n".join(rows)


def show_results(key, names, addresses, count):
    lines = pack_lines(names, addresses)
    full_text = "\n\n".join(lines)
    st.success(f"Generated {len(addresses)} variations")
    st.markdown('<p class="mv-kicker">EXPORT</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "Download TXT", full_text, file_name=f"{key}_variations_{count}.txt",
            mime="text/plain", use_container_width=True, type="primary", key=f"{key}-txt",
        )
    with col2:
        st.download_button(
            "Download CSV", to_csv(names, addresses), file_name=f"{key}_variations_{count}.csv",
            mime="text/csv", use_container_width=True, key=f"{key}-csv",
        )
    st.subheader("Preview (first 10)")
    st.text("\n\n".join(lines[:10]))
    with st.expander(f"View all {len(addresses)} variations"):
        st.text_area("All results", full_text, height=400, key=f"{key}-all")
