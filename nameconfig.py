def getInfo():
    f = open("config.txt")
    info = f.readlines()
    username = info[0].rstrip()
    password = info[1]
    f.close()
    return (username, password)

def setInfo(username, password):
    f = open("config.txt", 'w')
    f.seek(0)
    f.truncate()
    f.write(username + '\n')
    f.write(password)



    