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


def state_forms(state: str):
    raw = (state or "").strip()
    key = raw.upper()
    if key in US_STATES:
        return key, US_STATES[key]
    for abbr, name in US_STATES.items():
        if name.lower() == raw.lower():
            return abbr, name
    return raw, raw


def unique_cards(cards):
    seen = set()
    unique = []
    for card in cards or []:
        number = re.sub(r"\s+", "", str(card.get("number") or ""))
        if not number or number in seen:
            continue
        seen.add(number)
        item = dict(card)
        item["number"] = number
        month = str(item.get("month") or "")
        if month.isdigit():
            item["month"] = month.zfill(2)
        unique.append(item)
    return unique


def card_pool(opts):
    cards = list(opts.get("cards") or [])
    if not cards and str(opts.get("card_number") or "").strip():
        cards = [{
            "name": opts.get("card_name") or "",
            "number": opts.get("card_number") or "",
            "month": opts.get("card_month") or "",
            "year": opts.get("card_year") or "",
            "cvv": opts.get("card_cvv") or "",
            "type": opts.get("card_type") or "",
        }]
    return unique_cards(cards)


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
        state_abbr, state_full = state_forms(rec["state"])
        state = state_full if opts["full_state"] else state_abbr
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
            "state_abbr": state_abbr,
            "state_full": state_full,
            "country": opts["country"] or "United States",
        }
        if opts["same_billing"]:
            bill = dict(ship)
            bill["name"] = opts["billing_name"] or ship["name"]
            bill["email"] = opts["email"] or ship["email"]
            bill["phone"] = opts["billing_phone"] or ship["phone"]
        else:
            bill_abbr, bill_full = state_forms(opts["billing_state"])
            bill = {
                "name": opts["billing_name"],
                "phone": opts["billing_phone"] or opts["phone"],
                "email": opts["email"] or opts["ship_email"],
                "line1": opts["billing_line1"],
                "line2": opts["billing_line2"],
                "line3": "",
                "zip": opts["billing_zip"],
                "city": opts["billing_city"],
                "state": bill_full if opts["full_state"] else bill_abbr,
                "state_abbr": bill_abbr,
                "state_full": bill_full,
                "country": opts["country"] or "United States",
            }
        pool = card_pool(opts)
        if index - 1 < len(pool):
            card = pool[index - 1]
            card_name = card["name"]
            card_type = card["type"]
            card_number = card["number"]
            card_month = card["month"]
            card_year = card["year"]
            card_cvv = card["cvv"]
        else:
            card_name = ""
            card_type = ""
            card_number = ""
            card_month = ""
            card_year = ""
            card_cvv = ""
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


def to_sheet_csv(names, records, opts, rows=None) -> str:
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=SHEET_COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in rows if rows is not None else export_rows(names, records, opts):
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


def to_aycd_json(names, records, opts, rows=None) -> str:
    profiles = []
    for row in rows if rows is not None else export_rows(names, records, opts):
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


def split_name(full: str):
    parts = (full or "").split()
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def digits_only(text: str) -> str:
    return re.sub(r"\D", "", text or "")


def phone_dashed(text: str) -> str:
    number = digits_only(text)
    if len(number) == 11 and number.startswith("1"):
        number = number[1:]
    if len(number) == 10:
        return f"{number[:3]}-{number[3:6]}-{number[6:]}"
    return number


def year_2(year: str) -> str:
    digits = digits_only(str(year or ""))
    if len(digits) >= 4:
        return digits[-2:]
    return digits


def year_4(year: str) -> str:
    digits = digits_only(str(year or ""))
    if len(digits) == 2:
        return "20" + digits
    return digits


def month_2(month: str) -> str:
    digits = digits_only(str(month or ""))
    if not digits:
        return ""
    return digits.zfill(2)[-2:]


def month_plain(month: str) -> str:
    digits = digits_only(str(month or ""))
    if not digits:
        return ""
    return str(int(digits))


def is_us(country: str) -> bool:
    return (country or "").strip().lower() in {
        "", "us", "usa", "united states", "united states of america",
    }


def country_code(country: str) -> str:
    return "US" if is_us(country) else (country or "").strip()


def country_name(country: str) -> str:
    return "United States" if is_us(country) else (country or "").strip()


def extra_line(block: dict) -> str:
    return " ".join(part for part in (block.get("line2") or "", block.get("line3") or "") if part).strip()


