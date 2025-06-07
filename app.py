import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

st.set_page_config(page_title="Which Antibiotic Works Best?",
                   layout="wide",
                   initial_sidebar_state="collapsed")

st.title("Antibiotic Potency Across 16 Bacteria (Burtin, 1951)")
st.markdown(
"""
The lower the **MIC** (Minimum Inhibitory Concentration), the less drug needed to halt growth.  
**≤ 1 µg/mL** is a common “highly sensitive” benchmark in early literature.
"""
)


data = [
    {"Bacteria":"Aerobacter aerogenes","Penicillin":870,"Streptomycin":1,"Neomycin":1.6,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Bacillus anthracis","Penicillin":0.001,"Streptomycin":0.01,"Neomycin":0.007,"Gram_Staining":"positive","Genus": "other"},
    {"Bacteria":"Brucella abortus","Penicillin":1,"Streptomycin":2,"Neomycin":0.02,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Diplococcus pneumoniae","Penicillin":0.005,"Streptomycin":11,"Neomycin":10,"Gram_Staining":"positive","Genus": "other"},
    {"Bacteria":"Escherichia coli","Penicillin":100,"Streptomycin":0.4,"Neomycin":0.1,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Klebsiella pneumoniae","Penicillin":850,"Streptomycin":1.2,"Neomycin":1,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Mycobacterium tuberculosis","Penicillin":800,"Streptomycin":5,"Neomycin":2,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Proteus vulgaris","Penicillin":3,"Streptomycin":0.1,"Neomycin":0.1,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Pseudomonas aeruginosa","Penicillin":850,"Streptomycin":2,"Neomycin":0.4,"Gram_Staining":"negative","Genus": "other"},
    {"Bacteria":"Salmonella (Eberthella) typhosa","Penicillin":1,"Streptomycin":0.4,"Neomycin":0.008,"Gram_Staining":"negative","Genus": "Salmonella"},
    {"Bacteria":"Salmonella schottmuelleri","Penicillin":10,"Streptomycin":0.8,"Neomycin":0.09,"Gram_Staining":"negative","Genus": "Salmonella"},
    {"Bacteria":"Staphylococcus albus","Penicillin":0.007,"Streptomycin":0.1,"Neomycin":0.001,"Gram_Staining":"positive","Genus": "Staphylococcus"},
    {"Bacteria":"Staphylococcus aureus","Penicillin":0.03,"Streptomycin":0.03,"Neomycin":0.001,"Gram_Staining":"positive","Genus": "Staphylococcus"},
    {"Bacteria":"Streptococcus fecalis","Penicillin":1,"Streptomycin":1,"Neomycin":0.1,"Gram_Staining":"positive","Genus": "Streptococcus"},
    {"Bacteria":"Streptococcus hemolyticus","Penicillin":0.001,"Streptomycin":14,"Neomycin":10,"Gram_Staining":"positive","Genus": "Streptococcus"},
    {"Bacteria":"Streptococcus viridans","Penicillin":0.005,"Streptomycin":10,"Neomycin":40,"Gram_Staining":"positive","Genus": "Streptococcus"}
]

df = pd.DataFrame(data)

# tidy format (long)
long = df.melt(
    id_vars=["Bacteria", "Gram_Staining", "Genus"],
    value_vars=["Penicillin", "Streptomycin", "Neomycin"],
    var_name="Antibiotic",
    value_name="MIC"
)
long["logMIC"] = np.log10(long["MIC"])          # log10 for smooth colour
long["Sensitive"] = long["MIC"] <= 1            # bool for annotation

base = alt.Chart(long).encode(
    x=alt.X("Antibiotic:N", title=None),
    y=alt.Y("Bacteria:N", sort="-x", title=None),
)

heat = base.mark_rect().encode(
    color=alt.Color(
        "logMIC:Q",
        scale=alt.Scale(scheme="viridis", domain=[np.log10(0.001), np.log10(870)], reverse=True),
        legend=alt.Legend(title="log10 MIC\n(lower = stronger)")
    ),
    tooltip=[
        alt.Tooltip("Bacteria:N"),
        alt.Tooltip("Antibiotic:N"),
        alt.Tooltip("MIC:Q", title="MIC (µg/mL)", format=".3f"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
    ]
)

# outline the “clinically effective” cells
outline = base.transform_filter("datum.Sensitive").mark_rect(
    fillOpacity=0, stroke="black", strokeWidth=1.2
)

chart = (heat + outline).properties(
    width=550, height=450,
    title="Where Each Antibiotic Shines (black boxes = MIC ≤ 1 µg/mL)"
).configure_title(anchor="start", fontSize=18)

st.altair_chart(chart, use_container_width=False)

st.markdown(
"""
### What jumps out?

* **Penicillin** (left column) is stellar against nearly every *Gram-positive* species (black boxes galore) yet fails on all *Gram-negatives* (no outlines).  
* **Streptomycin** shows the broadest low-dose activity, including several Gram-negatives (*Aerobacter*, *E. coli*, *Salmonella*).  
* **Neomycin** is a reliable fallback—low MICs for most species—but note the dramatic resistance in *Streptococcus viridans* (far-right bright square).

> **Take-home:** Cell-wall structure matters. Gram-negative bacteria’s outer membrane blocks Penicillin, so clinicians pivot to Streptomycin or Neomycin for those infections.
"""
)

# data peek
with st.expander("See raw numbers"):
    st.dataframe(df.set_index("Bacteria"))



