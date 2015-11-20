import operator

def make_op(op_name):
    def op(*args):
        return Qutie(op_name, *args)
    return op

class Qutie(object):
    def __init__(self, op, *args):
        self.op = op
        self.args = args

    def __repr__(self):
        return '<Q %s %s>' % (self.op, self.args)

    def qu_apply(self, sor, applied=None):
        applied = { } if applied is None else applied

        if self in applied:
            return applied[self]

        if len(self.args) == 0:
            a = next(sor)
            applied[self] = a
            return a
        else:
            s = self.args[0]._apply(sor, applied=applied)
            a = getattr(s, self.op)(*[ (a._apply(sor, applied=applied) if isinstance(a, Qutie) else a) for a in self.args[1:] ])
            applied[self] = a
            return a

    def qu_iter(self):
        yield Qutie('__iter__', self)

_du_ops = { _ for _ in dir(operator) if _.startswith('__') }
_ignore_ops = { '__doc__', '__name__', '__hash__' }
_add_ops = { '__str__', '__getattr__', '__call__', '__iter__', 'next' }
_all_ops = _du_ops - _ignore_ops | _add_ops
for _ in _all_ops:
    setattr(Qutie, _, make_op(_))
