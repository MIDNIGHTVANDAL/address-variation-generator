#!/usr/bin/env python3
"""
Address Variation Generator
Created by Midnightvandal

Target tab: word+digit house number, junk letters on the street.
Best Buy tab: the Cirillo label pattern.
"""

import json
import os
import random
import re
import time
import uuid
from io import StringIO
import csv

import jsonschema
import streamlit as st
import usaddress

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "midnightvandal.png")
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = None

STORE_ITEMS = [
    "Laptop", "Coffee", "Shirt", "Headphones", "Keyboard", "Mouse", "Monitor",
    "Tablet", "Phone", "Charger", "Backpack", "Watch", "Sunglasses", "Shoes",
    "Jacket", "Hat", "Socks", "Mug", "Bottle", "Notebook", "Pen", "Pencil",
    "Calendar", "Clock", "Lamp", "Pillow", "Blanket", "Towel", "Candle",
    "Plant", "Mirror", "Camera", "Speaker", "Router", "Cable", "Drill",
    "Desk", "Chair", "Table", "Sofa", "Mixer", "Toaster", "Blender",
    "Dishwasher", "Pitcher", "Flashlight", "Battery", "Case",
]

NUMBER_WORDS = [
    "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN",
    "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
    "EIGHTEEN", "NINETEEN", "TWENTY",
]

# SSA most common given names, 50 male and 50 female.
FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Christopher", "Karen", "Charles", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Andrew", "Emily", "Paul", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Raymond", "Christine", "Gregory", "Debra",
    "Alexander", "Rachel", "Patrick", "Carolyn", "Frank", "Janet", "Dennis", "Catherine",
    "Jerry", "Maria", "Tyler", "Heather",
]

# US Census most common surnames.
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez",
]

STREET_TYPES = {
    "ALY": "ALLEY", "AVE": "AVENUE", "BLVD": "BOULEVARD", "CIR": "CIRCLE",
    "CT": "COURT", "DR": "DRIVE", "EXPY": "EXPRESSWAY", "HWY": "HIGHWAY",
    "LN": "LANE", "PKWY": "PARKWAY", "PL": "PLACE", "RD": "ROAD",
    "ST": "STREET", "TER": "TERRACE", "TRL": "TRAIL", "WAY": "WAY",
    "PLZ": "PLAZA", "SQ": "SQUARE", "LOOP": "LOOP", "RUN": "RUN",
    "PASS": "PASS", "PATH": "PATH", "ROW": "ROW", "WALK": "WALK",
}

COUNTS = [50, 100, 250, 500, 1000, 5000]
MAX_VARIATIONS = 20000
MAX_ADDRESSES = 10
UNIT_TYPES = ["Apt", "Unit", "#", "Suite", "Ste", "Floor"]
NAME_SUFFIXES = ["JR", "SR", "II", "III"]
HIDDEN_JIG = {
    "name_initial": False,
    "name_suffix": False,
    "unit_line": False,
    "zip_plus4": False,
}
LETTER_SWAPS = {"a": "e", "e": "a", "i": "y", "o": "u", "u": "o", "y": "i"}


def number_to_word_digit(num_str: str) -> str:
    if not num_str or not num_str.isdigit():
        return num_str
    word_map = {
        "1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR", "5": "FIVE",
        "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE", "0": "ZERO",
    }
    return f"{word_map.get(num_str[0], num_str[0])}{num_str}"


def expand_street_type(stype: str) -> str:
    key = stype.upper().rstrip(".,")
    return STREET_TYPES.get(key, key)


