val1=10
global val2
val2=11
def test1():
    # global val1
    val2=9
    print('test1 val2:',val2)

print(val2)
test1()
print(val2)