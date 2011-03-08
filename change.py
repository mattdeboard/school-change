import sys

from flask import flash, Flask, request, render_template
from flaskext.wtf import Form, FloatField, Required
from wtforms import ValidationError

from secret import secret_key

app = Flask(__name__)
app.secret_key = secret_key

class ChangeForm(Form):
    cost = FloatField("Total cost of item: $", default="0.00")
    tender = FloatField("Amount tendered: $",  default="0.00")

    def validate_tender(form, field):
        if form.cost.data > form.tender.data:
            raise ValidationError()

    
@app.route('/', methods=("GET", "POST"))
def user_inputs(change=None, c=None, t=None, vals=None):
    '''Instantiates ChangeForm() (which subclasses flaskext.wtf.Form()) 
    and renders change.html on GET. Once user inputs the requested data 
    and submits, this function then calls calc_coins() which executes 
    the logic which is the target of this assignment.'''
    form = ChangeForm()
    if request.method == "POST":
        form = ChangeForm(request.form)
        if form.validate():
            change = form.tender.data - form.cost.data
            print >> sys.stderr, change
            c = "%.2f" % form.cost.data
            t = "%.2f" % form.tender.data
            vals = calc_coins(change)
            return render_template("results.html", form=form, vals=vals, c=c, t=t)
        else: 
            flash("Amount tendered must be more than the cost.")

    return render_template("change.html", form=form)    


def calc_coins(change):
    '''This function does the logical heavy lifting required by this 
    assignment. Returns a list of strings which are then iteratively 
    rendered by Flask on the page.'''
    d = {20:'twenties', 10:'tens', 5:'fives', 1:'ones', .25:'quarters', 
         .1:'dimes', .05:'nickels', .01:'pennies'}

    denoms = [20, 10, 5, 1, .25, .1, .05, .01]
    vals = []
    i = 0
    while i < len(denoms):
        if change >= denoms[i]:
            vals.append("%s: %d" % (d[denoms[i]], change/denoms[i]))
            change = change%denoms[i]
        i += 1

    return vals
    
if __name__ == "__main__":
    app.run(debug=True)
