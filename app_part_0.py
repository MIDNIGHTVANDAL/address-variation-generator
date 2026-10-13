#!/usr/bin/env python3
"""
Address Variation Generator
Created by Midnightvandal

Streamlit web app for generating large batches of custom address variations
with configurable store-item first names and number-based last names.
"""

import streamlit as st
import re
import random
import os

# ---------- Branding image ----------
# Looks for midnightvandal.png in the same folder as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "midnightvandal.png")
if not os.path.exists(IMAGE_PATH):
    IMAGE_PATH = None  # fallback if not found

# ---------- Core data ----------
STORE_ITEMS = [
    "Laptop", "Coffee", "Shirt", "Headphones", "Keyboard", "Mouse", "Monitor",
    "Tablet", "Phone", "Charger", "Backpack", "Watch", "Sunglasses", "Shoes",
    "Jacket", "Hat", "Socks", "Mug", "Bottle", "Notebook", "Pen", "Pencil",
    "Eraser", "Ruler", "Glue", "Scissors", "Stapler", "Folder", "Binder",
    "Calendar", "Clock", "Lamp", "Pillow", "Blanket", "Towel", "Soap",
    "Shampoo", "Toothbrush", "Toothpaste", "Deodorant", "Lotion", "Perfume",
    "Candle", "Incense", "Plant", "Vase", "Picture", "Frame", "Mirror",
    "Rug", "Curtain", "Blinds", "Fan", "Heater", "Vacuum", "Broom", "Mop",
    "Bucket", "Sponge", "Detergent", "Bleach", "Trash", "Bag", "Box", "Tape",
    "Scissors", "Knife", "Fork", "Spoon", "Plate", "Bowl", "Cup", "Glass",
    "Pitcher", "Pan", "Pot", "Oven", "Microwave", "Toaster", "Blender",
    "Mixer", "Fridge", "Freezer", "Dishwasher", "Washer", "Dryer", "Iron",
    "Board", "Hanger", "Closet", "Shelf", "Drawer", "Desk", "Chair", "Table",
    "Sofa", "Bed", "Mattress", "Pillow", "Sheet", "Comforter", "Duvet",
    "Curtain", "Rod", "Hook", "Nail", "Screw", "Hammer", "Wrench", "Pliers",
    "Drill", "Saw", "Level", "Tape", "Measure", "Flashlight", "Battery",
    "Cable", "Adapter", "Router", "Modem", "Speaker", "Camera", "Lens",
    "Tripod", "Microphone", "Stand", "Light", "Diffuser", "Filter", "Case"
]

NUMBER_WORDS = [
    "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE", "TEN",
    "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN", "SEVENTEEN",
    "EIGHTEEN", "NINETEEN", "TWENTY"
]

STREET_TYPES = {
    "ALY": "ALLEY", "AVE": "AVENUE", "BLVD": "BOULEVARD", "CIR": "CIRCLE",
    "CT": "COURT", "DR": "DRIVE", "EXPY": "EXPRESSWAY", "HWY": "HIGHWAY",
    "LN": "LANE", "PKWY": "PARKWAY", "PL": "PLACE", "RD": "ROAD",
    "ST": "STREET", "TER": "TERRACE", "TRL": "TRAIL", "WAY": "WAY",
    "PLZ": "PLAZA", "SQ": "SQUARE", "LOOP": "LOOP", "RUN": "RUN",
    "PASS": "PASS", "PATH": "PATH", "ROW": "ROW", "WALK": "WALK",
}

def number_to_word_digit(num_str: str) -> str:
    if not num_str or not num_str.isdigit():
        return num_str
    first = num_str[0]
    word_map = {"1": "ONE", "2": "TWO", "3": "THREE", "4": "FOUR", "5": "FIVE",
                "6": "SIX", "7": "SEVEN", "8": "EIGHT", "9": "NINE", "0": "ZERO"}
    word = word_map.get(first, first)
    return f"{word}{num_str}"

def expand_street_type(stype: str) -> str:
    stype = stype.upper().rstrip(".,")
    return STREET_TYPES.get(stype, stype)

def random_junk(length: int = 2) -> str:
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=length))

def parse_address(addr: str):
    """
    Robust parser for common US address formats.
    Handles:
      15504 SW 144TH TER Portland OR 97224
      1 Lafayette Rd Hampton NH 03842
      123 Main Street Anytown CA 90210
    """
    # Normalize
    addr = " ".join(addr.replace(",", " ").split()).strip()
    
    # Extract ZIP
    zip_match = re.search(r"\b(\d{5})(?:-\d{4})?\b\s*$", addr)
    zipcode = zip_match.group(1) if zip_match else ""
    if zip_match:
        addr = addr[:zip_match.start()].strip()

    tokens = addr.split()
    if len(tokens) < 4:
        raise ValueError("Address too short. Need at least: number street city state")

    # House number = first token if numeric
    house = tokens[0] if re.match(r"^\d+", tokens[0]) else ""
    rest = tokens[1:] if house else tokens

    # State = last token (usually 2 letters)
    state = rest[-1].upper() if rest else ""
    rest = rest[:-1]

    # Directionals
    dirs = {"N", "S", "E", "W", "NE", "NW", "SE", "SW",
            "NORTH", "SOUTH", "EAST", "WEST", "NORTHEAST", "NORTHWEST",
            "SOUTHEAST", "SOUTHWEST"}

    # Known street types (abbreviated and full)
    street_type_keys = set(STREET_TYPES.keys()) | {
        "TERRACE", "ROAD", "STREET", "AVENUE", "DRIVE", "LANE", "COURT",
        "BOULEVARD", "CIRCLE", "PLACE", "WAY", "TRAIL", "HIGHWAY"
    }

    # Walk from the end of remaining tokens looking for street type
    street_type = ""
    street_name_parts = []
    city_parts = []

    # Find the rightmost token that looks like a street type
    stype_idx = -1
    for i in range(len(rest) - 1, -1, -1):
        tok = rest[i].upper().rstrip(".")
        if tok in street_type_keys or tok in STREET_TYPES:
            stype_idx = i
            street_type = tok
            break

    if stype_idx >= 0:
        # Everything before street type is street name (minus directional)
        before = rest[:stype_idx]
        after = rest[stype_idx + 1:]
        
        # Remove leading directional if present
        if before and before[0].upper() in dirs:
            before = before[1:]
        
        street_name_parts = before
        city_parts = after
    else:
        # Fallback: assume last token before state is street type
        if rest:
            street_type = rest[-1].upper()
            street_name_parts = rest[:-1]
            # still strip directional
            if street_name_parts and street_name_parts[0].upper() in dirs:
                street_name_parts = street_name_parts[1:]
            city_parts = []

    street_name = "".join(street_name_parts).upper() if street_name_parts else "MAIN"
    city = " ".join(city_parts).title() if city_parts else "Unknown"

    # Clean street type
    street_type = street_type.upper().rstrip(".")
