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


def spell_city(city: str, mode: str) -> str:
    if mode == "doubled":
        return " ".join(double_first_vowel(word) for word in city.split())
    return city


def format_bestbuy(parts, code_on=True, code_letters=4, code_digits=4, city_mode="both") -> dict:
    street = mutate_street_name(parts["street_name"])
    stype = mutate_street_type(parts["street_type"])
    city = spell_city(parts["city"], "doubled" if city_mode == "doubled" else "regular")
    line1 = f"{random_junk(3, 'abcdefghijklmnopqrstuvwxyz')}{parts['house']} {street} {stype}"
    line2 = ""
    if code_on and (code_letters or code_digits):
        letters = random_junk(code_letters) if code_letters else ""
        digits = f"{random.randint(0, 10 ** code_digits - 1):0{code_digits}d}" if code_digits else ""
        line2 = " ".join(part for part in (letters, digits) if part)
    rec = {
        "kind": "bestbuy",
        "line1": line1,
        "line2": line2,
        "line3": "",
        "city": city,
        "state": parts["state"],
        "zip": parts["zip"],
    }
    rec["text"] = render_text(rec)
    return rec


def generate_bestbuy(addresses, count, code_on, code_letters, code_digits, city_mode, jig):
    quotas = spread_count(count, len(addresses))
    seen = set()
    results = []
    for address, qty in zip(addresses, quotas):
        if qty == 0:
            continue
        parts = parse_address(address)
        seq = {"n": 0}

        def build(attempt, parts=parts, qty=qty):
            letters = code_letters + (1 if attempt > max(qty * 12, 800) else 0)
            mode = city_mode
            if city_mode == "both":
                mode = "regular" if seq["n"] % 2 == 0 else "doubled"
            seq["n"] += 1
            rec = format_bestbuy(parts, code_on, letters, code_digits, mode)
            return apply_line_jig(rec, jig)

        batch = _take_unique(qty, build)
        for rec in batch:
            if rec["text"] in seen:
                raise RuntimeError("Two of the addresses produced the same line. Change one of them.")
            seen.add(rec["text"])
        results.extend(batch)
    return results


def get_first_name(mode, fixed=""):
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    if mode in ("store", "random"):
        return random.choice(STORE_ITEMS).upper()
    if mode == "real":
        return random.choice(FIRST_NAMES).upper()
    return ""


def get_last_name(mode, fixed=""):
    if mode == "fixed" and fixed.strip():
        return fixed.strip().upper()
    if mode in ("number", "random"):
        return random.choice(NUMBER_WORDS)
    if mode == "real":
        return random.choice(LAST_NAMES).upper()
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
    if "store" in label.lower():
        return "store"
    if "One-Twenty" in label:
        return "number"
    if "real" in label.lower():
        return "real"
    if "Random" in label:
        return "random"
    return "blank"


def pack_lines(names, addresses):
    lines = []
    for name, addr in zip(names, addresses):
        text = addr["text"] if isinstance(addr, dict) else addr
        lines.append(f"{name}\n{text}" if name else text)
    return lines


US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
    "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
    "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
    "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
    "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
    "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia",
    "WA": "Washington", "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
}

SHEET_COLUMNS = [
    "Email Address", "Profile Name", "Only One Checkout", "Name on Card", "Card Type",
    "Card Number", "Expiration Month", "Expiration Year", "CVV", "Same Billing/Shipping",
    "Shipping Name", "Shipping Phone", "Shipping Address", "Shipping Address 2",
    "Shipping Address 3", "Shipping Post Code", "Shipping City", "Shipping State",
    "Shipping Country", "Billing Name", "Billing Phone", "Billing Address",
    "Billing Address 2", "Billing Address 3", "Billing Post Code", "Billing City",
    "Billing State", "Billing Country", "Size (Optional)",
]


def spell_state(state: str, full: bool) -> str:
    raw = (state or "").strip()
    key = raw.upper()
    if full:
        return US_STATES.get(key, raw)
    return key if key in US_STATES else raw


def jig_profile_name(prefix: str) -> str:
    alphabet = "0123456789abcdef"
    def tok(n):
        return "".join(random.choices(alphabet, k=n))
    base = prefix.strip() or "Address"
    return f"{base}-@{tok(3)}-#{tok(3)}-%{tok(3)}-&{tok(3)}-@{tok(3)}-%{tok(3)}"


