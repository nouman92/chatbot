import os
import sys
import json
import requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def verify():
    if request.args.get("hub.mod") == "subscribe" and request.args.get("hub.challange"):
        if not request.args.get("hub.verify_token") == os.getenviron["VERIFY_TOKEN"]:
            return "Verification token mismatch",403
        return request.args["hub.challange"],200
    return "Hello Bot", 200

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    log( data )
    if data["object"] == "page":
        for entry in data["entry"]:
            for messages_events in entry["messaging"]:
                if messages_events.get("message"):
                    sender_id = messages_events["sender"]["id"]
                    recipient = messages_events["recipient"]["id"]
                    messag_txt= messages_events["message"]["text"]
                    send_message(sender_id,"GOT IT!")

                if messages_events.get("delivery"):
                    pass

                if messages_events.get("option"):
                    pass

                if messages_events.get("postback"):
                    pass


    return "OK", 200

def send_message( recipient_id , text_message):
    log("Sending message to {recipient}:{text}".format(recipient=recipient_id, text=text_message))
    params = {
        "access_token" : os.environ["page_access_token"]
    }
    headers = {
        "Content-Type" : "application/json"
    }
    data = json.dumps({
        "recipient" : {
            "id" : recipient_id
        },
        "message" : {
            "text" : text_message
        }
    })
    re = requests.post("https://graph.facebook.com/v2.6/me/messages",params=params, headers=headers, data=data)
    if re.status.code == 200:
        log(re.status_code)
        log(re.text)


def log(text):
    print str(text)
    sys.stdout.flush()


if __name__ == "__main__":
        app.run(debug=True)
