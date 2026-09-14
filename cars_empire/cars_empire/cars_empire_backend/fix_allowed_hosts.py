import re

# Read the settings file
with open('settings.py', 'r') as f:
    content = f.read()

# Replace existing ALLOWED_HOSTS
content = re.sub(
    r"ALLOWED_HOSTS\s*=\s*\[.*?\]",
    "ALLOWED_HOSTS = ['carsempire.net', 'www.carsempire.net', '*', 'testserver', 'localhost', '127.0.0.1']",
    content,
    flags=re.DOTALL
)

# Write the file back
with open('settings.py', 'w') as f:
    f.write(content)

print("Fixed ALLOWED_HOSTS setting")
