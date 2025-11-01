#Rag model for resume filteering
-tech stack
  front-end(streamlit)
  backend(python,flask, rest apis,NLP)
  db(mongo db)
  genai(rag, prompt-techniques,llms)

#project setup
-frontend
 venv
 req.txt
 app.py
 readme.md
 .env(development)
-backend
 venv
 req.txt
 server.py

#project running commends
 -frontend
  cd frontend
  python -m venv venv
  venv\Scripts\activate
  pip install -r req.txt
  stramlit -r app.py
-backend
 cd backendend
  python -m venv venv
  venv\Scripts\activate
  pip install -r req.txt
  python server.py

#project features
 -frontend
  streamlit file updloading button
  reading pdf documents
  api calling
 -backend
  
