from math import sqrt as math_sqrt, log, floor, log10
from numpy import array, float128
from typing import Literal, Any

realy_small_number = 10**-30

class Me:
    def __init__(self, m:float|int, u:float|int = 0, s:float|int = 1) -> None:
        """
        Constructor for the Me class.

        Parameters:
        m (float | int): The measure value.
        u (float | int, optional): The uncertainty value. Defaults to 0.
        s (float | int, optional): The scale factor. Defaults to 1.

        The constructor initializes the measure and uncertainty, applying the scale factor to both.
        """
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
            factor = 10**(decimal-1)
            return f"({(self.m*factor):.1f} ± {(self.u*factor):.1f})e{-decimal+1}"

        factor = 10**decimal
        decimal = -decimal
        return f"({(self.m*factor):.{decimal}f} ± {(self.u*factor):.0f})e{decimal}"

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

def sqrt(me):
    if isinstance(me, Me):
        m = sqrt(me.m)
        return Me(m, abs(m*me.u/(2*me.m)))
    return math_sqrt(me)

def list2numpy(list:list[Me], mode:Literal["twoArrays","listTwoArrays", "list[[u,m]]"] = "twoArrays", dtype:Any = float128):
    """
    Transforms a Me() list into a numpy array in three different forms.

    Parameters:
    list (List[Me]): A list of Me instances to be transformed.

    mode (Literal["twoArrays", "listTwoArrays", "list[[u,m]]"]): 
        - "twoArrays": Returns two separate arrays, one for measures (m) and one for uncertainties (u).
        - "listTwoArrays": Returns a single array with two rows, the first for measures (m) and the second for uncertainties (u).
        - "list[[u,m]]": Returns a single array where each element is a [m, u] pair.

    dtype: The desired data type for the numpy arrays. Default is np.float128.

    Returns:
    Depending on the mode, returns one of the following:
        - Two separate numpy arrays if mode is "twoArrays".
        - A single numpy array with two rows if mode is "listTwoArrays".
        - A single numpy array with pairs of [m, u] if mode is "list[[u,m]]".
    """
    if mode == "twoArrays":
        return array([i.m for i in list], dtype=dtype), array([i.u for i in list], dtype=dtype)
    elif mode == "listTwoArrays":
        return array([
            [i.m for i in list],
            [i.u for i in list]
            ],
            dtype=dtype
        )
    else:
        return array([[i.m, i.u] for i in list], dtype=dtype)