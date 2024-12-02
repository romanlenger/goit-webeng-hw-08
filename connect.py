from mongoengine import connect

connect(
    db="Cluster0",
    username="romero",
    password="mort123mort",
    host="mongodb+srv://cluster0.gy9s2.mongodb.net",
    authentication_source="admin"
)