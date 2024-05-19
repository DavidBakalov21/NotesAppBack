def display_all(collection,email):
    try:
        documents = collection.find({"email":email})
        documents_list = [doc for doc in documents]
        return documents_list
    except Exception as e:
        print(e)