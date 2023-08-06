from copy import deepcopy

from apronpy.coeff import PyMPQScalarCoeff

from apronpy.linexpr1 import PyLinexpr1

from apronpy.scalar import PyDoubleScalar, PyMPQScalar

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

        o1 = PyVar('o1')
        o2 = PyVar('o2')
        h1 = PyVar('h1')
        h2 = PyVar('h2')
        h3 = PyVar('h3')
        h4 = PyVar('h4')
        h5 = PyVar('h5')
        h6 = PyVar('h6')
        h7 = PyVar('h7')
        h8 = PyVar('h8')
        h9 = PyVar('h9')
        # print(o1, o2, h1, h2, h3, h4, h5, h6, h7, h8, h9)
        e = PyEnvironment([], [o1, o2, h1, h2, h3, h4, h5, h6, h7, h8, h9])
        p0 = PyPolkaMPQstrict(e)
        # print(p0)

        o01 = PyTexpr1.var(e, PyVar('o1'))
        o02 = PyTexpr1.var(e, PyVar('o2'))
        x0 = PyTexpr1.binop(TexprOp.AP_TEXPR_SUB, o02, o01, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        c0 = PyTcons1.make(x0, ConsTyp.AP_CONS_SUP)     # o2 - o1 > 0
        a0 = PyTcons1Array([c0])
        p1 = deepcopy(p0).meet(a0)
        print(p1)

        # o11 = PyTexpr1.var(e, PyVar('o1'))
        # o12 = PyTexpr1.var(e, PyVar('o2'))
        # c11 = PyTcons1.make(o11, ConsTyp.AP_CONS_SUPEQ)   # o1 >= 0
        # c12 = PyTcons1.make(o12, ConsTyp.AP_CONS_SUPEQ)   # o2 >= 0
        # a1 = PyTcons1Array([c11, c12])
        # p2 = deepcopy(p1).meet(a1)
        # # print(p2)
        #
        # h21 = PyTexpr1.var(e, PyVar('h1'))
        # h22 = PyTexpr1.var(e, PyVar('h2'))
        # h23 = PyTexpr1.var(e, PyVar('h3'))
        # h24 = PyTexpr1.var(e, PyVar('h4'))
        # h25 = PyTexpr1.var(e, PyVar('h5'))
        # h26 = PyTexpr1.var(e, PyVar('h6'))
        # h27 = PyTexpr1.var(e, PyVar('h7'))
        # h28 = PyTexpr1.var(e, PyVar('h8'))
        # h29 = PyTexpr1.var(e, PyVar('h9'))
        # k20 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.2))
        # t20 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k20, h21, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k21 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.3))
        # t21 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k21, h22, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k22 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.1))
        # t22 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k22, h23, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k23 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.2))
        # t23 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k23, h24, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k24 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.1))
        # t24 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k24, h25, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k25 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.3))
        # t25 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k25, h26, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k26 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
        # t26 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k26, h27, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k27 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.2))
        # t27 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k27, h28, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k28 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.1))
        # t28 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k28, h29, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k29 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
        # x20 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, t20, t21, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x21 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x20, t22, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x22 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x21, t23, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x23 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x22, t24, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x24 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x23, t25, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x25 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x24, t26, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x26 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x25, t27, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x27 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x26, t28, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x28 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x27, k29, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # p3 = deepcopy(p2).substitute(PyVar('o2'), x28)
        # # print(p3)
        #
        # h31 = PyTexpr1.var(e, PyVar('h1'))
        # h32 = PyTexpr1.var(e, PyVar('h3'))
        # h33 = PyTexpr1.var(e, PyVar('h3'))
        # h34 = PyTexpr1.var(e, PyVar('h4'))
        # h35 = PyTexpr1.var(e, PyVar('h5'))
        # h36 = PyTexpr1.var(e, PyVar('h6'))
        # h37 = PyTexpr1.var(e, PyVar('h7'))
        # h38 = PyTexpr1.var(e, PyVar('h8'))
        # h39 = PyTexpr1.var(e, PyVar('h9'))
        # k30 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
        # t30 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k30, h31, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k31 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.1))
        # t31 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k31, h32, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k32 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.2))
        # t32 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k32, h33, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k33 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.3))
        # t33 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k33, h34, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k34 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.1))
        # t34 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k34, h35, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k35 = PyTexpr1.cst(e, PyMPQScalarCoeff(-0.2))
        # t35 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k35, h36, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k36 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
        # t36 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k36, h37, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k37 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.3))
        # t37 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k37, h38, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k38 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.1))
        # t38 = PyTexpr1.binop(TexprOp.AP_TEXPR_MUL, k38, h39, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # k39 = PyTexpr1.cst(e, PyMPQScalarCoeff(0.4))
        # x30 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, t30, t31, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x31 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x30, t32, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x32 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x31, t33, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x33 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x32, t34, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x34 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x33, t35, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x35 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x34, t36, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x36 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x35, t37, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x37 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x36, t38, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # x38 = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x37, k39, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        # p4 = deepcopy(p3).substitute(PyVar('o1'), x38)
        # print(p4)


main()
