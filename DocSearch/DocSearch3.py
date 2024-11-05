import math

def createDictionary(file):
    dictionary = set()
    for line in file:
        dictionary.update(line.split())
    return sorted(list(dictionary))

def inverted_index(file):
    i_index = {}
    for id, line in enumerate(file, start=1): #Assigning an ID starting at 1
        words = line.split()
        for word in words:
            if word not in i_index:
                i_index[word] = [id] #Add word with the current ID
            elif id not in i_index[word]:
                i_index[word].append(id) #If word is in the inverted index but the current ID isn't
    return i_index

#Query vector
def create_vector(dictionary, query):
    vector = []
    for word in query:
        if word in dictionary:
            vector.append(1)
        else:
            vector.append(0)
    return vector

def create_doc_vectors(docsFile, dictionary):
    document_vectors = []
    for doc in docsFile:
        doc_vector = [doc.count(word) for word in dictionary]
        document_vectors.append(doc_vector)
    return document_vectors

def calc_angle(docVector, queryVector):
    dot_product = sum(x * y for x, y in zip(docVector, queryVector))
    docNorm = math.sqrt(sum(x ** 2 for x in docVector))
    queryNorm = math.sqrt(sum(x ** 2 for x in queryVector))
    
    if docNorm == 0 or queryNorm == 0:
        return 0
    
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
    
    #Calc document vector
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

        print("Relevant documents:", " ".join(map(str, relevant_docs)))

        #Create vector and angle
        if relevant_docs:
            relevant_docs_angles = []
            queryVector = create_vector(query, dictionary)

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

