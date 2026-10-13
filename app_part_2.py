        transform: translateY(-3px) scale(1.015) !important;
        filter: brightness(1.12);
        box-shadow:
            0 0 0 1px rgba(255, 180, 230, 0.45),
            0 14px 32px rgba(0, 0, 0, 0.5),
            0 0 36px rgba(255, 45, 149, 0.7) !important;
    }
    .stButton > button:active, .stDownloadButton > button:active {
        transform: translateY(0) scale(0.99) !important;
    }
    [data-testid="stRadio"] label, [data-testid="stCheckbox"] label {
        font-family: 'Rajdhani', sans-serif !important;
        letter-spacing: 0.04em;
    }
    .mv-kicker {
        font-family: 'Orbitron', sans-serif;
        font-size: 0.72rem;
        letter-spacing: 0.28em;
        color: #ff7ac8;
        margin: 0 0 0.35rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

col_img, col_title = st.columns([1, 5])
with col_img:
    if IMAGE_PATH and os.path.exists(IMAGE_PATH):
        st.image(IMAGE_PATH, width=80)
with col_title:
    st.title("Address Variation Generator")
    st.caption("Created by Midnightvandal")

st.markdown('<p class="mv-kicker">SOURCE ADDRESS</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Name Settings")
    first_mode = st.radio(
        "First Name",
        ["Fixed", "Random (store item)", "Blank"],
        index=1,
    )
    fixed_first = st.text_input("Fixed First Name", value="LAPTOP", disabled=(first_mode != "Fixed"))
    last_mode = st.radio(
        "Last Name",
        ["Fixed", "Random (One-Twenty)", "Blank"],
        index=1,
    )
    fixed_last = st.text_input("Fixed Last Name", value="ONE", disabled=(last_mode != "Fixed"))
    st.header("Variation Settings")
    num_options = [50, 100, 250, 500, 1000, 5000]
    count = st.selectbox("Number of variations", num_options, index=1)
    junk_len = st.slider("Junk letter length", 1, 4, 2)
    include_dash = st.checkbox("Include ' - ' separator", value=True)
    extra_spaces = st.checkbox("Extra spaces in street line", value=False)
    case_style = st.selectbox("Case style", ["mixed", "upper", "lower"], index=0)

address_input = st.text_area(
    "Enter real address",
    value="",
    height=80,
    placeholder="15504 SW 144TH TER Portland OR 97224",
    help="Example: 15504 SW 144TH TER Portland OR 97224",
)

if st.button("GENERATE VARIATIONS", type="primary", use_container_width=True):
    if not address_input.strip():
        st.error("Please enter an address.")
    else:
        with st.spinner(f"Generating {count} variations..."):
            try:
                addresses = generate_address_variations(
                    address_input.strip(),
                    count,
                    junk_len=junk_len,
                    include_dash=include_dash,
                    extra_spaces=extra_spaces,
                    case_style=case_style,
                )
                f_mode = "fixed" if first_mode == "Fixed" else ("random" if "Random" in first_mode else "blank")
                l_mode = "fixed" if last_mode == "Fixed" else ("random" if "Random" in last_mode else "blank")
                names = generate_names(len(addresses), f_mode, l_mode, fixed_first, fixed_last)
                lines = []
                for name, addr in zip(names, addresses):
                    lines.append(f"{name}\n{addr}" if name else addr)
                full_text = "\n\n".join(lines)
                st.success(f"Generated {len(addresses)} variations")
                st.markdown('<p class="mv-kicker">EXPORT</p>', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download TXT",
                        data=full_text,
                        file_name=f"address_variations_{count}.txt",
                        mime="text/plain",
                        use_container_width=True,
                        type="primary",
                    )
                with col2:
                    csv_lines = ["Name,Address"]
                    for name, addr in zip(names, addresses):
                        name_esc = name.replace('"', '""')
                        addr_esc = addr.replace('"', '""')
                        csv_lines.append(f'"{name_esc}","{addr_esc}"')
                    st.download_button(
                        label="Download CSV",
                        data="\n".join(csv_lines),
                        file_name=f"address_variations_{count}.csv",
                        mime="text/csv",
                        use_container_width=True,
                    )
                st.subheader("Preview (first 10)")
                st.text("\n\n".join(lines[:10]))
                with st.expander(f"View all {len(addresses)} variations"):
                    st.text_area("All results", full_text, height=400)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Try a clearer address format.")

st.caption("First name = store item. Last name = One-Twenty. Junk letters. Spelled-out street type.")
