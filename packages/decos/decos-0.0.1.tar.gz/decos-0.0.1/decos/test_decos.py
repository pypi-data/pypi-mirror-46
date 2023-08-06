from decos import safe_run,debug,timer

@timer
@debug
@safe_run(dcs={'dv':2})
def mag(a,b):
    return a+b

assert (2+3) == mag(2,3)

# assert 2 == mag('2'+3)

class TestDecos:
    
    def mag(self):
        assert 4 == mag(2,2)
