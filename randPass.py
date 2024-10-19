# Import necessary libraries
from flask import Flask, render_template_string, request, jsonify
import random
import string

# Create Flask app
app = Flask(__name__)

# Function to generate a strong password
def generate_strong_password(length=12):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    all_chars = lower + upper + digits + special_chars
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(special_chars)
    ]

    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)
    return ''.join(password)

# Route for home page
@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Generator</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css">
    </head>
    <body>
        <section class="section">
            <div class="container">
                <h1 class="title">Random Password Generator</h1>
                <div class="field">
                    <label class="label">Password Length</label>
                    <div class="control">
                        <input class="input" type="number" id="length" value="16" min="4">
                    </div>
                </div>
                <div class="control">
                    <button class="button is-primary" onclick="generatePassword()">Generate Password</button>
                    <button class="button is-primary" onclick="reset()">Reset</button>
                </div>
                <div class="field">
                    <label class="label">Generated Password</label>
                    <div class="control">
                        <input class="input" type="text" id="password" readonly>
                    </div>
                </div>
            </div>
        </section>
        <script>
            function generatePassword() {
                const length = document.getElementById("length").value;
                fetch(`/generate-password?length=${length}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("password").value = data.password;
                    });
            }

            function reset() {  
                document.getElementById("password").value = "";
            }
        </script>
    </body>
    </html>
    ''')

# Route for generating password
@app.route('/generate-password')
def generate_password():
    length = request.args.get('length', default=12, type=int)
    password = generate_strong_password(length)
    return jsonify(password=password)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
