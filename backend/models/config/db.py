from mongoengine import connect
def connect_db():
    try:
        connect(host="mongodb://localhost:27017/resume_filter_db")
        print("data base connected")
    except Exception as e:
        print("database connection failed",e)