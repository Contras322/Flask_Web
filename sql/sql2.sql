select distinct s_name, p_price from storage.supplier s join (select p_price, s_id, p_name from
(select * from storage.supply as sup join storage.basket as bas using(basket_id)) as n join storage.product using(p_id)) p
on s.s_id = p.s_id where p_price = (select min(p_price) from (select p_price, s_id, p_name from
(select * from storage.supply as sup join storage.basket as bas using(basket_id)) as n join storage.product using(p_id)) k
where p_name = '$gener1');
