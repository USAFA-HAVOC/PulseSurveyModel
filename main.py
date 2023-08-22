from flask import Flask, render_template, request, redirect, url_for
from textblob import TextBlob
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

# Store the results
data = {
    'close_ended': [],
    'open_ended': []
}

# Model functions from before


def score_close_ended(response, question_num):
    scoring = {
        "strongly disagree": 1,
        "disagree": 2,
        "neutral": 3,
        "agree": 4,
        "strongly agree": 5
    }

    # For questions where disagreeing is a positive response
    reverse_scoring = {
        "strongly disagree": 5,
        "disagree": 4,
        "neutral": 3,
        "agree": 2,
        "strongly agree": 1
    }

    if question_num in [1, 2]:
        return reverse_scoring[response.lower()]
    else:
        return scoring[response.lower()]


def score_open_ended(response):
    analysis = TextBlob(response)
    if analysis.sentiment.polarity > 0.2:
        return 5  # Positive
    elif analysis.sentiment.polarity < -0.2:
        return 1  # Negative
    else:
        return 3  # Neutral


@app.template_filter('enumerate')
def jinja_enumerate(sequence):
    return enumerate(sequence)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get responses and store the scores
        for i in range(8):  # 8 close-ended questions
            response = request.form.get(f'q{i+1}')
            score = score_close_ended(response, i+1)
            data['close_ended'].append((response, score))
        for i in range(6):  # 6 open-ended questions
            response = request.form.get(f'oq{i+1}')
            score = score_open_ended(response)
            data['open_ended'].append((response, score))
        return redirect(url_for('results'))
    return render_template('survey.html')  # Survey page


@app.route('/results')
def results():
    # Generate graph
    close_ended_scores = [score for _, score in data['close_ended']]
    open_ended_scores = [score for _, score in data['open_ended']]

    close_ended_avg = sum(close_ended_scores) / \
        len(close_ended_scores) if close_ended_scores else 0
    open_ended_avg = sum(open_ended_scores) / \
        len(open_ended_scores) if open_ended_scores else 0

    graph = {
        'data': [
            go.Bar(
                x=['Close-ended Questions', 'Open-ended Questions'],
                y=[close_ended_avg, open_ended_avg]
            )
        ],
        'layout': go.Layout(title='Survey Results')
    }

    graphJSON = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('results.html', graphJSON=graphJSON,
                           close_ended=data['close_ended'],
                           open_ended=data['open_ended'])


if __name__ == '__main__':
    app.run(debug=True)