def random_junk(length: int = 2, letters: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ") -> str:
    return "".join(random.choices(letters, k=length))


def peel_state(tokens):
    """Only a real state name or abbreviation leaves the city. Square stays in Newtown Square."""
    if not tokens:
        return "", tokens
    by_name = {name.upper(): abbr for abbr, name in US_STATES.items()}

    def take(count, abbr):
        return abbr, tokens[:-count]

    if len(tokens) >= 3:
        three = " ".join(tok.upper().rstrip(".") for tok in tokens[-3:])
        if three in by_name:
            return take(3, by_name[three])
    if len(tokens) >= 2:
        two = " ".join(tok.upper().rstrip(".") for tok in tokens[-2:])
        if two in by_name:
            return take(2, by_name[two])
    last = tokens[-1].upper().rstrip(".")
    if last in US_STATES:
        return take(1, last)
    if last in by_name:
        return take(1, by_name[last])
    return "", tokens


def abbreviate_state(raw: str) -> str:
    text = (raw or "").strip().rstrip(".")
    key = text.upper()
    if key in US_STATES:
        return key
    for abbr, name in US_STATES.items():
        if name.upper() == key:
            return abbr
    return key


def _parse_with_usaddress(addr: str):
    try:
        tagged, _kind = usaddress.tag(addr)
    except (usaddress.RepeatedLabelError, Exception):
        return None
    house = (tagged.get("AddressNumber") or "").strip()
    street = "".join((tagged.get("StreetName") or "").split()).upper()
    street_type = (tagged.get("StreetNamePostType") or "").upper().rstrip(".")
    city = " ".join((tagged.get("PlaceName") or "").split()).title()
    state = abbreviate_state(tagged.get("StateName") or "")
    zipcode = re.sub(r"\D", "", tagged.get("ZipCode") or "")[:5]
    if not house or not street or not city:
        return None
    if not street_type:
        street_type = "ST"
    return {
        "house": house,
        "street_name": street,
        "street_type": street_type,
        "city": city,
        "state": state if state in US_STATES else "",
        "zip": zipcode,
    }


def parse_address(addr: str):
    cleaned = " ".join(addr.replace(",", " ").split()).strip()
    parsed = _parse_with_usaddress(cleaned)
    if parsed:
        return parsed
    return _parse_address_tokens(cleaned)


def _parse_address_tokens(addr: str):
    addr = " ".join(addr.replace(",", " ").split()).strip()
    zip_match = re.search(r"\b(\d{5})(?:-\d{4})?\b\s*$", addr)
    zipcode = zip_match.group(1) if zip_match else ""
    if zip_match:
        addr = addr[:zip_match.start()].strip()

    tokens = addr.split()
    if len(tokens) < 4:
        raise ValueError("Need a house number, street, and city.")

    house = tokens[0] if re.match(r"^\d+", tokens[0]) else ""
    rest = tokens[1:] if house else tokens
    state, rest = peel_state(rest)

    dirs = {
        "N", "S", "E", "W", "NE", "NW", "SE", "SW",
        "NORTH", "SOUTH", "EAST", "WEST", "NORTHEAST", "NORTHWEST",
        "SOUTHEAST", "SOUTHWEST",
    }
    type_keys = set(STREET_TYPES) | {
        "TERRACE", "ROAD", "STREET", "AVENUE", "DRIVE", "LANE", "COURT",
        "BOULEVARD", "CIRCLE", "PLACE", "WAY", "TRAIL", "HIGHWAY",
    }

    stype_idx = -1
    street_type = ""
    for i in range(len(rest) - 1, -1, -1):
        tok = rest[i].upper().rstrip(".")
        if tok in type_keys:
            stype_idx = i
            street_type = tok
            break

    if stype_idx >= 0:
        name_parts = rest[:stype_idx]
        city_parts = rest[stype_idx + 1:]
        if name_parts and name_parts[0].upper() in dirs:
            name_parts = name_parts[1:]
    else:
        street_type = rest[-1].upper() if rest else "ST"
        name_parts = rest[:-1]
        if name_parts and name_parts[0].upper() in dirs:
            name_parts = name_parts[1:]
        city_parts = []

    return {
        "house": house,
        "street_name": "".join(name_parts).upper() if name_parts else "MAIN",
        "street_type": street_type.upper().rstrip("."),
        "city": " ".join(city_parts).title() if city_parts else "Unknown",
        "state": state,
        "zip": zipcode,
    }


def load_hidden_jig():
    path = os.path.join(SCRIPT_DIR, "hidden", "jig_options.json")
    options = dict(HIDDEN_JIG)
    try:
        with open(path, encoding="utf-8") as handle:
            saved = json.load(handle)
        for key in options:
            if key in saved:
                options[key] = bool(saved[key])
    except Exception:
        pass
    return options


def split_addresses(raw: str):
    lines = [line.strip() for line in raw.splitlines() if line.strip()]
    if not lines:
        raise ValueError("Please enter an address.")
    if len(lines) > MAX_ADDRESSES:
        raise ValueError(f"Use {MAX_ADDRESSES} addresses or fewer. Put one address on each line.")
    return lines


def spread_count(total: int, groups: int):
    base, extra = divmod(total, groups)
    return [base + (1 if index < extra else 0) for index in range(groups)]


def render_text(rec) -> str:
    city = rec["city"]
    state = (rec.get("state") or "").strip()
    zipcode = (rec.get("zip") or "").strip()
    if rec.get("kind") == "bestbuy":
        tail = " ".join(part for part in (state, zipcode) if part)
        loc = f"{city}, {tail}" if tail else city
        lines = [rec["line1"]]
        if rec.get("line2"):
            lines.append(rec["line2"])
        if rec.get("line3"):
            lines.append(rec["line3"])
        lines.append(loc)
        return "\n".join(lines)
    extra = f" {rec['line2']}" if rec.get("line2") else ""
    if state and zipcode:
        loc = f"{city}, {state}, {zipcode}"
    elif zipcode:
        loc = f"{city}, {zipcode}"
    elif state:
        loc = f"{city}, {state}"
    else:
        loc = city
    return f"{rec['line1']}{extra} {loc}"


def apply_line_jig(rec, jig):
    rec = dict(rec)
    if jig.get("zip_plus4") and rec["zip"].isdigit() and len(rec["zip"]) == 5:
        rec["zip"] = f"{rec['zip']}-{random.randint(1000, 9999)}"
    if jig.get("unit_line"):
        unit = f"{random.choice(UNIT_TYPES)} {random.randint(1, 999)}"
        if rec.get("kind") == "bestbuy" and rec.get("line2"):
            rec["line3"] = unit
        else:
            rec["line2"] = unit
    rec["text"] = render_text(rec)
    return rec


def apply_name_jig(name, jig):
    if not name:
        return name
    parts = name.split()
    if jig.get("name_initial") and parts and len(parts[0]) > 1:
        parts[0] = parts[0][0] + "."
    if jig.get("name_suffix"):
        parts.append(random.choice(NAME_SUFFIXES))
    return " ".join(parts)


def format_target(parts, junk1, junk2, include_dash, extra_spaces, case_style) -> dict:
    sep = " - " if include_dash else " "
    gap = "  " if extra_spaces else " "
    street_line = (
        f"{number_to_word_digit(parts['house'])}{sep}{junk1}{parts['street_name'].replace(' ', '')}"
        f"{gap}{junk2}{expand_street_type(parts['street_type'])}"
    )
    city = parts["city"]
    state = parts["state"]
    zipcode = parts["zip"]
    if case_style == "upper":
        street_line, city, state = street_line.upper(), city.upper(), state.upper()
    elif case_style == "lower":
        street_line, city, state = street_line.lower(), city.lower(), state.lower()
    rec = {
        "kind": "target",
        "line1": street_line.strip(),
        "line2": "",
        "line3": "",
        "city": city,
        "state": state,
        "zip": zipcode,
    }
    rec["text"] = render_text(rec)
    return rec


def _take_unique(count, build):
    seen = set()
    results = []
    attempts = 0
    limit = max(count * 60, 200)
    while len(results) < count and attempts < limit:
        attempts += 1
        rec = build(attempts)
        if rec["text"] in seen:
            continue
        seen.add(rec["text"])
        results.append(rec)
    if len(results) < count:
        raise RuntimeError(
            f"Only {len(results)} unique variations fit these settings. Turn on a jig option or lengthen the junk or code line."
        )
    return results


def generate_target(addresses, count, junk_len, include_dash, extra_spaces, case_style, jig):
    quotas = spread_count(count, len(addresses))
    seen = set()
    results = []
    for address, qty in zip(addresses, quotas):
        if qty == 0:
            continue
        parts = parse_address(address)

        def build(attempt, parts=parts, qty=qty):
            extra = 0
            if attempt > max(qty * 8, 400):
                extra = 1
            if attempt > max(qty * 25, 2000):
                extra = 2
            rec = format_target(
                parts,
                random_junk(junk_len + extra),
                random_junk(junk_len + extra),
                include_dash,
                extra_spaces,
                case_style,
            )
            return apply_line_jig(rec, jig)

        batch = _take_unique(qty, build)
        for rec in batch:
            if rec["text"] in seen:
                raise RuntimeError("Two of the addresses produced the same line. Change one of them.")
            seen.add(rec["text"])
        results.extend(batch)
    return results