def normalize_card_type(raw: str) -> str:
    key = " ".join((raw or "").strip().lower().split())
    return {
        "visa": "Visa",
        "mastercard": "Mastercard",
        "master card": "Mastercard",
        "mc": "Mastercard",
        "amex": "AmericanExpress",
        "american express": "AmericanExpress",
        "americanexpress": "AmericanExpress",
        "discover": "Discover",
    }.get(key, (raw or "").strip())


def parse_card_csv(text: str):
    sample = text.lstrip("\ufeff")
    reader = csv.DictReader(StringIO(sample))
    if not reader.fieldnames:
        raise ValueError("The card file needs a header row.")
    fields = {name.strip().lower(): name for name in reader.fieldnames if name}

    def col(row, *names):
        for name in names:
            key = fields.get(name)
            if key and row.get(key):
                return str(row[key]).strip()
        return ""

    cards = []
    for row in reader:
        number = re.sub(r"\s+", "", col(row, "card number"))
        if not number:
            continue
        status = col(row, "card state").lower()
        if status and status not in {"active", "yes", "true"}:
            continue
        month = col(row, "expiration month")
        if month.isdigit():
            month = month.zfill(2)
        cards.append({
            "name": col(row, "name on card"),
            "number": number,
            "month": month,
            "year": col(row, "expiration year"),
            "cvv": col(row, "card cvv", "cvv"),
            "type": normalize_card_type(col(row, "card type")),
        })
    if not cards:
        raise ValueError("No cards found. The file needs a Card Number column.")
    return cards


def export_rows(names, records, opts):
    rows = []
    for index, (name, rec) in enumerate(zip(names, records), start=1):
        state = spell_state(rec["state"], opts["full_state"])
        ship = {
            "name": name,
            "phone": opts["phone"],
            "email": opts["ship_email"] or opts["email"],
            "line1": rec["line1"],
            "line2": rec["line2"],
            "line3": rec["line3"],
            "zip": rec["zip"],
            "city": rec["city"],
            "state": state,
            "country": opts["country"] or "United States",
        }
        if opts["same_billing"]:
            bill = dict(ship)
            bill["name"] = opts["billing_name"] or ship["name"]
            bill["email"] = opts["email"] or ship["email"]
            bill["phone"] = opts["billing_phone"] or ship["phone"]
        else:
            bill = {
                "name": opts["billing_name"],
                "phone": opts["billing_phone"] or opts["phone"],
                "email": opts["email"] or opts["ship_email"],
                "line1": opts["billing_line1"],
                "line2": opts["billing_line2"],
                "line3": "",
                "zip": opts["billing_zip"],
                "city": opts["billing_city"],
                "state": spell_state(opts["billing_state"], opts["full_state"]) if opts["billing_state"] else "",
                "country": opts["country"] or "United States",
            }
        cards = opts.get("cards") or []
        if cards:
            card = cards[(index - 1) % len(cards)]
            card_name = card["name"]
            card_type = card["type"]
            card_number = card["number"]
            card_month = card["month"]
            card_year = card["year"]
            card_cvv = card["cvv"]
        else:
            card_name = opts["card_name"]
            card_type = opts["card_type"]
            card_number = opts["card_number"]
            card_month = opts["card_month"]
            card_year = opts["card_year"]
            card_cvv = opts["card_cvv"]
        if opts["match_card"] and not card_name:
            card_name = bill["name"] or ship["name"]
        profile = jig_profile_name(opts["prefix"]) if opts["jig_names"] else f"{opts['prefix'].strip() or 'Address'} {index}"
        rows.append({
            "profile": profile,
            "ship": ship,
            "bill": bill,
            "card_name": card_name,
            "card_type": card_type,
            "card_number": card_number,
            "card_month": card_month,
            "card_year": card_year,
            "card_cvv": card_cvv,
            "notes": opts["notes"],
            "size": opts["size"],
            "only_once": opts["only_once"],
            "same_billing": opts["same_billing"],
            "match_card": opts["match_card"],
            "email": opts["email"] or ship["email"],
        })
    return rows


