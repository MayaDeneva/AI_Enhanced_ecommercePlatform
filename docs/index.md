Assignment 1	Project Summary
Course	Intelligent Agents with Generative AI - 2024

Project author 
Maya Deneva
Faculty Number 2MI0700013

Project name	AI-Enhanced E-commerce Platform

1.	Short project description (Business needs and system features)
This project aims to develop an AI-powered e-commerce multivendor platform that leverages advanced machine learning (ML) and artificial intelligence (AI) technologies to enhance user experience and vendor efficiency. The platform will incorporate natural language processing, computer vision, and intelligent automation to enable intuitive product searches and streamlined vendor operations.The system is called Persona (Personal assisting agents) and will consist of following agents:
1.	Search Agent: Interprets natural language queries to provide relevant search results.
2.	Categorization Agent: Automatically categorizes products based on uploaded images.
3.	Keyword Generation Agent: Generates relevant keywords from product images to improve discoverability.
4.	Detail Suggestion Agent: Suggests and auto-fills product attributes such as dimensions and specifications.
5.	Visual Search Agent: Matches uploaded product images with similar or identical items in the database.
Communication Protocols:
•	RESTful APIs will enable seamless communication between agents and the platform.
•	WebSocket protocols will facilitate real-time interactions, such as visual search results.

Implementation Technologies:
•	ML/AI Models:
o	NLP models (e.g., OpenAI GPT, BERT) for natural language query interpretation.
o	Computer Vision models (e.g., YOLO, ResNet) for image-based categorization and visual search.
o	Recommendation systems (e.g., collaborative filtering algorithms) for keyword and detail suggestion.


Datasets:
•	Open Images Dataset for training image recognition models.
•	Kaggle’s product datasets for NLP and recommendation models.
•	Proprietary vendor data for fine-tuning.

Technologies:

•	Frontend: React.js/Quick for a responsive UI.
•	Backend: Python with Flask/Django for API endpoints.
•	Cloud Services: AWS S3 for image storage and AWS Lambda for serverless functions.

Input and Output Data:

•	Input: Natural language queries, product images, and vendor-provided data.
•	Output: Search results, product categories, generated keywords, auto-filled attributes, and similar item matches.

2.	ML/Agent System Description using PEAS [https://aima.cs.berkeley.edu/4th-ed/pdfs/newchap02.pdf]

Agent name	Performance Measure	Environment	Actuators/Outputs	Sensors/Inputs
1.	Search Agent	Accuracy of query interpretation and relevance of results.	Product database and user-provided queries.
	API delivering search results (product listings) to the user.
	NLP module for text input.

2.Category Agent	Precision and recall of product categorization.
	Admin panel of vendor, UI for creating a product listing; Vendor-uploaded images and product database.	API delivering category labels for products.
	Computer vision module for image input.

3.Keyword generation agent	Quality and relevance of generated keywords.
	Product image and textual data from vendors.
	API delivering generated keywords for listings.
	Computer vision and NLP modules.

4. Detail Suggestion Agent
	Completeness and accuracy of suggested product attributes.
	Vendor-uploaded product data and related database entries.
	API delivering suggested attributes like dimensions and specifications.
	NLP and database query modules.

5.Visual Search Agent	Similarity accuracy between uploaded images and matched items.
	Product image database and user-uploaded images.
	API delivering matched or similar products.
	Computer vision module for image input.


3.	Main Use Cases / Scenarios
Use case name	Brief Descriptions	Actors Involved
1.	Search Through Natural Language Queries	Customers can search for products using natural language queries.
	Customer
2.	Automatically Categorize Products	Vendors upload product images, which are automatically categorized.
	Vendor
3.	Generate Keywords from Images	Vendors receive AI-generated keywords for improved product discoverability.
	Vendor
4.	Auto-Fill Product Details	Vendors benefit from auto-filled product attributes based on AI suggestions.
	Vendor
5.	Search Using Uploaded Images	Customers upload product images to find visually similar or identical items.
	Customer



4.API Resources (REST/SSE/WebSocket Backend)
View name	Brief Descriptions	URI
1.	Products listings	(POST): Accepts natural language queries and returns search results containing product listings.	/search
2.	Product Category	(POST): Processes uploaded images and assigns pre-defined categories.
	/dashboard/product#/category

3.	Product Keywords	(POST): Extracts keywords from product images
	/dashboard/product#/keywords
4.	Product Details	(POST): Suggests product specifications and attributes.
	/dashboard/product#/details
5.	Similar Products	(POST) Matches uploaded images with similar products in the database.
	/visual-search


Used External Resources
•	Open Images Dataset: https://storage.googleapis.com/openimages/web/index.html
•	Kaggle Product Datasets: https://www.kaggle.com/datasets
https://www.kaggle.com/datasets/asaniczka/amazon-products-dataset-2023-1-4m-products
•	AWS Cloud Services: https://aws.amazon.com/
•	Pre-trained Models: BERT (https://huggingface.co/bert), YOLO (https://github.com/ultralytics/yolov5)
