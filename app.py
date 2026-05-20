from flask import Flask, render_template, request, redirect
import csv
import os
import datetime

app = Flask(__name__)

FILE_NAME = "water_log.csv"

# --------------------
# CREATE CSV FILE
# --------------------
def create_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Goal (Ounces)", "Interval (Hours)", "Date"])

create_file()

# --------------------
# HOME PAGE
# --------------------
@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    progress = []

    if request.method == "POST":
        name = request.form.get("name")
        total_water = request.form.get("goal")
        interval = request.form.get("interval")

        if name and total_water and interval:
            total_water = float(total_water)
            interval = int(interval)

            times = 10 // interval
            water_each_time = round(total_water / times, 1)

            summary = f"{name}, drink {water_each_time} oz every {interval} hour(s) from 8AM–6PM."

            date = datetime.date.today()

            with open(FILE_NAME, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, total_water, interval, date])

    # LOAD CSV DATA
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            progress.append(row)

    return render_template("index.html", summary=summary, progress=progress)

# --------------------
# RESET CSV
# --------------------
@app.route("/reset")
def reset():
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Goal (Ounces)", "Interval (Hours)", "Date"])

    return redirect("/")

# --------------------
# RUN APP
# ---------------------
if __name__=="__main__":
    app.run(debug=True)
