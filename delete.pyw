import os.path
if os.path.isfile("passwords-chrome.txt"):
    os.remove("passwords-chrome.txt")
if os.path.isfile("passwords-edge.txt"):
    os.remove("passwords-edge.txt")