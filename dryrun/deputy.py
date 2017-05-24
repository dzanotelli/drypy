
from .simple import simple


class sheriff(simple):
    def __init__(self, func):
        self.function = func
        self.deputy_function = None

    def __call__(self, *args, **kwargs):
        if not self.deputy_function:
            return super().__call__(*args, **kwargs)
        else:
            return self.deputy_function(*args, **kwargs)

    def deputy(self, dep):
        self.deputy_function = dep
        return dep

def test():
    @sheriff
    def func(a, b):
        print(a + b)

    @sheriff
    def func2(a):
        print(a)

    @func2.deputy
    def func2dryrun(a):
        print("dryrun: got arg {}".format(a))

    func(1, 2)
    func2('antani')

if __name__ == "__main__":
    test()
