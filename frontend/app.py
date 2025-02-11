import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO
from PIL import Image
import altair as alt
import re 
from backend.categorization_agent import predict_category

#  Initialize session state for product storage
if 'products' not in st.session_state:
    st.session_state.products = []
if 'generated_category' not in st.session_state:
    st.session_state.generated_category = ""

#  Sidebar controls
with st.sidebar:
    st.title("Admin Panel")
    if st.button("Add a Product"):
        st.session_state.show_form = True
        st.session_state.show_products = False
    if st.button("Added Products"):
        st.session_state.show_products = True
        st.session_state.show_form = False

#  Display added products with search functionality
if st.session_state.get("show_products", False) and st.session_state.products:
    st.subheader("Added Products")
    search_query = st.text_input("Search by Title", "")
    uploaded_search_image = st.file_uploader("Search by Image", type=["jpg", "png", "jpeg"], key="search_image")

    filtered_products = [p for p in st.session_state.products if search_query.lower() in p["Title"].lower()]

    if uploaded_search_image:
        search_image = Image.open(uploaded_search_image)
        search_bytes = BytesIO()
        search_image.save(search_bytes, format="PNG")
        search_data = search_bytes.getvalue()
        filtered_products = [p for p in filtered_products if p["Image"] == search_data]

    for product in filtered_products:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(Image.open(BytesIO(product["Image"])), width=100)
        with col2:
            st.subheader(product["Title"])
            st.write("**Category (AI Predicted):**", product["Category"])
            st.write("**Keywords:**", product["Keywords"])
            st.write("**Description:**", product["Description"])

#  Product form
if st.session_state.get("show_form", False):
    st.subheader("Add Product Details")
    product_title = st.text_input("Product Title")
    if product_title:
        st.session_state.generated_category = predict_category(product_title)

    category = st.text_input("Category", value=st.session_state.generated_category, key="category_input")
    product_keywords = st.text_input(
    "Keywords (comma-separated)", 
    value=st.session_state.get("generated_keywords", ""),  #  Autofill from session_state
    key="keywords_input"
)

    product_description = st.text_area("Product Description")
    uploaded_image = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"])

#  Keyword Generation with Interest Over Time Data
    if st.button("Generate Keywords & Trends"):
        with st.spinner("🔍 Generating SEO Keywords & Fetching Trends..."):
            try:
                response = requests.post(
                    "http://localhost:8001/generate_keywords",
                    data={"title": product_title, "description": product_description}
                )
                if response.status_code == 200:
                    data = response.json()
                    
                    #  Extract Keywords & Interest Data
                    keywords = data["keywords"]  # This is now a list of strings
                    interest_over_time = data["interest_over_time"]  # Dictionary containing trend data

                    #  Autofill Keywords in Input Field
                    if keywords:
                        st.session_state.generated_keywords = ", ".join(keywords)  # Store in session state
                        st.success("✅ Keywords Generated!")
                        st.write(" | ".join([f"🔹 **{kw}**" for kw in keywords]))  # Display as a nice sentence
                
                    #  Display Interest Over Time Graph
                    if interest_over_time:
                        st.subheader("📊 Interest Over Time")

                        # Extract timeline data from API response
                        timeline_data = interest_over_time.get("timeline_data", [])

                        if timeline_data:
                            # Extract dates and format data
                            dates = [entry["date"] for entry in timeline_data]
                            df = pd.DataFrame(index=dates)

                            for entry in timeline_data:
                                for value in entry["values"]:
                                    query = value["query"]
                                    extracted_value = value["extracted_value"]
                                    if query not in df:
                                        df[query] = None
                                    df.at[entry["date"], query] = extracted_value

                            #  Plot the graph
                            st.line_chart(df)

                        else:
                            st.warning("⚠️ No trend data available for these keywords.")

                else:
                    st.error("❌ Failed to fetch keywords. Try again.")

            except requests.exceptions.ConnectionError:
                st.error("❌ Could not connect to the backend. Is FastAPI running?")



    #  Save Product
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Save Product"):
        if product_title and product_keywords and product_description and uploaded_image and category:
            #  Save image in memory
            img_bytes = BytesIO()
            image.save(img_bytes, format="PNG")
            img_data = img_bytes.getvalue()

            #  Append product with AI-generated category
            st.session_state.products.append({
                "Title": product_title,
                "Category": category,  # AI or user input
                "Keywords": product_keywords,
                "Description": product_description,
                "Image": img_data
            })

            st.success(f" Product added successfully! (Category: {category})")
            st.session_state.show_form = False
            st.session_state.generated_category = ""  # Reset generated category
            
        else:
            st.error("⚠️ Please fill all fields and upload an image.")
