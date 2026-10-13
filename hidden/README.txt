Jig options
===========

This folder is the switch box. Edit jig_options.json, then reboot the app.
These four keys are live. true turns that switch on the next fresh session.

name_initial   First name becomes an initial, like J. SMITH
name_suffix    Adds JR, SR, II, or III
unit_line      Adds Apt, Unit, Suite, Ste, Floor, or #
zip_plus4      Adds a ZIP+4, like 19720-4412

The sidebar expander named "Jig options" uses these as the starting values.
A choice you click in the app overrides the file until you reboot.

Not wired yet. Add one of these next if you want more control:

street_type_mix     Sometimes St, sometimes Street, sometimes Str
city_nickname       NYC, LA, or SF when the city is one of those
zip_last4           Show the ZIP as -9720 instead of 97224
directionals        Stick N, S, E, or W on the street line
tight_spacing       Remove the spaces in the street line

Leave city/state swaps and name anagrams out. They stop looking like the real address.
