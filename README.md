## Streamlit chatbot demo with a VectorStore

### Description
This project is a Streamlit-based chatbot application that uses a VectorStore for querying and retrieving 
relevant documents. The chatbot is designed to help users find recipes based on their input. We populate the 
vectorstore with some default descriptions of popular recipes. 

### Key Components
- Streamlit: Used for building the web interface of the chatbot.
- LangChain: Utilized for managing the conversation flow with OpenAI's language model.
- ChromaDB: A vectorstore used for storing and querying document embeddings.

### Project Structure
```
chatbot-demo/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── utils.py
│   └── vectorstore.py
├── data/
│   └── recipes.json
├── .venv/
├── .env
├── requirements.txt
└── README.md
```

### Files
- app/app.py: Main application file that sets up the Streamlit interface and handles user interactions.
- app/utils.py: Contains utility functions used in the application as well as the prompt templates for the chatbot.
- app/vectorstore.py: Manages the creation, population, and querying of the vectorstore.
- data/recipes.json: A JSON file containing default recipe description data to populate the vectorstore.

### Create and activate a virtual environment
```bash
cd chatbot-demo  # In a terminal
python -m venv .venv  # Create a virtual environment
.venv\Scripts\activate  # On Linux use `source venv/bin/activate` 
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Create a .env file
Create a .env file in the root directory and add the following environment variables:
```bash
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=your-choice-of-model
```

### Setup and populate the VectorStore
```bash
python -m app.vectorstore.py  # This will create and populate the vectorstore with the # default recipe data. ~5-10 seconds
```

Run the application
```bash
streamlit run app/app.py
```
