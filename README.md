# AccountantGPT

![AccountantGPT Logo](https://github.com/lcubrilo/AccountantGPT/blob/main/assets/AccountantGPT-Dark-Horizontal.png)

AccountantGPT is an innovative project designed to assist users in navigating the complex world of tax advisory.

Visit the [link](https://AccountantGPT.streamlit.app/) to try the application.


Utilizing a combination of RAG (Retrieval-Augmented Generation) technology and a deep knowledge base of law articles, this bot can intelligently reference relevant legal texts during interactions. It offers an interactive platform for querying legal information, making it a valuable tool for professionals, students, and anyone needing quick insights into legal matters. 

Setup involves **Venv** for dependency management, **Qdrant** for vector database functionality, and **Langfuse** for enhancing chatbot performance, ensuring a robust and efficient user experience.

## Setting Up the Project

### Step 3: Installing Dependencies
Install all the project's dependencies with:
```bash
pip install -r requirements.txt
```
> 📎 _**Note**: Use the `--no-root` option to skip installing the project package itself._

### Step 4: Activating the Virtual Environment
Post-installation, activate the virtual environment located in the `.venv` directory.

For macOS/Linux:
```bash
source .venv/bin/activate
```
For Windows:
```bash
.venv\Scripts\activate
```

### Step 5: Initializing Qdrant:

Qdrant is a sophisticated vector database and vector similarity search engine that operates as an API service. It allows for the searching of nearest high-dimensional vectors, transforming embeddings or neural network encoders into comprehensive applications suitable for matching, searching, recommending, among other functionalities.

For setup, you will require two crucial pieces of information: **QDRANT_CLUSTER_URL** and **QDRANT_API_KEY**.

To begin, create a free account with Qdrant by signing up [here](https://cloud.qdrant.io/login). Following account creation, proceed to set up a cluster for your vector database; this is where you'll obtain your **QDRANT_CLUSTER_URL**. Lastly, generate your **QDRANT_API_KEY** by navigating to the "Data Access Control" section within your Qdrant dashboard.

### Step 6: Integrate Langfuse

Langfuse plays a vital role in enhancing the functionality and performance of chatbots by offering observability, analytics, prompt management, and integration support. It is a valuable tool for developers looking to build and optimize chatbot applications powered by Large Language Models.

Here is an [overview](https://langfuse.com/docs) of Langfuse documentation.
To begin, create a free account on Langfuse by signing up [here](https://cloud.langfuse.com/auth/sign-up). Create a project, generate the necessary keys, and place them in `.env` file.

### Step 7: Environment variables:
For the project to work you need to create a `.env` file in the project root.

The file should look like this:
```yml
QDRANT_CLUSTER_URL=ADD_YOUR_QDRANT_CLUSTER_URL
QDRANT_API_KEY=ADD_YOUR_QDRANT_API_KEY

OPENAI_API_KEY=ADD_YOUR_OPENAI_API_KEY

LANGFUSE_SECRET_KEY=ADD_YOUR_LANGFUSE_SECRET_KEY
LANGFUSE_PUBLIC_KEY=ADD_YOUR_LANGFUSE_PUBLIC_KEY
LANGFUSE_HOST=ADD_YOUR_LANGFUSE_HOST
```

## Run the Demo:
You can run the demo locally simply by executing this command in your terminal:
```bash
streamlit run app.py  
```
And UI will be available in your browser on the URL:
```
http://localhost:8501
```
