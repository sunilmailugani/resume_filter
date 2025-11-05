from flask import Flask,request,jsonify
from models.text_model import text
from models.config.db import connect_db
import numpy as np
import faiss
import google.generativeai as genai

app=Flask(__name__)
connect_db()
@app.route('/upload_data',methods=['post'])
def upload_data():
    try:
        data=request.get_json()
        result=text(text=data['resume_text']).save()
        if result:
            return jsonify({'message':'data received'}),200
        else:
            return jsonify({'message':'failed to upload'}),204
    except:
        return jsonify({'message':'error occurred'}),500

@app.route('/ask-question',methods=['post'])
def ask_question():
    # build rag model here
    data=request.get_json()
    query=data['question']
    experience=data['experience']

    # 2 configure
    LLM_MODEL="gemini-2.0-flash-lite-001"
    API_KEY="AIzaSyC6mOLQ5WaYmXKvibdDs_dGAvK2M2p8TZg"
    EMBEDDING_MODEL="gemini-embedding-001"
    k=2   

    # get resumes from db
    data=text.objects()
    resumes=[]
    for resume in data:
        resumes.append(resume.text)
    #setup the model
    def configure_clint():
        genai.configure(api_key=API_KEY)

    def get_embeddings(texts):
        vectors=[]
        for text in texts:
            resp=genai.embed_content(model=EMBEDDING_MODEL,content=text)
            vectors.append(np.array(resp['embedding'],dtype=np.float32))
            # print(np.vstack(vectors))
        return np.vstack(vectors)

    #vector database
    def build_faiss_index(vectors):
        dim=vectors.shape[1]
        index=faiss.IndexFlatIP(dim)
        norms=np.linalg.norm(vectors,axis=1,keepdims=True)
        vectors=vectors/norms
        index.add(vectors)
        return index,vectors

    # retrive db (faiss)
    def retrive(query,index,docs,vectors,top_k):
        q_emb=get_embeddings([query])[0]
        q_emb=q_emb/np.linalg.norm(q_emb)
        scores,id=index.search(np.array([q_emb]),top_k)
        return [(int(i),float(score)) for i,score in zip(id[0],scores[0])]

    #generate answer
    def generate_answer(question,retrived,docs):
        context_parts=[f"doc {id} | score={score:.4f} \n{docs[id]}" for id,score in retrived]
        context_text="\n---\n".join(context_parts)

        prompt=(
            "hey you are a helpful assistent about choosing best resumes"
            "based on the provided resumes data use only the given context"
            "if unsure, simply say you don't  know.\n\n"
            f"context:{context_text}\n answer concisely"
            "show the resume also from which the answer is generated\n"
        )
        model=genai.GenerativeModel(LLM_MODEL)
        response=model.generate_content(prompt)
        return response.text if response else str(response)
    
    # main function
    def main():
        print("embedings+ faiss vector index")
        configure_clint()
        vectors=get_embeddings(resumes)
        index,norm_vectors=build_faiss_index(vectors)
        question=f"{query} with experience of {experience} years"
        retrived=retrive(question,index,resumes,norm_vectors,k)
        answer=generate_answer(question,retrived,resumes)
        return answer
    final_ans=main()
    return jsonify({"message":"success","reply":final_ans}),200

app.run(debug=True)