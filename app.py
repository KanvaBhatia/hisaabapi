from flask import Flask, request, jsonify
import pymongo
from urllib.parse import quote_plus
from werkzeug.security import generate_password_hash, check_password_hash
import pygsheets
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('SVG')
import numpy as np
import io
import time
import base64

########################################################################################

gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')

app = Flask(__name__)

passs = quote_plus("")
client = pymongo.MongoClient(f"mongodb+srv://KanvaBhatia:{passs}@cluster0.ltwqycz.mongodb.net/?retryWrites=true&w=majority")
db = client.OnlyHisaab_data
print(db.user_data.find_one({'email':'ooooo@ooo.com'})['pass'])
# if db.user_data.find_one({'email':'ooooo@oo.com'}):
#     print("ooo")

# print(col.find_one())

@app.route('/', methods = ['POST', 'GET'])
def getHandler():
    return "OK"

@app.route('/post/login', methods = ['POST'])
def login():
    print("Login")
    if request.method == "GET":
        return "Wrong Method!"
    try:
        r = (request.args if request.args else request.json)
        # print(r)
        email = r['email']
        password = r['password']
        # print(email, password)
        user_signed_up = "False"
        correct_pass = "False"
        user = db.user_data.find_one({'email': email})
        # print(user)
        if user:
            user_signed_up = "True"
            if check_password_hash(user['pass'], password):
                correct_pass = "True"
        return jsonify(user_signed_up = user_signed_up, correct_pass = correct_pass, name = user['name'])
    except Exception as e:
        return jsonify(error = str(e))

@app.route('/post/signup', methods = ['POST'])
def signup():
    if request.method == "GET":
        return "Wrong Method!"
    try:
        r = (request.args if request.args else request.json)
        email = r['email']
        name = r['name']
        password = r['password']
        user = db.user_data.find_one({'email': email})
        user_already_signed_up = "False"
        if user:
            user_already_signed_up = "True"
            return jsonify(user_already_signed_up = user_already_signed_up)
        else:
            db.user_data.insert_one({'name':name, 'email':email, 'pass':generate_password_hash(password, method='sha256')})

            gc.sheet.create(email)
            sh = gc.open(email)
            wks = sh[0]

            pygsheets.Cell(pos = (1,1),worksheet = wks).set_value("Date").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,2),worksheet = wks).set_value("Expense for").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,3),worksheet = wks).set_value("Expense Amount").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,4),worksheet = wks).set_value("Classify").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,5),worksheet = wks).set_value("Food").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,6),worksheet = wks).set_value("Travel").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,7),worksheet = wks).set_value("Padhai").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,8),worksheet = wks).set_value("Others").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,9),worksheet = wks).set_value("Total").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
            pygsheets.Cell(pos = (1,10),worksheet = wks).set_value("Month").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)

            pygsheets.Cell(pos = (2,1),worksheet = wks).set_value(str(datetime.date.today()))
            pygsheets.Cell(pos = (2,2),worksheet = wks).set_value("Random record please don't delete!!")
            pygsheets.Cell(pos = (2,3),worksheet = wks).set_value(1)
            pygsheets.Cell(pos = (2,4),worksheet = wks).set_value('none')
            pygsheets.Cell(pos = (2,5),worksheet = wks).set_value('=IF(D2="food", C2, 0)')
            pygsheets.Cell(pos = (2,6),worksheet = wks).set_value('=IF(D2="travel", C2, 0)')
            pygsheets.Cell(pos = (2,7),worksheet = wks).set_value('=IF(D2="padhai", C2, 0)')
            pygsheets.Cell(pos = (2,8),worksheet = wks).set_value('=IF(D2="others", C2, 0)')
            pygsheets.Cell(pos = (2,9),worksheet = wks).set_value("=E2+F2+G2+H2")
            pygsheets.Cell(pos = (2,10),worksheet = wks).set_value('=year(A2) &"-"& MONTH(A2)')


            sh.share("kbthebest181@gmail.com", role='writer', type = 'user', emailMessage = email+" just created an account and here's the spreadsheet.")
            sh.share(email, role='reader', type = 'user', emailMessage = f"Congratulations for registering with OnlyHisaab, {r['name']}!\nHere is the access to your spreadsheet. You cannot edit it, contact us for any issue.")

            return jsonify(user_already_signed_up = user_already_signed_up, user_new_signup = "True")
    except Exception as e:
        return jsonify(user_already_signed_up = user_already_signed_up, user_new_signup = "False", error = str(e))

