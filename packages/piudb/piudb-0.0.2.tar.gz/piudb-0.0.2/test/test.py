from xiudb.piudb.classes import *
class TestClass(Model):
    __table__='test_table'
    tid=StringField(primary_key=True)
    content=StringField(default='this is content')
opener=TableOpener()
tb=opener.open('../db/test_table','a',TestClass)
def test1():
    a=TestClass(
        tid='ppppp'
    )
    tb._insert_(a)
    [a]=tb._findAll_()
    print(a)

if __name__=="__main__":
    test1()