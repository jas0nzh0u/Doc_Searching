import math
import numpy as np

def createDictionary(file):
    dictionary = set()
    for line in file:
        dictionary.update(line.split())
    return sorted(list(dictionary))

def inverted_index(file):
    i_index = {}
    for id, line in enumerate(file, start=1): #Assigning an ID starting at 1
        for word in line.split():
            if word not in i_index:
                i_index[word] = [id] #Add word with the current ID
            elif id not in i_index[word]:
                i_index[word].append(id) #If word is in the inverted index but the current ID isn't
    return i_index

def create_doc_vectors(docsFile, dictionary):
    dictionary_index = {word: index for index, word in enumerate(dictionary)}
    vectors = []
    for doc in docsFile:
        vector = [0] * len(dictionary)
        for word in doc.split():
            if word in dictionary_index:
                vector[dictionary_index[word]] += 1 #Adds to the count when the word is found
        vectors.append(vector)
    return vectors


def calc_angle(docVector, queryVector):
    docNorm = np.linalg.norm(docVector)
    queryNorm = np.linalg.norm(queryVector)
    dot_product = np.dot(docVector, queryVector)
    cos_theta = dot_product / (docNorm * queryNorm)
    theta = math.degrees(math.acos(cos_theta))
    return theta

def main():
    # Read documents
    with open('docs.txt', 'r') as f:
        docsFile = f.readlines()

    # Read queries
    with open('queries.txt', 'r') as f:
        queriesFile = f.readlines()


    #Create dictionary and inverted index
    dictionary = createDictionary(docsFile)
    index = inverted_index(docsFile)
    print("Words in dictionary:",len(dictionary))
    
    #Calculate document vector
    doc_vector = create_doc_vectors(docsFile, dictionary)
    
    #Process query
    for query in queriesFile:
        query = query.strip()
        print(f"Query:", query)

        q_words = set(query.split())
        relevant_docs = set()

        #Finding relevant documents
        for word in q_words:
            if word in index:
                if not relevant_docs:
                    relevant_docs = set(index[word])
                else:
                    relevant_docs = relevant_docs.intersection(index[word])
        relevant_docs = sorted(relevant_docs) if relevant_docs else []

        print("Relevant documents:", " ".join(map(str, relevant_docs))) #converts each element to a string and concatenates

        #Create vector and angle
        if relevant_docs:
            relevant_docs_angles = []
            queryVector =[1 if word in q_words else 0 for word in dictionary]

            for id in relevant_docs:
                docVector = doc_vector[id - 1]
                angle = calc_angle(docVector, queryVector)
                relevant_docs_angles.append((id, angle))
            relevant_docs_angles.sort(key=lambda x: x[1])

            #Print relevant documents with angles
            for id, angle in relevant_docs_angles:
                print(f"{id} {angle:.2f}")

if __name__ == "__main__":
    main()