def to_sheet_csv(names, records, opts) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=SHEET_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in export_rows(names, records, opts):
        ship, bill = row["ship"], row["bill"]
        writer.writerow({
            "Email Address": row["email"],
            "Profile Name": row["profile"],
            "Only One Checkout": "true" if row["only_once"] else "false",
            "Name on Card": row["card_name"],
            "Card Type": row["card_type"],
            "Card Number": row["card_number"],
            "Expiration Month": row["card_month"],
            "Expiration Year": row["card_year"],
            "CVV": row["card_cvv"],
            "Same Billing/Shipping": "true" if row["same_billing"] else "false",
            "Shipping Name": ship["name"],
            "Shipping Phone": ship["phone"],
            "Shipping Address": ship["line1"],
            "Shipping Address 2": ship["line2"],
            "Shipping Address 3": ship["line3"],
            "Shipping Post Code": ship["zip"],
            "Shipping City": ship["city"],
            "Shipping State": ship["state"],
            "Shipping Country": ship["country"],
            "Billing Name": bill["name"],
            "Billing Phone": bill["phone"],
            "Billing Address": bill["line1"],
            "Billing Address 2": bill["line2"],
            "Billing Address 3": bill["line3"],
            "Billing Post Code": bill["zip"],
            "Billing City": bill["city"],
            "Billing State": bill["state"],
            "Billing Country": bill["country"],
            "Size (Optional)": row["size"],
        })
    return buffer.getvalue()


def to_aycd_json(names, records, opts) -> str:
    profiles = []
    for row in export_rows(names, records, opts):
        ship, bill = row["ship"], row["bill"]
        profiles.append({
            "name": row["profile"],
            "notes": row["notes"],
            "billingAddress": {
                "name": bill["name"],
                "email": bill["email"],
                "phone": bill["phone"],
                "line1": bill["line1"],
                "line2": bill["line2"],
                "line3": bill["line3"],
                "postCode": bill["zip"],
                "city": bill["city"],
                "country": bill["country"],
                "state": bill["state"],
            },
            "shippingAddress": {
                "name": ship["name"],
                "email": ship["email"],
                "phone": ship["phone"],
                "line1": ship["line1"],
                "line2": ship["line2"],
                "line3": ship["line3"],
                "postCode": ship["zip"],
                "city": ship["city"],
                "country": ship["country"],
                "state": ship["state"],
            },
            "paymentDetails": {
                "nameOnCard": row["card_name"],
                "cardType": row["card_type"],
                "cardNumber": row["card_number"],
                "cardExpMonth": row["card_month"],
                "cardExpYear": row["card_year"],
                "cardCvv": row["card_cvv"],
            },
            "sameBillingAndShippingAddress": row["same_billing"],
            "onlyCheckoutOnce": row["only_once"],
            "matchNameOnCardAndAddress": row["match_card"],
        })
    return json.dumps(profiles, indent=2)


def show_results(key, names, addresses, count, opts):
    lines = pack_lines(names, addresses)
    full_text = "\n\n".join(lines)
    st.success(f"Generated {len(addresses)} variations")
    st.markdown('<p class="mv-kicker">EXPORT</p>', unsafe_allow_html=True)
    st.caption("TXT is the on-screen list. CSV/Google Sheet uses the spreadsheet columns. AYCD is the profile JSON. Card and billing cells stay blank unless you fill Export fields.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "Download TXT", full_text, file_name=f"{key}_variations_{count}.txt",
            mime="text/plain", use_container_width=True, type="primary", key=f"{key}-txt",
        )
    with col2:
        st.download_button(
            "CSV / Google Sheet", to_sheet_csv(names, addresses, opts),
            file_name=f"{key}_variations_{count}.csv",
            mime="text/csv", use_container_width=True, key=f"{key}-csv",
        )
    with col3:
        st.download_button(
            "Export AYCD", to_aycd_json(names, addresses, opts),
            file_name=f"{key}_variations_{count}.json",
            mime="application/json", use_container_width=True, key=f"{key}-aycd",
        )
    st.subheader("Preview (first 10)")
    st.text("\n\n".join(lines[:10]))
    with st.expander(f"View all {len(addresses)} variations"):
        st.text_area("All results", full_text, height=400, key=f"{key}-all")


