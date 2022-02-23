from statistics import mode
from sentence_transformers import SentenceTransformer, util
import numpy as np

model = SentenceTransformer("./aimodel")

corpus = ["Golang is a very fast programming language",
          "Unity shadow element on X axis",
          "Rust vs Golang which is fast?",
          "Hello world in Javascript",
          "Hello world in Golang"]


corpus_embeddings = model.encode(corpus, convert_to_tensor=True)
sentence = "First Snippet in Golang"

sentence_embedding = model.encode(sentence, convert_to_tensor=True)
top_k = 2

cos_scores = util.pytorch_cos_sim(sentence_embedding, corpus_embeddings)[0]

top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

print("Sentence:", sentence, "\n")
print(top_results)
arr=[]
print("Top", top_k, "most similar sentences in corpus:")
for idx in top_results[0:top_k]:
    print(corpus[idx], "(Score: %.4f)" % (cos_scores[idx]))
    arr.append(idx.item())
print(arr)

