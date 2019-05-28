from flask import Flask, Response, render_template, request

import requests
import hashlib
import redis


app = Flask(__name__)
cache = redis.StrictRedis(host="redis",
                          port=6379,
                          db=0)
salt = "UNIQUE_SALT"
default_name = ""


@app.route("/", methods=["GET", "POST"])
def index():
    name = request.form.get('name') or default_name
    name_hash = None

    if request.method == "POST" and name != default_name:
        salted_name = salt + name
        name_hash = hashlib.sha256(salted_name.encode()).hexdigest()

    return render_template("index.html",
                           name=name,
                           name_hash=name_hash)


@app.route("/monster/<name>")
def get_identicon(name: str):
    image = cache.get(name)

    if image is None:
        print("Cache miss", flush=True)
        url = "http://dnmonster:8080/monster/" \
              + name \
              + "?size=80"
        r = requests.get(url)
        image = r.content
        cache.set(name, image)

    return Response(image,
                    mimetype="image/png")


def get_monster_url(name: str) -> str:
    return "http://dnmonster:8080/monster/"\
           + name\
           + "?size=80"


if __name__ == "__main__":
    app.run(debug=True,
            host="0.0.0.0")
