import streamlit as st
from scripts.recommend import SHLRecommender

st.set_page_config(
    page_title="SHL GenAI Assessment Recommender",
    layout="centered"
)

st.title("SHL GenAI Assessment Recommendation Engine")
st.write(
    "Enter a job description or requirement to get relevant SHL individual assessments."
)

# Cache the recommender so it loads only once
@st.cache_resource
def load_recommender(_version="v2"):
    return SHLRecommender(top_k=10)

recommender = load_recommender()

query = st.text_area(
    "Job description / Query",
    height=150,
    placeholder="e.g. Need a Java developer who is good at collaboration..."
)

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Finding relevant assessments..."):
            results = recommender.recommend(query)

        st.subheader("Recommended Assessments")

        for r in results:
            st.markdown(
                f"- **{r.get('assessment_name', r.get('name'))}**  \n"
                f"  {r.get('assessment_url', r.get('url'))}"
            )

        # Optional: show raw JSON (good for reviewers)
        with st.expander("Show raw JSON response"):
            st.json({"recommendations": results})
