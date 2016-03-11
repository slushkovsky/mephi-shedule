from flask import Flask, render_template, jsonify
import shedule_maker

app = Flask(__name__)

app.route("/")
def interface():
	shedule = shedule_maker.get_shedule()

	by_days = {day_name: jsonify(shedule[day_name]) for day_name in ("Понедельник", "Вторинк", "Среда", "Четверг", "Пятница", "Суббота")}

	print(by_days)



if __name__ == "__main__": 
	app.debug = True

	app.run()

	