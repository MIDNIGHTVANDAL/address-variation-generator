import pathlib

_here = pathlib.Path(__file__).resolve().parent
_src = "".join(
    (_here / name).read_text(encoding="utf-8")
    for name in ("app_part_0.py", "app_part_1.py", "app_part_2.py")
)
exec(
    compile(_src, str(_here / "address_variator_app.py"), "exec"),
    {"__name__": "__main__", "__file__": str(_here / "address_variator_app.py")},
)
