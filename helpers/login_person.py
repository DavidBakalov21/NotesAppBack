def login_user(email, password, collection):
    try:
        result=collection.find_one({"email":email})
        if result['password']==password: 
          return "success" 
        else:
            return "failure"
    except Exception as e:
        print(e)