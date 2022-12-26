from sentence_transformers import SentenceTransformer
from numpy import dot
from numpy.linalg import norm
import pickle

model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

with open('./ml_model/sbert_chatbot.pickle', 'rb') as f:
    train_data = pickle.load(f)
    
def cos_sim(A, B):
  return dot(A, B)/(norm(A)*norm(B))

def get_response(question):
    embedding = model.encode(question)
    train_data['score'] = train_data.apply(lambda x: cos_sim(x['embedding'], embedding), axis=1)
    
    return train_data.loc[train_data['score'].idxmax()]['A']
