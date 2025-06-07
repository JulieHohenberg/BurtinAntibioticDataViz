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

df = pd.DataFrame(data)

THRESHOLD = 1           # μg/mL
df["Status"] = df["Penicillin"].apply(lambda x: "Highly sensitive (≤1)" if x <= THRESHOLD else "Resistant (>1)")

# sort so most-resistant appear at top for quick comparison
df_sorted = df.sort_values("Penicillin", ascending=False)

base = alt.Chart(df_sorted).encode(
    y=alt.Y("Bacteria:N", sort="-x", title=None),
    x=alt.X("Penicillin:Q",
            scale=alt.Scale(type="log"),
            title="Penicillin MIC (μg/mL, log scale)"),
    color=alt.Color("Gram_Staining:N",
                    scale=alt.Scale(domain=["positive", "negative"],
                                    range=["#7b2cbf", "#e63946"]),
                    legend=alt.Legend(title="Gram stain")),
    tooltip=[
        alt.Tooltip("Bacteria:N"),
        alt.Tooltip("Penicillin:Q", format=".3f", title="MIC (μg/mL)"),
        alt.Tooltip("Gram_Staining:N", title="Gram"),
        alt.Tooltip("Status:N")
    ]
)

bars = base.mark_bar(size=10, opacity=0.9)

# Vertical rule for clinical threshold
rule = alt.Chart(pd.DataFrame({"x":[THRESHOLD]})).mark_rule(
        strokeDash=[4,4], color="black").encode(x="x:Q")

rule_text = alt.Chart(pd.DataFrame({
        "x":[THRESHOLD*1.1], "y":[df_sorted["Bacteria"].iloc[0]],
        "text":["≤1 μg/mL → usually curative"]
    })).mark_text(align="left", baseline="middle",
                  dx=4, fontSize=12, fontStyle="italic").encode(
        x="x:Q", y="y:N", text="text:N")

# Call-out labels for extreme points
extremes = df_sorted[(df_sorted["Penicillin"]<=0.01) | (df_sorted["Penicillin"]>=800)]

labels = alt.Chart(extremes).mark_text(
        align="left", dx=4, fontSize=11, fontWeight="bold"
    ).encode(
        y="Bacteria:N",
        x="Penicillin:Q",
        text=alt.Text("Bacteria:N")
    )

# Layer everything
chart = (bars + rule + rule_text + labels).properties(
            width=800, height=500,
            title="Gram-positive bacteria need tiny doses of Penicillin, "
                  "while Gram-negative strains often resist it"
        ).configure_title(fontSize=18, anchor="start")

st.altair_chart(chart, use_container_width=True)



