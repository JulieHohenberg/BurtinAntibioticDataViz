import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import textwrap

#Page setup & intro

st.set_page_config(page_title="Which Antibiotic Works Best?",
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.title("How Potent Are Penicillin, Streptomycin & Neomycin?")
with st.container():
    st.markdown(
        textwrap.dedent("""\
        <div style='text-align:left;width:100%;font-size:1.05rem'>
          <strong>Robert Burtin’s classic 1951 experiment</strong> measured the
          <em>minimum inhibitory concentration</em> (<strong>MIC</strong>)
          of three antibiotics on 16 bacterial species.

          <ul>
            <li><strong>Lower MIC ⇒ more potent drug</strong> (less needed to stop growth).</li>
            <li><strong>MIC ≤ 1 µg/mL</strong> is a <strong>“highly sensitive”</strong> threshold.</li>
            <li><strong>Goal:</strong> Spot which drug works for which bug—and where resistance lurks.</li>
          </ul>

          Use the dropdown to focus on <strong>one antibiotic</strong> or compare <strong>all three</strong>.
        </div>
        """),
        unsafe_allow_html=True
    )

data = [
    {"Bacteria":"Aerobacter aerogenes","Penicillin":870,"Streptomycin":1,"Neomycin":1.6,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Bacillus anthracis","Penicillin":0.001,"Streptomycin":0.01,"Neomycin":0.007,"Gram_Staining":"positive","Genus":"other"},
    {"Bacteria":"Brucella abortus","Penicillin":1,"Streptomycin":2,"Neomycin":0.02,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Diplococcus pneumoniae","Penicillin":0.005,"Streptomycin":11,"Neomycin":10,"Gram_Staining":"positive","Genus":"other"},
    {"Bacteria":"Escherichia coli","Penicillin":100,"Streptomycin":0.4,"Neomycin":0.1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Klebsiella pneumoniae","Penicillin":850,"Streptomycin":1.2,"Neomycin":1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Mycobacterium tuberculosis","Penicillin":800,"Streptomycin":5,"Neomycin":2,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Proteus vulgaris","Penicillin":3,"Streptomycin":0.1,"Neomycin":0.1,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Pseudomonas aeruginosa","Penicillin":850,"Streptomycin":2,"Neomycin":0.4,"Gram_Staining":"negative","Genus":"other"},
    {"Bacteria":"Salmonella (Eberthella) typhosa","Penicillin":1,"Streptomycin":0.4,"Neomycin":0.008,"Gram_Staining":"negative","Genus":"Salmonella"},
    {"Bacteria":"Salmonella schottmuelleri","Penicillin":10,"Streptomycin":0.8,"Neomycin":0.09,"Gram_Staining":"negative","Genus":"Salmonella"},
    {"Bacteria":"Staphylococcus albus","Penicillin":0.007,"Streptomycin":0.1,"Neomycin":0.001,"Gram_Staining":"positive","Genus":"Staphylococcus"},
    {"Bacteria":"Staphylococcus aureus","Penicillin":0.03,"Streptomycin":0.03,"Neomycin":0.001,"Gram_Staining":"positive","Genus":"Staphylococcus"},
    {"Bacteria":"Streptococcus fecalis","Penicillin":1,"Streptomycin":1,"Neomycin":0.1,"Gram_Staining":"positive","Genus":"Streptococcus"},
    {"Bacteria":"Streptococcus hemolyticus","Penicillin":0.001,"Streptomycin":14,"Neomycin":10,"Gram_Staining":"positive","Genus":"Streptococcus"},
    {"Bacteria":"Streptococcus viridans","Penicillin":0.005,"Streptomycin":10,"Neomycin":40,"Gram_Staining":"positive","Genus":"Streptococcus"}
]

df = pd.DataFrame(data)

long = df.melt(
    id_vars=["Bacteria", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)
long["logMIC"]    = np.log10(long["MIC"])
long["Sensitive"] = long["MIC"] <= 1


# Dropdown selector

choice = st.selectbox(
    "Antibiotic selection",
    ["All", "Penicillin", "Streptomycin", "Neomycin"],
    index=0
)

data_sel = long if choice == "All" else long[long["Antibiotic"] == choice]
single   = choice != "All"

# Heat-map with conditional stroke (tooltips intact)

LOG_DOMAIN = [np.log10(0.001), np.log10(870)]

# band width & height
chart_width  = 320 if single else 600
chart_height = data_sel["Bacteria"].nunique() * 30

heat = alt.Chart(data_sel).mark_rect().encode(
    x=alt.X("Antibiotic:N",
            title=None,
            axis=alt.Axis(labelAngle=-90)),   # vertical column names
    y=alt.Y("Bacteria:N", sort="-x", title=None),
    color=alt.Color("logMIC:Q",
                    scale=alt.Scale(scheme="viridis",
                                    domain=LOG_DOMAIN,
                                    reverse=True),
                    legend=None if single else alt.Legend(title="log₁₀ MIC\n(lower = stronger)")),
    stroke=alt.condition("datum.Sensitive", alt.value("black"), alt.value("transparent")),
    strokeWidth=alt.condition("datum.Sensitive", alt.value(1.3), alt.value(0)),
    tooltip=[
        alt.Tooltip("Bacteria:N"),
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("MIC:Q", title="MIC (µg/mL)", format=".3f"),
        alt.Tooltip("Gram_Staining:N", title="Gram")
    ]
).properties(
    width=chart_width,
    height=chart_height,
    title=f"{'All Antibiotics' if choice=='All' else choice} Potency • Black outline = MIC ≤ 1 µg/mL"
).configure_title(anchor="start", fontSize=18)

st.altair_chart(heat, use_container_width=True)

# Narrative (same text, minor tweak)

if choice == "All":
    st.markdown(
    """
    ### Quick observations
    * **Penicillin** only excels on *Gram-positives* (left column full of outlines).  
    * **Streptomycin** has the broadest low-dose reach, even on some *Gram-negatives*.  
    * **Neomycin** is generally potent, but *Streptococcus viridans* resists it strongly.
    """
    )
else:
    notes = {
        "Penicillin":   "Great for Gram-positives; ineffective for Gram-negatives.",
        "Streptomycin": "Cross-gram activity; good fallback when Penicillin fails.",
        "Neomycin":     "Broad but *Strep. viridans* stands out as resistant."
    }
    st.markdown(f"### Insight on **{choice}**\n{notes[choice]}")

# Raw data table

with st.expander("Show exact MIC numbers"):
    if single:
        st.dataframe(
            df[["Bacteria", choice]]
              .set_index("Bacteria")
              .rename(columns={choice: f"{choice} MIC (µg/mL)"})
        )
    else:
        st.dataframe(df.set_index("Bacteria"))
