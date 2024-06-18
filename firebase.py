import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore


def base64_to_dict(encoded: str) -> dict:
    json_decoded = base64.b64decode(encoded)
    return json.loads(json_decoded)


FIREBASE_ENCODED = os.getenv("FIREBASE_ENCODED")
cred = credentials.Certificate(base64_to_dict(FIREBASE_ENCODED))
firebase_admin.initialize_app(cred)

db = firestore.client()
