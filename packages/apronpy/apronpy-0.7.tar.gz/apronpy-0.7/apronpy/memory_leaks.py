from apronpy.lincons0 import ConsTyp

from apronpy.environment import PyEnvironment
from apronpy.mpq import PyMPQ
from apronpy.mpz import PyMPZ
from memory_profiler import profile, memory_usage

from apronpy.polka import PyPolkaMPQstrict
from apronpy.tcons1 import PyTcons1, PyTcons1Array
from apronpy.texpr0 import TexprOp, TexprRtype, TexprRdir
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar


@profile
def main():
    size = 100000

    for i in range(size):
        # z = PyMPZ(3)
        # del z
        # q = PyMPQ(3)
        # del q
        x = PyVar('o1')
        e = PyEnvironment([], [x, PyVar('o2')])
        o1 = PyTexpr1.var(e, PyVar('o1'))
        o2 = PyTexpr1.var(e, PyVar('o2'))
        x0 = PyTexpr1.binop(TexprOp.AP_TEXPR_SUB, o2, o1, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        c0 = PyTcons1.make(x0, ConsTyp.AP_CONS_SUP)
        a0 = PyTcons1Array([c0])
        p0 = PyPolkaMPQstrict(e)
        p1 = PyPolkaMPQstrict(e)
        p = p0.meet(a0)
        # p = p0.join(p1)


main()
