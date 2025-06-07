import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

#Page setup & intro

st.set_page_config(page_title="Which Antibiotic Works Best?",
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.title("Antibiotic Potency Across 16 Bacteria (Burtin, 1951)")
st.markdown(
"""
Lower **MIC** (Minimum Inhibitory Concentration) → greater potency.  
Cells outlined in **black** meet a “highly sensitive” rule-of-thumb (**MIC ≤ 1 µg/mL**).
"""
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

# Colour scale domain frozen so the palette is consistent
LOG_DOMAIN = [np.log10(0.001), np.log10(870)]  # [-3, 2.94]

#Selector

choice = st.selectbox(
    "Pick an antibiotic (or view them all):",
    ["All", "Penicillin", "Streptomycin", "Neomycin"]
)

data_sel = long if choice == "All" else long[long["Antibiotic"] == choice]

# Chart width & legend handling
single_col = choice != "All"
chart_width = 340 if single_col else 600
show_legend = not single_col   # hide legend when there’s just one column

# Chart height = 30 px per row
unique_bugs = data_sel["Bacteria"].nunique()
chart_height = unique_bugs * 30

#Heat-map with fixed band size

# We keep the outline separate so it never hides the colour.
base = alt.Chart(data_sel).encode(
    x=alt.X("Antibiotic:N",
            title=None,
            axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Bacteria:N",
            sort="-x",
            title=None)
)

heat = base.mark_rect().encode(
    color=alt.Color(
        "logMIC:Q",
        scale=alt.Scale(scheme="viridis",
                        domain=LOG_DOMAIN,
                        reverse=True),
        legend=None if not show_legend else alt.Legend(title="log₁₀ MIC\n(lower = stronger)")
    )
).properties(width=chart_width, height=chart_height)

outline = base.transform_filter("datum.Sensitive")\
              .mark_rect(fillOpacity=0, stroke="black", strokeWidth=1.2)

chart = (heat + outline).properties(
    title=f"{'All Antibiotics' if choice=='All' else choice} Potency "
          "(black outline = MIC ≤ 1 µg/mL)"
).configure_title(anchor="start", fontSize=18)

st.altair_chart(chart, use_container_width=True)

#Narrative blurb

if choice == "All":
    st.markdown(
    """
    ### What jumps out?
    * **Penicillin** excels only on *Gram-positives* (leftmost column full of outlines).  
    * **Streptomycin** is the broadest hitter, covering several *Gram-negatives*.  
    * **Neomycin** is usually dependable, yet *Streptococcus viridans* resists it.

    **Clinical takeaway:** Gram-negative outer membranes block Penicillin, so broader drugs are used for those infections.
    """
    )
else:
    notes = {
        "Penicillin":     "Great for most Gram-positives; ineffective for Gram-negatives.",
        "Streptomycin":   "Covers both Gram groups; handy for Penicillin-resistant bugs.",
        "Neomycin":       "Potent overall but watch for *Strep. viridans* resistance."
    }
    st.markdown(f"### Quick insight\n{notes[choice]}")

#Data table

with st.expander("See raw MIC numbers"):
    if choice == "All":
        st.dataframe(df.set_index("Bacteria"))
    else:
        st.dataframe(
            df[["Bacteria", choice]]
              .set_index("Bacteria")
              .rename(columns={choice: f"{choice} MIC (µg/mL)"})
        )
