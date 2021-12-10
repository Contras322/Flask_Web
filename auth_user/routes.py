from flask import Blueprint, session, render_template, request, current_app

from DB.database import work_with_db
from DB.sql_provider import SQL_Provider

login_app = Blueprint('login_app', __name__, template_folder='templates')
provider = SQL_Provider('sql/')

@login_app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        sql = provider.get('sql_access.sql', gener1=login, gener2=password)
        result = work_with_db(current_app.config['DB_CONFIG'], sql)

        if result:
            if login == result[0]['user_login'] and password == result[0]['user_password']:
                session['group_name'] = result[0]['role']

                return render_template('right_enter.html')

        return render_template('error_enter.html')

