
insert into test_t5 (c51, c52)
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
) t4;


insert into test_t7 (c71, c72, c73)
select c11, c12, c32
from test_t1 t1 
join (select c22, c23, c32  
      from test_t2  
      join (select c32, c33   
            from test_t3
            union
            select c51, c52
            from test_t5) t3
      on c21 = c33
      union
      select c51, c52, c53
      from test_t5) t2 
on t1.c11 = t2.c23;

