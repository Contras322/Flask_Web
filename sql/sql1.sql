select distinct p.p_id, p.p_name from storage.product p
join (select s_name, p_id, sy_date from storage.supplier join
(select * from storage.supply as sup join storage.basket as bas using(basket_id)) as al
using(s_id) where year(sy_date) = 2021) s
on s.p_id = p.p_id
where s_name = '$gener1';