def card_label(card_type: str, style: str) -> str:
    key = normalize_card_type(card_type) if card_type else ""
    table = {
        "AmericanExpress": {"stellar": "Amex", "valor": "amex", "aycd": "AmericanExpress"},
        "Visa": {"stellar": "Visa", "valor": "visa", "aycd": "Visa"},
        "Mastercard": {"stellar": "Mastercard", "valor": "mastercard", "aycd": "Mastercard"},
        "Discover": {"stellar": "Discover", "valor": "discover", "aycd": "Discover"},
    }
    if not key:
        return ""
    return table.get(key, {}).get(style, key)


def valor_number(number: str, card_type: str) -> str:
    digits = digits_only(number)
    if card_label(card_type, "valor") == "amex" and len(digits) == 15:
        return f"{digits[:4]} {digits[4:10]} {digits[10:]}"
    if len(digits) == 16:
        return " ".join(digits[i:i + 4] for i in range(0, 16, 4))
    return digits


def to_stellar_json(rows) -> str:
    profiles = []
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        ship_first, ship_last = split_name(ship["name"])
        bill_first, bill_last = split_name(bill["name"])
        profiles.append({
            "profileName": row["profile"],
            "email": bill["email"] or row["email"],
            "phone": digits_only(ship["phone"]),
            "shipping": {
                "firstName": ship_first,
                "lastName": ship_last,
                "country": country_code(ship["country"]),
                "address": ship["line1"],
                "address2": extra_line(ship),
                "state": ship["state_abbr"],
                "city": ship["city"],
                "zipcode": ship["zip"],
            },
            "billingAsShipping": row["same_billing"],
            "oneCheckoutPerProfile": row["only_once"],
            "billing": {
                "firstName": bill_first,
                "lastName": bill_last,
                "country": country_code(bill["country"]),
                "address": bill["line1"],
                "address2": extra_line(bill),
                "state": bill["state_abbr"],
                "city": bill["city"],
                "zipcode": bill["zip"],
            },
            "payment": {
                "cardName": row["card_name"],
                "cardType": card_label(row["card_type"], "stellar"),
                "cardNumber": digits_only(row["card_number"]),
                "cardMonth": month_2(row["card_month"]),
                "cardYear": year_2(row["card_year"]),
                "cardCvv": row["card_cvv"],
            },
        })
    return json.dumps(profiles, indent=2)


def to_valor_json(rows) -> str:
    profiles = {}
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        ship_first, ship_last = split_name(ship["name"])
        bill_first, bill_last = split_name(bill["name"])
        profile_id = str(uuid.uuid4())
        profiles[profile_id] = {
            "name": row["profile"],
            "email": ship["email"] or row["email"],
            "phoneNumber": phone_dashed(ship["phone"]),
            "billingSameAsShipping": row["same_billing"],
            "oneCheckout": row["only_once"],
            "quickTask": False,
            "card": {
                "holder": row["card_name"],
                "number": valor_number(row["card_number"], row["card_type"]),
                "expiration": "/".join(
                    part for part in (month_2(row["card_month"]), year_2(row["card_year"])) if part
                ),
                "cvv": row["card_cvv"],
                "type": card_label(row["card_type"], "valor"),
            },
            "shipping": {
                "firstName": ship_first,
                "lastName": ship_last,
                "addressLine1": ship["line1"],
                "addressLine2": extra_line(ship),
                "city": ship["city"],
                "countryName": country_name(ship["country"]),
                "countryCode": country_code(ship["country"]),
                "state": ship["state_full"],
                "zipCode": ship["zip"],
            },
            "billing": {
                "firstName": bill_first,
                "lastName": bill_last,
                "addressLine1": bill["line1"],
                "addressLine2": extra_line(bill),
                "city": bill["city"],
                "countryName": country_name(bill["country"]),
                "countryCode": country_code(bill["country"]),
                "state": bill["state_full"],
                "zipCode": bill["zip"],
            },
            "id": profile_id,
            "totalSpent": 0,
        }
    return json.dumps(profiles, indent=2)


