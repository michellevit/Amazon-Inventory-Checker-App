# generate_django_secret_key.py
#
# PURPOSE:
## This script is used to generate a secret key for the Django app.
#
# INSTRUCTIONS: 
## Ensure python is installed
## Open a powershell terminal and navigate to the project's root dir
## Run: python ./generate_django_secret_key.py
## Copy-paste the result into the config var ‘Value’ field
## Note: You may delete this script from the project once the Django secret key has been set


import string
from random import choice

def generate_secret_key(length=50):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(choice(chars) for _ in range(length))

print(generate_secret_key())