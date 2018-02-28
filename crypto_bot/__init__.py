import os

#Set Environment Variables
cwd = os.getcwd() + '/crypto_bot/'
logs_dir = cwd + 'logs/'
os.environ["LOGS"] = logs_dir
if not os.path.isdir(logs_dir):
    os.makedirs(logs_dir)
