

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

