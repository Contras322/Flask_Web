from flask import session


def add_supplier(items):
    suppliers = session.get('suppliers', [])
    print(session)
    for item in items:
        suppliers.append(item)

    session['suppliers'] = suppliers


def add_to_basket(items):
    basket = session.get('basket', [])
    count = 1
    for item in items:
        item.update(dict(count=count))

    for item in items:
        key = True
        for i in basket:
            if item['p_id'] == i['p_id']:
                i['count'] += 1
                key = False
        if key:
            basket.append(item)
    session['basket'] = basket


def clear_basket():
    if 'basket' in session:
        session.pop('basket')


def clear_suppliers():
    if 'suppliers' in session:
        session.pop('suppliers')