import os

path = os.environ["LOGS"]
output_file = os.path.join(path, 'log.txt')

def clear_output_log():
    with open(output_file, 'w') as f:
        f.write("\n")

def log_output(*args):
    with open(output_file, 'a') as f:
        for _, output_item in enumerate(args):
            f.write(str(output_item))
        f.write("\n")
