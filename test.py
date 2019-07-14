from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")

#how to include html file
def index():
   return render_template("index.html")
#return render_template("helloworld.html")

#how to include a button
@app.route('/contact', methods=['POST','GET'])   
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            print("Hellow")
            pass # do something
        elif request.form['submit_button'] == 'Do Something Else':
            pass # do something else
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('helloworld.html', form=form)

#@app.route('/handle_data', methods=['POST'])
#def handle_data():
 #   projectpath = request.form['projectFilepath']    
if __name__ == '__main__':
   app.run(debug = True)
