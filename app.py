import functions

from flask import Flask, render_template, request

app = Flask(__name__)


# Create a view function for /
@app.route('/', methods=['GET'])
def welcome():
    return render_template('welcome.html')

# Create a view function for /results
@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'POST':
        file = request.files['file']
        employment_types = str(request.form['employment'])
        date_posted = str(request.form['date_posted'])
        num_pages = str(request.form['page'])
        name = str(request.form['name'])
        resume_result = functions.resume_ph(file, name)
        query = resume_result[0] + " in " + resume_result[1]
        job_result = functions.job_search(query = query, date_posted = date_posted, employment_types = employment_types, numpages = num_pages)
        return render_template('results.html', job_result= job_result, name = name)
    else:
        return 'Wrong HTTP method', 400