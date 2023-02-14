
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


insert into test_t8
select c11, c12, c73
from test_t1 t1 
join (select c22, c73  
      from test_t2  
      join (select c72, c73   
            from test_t7
            union
            select c32, c33
            from test_t3) t7  
      on c21 = c73) t2 
on t1.c11 = t2.c22;


insert into test_t12
select c11, c12, c22, c82 
from test_t1 t1 
join (select c22, c23, c82
      from test_t2
      join (select c82, c83
            from test_t8
            union
            select c72, c73
            from test_t7) t8  
      on c21 = c83) t7 
on t1.c11 = t7.c82
;
