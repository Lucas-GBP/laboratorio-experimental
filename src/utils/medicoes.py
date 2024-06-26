from math import sqrt, log, floor, log10

realy_small_number = 0.000000000000000000000000000001

class Me:
    def __init__(self, m:float|int, u:float|int = 0, s:float|int = 1) -> None:
        self.m = m*s
        self.u = u*s
        pass

    def get(self):
        return [self.m, self.u]

    def get_measurement(self):
        return self.m
    
    def get_uncertainty(self):
        return self.u
    
    def __repr__(self, signf:int = 2):
        if self.u < realy_small_number:
            return f"{self.m} ± {self.u:.{signf-1}f}"
        
        decimal = signf - (floor(log10(abs(self.u)))+1)
        if decimal >= 0:
            return f"{self.m:.{decimal}f} ± {self.u:.{decimal}f}"
        
        factor = 10**decimal
        decimal = -decimal
        return f"( {(self.m*factor):.{decimal}f} ± {(self.u*factor):.0f} )x10^{decimal}"

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Me(self.m + other.m, sqrt(self.u**2 + other.u**2))
        else:
            return Me(self.m + other, self.u)
    def __radd__(self, other):
        self.__add__(other)
        
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Me(self.m - other.m, sqrt(self.u**2 + other.u**2))
        else:
            return Me(self.m - other, self.u)
    def __rsub__(self, other):
        self.__sub__(other)
        
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            m = self.m*other.m
            return Me(m, m*sqrt((self.u/self.m)**2 + (other.u/other.m)**2))
        else:
            return Me(self.m*other, self.u*other)
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            m = self.m/other.m
            return Me(m, m*sqrt((self.u/self.m)**2 + (other.u/other.m)**2))
        else:
            return Me(self.m/other, self.u/other)
    def __rtruediv__(self, other):
        self.__truediv__(other)
        
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            if abs(self.m) < realy_small_number:
                return self
    
            m = self.m**other.m
            return Me(m,
                m*sqrt((other.m*self.u/self.m)**2 + (log(self.m)*other.u)**2)
            )
        else:
            if abs(self.m) < realy_small_number:
                return self
            m = self.m**other
            return Me(m, m*(other*self.u/self.m))
        
def average(elements:list[Me]):
    soma_medidas = sum(i.m for i in elements)
    soma_incertezas = sum(i.u for i in elements)
    quant = len(elements)
    
    return Me(soma_medidas/quant, soma_incertezas/quant)

def sqrt_me(me):
    if isinstance(me, Me):
        m = sqrt(me.m)
        return Me(m, abs(m*me.u/(2*me.m)))
    return sqrt(me)