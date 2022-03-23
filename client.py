import requests
url = "http://127.0.0.1:8000/"
print("Hard coded url is:",url)
commandList = """Commands:
    'register <username> <password> <email>' - Register account with given credentials
    'login <username> <password>' - Login to session with given credentials
    'logout' - Logout of session
    'list' - Lists all modules and the professors teaching them
    'view' - Lists the average rating of all professors over all modules they teach
    'average <profID> <moduleID>' - Gives the average rating of a given professor on a given module
    'rate <profID> <moduleID> <year> <semester> <rating>' - Rate a professor in a given module, year and semester, rating is 1-5, must be logged in
    'url <new-url>' - Change the hard coded url to a different one
    'help' - See this list of commands
    'quit' - Exit the program"""
print(commandList)

def register(command):
    if(len(command) != 4):
        print("register usage:\nregister <username> <password> <email>")
        return
    res = session.post(url+"api/register",data={"username":command[1],"password":command[2],"email":command[3]})
    print(res.text)
    return

def login(command):
    if(len(command) != 3):
        print("login usage:\nlogin <username> <password>")
        return
    res = session.post(url+"api/login",data={"username":command[1],"password":command[2]})
    print(res.text)
    return

def logout():
    res = session.post(url+"api/logout")
    print(res.text)
    return

def list():
    res = session.get(url+"api/list")
    print(res.json())
    return

def view():
    res = session.get(url+"api/view")
    print(res.json())
    return

def average(command):
    if(len(command) != 3):
        print("average usage:\naverage <profID> <moduleID>")
        return
    res = session.post(url+"api/average",data={"profID":command[1],"moduleID":command[2]})
    print(res.json())
    return

def rate(command):
    if(len(command) != 6):
        print("rate usage:\nrate <profID> <moduleID> <year> <semester> <rating>")
        return
    res = session.post(url+"api/rate",data={"profID":command[1],"moduleID":command[2],"year":command[3],"semester":command[4],"rating":command[5]})
    print(res.text)
    return

def changeUrl(command):
    if(len(command) != 2):
        print("url usage:\nurl <new-url>")
    global url 
    url = command[1]

session = requests.Session()
while True:
    print(">", end="")
    command = input().split(" ")
    if command[0] == "register":
        register(command)
    elif command[0] == "login":
        login(command)
    elif command[0] == "logout":
        logout()
    elif command[0] == "list":
        list()
    elif command[0] == "view":
        view()
    elif command[0] == "average":
        average(command)
    elif command[0] == "rate":
        rate(command)
    elif command[0] == "url":
        changeUrl(command)
    elif command[0] == "quit":
        break
    elif command[0] == "help":
        print(commandList)
    else:
        print("Invalid command, use 'help' to see list of commands")