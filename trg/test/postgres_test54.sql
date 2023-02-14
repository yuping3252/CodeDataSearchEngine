
insert into test_t12
select c11
from test_t1 t1
union
select c21
from test_t2 t2;

