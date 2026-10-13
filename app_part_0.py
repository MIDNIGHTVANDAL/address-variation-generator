#!/usr/bin/env python3
"""
Address Variation Generator
Created by Midnightvandal

Target tab: word+digit house number, junk letters on the street.
Best Buy tab: the Cirillo label pattern.
"""

import os
import random
import re

import streamlit as st

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

STREET_TYPES = {
    "ALY": "ALLEY", "AVE": "AVENUE", "BLVD": "BOULEVARD", "CIR": "CIRCLE",
    "CT": "COURT", "DR": "DRIVE", "EXPY": "EXPRESSWAY", "HWY": "HIGHWAY",
    "LN": "LANE", "PKWY": "PARKWAY", "PL": "PLACE", "RD": "ROAD",
    "ST": "STREET", "TER": "TERRACE", "TRL": "TRAIL", "WAY": "WAY",
    "PLZ": "PLAZA", "SQ": "SQUARE", "LOOP": "LOOP", "RUN": "RUN",
    "PASS": "PASS", "PATH": "PATH", "ROW": "ROW", "WALK": "WALK",
}

COUNTS = [50, 100, 250, 500, 1000, 5000]
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


def parse_address(addr: str):
    addr = " ".join(addr.replace(",", " ").split()).strip()
    zip_match = re.search(r"\b(\d{5})(?:-\d{4})?\b\s*$", addr)
    zipcode = zip_match.group(1) if zip_match else ""
    if zip_match:
        addr = addr[:zip_match.start()].strip()

    tokens = addr.split()
    if len(tokens) < 4:
        raise ValueError("Need a house number, street, city, and state.")

    house = tokens[0] if re.match(r"^\d+", tokens[0]) else ""
    rest = tokens[1:] if house else tokens
    state = rest[-1].upper() if rest else ""
    rest = rest[:-1]

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


def format_target(parts, junk1, junk2, include_dash, extra_spaces, case_style) -> str:
    sep = " - " if include_dash else " "
    gap = "  " if extra_spaces else " "
    line = (
        f"{number_to_word_digit(parts['house'])}{sep}{junk1}{parts['street_name'].replace(' ', '')}"
        f"{gap}{junk2}{expand_street_type(parts['street_type'])} "
        f"{parts['city']}, {parts['state']}, {parts['zip']}"
    )
    if case_style == "upper":
        return line.upper()
    if case_style == "lower":
        return line.lower()
    return line


def generate_target(address, count, junk_len, include_dash, extra_spaces, case_style):
    parts = parse_address(address)
    results = []
    used = set()
    attempts = 0
    while len(results) < count and attempts < count * 40:
        attempts += 1
        j1, j2 = random_junk(junk_len), random_junk(junk_len)
        if (j1, j2) in used and len(used) < 26 ** max(junk_len, 1):
            continue
        used.add((j1, j2))
        results.append(format_target(parts, j1, j2, include_dash, extra_spaces, case_style))
    while len(results) < count:
        results.append(format_target(
            parts, random_junk(junk_len), random_junk(junk_len),
            include_dash, extra_spaces, case_style,
        ))
    return results
