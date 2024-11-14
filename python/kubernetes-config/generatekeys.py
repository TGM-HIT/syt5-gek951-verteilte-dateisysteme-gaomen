#!/usr/bin/python3
import os
import base64

# Generate a random 16-character access key
access_key = base64.urlsafe_b64encode(os.urandom(12)).decode('utf-8')

# Generate a random 32-character secret key
secret_key = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')

print("access_key:", access_key)
print("secret_key:", secret_key)

