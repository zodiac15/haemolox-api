import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="python"
)

curr = db.cursor(buffered=True)
username = 'abc'
sql = "select password from user where email = '{}'".format(str(username))
curr.execute(sql)
db.commit()
res = curr.fetchone()
password_db = res[0]
print(password_db)