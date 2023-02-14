

insert into test_t12 (c121, c122, c123, c124)
select c11, c12, c22, c32 
from test_t1 t1 
join (select c22, c23, c32  
       from test_t2
       join (select c32, c33
             from test_t3
             union
             select c41, c42
             from test_t4  t4
	         join test_t6  t6
	         on   t4.c43 = t6.c63
 	         union
	         select c71, c72
	         from test_t7 t7
	         join test_t8 t8
	         on   t7.c72 = t8.c82
	         join test_t9 t9
	         on   t8.c81 = t9.c91
	         join (select c101, c102
		            from test_t10  t10
		            join test_t11  t11
		            on   t10.c101 = t11.c111   ) t1011
	         on t9.c92 = t1011.c102    ) t3
       on c21 = c33
       union
       select c51, c52, c53
       from test_t5   ) t2
on t1.c11 = t2.c23;

