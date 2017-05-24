# (C) 2017 - Daniele Zanotelli
#            dazano [at] gmail [dot] com
#

class simple:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        func_args = list()
        if args:
            func_args.extend([str(arg) for arg in args])
        if kwargs:
            func_args.extend(["{k}={v}".format(k=k, v=v)
                              for k, v in kwargs.items()])

        msg = "[DRY-RUN] call to '{func}({args})'"
        msg = msg.format(func=self.function.__name__,
                         args=", ".join(func_args))

        print(msg) # FIXME replace with logger



def test():
    def func(a, b):
        print(a + b)

    print('normal run:')
    func(1, 2)

    @simple
    def func2(a, b):
        print(a + b)

    print ('dry run')
    func2(1, 2)

if __name__ == "__main__":
    test()
