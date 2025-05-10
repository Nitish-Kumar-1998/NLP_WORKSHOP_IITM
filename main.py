import time
import hmac
import hashlib
import struct
import base64
import json
from urllib.request import Request, urlopen

def generate_totp(secret, digits=10, timestep=30, t0=0):
    # Generate a TOTP code according to RFC6238 with HMAC-SHA-512
    counter = int((int(time.time()) - t0) // timestep)
    key = secret.encode()
    msg = struct.pack(">Q", counter)
    h = hmac.new(key, msg, hashlib.sha512).digest()
    offset = h[-1] & 0x0F
    code = (struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return str(code).zfill(digits)

def main():
    # ====== CHANGE THESE VALUES ======
    email = "nitishkumar199824@gmail.com"  # <-- Put your email here
    gist_url = "https://gist.github.com/Nitish-Kumar-1998/b3333f71d8bd30ae5e432efc0bc2f839"  # <-- Put your Gist URL here
    language = "python"  
    # =================================

    secret = email + "HENNGECHALLENGE004"
    totp = generate_totp(secret)

    json_data = {
        "github_url": gist_url,
        "contact_email": email,
        "solution_language": language
    }

    # Prepare HTTP request
    url = "https://api.challenge.hennge.com/challenges/backend-recursion/004"
    data = json.dumps(json_data).encode()
    auth_str = f"{email}:{totp}"
    auth_header = "Basic " + base64.b64encode(auth_str.encode()).decode()
    headers = {
        "Content-Type": "application/json",
        "Authorization": auth_header
    }

    req = Request(url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req) as response:
            print("Status Code:", response.status)
            print("Response:", response.read().decode())
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
