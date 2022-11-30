import mathlib.matrix as matrix
import mathlib.vector as vec

from mathlib.quaternion import Quaternion as Q
from mathlib.dual_number import DualNumber as DN

class DualQuaternion:
    def __init__(self, D0: Q=None, 
                       D1: Q=None):
        if not D0:
            self.__D0 = Q()
        else:
            self.__D0 = D0
        if not D1:
            self.__D1 = Q()
        else:
            self.__D1 = D1

    @property
    def D0(self):
        return self.__D0

    @property
    def D1(self):
        return self.__D1

    @property
    def Dual(self):
        return self.__D1

    @property
    def Real(self):
        return self.__D0

    @property
    def scalar(self):
        return DN(real=self.__D0.Re, imagine=self.__D1.Re)

    @property
    def vector(self):
        return vec.wedge(v1=self.__D0.Im, v2=self.__D1.Im)

    @Dual.setter
    def Dual(self, dual: Q):
        if isinstance(dual, Q):
            self.__D1 = dual
        
    @Real.setter
    def Real(self, real: Q):
        if isinstance(real, Q):
            self.__D0 = real

    @D0.setter
    def D0(self, D0: Q):
        if isinstance(D0, Q):
            self.__D0 = D0

    @D1.setter
    def D1(self, D1: Q):
        if isinstance(D1, Q):
            self.__D1 = D1

    @property
    def parameter(self):
        return sum([q*q1 for q, q1 in zip(self.__D0.quaternion, self.__D1.quaternion)]) / self.__D0.norm

    @property
    def norm(self):
        return DN(real=self.__D0.norm, imagine=2*self.parameter*self.__D0.norm)
    
    @property
    def module(self):
        return DN(real=self.__D0.module, imagine=self.__D0.module*self.parameter)

    @property
    def dual_quaternion(self):
        return [[q for q in self.__D0.quaternion], [q for q in self.__D1.quaternion]]

    def __repr__(self):
        return f'{self.__class__.__name__}\n{self.scalar}' \
               f'Vector:\n{matrix.fprt_mat(m=self.vector, rnd=True, dec=5)}' \
               f'Norm={self.norm}' \
               f'Module={self.module}' \
               f'Parameter={self.parameter}\n\n' \
               f'D0: {self.__D0}\nD1: {self.__D1}\n' \
               f'DQ: [({self.__D0.q0}) + ({self.__D0.q1})i + ({self.__D0.q2})j + ({self.__D0.q3})k] + ' \
               f'[({self.__D1.q0}) + ({self.__D1.q1})i + ({self.__D1.q2})j + ({self.__D1.q3})k]e'

    def addition(self, DQ: object) -> object:
        return DualQuaternion(
            D0=self.Real.addition(DQ.Real), D1=self.Dual.addition(DQ.Dual)
        )
    
    def substraction(self, DQ: object) -> object:
        return DualQuaternion(
            D0=self.Real.substraction(DQ.Real), D1=self.Dual.substraction(DQ.Dual)
        )

    def scalar_product(self, scalar: float) -> object:
        return DualQuaternion(D0=self.__D0.scalar_product(scalar=scalar),
                              D1=self.__D1.scalar_product(scalar=scalar))

    def dot(self, DQ: object) -> object:
        return DualQuaternion(D0=self.__D0.dot(DQ.Real),
                              D1=self.__D1.dot(DQ.Real).addition(self.__D0.dot(DQ.Dual)))

    def cross(self, DQ: object) -> object:
        return DualQuaternion(D0=self.Real.cross(DQ.Real),
                              D1=self.Dual.cross(DQ.Real).addition(self.Real.mult(DQ.Dual)))

    def circle(self, DQ: object) -> object:
        return DualQuaternion(D0=self.Real.mult(DQ.Real).addition(self.Dual.mult(DQ.Dual)),
                              D1=Q(scalar=0.0, vector=[0.0, 0.0, 0.0]))

    def mult(self, DQ: object) -> object:
        Real = self.Real.mult(DQ.Real)
        Dual1 = self.Real.mult(DQ.Dual)
        Dual2 = self.Dual.mult(DQ.Real)
        Dual = Dual1.addition(Dual2)
        return DualQuaternion(D0=Real, D1=Dual)

    def swap(self):
        self.__D0, self.__D1 = self.__D1, self.__D0

    def quaternion_conjugate(self):
        return DualQuaternion(D0=self.__D0.conjugate(), D1=self.__D1.conjugate())

    def dual_number_conjugate(self):
        return DualQuaternion(D0=self.__D0, D1=self.__D1.scalar_product(scalar=-1.0))

    def conjugate(self):
        return DualQuaternion(D0=self.__D0.conjugate(),
                              D1=self.__D1.conjugate().scalar_product(scalar=-1.0))

    def normed(self):
        module = self.module
        D11 = self.__D1.scalar_product(scalar=module.Re)
        D12 = self.__D0.scalar_product(scalar=module.Im)
        self.__D1 = (D11.substraction(D12)).scalar_product(scalar=(1/(module.Re**2)))
        self.__D0 = self.__D0.scalar_product(scalar=(1/module.Re))

    def inverse(self):
        norm = self.norm
        conjugate = self.quaternion_conjugate()
        D11 = conjugate.D1.scalar_product(scalar=norm.Re)
        D12 = conjugate.D0.scalar_product(scalar=norm.Im)
        D1112 = D11.substraction(D12)
        self.__D1 = D1112.scalar_product(scalar=(1/(norm.Re**2)))
        self.__D0 = conjugate.D0.scalar_product(scalar=(1/norm.Re))

    @staticmethod
    def derivate(dq: object, deldq: object, del_arg):
        D0_derivate = Q.derivate(q=dq.D0, delq=deldq.D0, del_arg=del_arg)
        D1_derivate = Q.derivate(q=dq.D1, delq=deldq.D1, del_arg=del_arg)

        return DualQuaternion(D0=D0_derivate, D1=D1_derivate)
