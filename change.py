from flask import Flask, request, render_template
from flaskext.wtf import Form, FloatField, Required

app = Flask(__name__)
app.secret_key = 'b\xcaf\xde\xc3\xc6\xdc\x03\xf0ls\xd6\x08\xe7\x9a2\x02j\xdf\xa7n\xe5\xf4\xdd'

class ChangeForm(Form):
    cost = FloatField("Total cost of item: $")
    tender = FloatField("Amount tendered: $")
    
@app.route('/', methods=("GET", "POST"))
def user_inputs():
    form = ChangeForm()
    form.errors
    if form.validate_on_submit():
        c = form.cost.data
        t = form.tender.data
        print c,t
        c = "%.2f" % c
        t = "%.2f" % t
        vals = calc_coins(change)
        return render_template("results.html", form=form, vals=vals, c=c, t=t)
    else:
        return render_template("change.html", form=form)    

def calc_coins(change):
    d = {20:'twenties',
         10:'tens',
         5:'fives',
         1:'ones',
         .25:'quarters',
         .1:'dimes',
         .05:'nickels',
         .01:'pennies'}
    denoms = [20, 10, 5, 1, .25, .1, .05, .01]
    vals = []
    i = 0
    while i < len(denoms):
        if change/denoms[i]:
            vals.append("%s: %d" % (d[denoms[i]], change/denoms[i]))
            change = change%denoms[i]
        i += 1
    return vals  
    
if __name__ == "__main__":
    app.run(debug=True)
