__author__ = 'Drew'

import operator
import math

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow}


class Fraction(object):
    """Fraction class. Contains numerator and denominator
        of fraction. Overrides operator methods
    """

    def __init__(self, numerator=0, denominator=1):
        """Initializer of Fraction class

        :param numerator: numerator of the number
        :param denominator: denominator of the number
        """
        self.numerator = numerator
        self.denominator = denominator

    def __str__(self):
        """ToString method of Fraction. Used when printing out fractions.

        :return: string containing the fraction in form A/B
        """
        if str(self.numerator).find('-') != -1:
            if -1 * self.numerator > self.denominator:
                w = -1 * self.numerator / self.denominator
                f = self.numerator % self.denominator
                return str(w) + ' ' + str(f) + '/' + str(self.denominator)
        elif self.numerator > self.denominator:
            w = self.numerator / self.denominator
            f = self.numerator % self.denominator
            return str(w) + ' ' + str(f) + '/' + str(self.denominator)
        else:
            return str(self.numerator) + '/' + str(self.denominator)

    def __mul__(self, other):
        """Overridden multiply function

        :param other: the number being multiplied by
        :return: the product
        """
        self.numerator = self.numerator * other.numerator
        self.denominator = self.denominator * other.denominator
        return self

    def __float__(self):
        """Overridden floating point conversion function

        :return: the floating point version of the fraction
        """
        return float(self.numerator) / self.denominator

    def reciprocal(self):
        """The reciprocal function of Fraction

        :return: the reciprocal of the fraction
        """
        inverse = Fraction(self.denominator, self.numerator)
        return inverse

    def __add__(self, other):
        """Overridden addition function

        :param other: the number being added by
        :return: the sum
        """
        commondenom = self.denominator * other.denominator
        newnumer = self.numerator * other.denominator + \
            other.numerator * self.denominator
        self.numerator = newnumer
        self.denominator = commondenom
        return self

    def __sub__(self, other):
        """Overridden subtract function

        :param other: the number being subtracted
        :return: the difference
        """
        commondenom = self.denominator * other.denominator
        newnumer = self.numerator * other.denominator - \
            other.numerator * self.denominator
        self.numerator = newnumer
        self.denominator = commondenom
        return self

    def __truediv__(self, other):
        """Overridden division function

        :param other: the divisor
        :return: the quotient
        """
        if other.numerator == 0:
            return None
        else:
            return self * other.reciprocal()

    def __pow__(self, other):
        """Overridden exponentiation function

        :param other: the exponent
        :return: the exponentiated number
        """
        exponent = other.numerator / float(other.denominator)
        self.numerator **= exponent
        self.denominator **= exponent
        return Decimal(self.numerator, self.denominator) #TODO need to fix

    def __neg__(self):
        """Overridden negative function

        :return: the negative value of the number
        """
        return self * -1

    def simplify(self):
        """Simplifies the fraction

        :return: simplified fraction
        """
        divisor = Fraction.gcd(self)
        newnumer = self.numerator / divisor
        newdenom = self.denominator / divisor
        if newdenom == 1:
            return newnumer
        else:
            return Fraction(newnumer, newdenom)

    def gcd(self):
        """Greatest common denominator of numerator
            and denominator of fraction

        :return: GCD
        """
        a = self.numerator
        b = self.denominator
        if b == 0:
            return a
        return Fraction.gcd(Fraction(b, a % b))


class Decimal(Fraction):
    """Decimal class. Subclass of Fraction. Overrides
        str method in order to print decimals in correct format.
    """

    def __init__(self, numerator=0, denominator=1):
        """Decimal initializer

        :param numerator: numerator of decimal in fraction form
        :param denominator: denominator of decimal in fraction form
        """
        super(Decimal, self).__init__(numerator, denominator)

    def __str__(self):
        """Overridden str method.

        :return: string containing decimal in A.B form
        """
        number = float(self.numerator) / float(self.denominator)
        dot = str(number).find('.')
        whole = str(number)[:dot]
        frac = str(number)[dot:]
        return whole + frac


def clean(num):
    """Cleans the number by converting it from raw input
        to appropriate type (Fraction, Decimal, etc.)

    :param num: number to be cleaned
    :return: cleaned number
    """
    slash = num.find('/')
    dot = num.find('.')
    negt = num.find('-')
    if slash != -1:
        space = num.find(' ')
        if space != -1:
            w = int(num[:space])
            n = int(num[space + 1:slash])
            d = int(num[slash + 1:])
            if d == 0:
                return None
            return Fraction(w * d + n, d)
        else:
            n = int(num[:slash])
            d = int(num[slash + 1:])
            if d == 0:
                return None
            return Fraction(n, d)
    elif dot != -1:
        num = float(num)
        num = str(num)
        if dot == 0:
            dot += 1
        w = num[:dot]
        f = num[dot:]
        tens = len(f[1:])
        realfrac = f[1:]
        d = 10 ** tens
        if negt !=-1:
            numer = -1 * int(w) * int(d) + int(realfrac)
            return Decimal((numer * -1), d)
        numer = int(w) * int(d) + int(realfrac)
        return Decimal(numer, d)
    else:
        return Fraction(int(num), 1)


def evaluate(first, op, second):
    """Evaluates the expression given two numbers
        and an operator

    :param first: the first number
    :param op: the operator
    :param second: the second number
    :return: the result
    """
    if isinstance(first, Fraction) and op != '**':
        return Fraction.simplify(ops[op](first, second))
    else:
        return (ops[op](first, second))


while True:
    try:
        firstNum = clean(raw_input("Enter first number:"))
        operator = raw_input("Enter operator:")
        secondNum = clean(raw_input("Enter second number:"))
        ans = evaluate(firstNum, operator, secondNum)
        print (str(ans))
    except (ValueError, AttributeError, TypeError, KeyError):
        print("Invalid input")
