from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

FILENAME = "messages.json"

def update_file(file, data):
    file.seek(0)
    file.truncate()
    json.dump(data, file, indent=4)

@app.route("/")
def globall():
    messages : str
    display_name = request.args.get("display_name")\

    with open(FILENAME, "r") as file:
        data = json.load(file)
        messages = data["messages"]

    return render_template("global.html", messages=messages, displayer=display_name)

@app.route("/new-message", methods=["POST"])
def post():
    message = request.form.get("message")
    display_name = request.form.get("display_name")

    with open(FILENAME, "r+") as file:
        message_data = json.load(file)
        if not display_name:
            display_name = "User"
        message_data["messages"].append({"value": message, "displayname": display_name+": "})
        update_file(file, message_data)

    return redirect(url_for("globall", display_name=display_name))

@app.route("/get-messages", methods=["GET"])
def get_messages():
    with open(FILENAME, "r") as file:
        message_data = json.load(file)

    return jsonify(message_data)


if __name__ == "__main__":
    #app.run(debug=False, host="0.0.0.0") public
    app.run(debug=True) # debug