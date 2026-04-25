import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load Excel
file_path = file_path = "Opengov_Framework.xlsx"

vendors_df = pd.read_excel(file_path, sheet_name="Vendors", engine="openpyxl")
usage_df = pd.read_excel(file_path, sheet_name="Usage", engine="openpyxl")


def get_context(question):
    q = question.lower()

    # Vendor logic
    if "vendor" in q:
        vendors_df["Score"] = (
            (vendors_df["Cost"].max() - vendors_df["Cost"]) * 0.3 +
            vendors_df["SLA"] * 0.4 +
            vendors_df["Risk"].apply(lambda x: 50 if str(x).lower() == "low" else 10) * 0.3
        )

        best = vendors_df.sort_values(by="Score", ascending=False).iloc[0]

        return f"""
Best Vendor: {best['Vendor']}
Reason: Balanced cost, SLA, and risk
"""

    # Cost logic
    if "cost" in q:
        total = usage_df.iloc[0]["Total Licenses"]
        active = usage_df.iloc[0]["Active Users"]
        reduction = total - active

        return f"""
Unused Licenses: {reduction}
Opportunity: Reduce license count and renegotiate
"""

    return "General procurement analysis"


def ask_ai(question):
    context = get_context(question)

    prompt = f"""
You are a senior procurement consultant.

Context:
{context}

Answer clearly with:
- Recommendation
- Insights
- Actions

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=150
    )

    return response.choices[0].message.content.strip()
