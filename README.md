# Address Variation Generator

Created by Midnightvandal.

Two tabs, same batch sizes (50, 100, 250, 500, 1000, 5000):

- **Target** — word+digit house number and junk letters on the street.
- **Best Buy** — junk prefix on the house number, nudged street name, spelled-out street type with one inserted letter, an extra code line, and a doubled vowel in the city.

The app asks for a password before it opens. The password is not stored in this repo.

## Set the password on Streamlit Cloud

1. Open the app on [share.streamlit.io](https://share.streamlit.io).
2. Settings, then Secrets.
3. Paste this and replace the password, then Save:

```toml
APP_PASSWORD = "choose-a-password"
```

4. Reboot the app. Visitors only see an Unlock box until they enter that password.

## Run it on your computer

```bash
pip install -r requirements.txt
streamlit run address_variator_app.py
```

Create `.streamlit/secrets.toml` in this folder with the same `APP_PASSWORD` line. That file stays on your machine.
