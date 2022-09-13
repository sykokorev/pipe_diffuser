import mathlib.matrix as mat
import mathlib.vector as vec


class Quaternion:
    def __init__(self, scalar: float=0.0, vector: list=[0.0, 0.0, 0.0]):
        self.__v = [round(vi, 4) for vi in vector]
        self.__s = round(scalar, 4)


    @property
    def Im(self):
        return self.__v

    @property
    def Re(self):
        return self.__s

    @property
    def scalar(self):
        return self.__s

    @property
    def vector(self):
        return self.__v

    @property
    def q0(self):
        return self.__s

    @property
    def q1(self):
        return self.__v[0]
    
    @property
    def q2(self):
        return self.__v[1]

    @property
    def q3(self):
        return self.__v[2]

    @property
    def quaternion(self):
        return [self.__s, *self.__v]

    @scalar.setter 
    def scalar(self, scalar: float):
        if isinstance(scalar, (float, int)):
            self.__s = scalar

    @vector.setter
    def vector(self, vector: list):
        if hasattr(vector, '__iter__') and all([isinstance(item, (float, int)) for item in vector]):
            self.__v = vector

    @property
    def norm(self):
        return round((self.q0 ** 2 + sum(q ** 2 for q in self.vector)) ** 0.5, 4)

    def __repr__(self):
        return f'{self.__class__.__name__}\tRe: {round(self.Re, 5)}\t' \
               f'Im: [{mat.fprt_mat(m=self.Im, rnd=True, dec=5)}]\n' \
               f'{self.__class__.__name__}:\t{round(self.Re, 5)} + ({round(self.q1, 5)})i ' \
               f'+ ({round(self.q2, 5)})j + ({round(self.q3, 5)})k\n' \
               f'Norm:\t{round(self.norm, 5)}\n'

    def conjugate(self):
        return Quaternion(scalar=self.__s, vector=vec.scalar_vector(scalar=-1, vector=self.__v))

    def inverse(self):
        d = self.norm ** 2
        return Quaternion(scalar=self.scalar / d, vector=vec.scalar_vector(scalar=-1/d, vector=self.vector))

    def addition(self, q: object) -> object:
        sc = self.__s + q.q0
        vc = vec.addition(v1=self.__v, v2=q.Im)
        return Quaternion(scalar=sc, vector=vc)

    def substraction(self, q: object) -> object:
        sc = self.__s - q.q0
        vc = vec.substraction(v1=self.__v, v2=q.Im)
        return Quaternion(scalar=sc, vector=vc)

    def mult(self, q: object) -> object:
        sc = self.q0 * q.q0 - vec.dot(v1=self.Im, v2=q.vector)
        v1 = vec.scalar_vector(scalar=self.scalar, vector=q.vector)
        v2 = vec.scalar_vector(scalar=q.scalar, vector=self.vector)
        v3 = vec.cross(v1=self.vector, v2=q.vector)
        vc = vec.addition(v1=vec.addition(v1=v1, v2=v2), v2=v3)

        return Quaternion(scalar=sc, vector=vc)

    def dot(self, q: object) -> object:
        return Quaternion(scalar=vec.dot(v1=self.vector, v2=q.vector), vector=[0]*3)

    def cross(self, q: object) -> object:
        v1 = vec.scalar_vector(scalar=self.scalar, vector=q.vector)
        v2 = vec.scalar_vector(scalar=q.scalar, vector=self.vector)
        v3 = vec.cross(v1=self.vector, v2=q.vector)
        vc = vec.addition(v1=vec.addition(v1=v1, v2=v2), v2=v3)
        return Quaternion(scalar=0.0, vector=vc)

    def normed(self):
        d = self.norm
        self.__v = vec.scalar_vector(scalar=1/d, vector=self.vector)
        self.__s = self.__s / d 

    def scalar_product(self, scalar: float) -> object:
        return Quaternion(scalar=self.scalar*scalar, vector=vec.scalar_vector(scalar=scalar, vector=self.vector))

    def derivate(self, delq: object, delt: float) -> object:
        derivative = self.substraction(delq)
        derivative = self.scalar_product(scalar=1/delt)
        return derivative
