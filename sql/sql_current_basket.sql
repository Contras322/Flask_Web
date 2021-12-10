select basket_id, p_name, count, p_price from storage.basket join storage.product using(p_id)
where basket_id=$b_id;