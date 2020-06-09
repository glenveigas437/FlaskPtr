from flask import Flask, render_template, request

app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def root():
	return render_template('index.html')


@app.route('/marks', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/getdetails', methods=['GET', 'POST'])
def getdetails():
    global name
    if request.method == 'POST':
        name = request.form['name']
        sems = request.form['sems']
        sems=int(sems)
        return render_template('new.html', n=name, s=sems)
    return render_template('index.html')
    return name	


if __name__ == '__main__':
    app.run()

