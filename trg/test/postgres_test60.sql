

select c21, c22 from test_t2 t2
union
select c31, c32 from test_t3 t3
union
select c41, c42 from 
(select c41, c42
 from test_t4 t41
 union
 select c61, c62
 from test_t6 t6
) t46
;
