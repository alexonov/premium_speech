from flask import Flask, request, render_template
from premium.brown import get_text
from premium.main import apply_premium_speak


app = Flask(__name__)


def highlighter(new_word, original_word):
    return f'<b title="{original_word}" class="highlighted">{new_word}</b>'


def highlighter2(new_word, original_word):
    return f'<span>{new_word}</span>'


@app.route('/', methods=["GET", "POST"])
def index():
    input_text = request.form.get('text-input') or ''
    output_text = request.form.get('text-output') or ''

    if request.method == 'POST':

        if request.form.get('button-submit') == 'submit':
            output_text = apply_premium_speak(input_text, highlighter=highlighter)

        elif request.form.get('button-generate') == 'generate':
            input_text = ' '.join(get_text())
            print(input_text)

        else:
            pass  # unknown

    return render_template("index.html", input_text=input_text, output_text=output_text)


if __name__ == '__main__':
    app.run(debug=True)
