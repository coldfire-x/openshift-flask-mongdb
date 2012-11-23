from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        do_the_login()

    else:
        return render_template('login.html')

if __name__ == "__main__":
    app.run()
