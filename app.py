from flask import Flask, render_template, jsonify
import shedule_maker

app = Flask(__name__)

@app.route("/")
def interface():
    shedule = shedule_maker.get_shedule()

    return render_template("index.html", shedule=shedule.week_even())

if __name__ == "__main__": 
    app.debug = True
    app.run()

    