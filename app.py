import os
from flask import Flask
if os.path.exists("env.py"):
    import env

# installing instance of Flask:
app = Flask(__name__)

