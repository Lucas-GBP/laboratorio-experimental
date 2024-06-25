from medicoes import Me
from typing import Mapping

## Caracteristicas do multimetro
multimeterData = {
    "MINIPA ET-2082E": {
        "tensao DC": {
            "faixa": [200*(10**-3), 2, 20, 200, 1000],
            "resolucao": [0.1*3*(10**(-3)), 0.001*3, 0.01*3, 0.1*3, 1*10],
            "precisao": [0.005, 0.005, 0.005, 0.005, 0.008]
        },
        "tensao AC": {
            "faixa": [200*(10**-3), 2, 20, 200, 750],
            "resolucao": [0.1*5*(10**(-3)), 0.001*5, 0.01*5, 0.1*5, 1*10],
            "precisao": [0.008, 0.008, 0.008, 0.008, 0.012]
        },
        "corrente DC": {
            "faixa": [0.0002, 0.002, 0.020, 0.2, 20],
            "resolucao": [0.0000001*10, 0.000001*10, 0.00001*10, 0.0001*10, 0.01*5],
            "precisao": [0.008, 0.008, 0.008, 0.008, 0.02]
        },
        "corrente AC": {
            "faixa": [200*(10**(-6)), 2000*(10**(-6)), 20*(10**(-3)), 200*(10**(-3)), 20],
            "resolucao": [0.1*10*(10**(-6)), 1*10*(10**(-6)), 0.01*10*(10**(-3)), 0.1*10*(10**(-3)), 0.01*5],
            "precisao": [0.008, 0.008, 0.008, 0.008, 0.02]
        }
    }
}

## Funsão para calcular a incerteza de uma medida
def calculateUncertainty(amostra:float|int, data:Mapping[str, list[int|float]]):
    absAmostra = abs(amostra)
    i = 0
    while i < (len(data["faixa"])-1):
        if data["faixa"][i] >= absAmostra:
            break
        i = i+1

    return Me(amostra, absAmostra*data["precisao"][i] + data["resolucao"][i])