import streamlit as st
import openai
import requests

st.set_page_config(page_title="Project Ragnarok", page_icon="⚔️", layout="wide")

try:
    AI_KEY = st.secrets["OPENAI_API_KEY"]
    SEARCH_KEY = st.secrets["TAVILY_API_KEY"]
except:
    st.error("Secrets not found. Please add API keys to Streamlit Settings.")
    st.stop()

with st.sidebar:
    st.title("⚔️ PROJECT RAGNAROK")
    st.divider()
    st.subheader("The Mission:")
    st.caption("Zero BS. Zero Hallucinations. Pure Data.")
    st.markdown("[Upgrade to Operative](https://buy.stripe.com/your_link_here)")

def verify(query):
    url = "https://api.tavily.com/search"
    payload = {"api_key": SEARCH_KEY, "query": query, "search_depth": "advanced"}
    return requests.post(url, json=payload).json().get('results', [])

def generate(query, context):
    client = openai.OpenAI(api_key=AI_KEY)
    ctx = "\n".join([f"DATA: {r['content']} | SRC: {r['title']}" for r in context])
    res = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[{"role": "system", "content": "You are Project Ragnarok. Facts only. No fluff. Cite [Source]."},
                  {"role": "user", "content": f"Context: {ctx}\n\nQuestion: {query}"}],
        temperature=0
    )
    return res.choices[0].message.content

st.title("TRUTH ACQUISITION")
query = st.text_input("Enter claim for verification:")
if query:
    with st.spinner("Analyzing..."):
        data = verify(query)
        if data:
            st.info(generate(query, data))
            with st.expander("View Audit Trail"):
                for d in data: st.write(f"- [{d['title']}]({d['url']})")
