

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

