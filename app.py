import os
from flask import Flask
if os.path.exists("env.py"):
    import env

# installing instance of Flask:
app = Flask(__name__)


# telling app how & where to run app
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
