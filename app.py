# app.py
#
# Use this sample code to handle webhook events in your integration.
#
# 1) Paste this code into a new file (app.py)
#
# 2) Install dependencies
#   pip3 install flask
#   pip3 install stripe
#
# 3) Run the server on http://localhost:4242
#   python3 -m flask run --port=4242

import json
import os
import stripe

from flask import Flask, jsonify, request

# The library needs to be configured with your account's secret key.
# Ensure the key is kept out of any version control system you might be using.
stripe.api_key = "sk_test_51NYt3xAPRx2Hg8fSKVyF0SZKhpbuNXho3StGHCWpNzcHN36OFJAJUp67r067BfieEfpWYXIqd29lyJbYLUgPe5Pa00jkv1xbP9"

# This is your Stripe CLI webhook secret for testing your endpoint locally.
endpoint_secret = 'whsec_64196e3bde9fb1177dd5df344952b6905a92ba0306145cbf2f7eb66a57f3781c'

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    event = None
    payload = request.data
    sig_header = request.headers['STRIPE_SIGNATURE']
    print(sig_header)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        raise e
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        raise e

    # Handle the event
    if event['type'] == 'customer.created':
      customer = event['data']['object']
      print(customer)
    # ... handle other event types
    else:
      print('Unhandled event type {}'.format(event['type']))

    return jsonify(success=True)


if __name__ == '__main__':
    app.run(port=4242)





