def greet(name):
    return "Hello, " + name

def double(n):
    return n+n

def calc_bond_price1(face_value, coupon_rate, market_interest, years_to_maturity, payments_per_year):
    annual_coupon_payment = face_value * coupon_rate
    n = years_to_maturity * payments_per_year
    coupon_rate_per_payment = 1.0 + market_interest / payments_per_year
    coupon_pv = annual_coupon_payment / market_interest * (1.0 - coupon_rate_per_payment ** (-n))
    bond_pv = face_value * coupon_rate_per_payment ** (-n)
    return coupon_pv + bond_pv

def calc_bond_price2(face_value: float, coupon_rate: float, market_interest:float, years_to_maturity:int, payments_per_year:int=2) -> float:
    """
    Calculate the bond price.
    :param face_value: Bond face value, for example, 1000.00
    :param coupon_rate: Bond's declared coupon rate, e.g., .06 (which would be 6%)
    :param market_interest: Current market interest rate, e.g., 0.04 (for 4%)
    :param years_to_maturity: years to maturity, e.g., 10 (for 10 years)
    :param payments_per_year: payments per year, e.g., 2 (for semiannual)
    :return: a float of the bond price.
    """
    annual_coupon_payment = face_value * coupon_rate
    n = years_to_maturity * payments_per_year
    coupon_rate_per_payment = 1.0 + market_interest / payments_per_year
    coupon_pv = annual_coupon_payment / market_interest * (1.0 - coupon_rate_per_payment ** (-n))
    bond_pv = face_value * coupon_rate_per_payment ** (-n)
    return coupon_pv + bond_pv

print(f'Hello, World')
greeting = greet('Rajah')
print(greeting)

double_me = 5
print(f'Twice {double_me} is {double(double_me)}')

bond_price = calc_bond_price1(1000.0, 0.06, 0.04, 10, 2)
print(f'Bond price is ${bond_price:.2f}')

bond1 = (1000.0, 0.06, 0.04, 10, 2) # see last week's homework
bond2 = (1000.0, 0.10, 0.11359, 10, 2) # see https://dqydj.com/bond-pricing-calculator/
bond3 = (970.0, 40.0/970.0, 0.0375, 10, 2) # see https://www.brandonrenfro.com/bond-price-calculator/

bond_list = (bond1, bond2, bond3)
for fv, coup, mkt, years, compound_freq, in bond_list:
    price = calc_bond_price2(face_value=fv, coupon_rate=coup, market_interest=mkt, years_to_maturity=years, payments_per_year=compound_freq)
    print(f'Calculated price: {price:.2f}')
