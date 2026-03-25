from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    name = "frfrefregregre"
    return render_template("layout.html",name=name)


if __name__=="__main__":
    app.run(debug=True)