from flask import redirect, request, render_template, Flask
from util import ttsmp3

#create flask server
app = Flask(__name__)


@app.route('/')
def index():
	return render_template('./index.html')


@app.route('/speak', methods=['GET', 'POST'])
def speak_phrase():
	phrase = "error"
	if request.method == 'POST':
		phrase = request.form.get('phrase')
	elif request.method == 'GET':
		phrase = request.args.get('phrase')

	print("Got phrase:", phrase)
	ttsmp3(phrase)
	return redirect('/')



def main():
	app.run(debug=True)


if __name__ == "__main__":
	main()