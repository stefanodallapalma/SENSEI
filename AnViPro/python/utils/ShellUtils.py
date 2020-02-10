import subprocess

def check_program(program_name):
    # Check if JVM is installed
    try:
        process = subprocess.run([program_name, "--version"])
        return True
    except FileNotFoundError:
        return False

