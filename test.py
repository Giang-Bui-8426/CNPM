import re

def setEmail(newEmail):
        if re.findall(r"(\@)",newEmail):
            user = newEmail.split("@")
            if 6 > len(user[0]) or len(user[0]) > 64:
                return False
            if user[1][0] == "." or user[1][-1] == "." or not re.findall(r"(\.)",user[1]):
                return False
            return True
        else:
            return False
def transferText(text):
    i = 1
    newText = text[0].upper()
    while(i < len(text)):
        if (text[i].isspace()):
            newText += text[i:i+2].upper()
            i +=1
        else:
            newText += text[i].lower()
        i += 1
    return newText
def setUser(newUser):
        if len(newUser) < 6 or len(newUser) > 50 or re.search(r'[^A-Za-z0-9]',newUser):
            return False
        return True
print(setUser("gianggf*"))