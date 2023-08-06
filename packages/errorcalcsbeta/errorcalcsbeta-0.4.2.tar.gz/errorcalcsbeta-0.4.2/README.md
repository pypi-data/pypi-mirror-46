![Python 3.7](https://img.shields.io/badge/python-3.7-green.svg)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/leonfrcom/ErroRCalcS/blob/master/LICENSE)


![icon](./pictures/icon/logo_text.png)

"ErroRCalcS" is a GUI-tool to calculate uncertainties by using the uncertainties and the PyQt5 packages.

## ErroRCalcS-BETA
This is the beta version of ErroRCalcS. Please check out ![this](https://github.com/leonfrcom/errorcalcs) for the stable version.

## Input and Result Examples

### General Inpus
| variable | value | error | formula | result |
| ------ | ------ | ------ | ------ | ------ |
| V, T, n | 2, 283.5, 4.3 | 0, 0.5, 0.03 | (n\*8.314\*T)/V | 5067.591+/-36.467 |
| x | 4.3 | 1.1 | sin(x)*3.5 | -3.2066+/-1.5431 |
| y | 3.254 | 0.032 | log10(y) | 0.5124175+/-0,0042709 |
| x, y | 4.3, 3.254 | 1.1, 0.032 | log(x)\*\*y | 3.4156+/-1.9497 |

### Arithmetic Characters
| characters and operators | meaning |  example |
| ----- | ----- | ----- |
| + | plus | 4+2=6 |
| - | minus | 4-2=2 |
| \* | multiplication | 4\*2=8 |
| / | division | 4/2=2 |
| \*\* | exponent | 4\*\*2=16 |
| sqrt(x) | square root | sqrt(4)=2 |
| log(x) | natural logarithm | log(2.71828)=1 |
| logY(x) | logarithm with base Y | log10(2.71828)=0.4343 |
| sin(x) | sinus in radian | sin(1)=0.8415 |
| cos(x) | cosinus in radian | cos(1)=0.5403 |
| tan(x) | tangens in radian | tan(1)=1.5574 |
| asin(x) | arcsinus in radian | asin(1)=1.5707 |
| acos(x) | arccosinus in radian | acos(1)=0 |
| atan(x) | arctangens in radian | atan(1)=0.7854 |
| exp(x) | exponentialfunktion of e^(x) | exp(2)=7.3891 |



## Requirements
- Python >= 3.4
- uncertainties
- PyQt5

## Installation
errorcalcs-beta can be installed by `pip3 install errorcalcs-beta` or `python3 -m pip install errorcalcs-beta` (Linux) or simply `pip install errorcalcs-beta` (Windows). You can run the GUI with following code:

	from errorcalcs-beta.errorcalcs import run\_e\_c
	run\_e\_c()
# errorcalcs-beta
