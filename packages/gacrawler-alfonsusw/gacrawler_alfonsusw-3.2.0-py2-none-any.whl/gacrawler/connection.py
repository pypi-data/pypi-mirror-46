# import mysql.connector

# mydb = mysql.connector.connect(
#     host="localhost", user="root", passwd="123456", database="gacrawler")

# mycursor = mydb.cursor()

def insert_page(url, title, text, output_prefix):
    # sql = "INSERT IGNORE INTO pages VALUES (NULL, %s, %s, %s, CURRENT_TIMESTAMP)"
    # val = (url, title, text)
    # mycursor.execute(sql, val)
    # mydb.commit()
    try:
        with open(output_prefix + "relevant.txt", "a+") as f:
                f.write("%s\n" % (url))
        with open(output_prefix + "documents/" + title.replace(" ", "-") + ".txt",
                "a+") as f:
                f.write(text)
    except UnicodeEncodeError:
        pass


def trash_page(url, output_prefix):
    # sql = "INSERT IGNORE INTO trashes VALUES (NULL, %s, %s, CURRENT_TIMESTAMP)"
    # val = (url, reason)
    # mycursor.execute(sql, val)
    # mydb.commit()
    with open(output_prefix + "irrelevant.txt", "a+") as f:
        f.write("%s\n" % (url))

def find_page(url, output_prefix):
    # sql = "SELECT * FROM pages WHERE url='" + url + "'"
    # mycursor.execute(sql)
    # myresult = mycursor.fetchone()
    # if myresult is None:
    #     sql = "SELECT * FROM trashes WHERE url='" + url + "'"
    #     mycursor.execute(sql)
    #     myresult = mycursor.fetchone()
    # return myresult

    if url in open(output_prefix + "relevant.txt").read():
        return True
    if url in open(output_prefix + "irrelevant.txt").read():
        return True
    return False