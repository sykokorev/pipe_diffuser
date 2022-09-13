class DualNumber:
    def __init__(self, real: float, imagine: float):
        self.__Re = round(real, 5)
        self.__Im = round(imagine, 5)
        self.__vector = [self.__Re, self.__Im]

    
    @property
    def Re(self):
        return self.__Re

    @property
    def Im(self):
        return self.__Im
    
    @property
    def vector_form(self):
        return self.__vector

    @Re.setter
    def Re(self, value: float):
        if isinstance(value, (float, int)):
            self.__Re = round(value, 5)

    @Im.setter
    def Im(self, value: float) -> object:
        if isinstance(value, (float, int)):
            self.__Im = round(value, 5)

    def __repr__(self):
        return f'{__class__.__name__}\t({self.__Re} + {self.__Im})\n'

    def addition(self, dual_num: object):
        return DualNumber(real=self.Re + dual_num.Re, imagine=self.Im + dual_num.Re)

    def substraction(self, dual_num: object) -> object:
        return DualNumber(real=self.Re - dual_num.Re, imagine=self.Im - dual_num.Im)

    def mult(self, dual_num: object) -> object:
        return DualNumber(real=self.Re * dual_num.Re, imagine=self.Re * dual_num.Im + self.Im * dual_num.Re)

    def division(self, dual_num: object) -> object:
        if dual_num.Re:
            return -1
        else:
            return DualNumber(real=self.Re / dual_num.Re,
                              imagine=(self.Im * dual_num.Re - self.Re - dual_num.Im) / dual_num.Re ** 2)

    def conjugate(self):
        return DualNumber(real=self.__Re, imagine=-self.__Im)