def to_alpine_json(rows) -> str:
    profiles = []
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        ship_first, ship_last = split_name(ship["name"])
        bill_first, bill_last = split_name(bill["name"])
        profiles.append({
            "name": row["profile"],
            "email": bill["email"] or row["email"],
            "phoneNumber": digits_only(ship["phone"]),
            "sameAddress": row["same_billing"],
            "shippingAddress": {
                "addressLine1": ship["line1"],
                "addressLine2": extra_line(ship),
                "city": ship["city"],
                "zip": ship["zip"],
                "region": "",
                "state": ship["state_abbr"],
                "countryCode": country_code(ship["country"]),
                "firstName": ship_first,
                "lastName": ship_last,
            },
            "billingAddress": {
                "addressLine1": bill["line1"],
                "addressLine2": extra_line(bill),
                "city": bill["city"],
                "zip": bill["zip"],
                "region": "",
                "state": bill["state_abbr"],
                "countryCode": country_code(bill["country"]),
                "firstName": bill_first,
                "lastName": bill_last,
            },
            "card": {
                "cardNumber": digits_only(row["card_number"]),
                "cvv": row["card_cvv"],
                "expiryMonth": month_2(row["card_month"]),
                "expiryYear": year_2(row["card_year"]),
            },
        })
    return json.dumps(profiles, indent=2)


def to_hidden_json(rows) -> str:
    profiles = []
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        profiles.append({
            "name": row["profile"],
            "notes": row["notes"],
            "billingAddress": {
                "name": bill["name"],
                "email": bill["email"],
                "phone": digits_only(bill["phone"]),
                "line1": bill["line1"],
                "line2": bill["line2"],
                "line3": bill["line3"],
                "postCode": bill["zip"],
                "city": bill["city"],
                "country": country_name(bill["country"]),
                "state": bill["state_full"],
            },
            "shippingAddress": {
                "name": ship["name"],
                "email": ship["email"],
                "phone": digits_only(ship["phone"]),
                "line1": ship["line1"],
                "line2": ship["line2"],
                "line3": ship["line3"],
                "postCode": ship["zip"],
                "city": ship["city"],
                "country": country_name(ship["country"]),
                "state": ship["state_full"],
            },
            "paymentDetails": {
                "nameOnCard": row["card_name"],
                "cardType": card_label(row["card_type"], "aycd"),
                "cardNumber": digits_only(row["card_number"]),
                "cardExpMonth": month_2(row["card_month"]),
                "cardExpYear": year_4(row["card_year"]),
                "cardCvv": row["card_cvv"],
            },
            "sameBillingAndShippingAddress": row["same_billing"],
            "onlyCheckoutOnce": row["only_once"],
            "matchNameOnCardAndAddress": row["match_card"],
        })
    return json.dumps(profiles, indent=2)


