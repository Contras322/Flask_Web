select p_name, p_material, p_measure from storage.product p
left join (select * from (select * from storage.supply join storage.basket using(basket_id)) k where year(sy_date) = '$gener1') s
on p.p_id = s.p_id where sy_id is NULL
