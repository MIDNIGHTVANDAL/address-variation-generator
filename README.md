# Address Variation Generator

Created by Midnightvandal.

Two tabs, same batch sizes (50, 100, 250, 500, 1000, 5000):

- **Target** — word+digit house number and junk letters on the street.
- **Best Buy** — junk prefix on the house number, nudged street name, spelled-out street type with one inserted letter, an extra code line, and a doubled vowel in the city.

The address box starts empty. Placeholder text is "Enter address".

## Run it

```bash
pip install -r requirements.txt
streamlit run address_variator_app.py
```

On Windows, double-click `run_app.bat`.

## Live link

Deploy this repo on [Streamlit Community Cloud](https://share.streamlit.io) with main file `address_variator_app.py`. New commits update the live app.