def to_makebot_csv(rows) -> str:
    columns = [
        "profileName", "firstName", "lastName", "email", "address1", "address2",
        "city", "state", "zipcode", "country", "phoneNumber", "ccNumber",
        "ccMonth", "ccYear", "cvv",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        ship = row["ship"]
        first, last = split_name(ship["name"])
        writer.writerow({
            "profileName": row["profile"],
            "firstName": first,
            "lastName": last,
            "email": ship["email"] or row["email"],
            "address1": ship["line1"],
            "address2": extra_line(ship),
            "city": ship["city"],
            "state": ship["state_abbr"],
            "zipcode": ship["zip"],
            "country": country_code(ship["country"]),
            "phoneNumber": digits_only(ship["phone"]),
            "ccNumber": digits_only(row["card_number"]),
            "ccMonth": month_2(row["card_month"]),
            "ccYear": year_2(row["card_year"]),
            "cvv": row["card_cvv"],
        })
    return buffer.getvalue()


def to_refract_json(rows) -> str:
    now = int(time.time() * 1000)
    profiles = []
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        ship_first, ship_last = split_name(ship["name"])
        bill_first, bill_last = split_name(bill["name"])
        profiles.append({
            "name": row["profile"],
            "email": bill["email"] or row["email"],
            "oneTimeUse": row["only_once"],
            "shipping": {
                "firstName": ship_first,
                "lastName": ship_last,
                "address1": ship["line1"],
                "address2": extra_line(ship),
                "city": ship["city"],
                "province": ship["state_full"],
                "postalCode": ship["zip"],
                "country": country_name(ship["country"]),
                "phone": digits_only(ship["phone"]),
            },
            "billing": {
                "sameAsShipping": row["same_billing"],
                "firstName": bill_first,
                "lastName": bill_last,
                "address1": bill["line1"],
                "address2": extra_line(bill),
                "city": bill["city"],
                "province": bill["state_full"],
                "postalCode": bill["zip"],
                "country": country_name(bill["country"]),
                "phone": digits_only(bill["phone"]),
            },
            "payment": {
                "name": row["card_name"],
                "num": digits_only(row["card_number"]),
                "year": year_4(row["card_year"]),
                "month": month_2(row["card_month"]),
                "cvv": row["card_cvv"],
            },
            "id": f"prf-{uuid.uuid4()}",
            "createdAt": now,
            "updatedAt": now + 1000,
        })
    return json.dumps(profiles, indent=2)


def to_shikari_csv(rows) -> str:
    columns = [
        "profile_name", "first_name", "last_name", "email", "phone_num",
        "cc_number", "cc_exp_month", "cc_exp_year", "cc_cvv",
        "shipping_street", "shipping_street_2", "shipping_city", "shipping_state",
        "shipping_zip_code", "shipping_country",
        "billing_first_name", "billing_last_name", "billing_street", "billing_street_2",
        "billing_city", "billing_state", "billing_zip_code", "billing_country",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        ship, bill = row["ship"], row["bill"]
        ship_first, ship_last = split_name(ship["name"])
        bill_first, bill_last = split_name(bill["name"])
        writer.writerow({
            "profile_name": row["profile"],
            "first_name": ship_first,
            "last_name": ship_last,
            "email": ship["email"] or row["email"],
            "phone_num": digits_only(ship["phone"]),
            "cc_number": digits_only(row["card_number"]),
            "cc_exp_month": month_plain(row["card_month"]),
            "cc_exp_year": year_4(row["card_year"]),
            "cc_cvv": row["card_cvv"],
            "shipping_street": ship["line1"],
            "shipping_street_2": extra_line(ship),
            "shipping_city": ship["city"],
            "shipping_state": ship["state_abbr"],
            "shipping_zip_code": ship["zip"],
            "shipping_country": country_code(ship["country"]),
            "billing_first_name": bill_first,
            "billing_last_name": bill_last,
            "billing_street": bill["line1"],
            "billing_street_2": extra_line(bill),
            "billing_city": bill["city"],
            "billing_state": bill["state_abbr"],
            "billing_zip_code": bill["zip"],
            "billing_country": country_code(bill["country"]),
        })
    return buffer.getvalue()


def show_results(key, names, addresses, count, opts):
    lines = pack_lines(names, addresses)
    full_text = "\n\n".join(lines)
    rows = export_rows(names, addresses, opts)
    filled = sum(1 for row in rows if row["card_number"])
    st.success(f"Generated {len(addresses)} variations")
    if filled and filled < len(rows):
        st.warning(
            f"{len(rows)} profiles and {filled} unique cards. "
            "Extra profiles have no card so a card is never repeated."
        )
    elif filled:
        st.caption(f"{filled} unique cards, one per profile. Nothing is repeated.")
    st.markdown('<p class="mv-kicker">EXPORT</p>', unsafe_allow_html=True)
    st.caption("TXT is the on-screen list. The other buttons match each site's file. Card cells stay blank when there is no unique card left.")
    exports = [
        ("Download TXT", full_text, f"{key}_variations_{count}.txt", "text/plain", f"{key}-txt"),
        ("CSV / Google Sheet", to_sheet_csv(names, addresses, opts, rows), f"{key}_variations_{count}.csv", "text/csv", f"{key}-csv"),
        ("Export AYCD", to_aycd_json(names, addresses, opts, rows), f"{key}_variations_{count}_aycd.json", "application/json", f"{key}-aycd"),
        ("Stellar", to_stellar_json(rows), f"{key}_stellar_aio.json", "application/json", f"{key}-stellar"),
        ("Valor", to_valor_json(rows), f"{key}_valor.json", "application/json", f"{key}-valor"),
        ("Alpine", to_alpine_json(rows), f"{key}_alpine_aio.json", "application/json", f"{key}-alpine"),
        ("Hidden", to_hidden_json(rows), f"{key}_hidden_aio.json", "application/json", f"{key}-hidden"),
        ("Makebot", to_makebot_csv(rows), f"{key}_makebot.csv", "text/csv", f"{key}-makebot"),
        ("Refract", to_refract_json(rows), f"{key}_refract.json", "application/json", f"{key}-refract"),
        ("Shikari", to_shikari_csv(rows), f"{key}_shikari.csv", "text/csv", f"{key}-shikari"),
    ]
    for start in range(0, len(exports), 3):
        columns = st.columns(3)
        for column, (label, data, filename, mime, button_key) in zip(columns, exports[start:start + 3]):
            with column:
                st.download_button(
                    label, data, file_name=filename, mime=mime,
                    use_container_width=True, key=button_key,
                    type="primary" if button_key.endswith("-txt") else "secondary",
                )
    st.subheader("Preview (first 10)")
    st.text("\n\n".join(lines[:10]))
    with st.expander(f"View all {len(addresses)} variations"):
        st.text_area("All results", full_text, height=400, key=f"{key}-all")


