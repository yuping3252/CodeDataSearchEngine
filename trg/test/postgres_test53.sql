
insert into test_t12
select c11
from test_t1 t1;


insert into test_t12
select c11
from test_t1 t1
union
select c21
from test_t2 t2;


insert into test_t12
select c11, c12, c22, c32 
from test_t1 t1 
join (select c22, c23, c32
      from test_t2
      join (select c32, c33
            from test_t3
            union
            select c42, c43
            from test_t4) t3  
      on c21 = c33) t2 
on t1.c11 = t2.c23;


insert into test_t12
select c11, c12, c22
from test_t1 t1 
join (select c22, c23  
      from test_t2  
      join (select c32, c33   
            from test_t3
            union
            select c42, c43
            from test_t4) t3  
      on c21 = c33) t2 
on t1.c11 = t2.c23;


insert into test_t12 (c121, c122, c123, c124)
select c11, c12, c22, c32 
from test_t1 t1 
join (select c22, c23, c32  
      from test_t2  
      join (select c32, c33   
            from test_t3
            union
            select c41, c42
            from test_t4) t3
      on c21 = c33
      union
      select c51, c52, c53
      from test_t5) t2 
on t1.c11 = t2.c23;


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
) t46
;
