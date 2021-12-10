from flask import Blueprint, render_template, current_app, request
from DB.sql_provider import SQL_Provider
from DB.database import work_with_db
from access import group_permission_decorator


user_app = Blueprint('user_app', __name__, template_folder='templates')
provider = SQL_Provider('sql/')


@user_app.route('/')
def user_index():
    return render_template('menu.html')


@user_app.route('/sql1', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql1():
    name = ['id товара', 'Название товара']
    if request.method == 'GET':
        return render_template('sql_1.html')
    else:
        value = request.form.get('value', None)
        if value is not None:
            sql = provider.get('sql1.sql', gener1=value)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                message = {'message': 'Not found!'}
                return render_template('notification.html', message=message)
            return render_template('result_1.html', res=result, name=name)
        else:
            message = {'message': 'Not found value!'}
            return render_template('notification.html', message=message)



@user_app.route('/sql2', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql2():
    name = ['Имя поставщика', 'Цена товара']
    if request.method == 'GET':
        return render_template('sql_2.html')
    else:
        value = request.form.get('value', None)
        if value is not None:
            sql = provider.get('sql2.sql', gener1=value)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                message = {'message': 'Not found!'}
                return render_template('notification.html', message=message)
            return render_template('result_2.html', res=result, name=name)
        else:
            message = {'message': 'Not found value!'}
            return render_template('notification.html', message=message)


@user_app.route('/sql3', methods=['GET', 'POST'])
@group_permission_decorator
def user_sql3():
    name = ['Название товара', 'Материал', 'Ед. измерения']
    if request.method == 'GET':
        return render_template('sql_3.html')
    else:
        value1 = request.form.get('value1', None)
        if value1 is not None:
            sql = provider.get('sql3.sql', gener1=value1)
            result = work_with_db(current_app.config['DB_CONFIG'], sql)
            if not result:
                message = {'message': 'Not found!'}
                return render_template('notification.html', message=message)
            return render_template('result_3.html', res=result, name=name)
        else:
            message = {'message': 'Not found value!'}
            return render_template('notification.html', message=message)
