import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Bacteria Antibiotic Resistance", layout="wide")
st.title("Bacteria Sensitivity to Antibiotics")


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

# Create DataFrame
df = pd.DataFrame(data)

antibiotic = st.sidebar.selectbox("Choose an Antibiotic", ["Penicillin", "Streptomycin", "Neomycin"])
sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])
gram_filter = st.sidebar.multiselect("Gram Staining", ["positive", "negative"], default=["positive", "negative"])

# Filtered + sorted DataFrame
filtered = df[df["Gram_Staining"].isin(gram_filter)].sort_values(by=antibiotic, ascending=(sort_order == "Ascending"))

# Bar chart
chart = alt.Chart(filtered).mark_bar().encode(
    x=alt.X(f"{antibiotic}:Q", scale=alt.Scale(type="log"), title=f"MIC of {antibiotic} (μg/mL)"),
    y=alt.Y("Bacteria:N", sort="-x", title=None),
    color=alt.Color("Gram_Staining:N", scale=alt.Scale(domain=["positive", "negative"], range=["#8e44ad", "#e74c3c"])),
    tooltip=["Bacteria", "Gram_Staining", f"{antibiotic}"]
).properties(
    width=800,
    height=500,
    title=f"{antibiotic} Effectiveness Across Bacteria"
).configure_title(
    fontSize=20,
    anchor='start',
    color='black'
)

# Display chart
st.altair_chart(chart, use_container_width=True)

# Insight box
st.markdown("### Key Insight")
if antibiotic == "Penicillin":
    st.info("Penicillin is highly effective against many Gram-positive bacteria (e.g. *Staphylococcus aureus*) but struggles with Gram-negative strains like *E. coli*.")
elif antibiotic == "Streptomycin":
    st.info("Streptomycin is broadly effective across both Gram-positive and Gram-negative bacteria, though some resistance exists (e.g. *Streptococcus hemolyticus*).")
else:
    st.info("Neomycin tends to be most effective in low doses against both Gram types, but some strains like *Streptococcus viridans* are highly resistant.")

# Footer
st.markdown("---")
st.caption("Data: Burtin's Antibiotic Chart | MIC = Minimum Inhibitory Concentration (μg/mL) — lower means more effective")




