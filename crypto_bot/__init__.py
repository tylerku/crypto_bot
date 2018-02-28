import os

#Set Environment Variables
cwd = os.getcwd() + '/crypto_bot/'
print("CWD: ", cwd)
os.environ["LOGS"] = cwd + 'logs/'
print(os.environ["LOGS"])