@app.route('/post/addtohisaab', methods = ['POST'])
def addexpense():
    if request.method == "GET":
        return "Wrong Method!"
    r = (request.args if request.args else request.json)

    email = r['email']
    dateee = r["date"]
    expensee = r["expense"]
    amount = r["amount"]
    classific = r["type"]
    adding_success = "False"
    error = "None"
    if email == "kanva.bhatia@gmail.com":
        gc = pygsheets.authorize(service_file='leafy-stock-354615-5b6f0be4032f.json')
        sh = gc.open('Expenses')
        wks = sh[0]
        try:
            lennn = (len(wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[0]))
            pygsheets.Cell(pos = (lennn+1, 1),worksheet = wks).set_value(dateee)
            pygsheets.Cell(pos = (lennn+1, 2),worksheet = wks).set_value(expensee)
            pygsheets.Cell(pos = (lennn+1, 3),worksheet = wks).set_value(int(amount))
            pygsheets.Cell(pos = (lennn+1, 10),worksheet = wks).set_value(classific)
            adding_success = "True"
            return jsonify(adding_success = adding_success, error = error)
        except Exception as e:
            return jsonify(adding_success = adding_success, error = str(e))
    else:
        gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')
        sh = gc.open(email)
        wks = sh[0]
        try:
            lennn = (len(wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[0]))
            pygsheets.Cell(pos = (lennn+1, 1),worksheet = wks).set_value(dateee)
            pygsheets.Cell(pos = (lennn+1, 2),worksheet = wks).set_value(expensee)
            pygsheets.Cell(pos = (lennn+1, 3),worksheet = wks).set_value(int(amount))
            pygsheets.Cell(pos = (lennn+1, 4),worksheet = wks).set_value(classific)
            pygsheets.Cell(pos = (lennn+1, 5),worksheet = wks).set_value(f'=IF(D{lennn+1}="food", E{lennn}+C{lennn+1}, E{lennn})')
            pygsheets.Cell(pos = (lennn+1, 6),worksheet = wks).set_value(f'=IF(D{lennn+1}="travel", F{lennn}+C{lennn+1}, F{lennn})')
            pygsheets.Cell(pos = (lennn+1, 7),worksheet = wks).set_value(f'=IF(D{lennn+1}="padhai", G{lennn}+C{lennn+1}, G{lennn})')
            pygsheets.Cell(pos = (lennn+1, 8),worksheet = wks).set_value(f'=IF(D{lennn+1}="others", H{lennn}+C{lennn+1}, H{lennn})')
            pygsheets.Cell(pos = (lennn+1, 9),worksheet = wks).set_value(f"=E{lennn+1}+F{lennn+1}+G{lennn+1}+H{lennn+1}")
            pygsheets.Cell(pos = (lennn+1, 10),worksheet = wks).set_value(f'=year(A{lennn+1}) &"-"& MONTH(A{lennn+1})')
            adding_success = "True"
            return jsonify(adding_success = adding_success, error = error)
        except Exception as e:
            return jsonify(adding_success = adding_success, error = str(e))


@app.route('/post/summary', methods = ['POST'])
def summary():
    if request.method == "GET":
        return "Wrong Method!"
    try:
        r = (request.args if request.args else request.json)

        email = r['email']
        month_chosen = r['month']
        if email == 'kanva.bhatia@gmail.com':
            gc = pygsheets.authorize(service_file='leafy-stock-354615-5b6f0be4032f.json')
            sh = gc.open('Expenses')
            wks = sh[0]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            current_month = months.index(month_chosen)+1
            row_last = wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1]
            for i in range(len(row_last)-1,-1,-1):
                if row_last[i] == (f"{datetime.date.today().year}-{current_month}"):
                    last_index = i
                    break
            first = ((wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1].index(f"{datetime.date.today().year}-{current_month}")))
            month_total_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][14])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][14])))
            month_others_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][13])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][13])))
            month_padhai_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][12])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][12])))
            month_travel_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][11])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][11])))
            month_food_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][10])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][10])))
        else:
            gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')
            sh = gc.open(email)
            wks = sh[0]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            current_month = months.index(month_chosen)+1
            row_last = wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1]
            for i in range(len(row_last)-1,-1,-1):
                if row_last[i] == (f"{datetime.date.today().year}-{current_month}"):
                    last_index = i
                    break
            first = ((wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1].index(f"{datetime.date.today().year}-{current_month}")))
            month_total_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][8])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][8])))
            month_others_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][7])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][7])))
            month_padhai_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][6])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][6])))
            month_travel_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][5])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][5])))
            month_food_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][4])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][4])))

        result = {"Food":month_food_expense, "Travel":month_travel_expense, "Padhai":month_padhai_expense, "Others":month_others_expense, "Total":month_total_expense}
        # import matplotlib.pyplot as plt
        # import matplotlib
        # matplotlib.use('SVG')
        # import numpy as np

        y = np.array([month_food_expense, month_travel_expense, month_padhai_expense, month_others_expense])
        mylabels = [f"Food = {round((month_food_expense*100/month_total_expense), 2)}%", f"Travel = {round((month_travel_expense*100/month_total_expense),2)}%", f"Padhai = {round((month_padhai_expense*100/month_total_expense),2)}%", f"Others = {round((month_others_expense*100/month_total_expense),2)}%"]
        img = io.BytesIO()
        plt.clf()
        plt.pie(y, labels = mylabels)
        plt.legend(title = "Expenses:",bbox_to_anchor=(1.2,1.05), loc="upper right", fontsize=10, bbox_transform=plt.gcf().transFigure)
        plt.savefig(img, format = 'png', bbox_inches="tight") 
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return jsonify(summary_res = "True", result = result, image = plot_url , month = month_chosen)
    except Exception as e:
        return jsonify(summary_res = "False", error = str(e))



# app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    # db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True, host = '0.0.0.0') # run the flask app on debug mode
