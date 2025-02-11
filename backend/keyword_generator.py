from fastapi import FastAPI, Form
from keybert import KeyBERT
import yake
import requests
import ollama  #  Import Ollama for local Llama 3.2
import pandas as pd
from pytrends.request import TrendReq
from serpapi.google_search import GoogleSearch

#  Initialize models
kw_model = KeyBERT()
# pytrends = TrendReq(hl="en-US", tz=360)

#  Setup FastAPI
app = FastAPI()

def expand_keywords_with_ollama(keyword):
    """Expands the given keyword into related SEO-friendly keywords using Llama 3.2 (via Ollama)."""
    try:
        prompt = f"""
        Suggest 10 highly relevant SEO keywords related to '{keyword}'.
        Only return a comma-separated list of keywords. Produce ONLY keywords, DO NOT generate more text. 
        """
        response = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": prompt}])

        keywords = response["message"]["content"].split(", ")
        return keywords
    except Exception as e:
        print(f" Error with Ollama Llama 3.2 expansion: {e}")
        return []

def extract_keywords(text):
    """Extracts potential keywords using YAKE and KeyBERT"""
    try:
        # YAKE keyword extraction
        yake_extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.9, top=10, features=None)
        yake_keywords = [kw[0] for kw in yake_extractor.extract_keywords(text)]

        #  KeyBERT keyword extraction
        keybert_keywords = [kw[0] for kw in kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english')]

        #  Merge and deduplicate
        final_keywords = list(set(yake_keywords + keybert_keywords))
        return final_keywords[:10]
    except Exception as e:
        print(f" Error extracting keywords: {e}")
        return []

def get_interest(keywords):
    """
    Fetches 'Interest Over Time' data for up to five keywords using SerpApi's Google Trends API.
    Returns the 'interest_over_time' data for visualization.
    """
    try:
        if len(keywords) > 5:
            raise ValueError("A maximum of 5 keywords is allowed per query.")
        
        # Join keywords with commas
        query = ",".join(keywords)
        
        # Set up the parameters for the API request
        params = {
            "engine": "google_trends",
            "q": query,
            "api_key": "49d22dd4f4c272befabf0a59da2486b3d0bb023763d36dcf894c692ed1abdd85",
            "data_type": "TIMESERIES",  # Interest over time
            "date": "today 12-m"        # Past 12 months
        }
        
        # Perform the API request
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Extract 'Interest Over Time' data
        interest_over_time = results.get("interest_over_time", {})
        if interest_over_time:
            return interest_over_time
        else:
            print(f"No 'Interest Over Time' data found for keywords: {keywords}")
            return {}
    except Exception as e:
        print(f"Error fetching 'Interest Over Time' data: {e}")
        return {}

def normalize_keywords(keywords):
    """Convert all keywords to lowercase to remove case-sensitive duplicates."""
    return list(set(kw.lower() for kw in keywords))


@app.post("/generate_keywords")
async def generate_keywords(title: str = Form(...)):
    """Generate SEO-friendly keywords for a product title and fetch their 'Interest Over Time' data."""
    # Step 1: Extract keywords from the title
    keywords = extract_keywords(title)

    # Step 2: Expand with Llama 3.2-generated keywords via Ollama
    related_keywords = expand_keywords_with_ollama(title)
    keywords.extend(related_keywords)

    # Step 3: Normalize keywords to lowercase and remove duplicates
    unique_keywords = normalize_keywords(keywords)

    # Step 4: Limit to top 5 keywords
    top_keywords = unique_keywords[:5]

    # Step 5: Fetch 'Interest Over Time' data
    interest_data = get_interest(top_keywords)

    return {"keywords": unique_keywords, "interest_over_time": interest_data} #  Return top 5 keywords

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
