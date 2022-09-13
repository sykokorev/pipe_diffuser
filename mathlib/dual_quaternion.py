import mathlib.matrix as matrix
import mathlib.quaternion as qtrn
import mathlib.dual_number as dn
import mathlib.vector as vec


class DualQuaternion:
    def __init__(self, D0: qtrn.Quaternion=qtrn.Quaternion(), 
                       D1: qtrn.Quaternion=qtrn.Quaternion(scalar=1.0, vector=[0.0, 0.0, 1.0]).normed()):
        self.__D0 = D0
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
        return dn.DualNumber(real=self.__D0.Re, imagine=self.__D1.Re)

    @property
    def vector(self):
        return vec.wedge(v1=self.__D0.Im, v2=self.__D1.Im)

    @Dual.setter
    def Dual(self, dual: qtrn.Quaternion):
        if isinstance(dual, qtrn.Quaternion):
            self.__D1 = dual
        
    @Real.setter
    def Real(self, real: qtrn.Quaternion):
        if isinstance(real, qtrn.Quaternion):
            self.__D0 = real

    @D0.setter
    def D0(self, D0: qtrn.Quaternion):
        if isinstance(D0, qtrn.Quaternion):
            self.__D0 = D0

    @D1.setter
    def D1(self, D1: qtrn.Quaternion):
        if isinstance(D1, qtrn.Quaternion):
            self.__D1 = D1

    @property
    def norm(self):
        d0_norm = self.__D0.norm
        q1 = self.__D0.conjugate().mult(self.__D1)
        q2 = self.__D1.conjugate().mult(self.__D0)
        return d0_norm + q1.addition(q2).scalar

    def __repr__(self):
        return f'{self.__class__.__name__}\n{self.scalar}' \
               f'Vector:\n{matrix.fprt_mat(m=self.vector, rnd=True, dec=5)}' \
               f'Norm={round(self.norm, 5)}\n\n' \
               f'D0: {self.__D0}\nD1: {self.__D1}\n'

    def addition(self, DQ: object) -> object:
        return DualQuaternion(
            D0=self.Real.addition(DQ.Real), D1=self.Dual.addition(DQ.Dual)
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
                              D1=qtrn.Quaternion())

    def mult(self, DQ: object) -> object:
        return DualQuaternion(
            D0=self.Real.mult(DQ.Real),
            D1=(self.Real.mult(DQ.Dual).addition(self.Dual.mult(DQ.Real)))
        )

    def swap(self):
        self.__D0, self.__D1 = self.__D1, self.__D0

    def quaternion_conjugate(self):
        return DualQuaternion(D0=self.__D0.conjugate(), D1=self.__D1.conjugate())

    def dual_number_conjugate(self):
        return DualQuaternion(D0=self.__D0, D1=self.__D1.scalar_product(scalar=-1.0))

    def conjugate(self):
        return DualQuaternion(D0=self.__D0.conjugate(),
                              D1=self.__D1.conjugate().scalar_product(scalar=-1.0))
