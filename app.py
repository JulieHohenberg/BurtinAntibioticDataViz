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
Lower **MIC** (Minimum Inhibitory Concentration) ⇒ less drug required to stop growth.  
Cells outlined in **black** meet a classic “highly sensitive” benchmark (**MIC ≤ 1 µg/mL**).
"""
)

#Raw data → DataFrame → tidy (long) format

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
long["logMIC"]   = np.log10(long["MIC"])
long["Sensitive"] = long["MIC"] <= 1

#Antibiotic selector

choice = st.selectbox(
    "Select an antibiotic or view all:",
    ["All", "Penicillin", "Streptomycin", "Neomycin"],
    index=0
)

if choice == "All":
    long_filt = long
    width_val = 550
else:
    long_filt = long[ long["Antibiotic"] == choice ]
    width_val = 250

#Heat-map (with outlined sensitive cells)

base = alt.Chart(long_filt).encode(
    x=alt.X("Antibiotic:N", title=None),
    y=alt.Y("Bacteria:N",   sort="-x", title=None)
)

heat = base.mark_rect().encode(
    color=alt.Color(
        "logMIC:Q",
        scale=alt.Scale(scheme="viridis",
                        domain=[np.log10(0.001), np.log10(870)],
                        reverse=True),
        legend=alt.Legend(title="log₁₀ MIC\n(lower = stronger)")
    ),
    tooltip=[
        "Bacteria:N",
        "Antibiotic:N",
        alt.Tooltip("MIC:Q", title="MIC (µg/mL)", format=".3f"),
        alt.Tooltip("Gram_Staining:N", title="Gram")
    ]
)

outline = base.transform_filter("datum.Sensitive").mark_rect(
    stroke="black", strokeWidth=1.2, fillOpacity=0
)

chart = (heat + outline).properties(
    width=width_val,
    height=450,
    title=f"{'All Antibiotics' if choice=='All' else choice} Potency (black outline = MIC ≤ 1 µg/mL)"
).configure_title(anchor="start", fontSize=18)

st.altair_chart(chart, use_container_width=False)

#Narrative section (static for brevity)

if choice == "All":
    st.markdown(
    """
    ### Key patterns

    * **Penicillin** works brilliantly on almost every *Gram-positive* species but fails on *Gram-negatives* (no black boxes).  
    * **Streptomycin** delivers the broadest low-dose coverage, including several Gram-negatives (*Aerobacter*, *E. coli*, *Salmonella*).  
    * **Neomycin** is potent for most bacteria, yet *Streptococcus viridans* shows strong resistance.

    **Clinical takeaway:** Gram-negative bacteria’s outer membrane blocks Penicillin, so other drugs are preferred for those infections.
    """
    )
else:
    # single-drug mini-insight
    single_note = {
        "Penicillin":
        "*Great for Gram-positives, ineffective for Gram-negatives.*",
        "Streptomycin":
        "*Good cross-gram activity; covers several Penicillin-resistant strains.*",
        "Neomycin":
        "*Broad coverage but beware of pockets of resistance (e.g., *Strep. viridans*).*"
    }[choice]
    st.markdown(f"### Quick insight\n{single_note}")

with st.expander("See raw numbers"):
    if choice == "All":
        st.dataframe(df.set_index("Bacteria"))
    else:
        st.dataframe(
            df[["Bacteria", choice]]
              .set_index("Bacteria")
              .rename(columns={choice: f"{choice} MIC (µg/mL)"})
        )
