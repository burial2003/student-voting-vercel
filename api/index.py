from flask import Flask, render_template, request, make_response
import random
import socket
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

app = Flask(__name__, template_folder=TEMPLATE_DIR)

hostname = socket.gethostname()


@app.route("/", methods=["GET", "POST"])
def hello():

    voter_id = request.cookies.get("voter_id")

    if not voter_id:
        voter_id = hex(random.getrandbits(64))[2:-1]

    if request.method == "POST":

        vote = request.form.get("vote")

        print(f"Vote received: {vote}")
        print(f"Voter ID: {voter_id}")

        response = make_response(
            f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport"
                      content="width=device-width, initial-scale=1.0">

                <title>Vote Submitted</title>

                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background: #f4f6f8;
                        text-align: center;
                        padding-top: 60px;
                    }}

                    .container {{
                        background: white;
                        width: 500px;
                        max-width: 90%;
                        margin: auto;
                        padding: 35px;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
                    }}

                    h1 {{
                        color: #27ae60;
                    }}

                    p {{
                        font-size: 18px;
                    }}

                    a {{
                        display: inline-block;
                        margin-top: 20px;
                        padding: 12px 25px;
                        background: #3498db;
                        color: white;
                        text-decoration: none;
                        border-radius: 8px;
                    }}
                </style>
            </head>

            <body>

                <div class="container">

                    <h1>Vote Submitted!</h1>

                    <p>
                        You voted for:
                        <strong>{vote}</strong>
                    </p>

                    <p>Thank you for voting.</p>

                    <a href="/">
                        Back to Voting
                    </a>

                </div>

            </body>
            </html>
            """
        )

        response.set_cookie("voter_id", voter_id)

        return response

    response = make_response(
        render_template(
            "index.html",
            hostname=hostname
        )
    )

    response.set_cookie("voter_id", voter_id)

    return response


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
