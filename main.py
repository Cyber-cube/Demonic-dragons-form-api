from flask import Flask, render_template, request, flash, redirect, url_for
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, origins=["https://github.com/Cyber-cube/Demonic-dragons/settings/pages"])

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register', methods=["POST"])
def register():
  device_id = str(request.form['device_id'])
  username = str(request.form['name'])

  with open("data.json") as f:
    data = json.load(f)
  if (username in data) or (device_id in data):
    return "Username or an account on this device is already made\n(is username ya to apke device pei ek account bana hua hai)"
  else:
    with open("unaccepted.json") as file:
      data_two = json.load(file)
    data_two["users"].append(f"{username} ({device_id})")
    data[str(device_id)] = {}
    data[str(device_id)]["name"] = str(username)
    data[str(device_id)]["account_accepted"] = False
    data[str(device_id)]["roles"] = []
    with open("data.json", "w") as f:
      json.dump(data, f, indent=2)
    with open("unaccepted.json", "w") as file:
      json.dump(data_two, file, indent=2)
    return "Your account has been made, an admin will look your account and accept\n(apka account ban gaya hai, ek admin apka account dekhega and accept karega)"

@app.route('/checkaccstatus', methods=["POST"])
def checkaccstatus():
  device_id = str(request.form["device_id"])

  with open("data.json") as f:
    data = json.load(f)
  if data[str(device_id)]["account_accepted"] == False:
    return "Your account is not accepted yet\n(apka account abhi tak accept nahi hua hai)"
  else:
    return "Your account has been accepted, you can login now\n(Apka account accept ho gaya hai, aab aap login kar sakte hai)"

@app.route('/login', methods=["POST"])
def login():
  device_id = str(request.form["device_id"])

  with open("data.json") as f:
    data = json.load(f)
  if data[str(device_id)]["account_accepted"] == False:
    return "Your account isn't accepted yet so you cannot login at moment\n(Apka account abhi tak accept nahi hua hai isliye aao abhi login nahi kar sakte("
  elif not str(device_id) in data:
    return "You haven't made an account yet, so make it by going back\n(Apne abhi tak ek account nahi banaya hai, aap pichle wale webpage pei jake login kar account bana sakte hai)"
  else:
    return render_template("mainpage.html")

@app.route('/acceptingaccpage', methods=["POST"])
def acceptingaccpage():
  device_id = str(request.form["device_id"])

  with open("data.json") as f:
    data = json.load(f)
  if not "Admin" in data[str(device_id)]["roles"]:
    return "You don't have the Admin role\n(Aapke pas Admin role nahi hai)"
  elif not str(device_id) in data:
    return "You don't have an account yet\n(Aapke pas abhi tak ek account nahi hai)"
  else:
    with open("unaccepted.json") as f:
      data_two = json.load(f)
    list = str(data_two["users"])
    return render_template("acceptpage.html", data=list)
    
@app.route('/accept', methods=["POST"])
def accept():
  device_id = request.form["device_id"]
  username = request.form["username"]

  with open("unaccepted.json") as f:
    data = json.load(f)
  if not f"{username} ({device_id})" in data["users"]:
    output = "The following user isn't in the unaccepted users list\n(Ye user unaccepted users ke list mei nahi hai)"
    return render_template("acceptpageoutput.html", data=output)
  else:
    with open("data.json") as file:
      data_two = json.load(file)
    data_two[str(device_id)]["account_accepted"] = True
    data_two[str(device_id)]["roles"].append("Member")
    data["users"].remove(f"{username} ({device_id})")
    with open("data.json", "w") as file:
      json.dump(data_two, file, indent=2)
    with open("unaccepted.json", "w") as f:
      json.dump(data, f, indent=2)
    output = "The user inputted is accepted now they can login\n(Ye user jo input hue hai, accept ho gaye aur aab vo login kar sakte hai)"
    return render_template("acceptpageoutput.html", data=output)

@app.route('/gobackacceptpage', methods=["POST"])
def gobackacceptpage():
  with open("unaccepted.json") as f:
    data = json.load(f)
  list = data["users"]
  return render_template("acceptpage.html", data=list)

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=8080)