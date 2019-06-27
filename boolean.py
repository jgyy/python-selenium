"""
== --> Value Equality
!= --> Not equal to
< --> Less than
> --> Greater than
<= --> Less than or equal to
>= --> Greater than or equal to
"""

BOOL_ONE = 10 == 11
NOT_EQUAL = 10 != 11
LESS_THAN = 10 < 11
GREATER_THAN = 10 > 9
LT_EQ = 10 <= 9
print(BOOL_ONE, NOT_EQUAL, LESS_THAN, GREATER_THAN, LT_EQ)

BOOL_OUTPUT = True or not False and False
# noinspection Pylint
# BOOL_OUTPUT_1 = (10 == 10 or not 10 > 10) and 10 > 10
print(BOOL_OUTPUT)
