from datetime import date
from flask import Blueprint, render_template, session, request, redirect, current_app
from DB.database import work_with_db, change_db
from DB.sql_provider import SQL_Provider
from access import group_permission_decorator
from .utils import add_to_basket, clear_basket, add_supplier, clear_suppliers

basket_app = Blueprint('basket', __name__, template_folder='templates')
provider = SQL_Provider('sql/')


@basket_app.route('/', methods=['GET', 'POST'])
@group_permission_decorator
def suppliers_list():
    if request.method == 'GET':
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_all_suppliers.sql'))
        return render_template('suppliers_list.html', items=items)
    else:
        s_id = request.form['s_id']
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_current_supplier.sql', s_id=s_id))
        if not items:
            return 'Item not found'
        add_supplier(items)

        return redirect('/basket/get_list')


@basket_app.route('/get_list', methods=['GET', 'POST'])
def list_orders_handler():
    if request.method == 'GET':
        current_basket = session.get('basket', [])
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_all_basket.sql'))
        return render_template('basket_order_list.html', items=items, basket=current_basket)
    else:
        product_id = request.form['p_id']
        items = work_with_db(current_app.config['DB_CONFIG'], provider.get('sql_current_product.sql', s_id=product_id))
        if not items:
            return 'Item not found'
        add_to_basket(items)

        return redirect('/basket/get_list')


@basket_app.route('/clear')
def clear_basket_handler():
    clear_basket()
    return redirect('/basket/get_list')


@basket_app.route('/buy')
def buy_basket_handler():
    current_basket = session.get('basket', [])
    suppliers = session.get('suppliers', [])
    print(suppliers)
    sup_id = suppliers[0]['s_id']
    sql_ido = provider.get('select_basket_id.sql')
    val_id = work_with_db(current_app.config['DB_CONFIG'], sql_ido)
    id = val_id[0]['basket_id'] + 1 if val_id else 1

    for item in current_basket:
        sql_add = provider.get('sql_insert_basket.sql', b_id=id, p_id=item['p_id'], count=item['count'])
        change_db(current_app.config['DB_CONFIG'], sql_add)

    sql_add = provider.get('sql_insert_supply.sql', date=date.today(), s_id=sup_id, basket_id=id)
    change_db(current_app.config['DB_CONFIG'], sql_add)

    clear_basket()

    sql_sel = provider.get('sql_current_basket.sql', b_id=id)
    items_sel = work_with_db(current_app.config['DB_CONFIG'], sql_sel)

    name = ['Название товара', 'Количество товара', 'Цена за единицу товара']

    clear_basket()
    clear_suppliers()
    return render_template('order_done.html', items=items_sel, number=id, name=name)
