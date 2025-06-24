import os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
vectorizer = TfidfVectorizer(
    lowercase=True,        # Converts text to lowercase
    stop_words='english',  # Removes common English stopwords
    norm=None,             # Don't normalize the TF-IDF vector (you will compute magnitude separately)
    use_idf=True,          # Use IDF weighting
    smooth_idf=False       # Use raw IDF formula: 1 + log(N / nt)
)

folder_name="leetcode"
main_folder_path = os.path.join(os.getcwd(), folder_name)
folder_name="problems_desc"
folder_path = os.path.join(main_folder_path, folder_name)

file_names=[]
i=1
while i<1079:
    file_names.append("problem"+str(i)+".txt")
    i=i+1


documents=[]
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        documents.append(content)


vectorizer = TfidfVectorizer(norm=None, smooth_idf=False, use_idf=True)
tfidf_matrix = vectorizer.fit_transform(documents)


# Writing keyword.txt (sorted by vocabulary index)
vocab = vectorizer.vocabulary_
inv_vocab = {i: w for w, i in vocab.items()}
sorted_terms = [inv_vocab[i] for i in sorted(inv_vocab)]

with open("keyword.txt", "w", encoding="utf-8") as f:
    for term in sorted_terms:
        f.write(term + "\n")

# Write IDF.txt (in order of sorted_terms)
idf_array = vectorizer.idf_
idf_map = {term: idf_array[vocab[term]] for term in vocab}

with open("IDF.txt", "w", encoding="utf-8") as f:
    for term in sorted_terms:
        f.write(f"{idf_map[term]:.6f}\n")

# Write TFIDF.txt (non-zero entries only)
coo = tfidf_matrix.tocoo()
with open("TFIDF.txt", "w", encoding="utf-8") as f:
    for i, j, v in zip(coo.row, coo.col, coo.data):
        f.write(f"{i} {j} {v:.6f}\n")

# Write Magnitude.txt
magnitudes = np.sqrt((tfidf_matrix.multiply(tfidf_matrix)).sum(axis=1)).A1
with open("Magnitude.txt", "w", encoding="utf-8") as f:
    for mag in magnitudes:
        f.write(f"{mag:.6f}\n")