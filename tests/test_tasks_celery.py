import pytest
from tasks import somar, fatorial

def test_somar():
    resultado = somar.apply(args=[5,3]).get()
    assert resultado == 8

def test_fatorial():
    resultado = fatorial.apply(args=[5]).get()
    assert resultado == 120

def test_fatorial_zero():
    resultado = fatorial.apply(args=[0]).get()
    assert resultado == 1

def test_fatorial_um():
    resultado = fatorial.apply(args=[1]).get()
    assert resultado == 1

def test_fatorial_dois():
    resultado = fatorial.apply(args=[2]).get()
    assert resultado == 2

def test_fatorial_grande():
    resultado = fatorial.apply(args=[10]).get()
    assert resultado == 3628800

def test_fatorial_negativo():
    with pytest.raises(ValueError, match="não-negativo"):
        fatorial.apply(args=[-1]).get()
