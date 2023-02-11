from flask import Flask, render_template, request
import pickle
import numpy as np
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
import os


class EditForm(FlaskForm):
    uid = IntegerField('User ID')
    submit = SubmitField('Рассчитать')


app = Flask(__name__)


SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@app.route('/result', methods=["GET", "POST"])
def result_of_recommend():
    if request.method == "GET":
        form = EditForm()
        return render_template('index.html', form=form)
    if request.method == "POST":
        args = dict(request.form)

        while True:
            try:
                testing = int(args['uid'])
                break
            except:
                result = 'Введите заново корректное целое число - ID пользователя'
                return render_template('result.html',
                                       result=result)

        uid = args['uid']

        with open('src/algo.pkl', 'rb') as input_file:
            algo = pickle.load(input_file)

        unique_items = np.loadtxt('src/unique_items.txt').astype(int)


        dict_ = {}
        sorted_dict = {}

        for iid in unique_items:
            dict_[iid] = algo.predict(uid, iid).est

        sorted_keys = sorted(dict_, key=dict_.get, reverse=True)

        for w in sorted_keys:
            sorted_dict[w] = dict_[w]

        first = list(sorted_dict)[:3][0]
        second = list(sorted_dict)[:3][1]
        third = list(sorted_dict)[:3][2]
        result = 'Recommendations for user {}: {}, {}, {}'.format(uid, first, second, third)
        return render_template('result.html',
                               result=result,
                               uid=uid,
                               first=first,
                               second=second,
                               third=third)


if __name__ == '__main__':
    app.run(debug=True)
