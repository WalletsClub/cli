# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import unicode_literals

import sys
import warnings
from decimal import Decimal, ROUND_DOWN

from errors import CriticalError

# Default, non-existent, currency
DEFAULT_CURRENCY_CODE = 'XXX'

PYTHON2 = sys.version_info[0] == 2


class Currency(object):
    """
    A Currency represents a form of money issued by governments, and
    used in one or more states/countries.  A Currency instance
    encapsulates the related data of: the ISO currency/numeric code, a
    canonical name, and countries the currency is used in.
    """

    def __init__(self, code='', numeric='999', name='', countries=None):
        if countries is None:
            countries = []
        self.code = code
        self.countries = countries
        self.name = name
        self.numeric = numeric

    def __eq__(self, other):
        return type(self) is type(other) and self.code == other.code

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.code

    def __hash__(self):
        return hash(tuple(self.code))

    @staticmethod
    def from_string(code=None, iso=None):
        try:
            if iso:
                return CURRENCIES_BY_ISO[str(iso)]
            return CURRENCIES[code]
        except KeyError:
            raise CurrencyDoesNotExist(code)


class CurrencyPair(object):
    def __init__(self, base_currency, target_currency):
        self.base_currency = base_currency
        self.target_currency = target_currency

    def __str__(self):
        return '{0}-{1}'.format(self.base_currency, self.target_currency)

    def __eq__(self, other):
        if self.base_currency == other.base_currency and self.target_currency == other.target_currency:
            return True
        else:
            return False


class MoneyComparisonError(TypeError):
    # This exception was needed often enough to merit its own
    # Exception class.

    def __init__(self, other):
        assert not isinstance(other, Money)
        self.other = other

    def __str__(self):
        # Note: at least w/ Python 2.x, use __str__, not __unicode__.
        return "Cannot compare instances of Money and %s" \
               % self.other.__class__.__name__


class CurrencyDoesNotExist(Exception):
    def __init__(self, code):
        super(CurrencyDoesNotExist, self).__init__(
            "No currency with code %s is defined." % code)


class Money(object):
    """
    A Money instance is a combination of data - an amount and a
    currency - along with operators that handle the semantics of money
    operations in a better way than just dealing with raw Decimal or
    ($DEITY forbid) floats.
    """

    def __init__(self, amount=Decimal('0.0'), currency=DEFAULT_CURRENCY_CODE):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        self.amount = amount

        if not isinstance(currency, Currency):
            currency = get_currency(str(currency).upper())
        self.currency = currency

    @staticmethod
    def from_string(s):
        s = s.replace(' ', '')
        currency = s[-3:].upper()
        amount = Decimal(s[:-3])

        return Money(amount, currency)

    def to_string(self):
        return '{0} {1}'.format(self.amount, self.currency)

    def set_amount(self, amount):
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        self.amount = amount

    def __repr__(self):
        return "%s %s" % (self.amount.to_integral_value(ROUND_DOWN),
                          self.currency)

    def __unicode__(self):
        # from kernel.money.localization import format_money
        # return format_money(self, locale='en_US')
        return str(self.amount) + ' ' + str(self.currency)

    def __str__(self):
        # from kernel.money.localization import format_money
        # return format_money(self, locale='en_US')
        return str(self.amount) + ' ' + str(self.currency)

    def __pos__(self):
        return self.__class__(
            amount=self.amount,
            currency=self.currency)

    def __neg__(self):
        return self.__class__(
            amount=-self.amount,
            currency=self.currency)

    def __add__(self, other):
        if other == 0:
            # This allows things like 'sum' to work on list of Money instances,
            # just like list of Decimal.
            return self
        if not isinstance(other, Money):
            raise TypeError('Cannot add or subtract a ' +
                            'Money and non-Money instance.')
        if self.currency == other.currency:
            return self.__class__(
                amount=self.amount + other.amount,
                currency=self.currency)

        raise TypeError('Cannot add or subtract two Money ' +
                        'instances with different currencies.')

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError('Cannot multiply two Money instances.')
        else:
            if isinstance(other, float):
                warnings.warn("Multiplying Money instances with floats is deprecated", DeprecationWarning)
            return self.__class__(
                amount=(self.amount * Decimal(str(other))),
                currency=self.currency)

    def __truediv__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise TypeError('Cannot divide two different currencies.')
            return self.amount / other.amount
        else:
            if isinstance(other, float):
                warnings.warn("Dividing Money instances by floats is deprecated", DeprecationWarning)
            return self.__class__(
                amount=self.amount / Decimal(str(other)),
                currency=self.currency)

    def __abs__(self):
        return self.__class__(
            amount=abs(self.amount),
            currency=self.currency)

    def __bool__(self):
        return bool(self.amount)

    if PYTHON2:
        __nonzero__ = __bool__

    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the
        operator must be a numeric value.

        Example:
         money = Money(200, 'USD')
         5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError('Invalid __rmod__ operation')
        else:
            if isinstance(other, float):
                warnings.warn("Calculating percentages of Money instances using floats is deprecated",
                              DeprecationWarning)
            return self.__class__(
                amount=(Decimal(str(other)) * self.amount / 100),
                currency=self.currency)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rtruediv__ = __truediv__

    # _______________________________________
    # Override comparison operators
    def __eq__(self, other):
        return (isinstance(other, Money)
                and (self.amount == other.amount)
                and (self.currency == other.currency))

    def __ne__(self, other):
        result = self.__eq__(other)
        return not result

    def __lt__(self, other):
        if not isinstance(other, Money):
            raise MoneyComparisonError(other)
        if (self.currency == other.currency):
            return (self.amount < other.amount)
        else:
            raise TypeError('Cannot compare Money with different currencies.')

    def __gt__(self, other):
        if not isinstance(other, Money):
            raise MoneyComparisonError(other)
        if (self.currency == other.currency):
            return (self.amount > other.amount)
        else:
            raise TypeError('Cannot compare Money with different currencies.')

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def exchange(self, exchange_rate=None, mode=None):

        if exchange_rate is None:
            raise CriticalError('??????????????????????????????')

        if exchange_rate.protocol.base_currency != self.currency:
            raise CriticalError('?????????????????????????????????')

        money = Money(self.amount * exchange_rate.val, exchange_rate.protocol.target_currency)

        if mode == 'floor':
            return money.floor()
        elif mode == 'ceil':
            return money.ceil()
        else:
            return money

    def floor(self):
        """ ???????????? """
        import math
        money = Money(math.floor(self.amount), self.currency)
        return money

    def ceil(self):
        """ ???????????? """
        import math
        money = Money(math.ceil(self.amount), self.currency)
        return money


# ____________________________________________________________________
# Definitions of ISO 4217 Currencies
# Source: http://www.iso.org/iso/support/faqs/faqs_widely_used_standards/widely_used_standards_other/currency_codes/currency_codes_list-1.htm

CURRENCIES = {}
CURRENCIES_BY_ISO = {}


def add_currency(code, numeric, name, countries):
    global CURRENCIES
    CURRENCIES[code] = Currency(
        code=code,
        numeric=numeric,
        name=name,
        countries=countries)
    CURRENCIES_BY_ISO[numeric] = CURRENCIES[code]
    return CURRENCIES[code]


def get_currency_by_code(code):
    try:
        if not isinstance(code, Currency):
            return CURRENCIES[code]
        else:
            return code
    except KeyError:
        raise CurrencyDoesNotExist(code)


def get_currency_by_iso(iso):
    try:
        return CURRENCIES_BY_ISO[str(iso)]
    except KeyError:
        raise CurrencyDoesNotExist(iso)


def get_currency(code=None, iso=None):
    try:
        if iso:
            return CURRENCIES_BY_ISO[str(iso)]
        return CURRENCIES[code]
    except KeyError:
        raise CurrencyDoesNotExist(code)


def currency_exist(code=None, iso=None):
    try:
        get_currency(code, iso)
        return True
    except:
        return False


DEFAULT_CURRENCY = add_currency(DEFAULT_CURRENCY_CODE, '999', 'Default currency.', [])

AED = add_currency('AED', '784', 'UAE Dirham', ['UNITED ARAB EMIRATES'])
AFN = add_currency('AFN', '971', 'Afghani', ['AFGHANISTAN'])
ALL = add_currency('ALL', '008', 'Lek', ['ALBANIA'])
AMD = add_currency('AMD', '051', 'Armenian Dram', ['ARMENIA'])
ANG = add_currency('ANG', '532', 'Netherlands Antillian Guilder', ['NETHERLANDS ANTILLES'])
AOA = add_currency('AOA', '973', 'Kwanza', ['ANGOLA'])
ARS = add_currency('ARS', '032', 'Argentine Peso', ['ARGENTINA'])
AUD = add_currency('AUD', '036', 'Australian Dollar',
                   ['AUSTRALIA', 'CHRISTMAS ISLAND', 'COCOS (KEELING) ISLANDS', 'HEARD ISLAND AND MCDONALD ISLANDS',
                    'KIRIBATI', 'NAURU', 'NORFOLK ISLAND', 'TUVALU'])
AWG = add_currency('AWG', '533', 'Aruban Guilder', ['ARUBA'])
AZN = add_currency('AZN', '944', 'Azerbaijanian Manat', ['AZERBAIJAN'])
BAM = add_currency('BAM', '977', 'Convertible Marks', ['BOSNIA AND HERZEGOVINA'])
BBD = add_currency('BBD', '052', 'Barbados Dollar', ['BARBADOS'])
BDT = add_currency('BDT', '050', 'Taka', ['BANGLADESH'])
BGN = add_currency('BGN', '975', 'Bulgarian Lev', ['BULGARIA'])
BHD = add_currency('BHD', '048', 'Bahraini Dinar', ['BAHRAIN'])
BIF = add_currency('BIF', '108', 'Burundi Franc', ['BURUNDI'])
BMD = add_currency('BMD', '060', 'Bermudian Dollar (customarily known as Bermuda Dollar)', ['BERMUDA'])
BND = add_currency('BND', '096', 'Brunei Dollar', ['BRUNEI DARUSSALAM'])
BRL = add_currency('BRL', '986', 'Brazilian Real', ['BRAZIL'])
BSD = add_currency('BSD', '044', 'Bahamian Dollar', ['BAHAMAS'])
BTN = add_currency('BTN', '064', 'Bhutanese ngultrum', ['BHUTAN'])
BWP = add_currency('BWP', '072', 'Pula', ['BOTSWANA'])
BYR = add_currency('BYR', '974', 'Belarussian Ruble', ['BELARUS'])
BZD = add_currency('BZD', '084', 'Belize Dollar', ['BELIZE'])
CAD = add_currency('CAD', '124', 'Canadian Dollar', ['CANADA'])
CDF = add_currency('CDF', '976', 'Congolese franc', ['DEMOCRATIC REPUBLIC OF CONGO'])
CHF = add_currency('CHF', '756', 'Swiss Franc', ['LIECHTENSTEIN'])
CLP = add_currency('CLP', '152', 'Chilean peso', ['CHILE'])
CNY = add_currency('CNY', '156', 'Yuan Renminbi', ['CHINA'])
CNH = add_currency('CNH', '156', 'Yuan Renminbi', ['CHINA'])
COP = add_currency('COP', '170', 'Colombian peso', ['COLOMBIA'])
CRC = add_currency('CRC', '188', 'Costa Rican Colon', ['COSTA RICA'])
CUC = add_currency('CUC', '931', 'Cuban convertible peso', ['CUBA'])
CUP = add_currency('CUP', '192', 'Cuban Peso', ['CUBA'])
CVE = add_currency('CVE', '132', 'Cape Verde Escudo', ['CAPE VERDE'])
CZK = add_currency('CZK', '203', 'Czech Koruna', ['CZECH REPUBLIC'])
DJF = add_currency('DJF', '262', 'Djibouti Franc', ['DJIBOUTI'])
DKK = add_currency('DKK', '208', 'Danish Krone', ['DENMARK', 'FAROE ISLANDS', 'GREENLAND'])
DOP = add_currency('DOP', '214', 'Dominican Peso', ['DOMINICAN REPUBLIC'])
DZD = add_currency('DZD', '012', 'Algerian Dinar', ['ALGERIA'])
EGP = add_currency('EGP', '818', 'Egyptian Pound', ['EGYPT'])
ERN = add_currency('ERN', '232', 'Nakfa', ['ERITREA'])
ETB = add_currency('ETB', '230', 'Ethiopian Birr', ['ETHIOPIA'])
EUR = add_currency('EUR', '978', 'Euro',
                   ['AKROTIRI AND DHEKELIA', 'ANDORRA', 'AUSTRIA', 'BELGIUM', 'CYPRUS', 'ESTONIA', 'FINLAND', 'FRANCE',
                    'GERMANY', 'GREECE', 'GUADELOUPE', 'IRELAND', 'ITALY', 'KOSOVO', 'LATVIA', 'LITHUANIA',
                    'LUXEMBOURG', 'MALTA', 'MARTINIQUE', 'MAYOTTE', 'MONACO', 'MONTENEGRO', 'NETHERLANDS', 'PORTUGAL',
                    'R??UNION', 'SAN MARINO', 'SAINT BARTH??LEMY', 'SAINT PIERRE AND MIQUELON', 'SAN MARINO', 'SLOVAKIA',
                    'SLOVENIA', 'SPAIN', 'VATICAN CITY'])
FJD = add_currency('FJD', '242', 'Fiji Dollar', ['FIJI'])
FKP = add_currency('FKP', '238', 'Falkland Islands Pound', ['FALKLAND ISLANDS (MALVINAS)'])
GBP = add_currency('GBP', '826', 'Pound Sterling', ['UNITED KINGDOM'])
GEL = add_currency('GEL', '981', 'Lari', ['GEORGIA'])
GHS = add_currency('GHS', '936', 'Ghana Cedi', ['GHANA'])
GIP = add_currency('GIP', '292', 'Gibraltar Pound', ['GIBRALTAR'])
GMD = add_currency('GMD', '270', 'Dalasi', ['GAMBIA'])
GNF = add_currency('GNF', '324', 'Guinea Franc', ['GUINEA'])
GTQ = add_currency('GTQ', '320', 'Quetzal', ['GUATEMALA'])
GYD = add_currency('GYD', '328', 'Guyana Dollar', ['GUYANA'])
HKD = add_currency('HKD', '344', 'Hong Kong Dollar', ['HONG KONG'])
HNL = add_currency('HNL', '340', 'Lempira', ['HONDURAS'])
HRK = add_currency('HRK', '191', 'Croatian Kuna', ['CROATIA'])
HTG = add_currency('HTG', '332', 'Haitian gourde', ['HAITI'])
HUF = add_currency('HUF', '348', 'Forint', ['HUNGARY'])
IDR = add_currency('IDR', '360', 'Rupiah', ['INDONESIA'])
ILS = add_currency('ILS', '376', 'New Israeli Sheqel', ['ISRAEL'])
IMP = add_currency('IMP', 'Nil', 'Isle of Man Pound', ['ISLE OF MAN'])
INR = add_currency('INR', '356', 'Indian Rupee', ['INDIA'])
IQD = add_currency('IQD', '368', 'Iraqi Dinar', ['IRAQ'])
IRR = add_currency('IRR', '364', 'Iranian Rial', ['IRAN'])
ISK = add_currency('ISK', '352', 'Iceland Krona', ['ICELAND'])
JMD = add_currency('JMD', '388', 'Jamaican Dollar', ['JAMAICA'])
JOD = add_currency('JOD', '400', 'Jordanian Dinar', ['JORDAN'])
JPY = add_currency('JPY', '392', 'Yen', ['JAPAN'])
KES = add_currency('KES', '404', 'Kenyan Shilling', ['KENYA'])
KGS = add_currency('KGS', '417', 'Som', ['KYRGYZSTAN'])
KHR = add_currency('KHR', '116', 'Riel', ['CAMBODIA'])
KMF = add_currency('KMF', '174', 'Comoro Franc', ['COMOROS'])
KPW = add_currency('KPW', '408', 'North Korean Won', ['KOREA'])
KRW = add_currency('KRW', '410', 'Won', ['KOREA'])
KWD = add_currency('KWD', '414', 'Kuwaiti Dinar', ['KUWAIT'])
KYD = add_currency('KYD', '136', 'Cayman Islands Dollar', ['CAYMAN ISLANDS'])
KZT = add_currency('KZT', '398', 'Tenge', ['KAZAKHSTAN'])
LAK = add_currency('LAK', '418', 'Kip', ['LAO PEOPLES DEMOCRATIC REPUBLIC'])
LBP = add_currency('LBP', '422', 'Lebanese Pound', ['LEBANON'])
LKR = add_currency('LKR', '144', 'Sri Lanka Rupee', ['SRI LANKA'])
LRD = add_currency('LRD', '430', 'Liberian Dollar', ['LIBERIA'])
LSL = add_currency('LSL', '426', 'Lesotho loti', ['LESOTHO'])
LTL = add_currency('LTL', '440', 'Lithuanian Litas', ['LITHUANIA'])
LVL = add_currency('LVL', '428', 'Latvian Lats', ['LATVIA'])
LYD = add_currency('LYD', '434', 'Libyan Dinar', ['LIBYAN ARAB JAMAHIRIYA'])
MAD = add_currency('MAD', '504', 'Moroccan Dirham', ['MOROCCO', 'WESTERN SAHARA'])
MDL = add_currency('MDL', '498', 'Moldovan Leu', ['MOLDOVA'])
MGA = add_currency('MGA', '969', 'Malagasy Ariary', ['MADAGASCAR'])
MKD = add_currency('MKD', '807', 'Denar', ['MACEDONIA'])
MMK = add_currency('MMK', '104', 'Kyat', ['MYANMAR'])
MNT = add_currency('MNT', '496', 'Tugrik', ['MONGOLIA'])
MOP = add_currency('MOP', '446', 'Pataca', ['MACAO'])
MRO = add_currency('MRO', '478', 'Ouguiya', ['MAURITANIA'])
MUR = add_currency('MUR', '480', 'Mauritius Rupee', ['MAURITIUS'])
MVR = add_currency('MVR', '462', 'Rufiyaa', ['MALDIVES'])
MWK = add_currency('MWK', '454', 'Malawian Kwacha', ['MALAWI'])
MXN = add_currency('MXN', '484', 'Mexican peso', ['MEXICO'])
MYR = add_currency('MYR', '458', 'Malaysian Ringgit', ['MALAYSIA'])
MZN = add_currency('MZN', '943', 'Metical', ['MOZAMBIQUE'])
NAD = add_currency('NAD', '516', 'Namibian Dollar', ['NAMIBIA'])
NGN = add_currency('NGN', '566', 'Naira', ['NIGERIA'])
NIO = add_currency('NIO', '558', 'Cordoba Oro', ['NICARAGUA'])
NOK = add_currency('NOK', '578', 'Norwegian Krone', ['BOUVET ISLAND', 'NORWAY', 'SVALBARD AND JAN MAYEN'])
NPR = add_currency('NPR', '524', 'Nepalese Rupee', ['NEPAL'])
NZD = add_currency('NZD', '554', 'New Zealand Dollar', ['COOK ISLANDS', 'NEW ZEALAND', 'NIUE', 'PITCAIRN', 'TOKELAU'])
OMR = add_currency('OMR', '512', 'Rial Omani', ['OMAN'])
PEN = add_currency('PEN', '604', 'Nuevo Sol', ['PERU'])
PGK = add_currency('PGK', '598', 'Kina', ['PAPUA NEW GUINEA'])
PHP = add_currency('PHP', '608', 'Philippine Peso', ['PHILIPPINES'])
PKR = add_currency('PKR', '586', 'Pakistan Rupee', ['PAKISTAN'])
PLN = add_currency('PLN', '985', 'Zloty', ['POLAND'])
PYG = add_currency('PYG', '600', 'Guarani', ['PARAGUAY'])
QAR = add_currency('QAR', '634', 'Qatari Rial', ['QATAR'])
RON = add_currency('RON', '946', 'New Leu', ['ROMANIA'])
RSD = add_currency('RSD', '941', 'Serbian Dinar', ['SERBIA'])
RUB = add_currency('RUB', '643', 'Russian Ruble', ['RUSSIAN FEDERATION'])
RWF = add_currency('RWF', '646', 'Rwanda Franc', ['RWANDA'])
SAR = add_currency('SAR', '682', 'Saudi Riyal', ['SAUDI ARABIA'])
SBD = add_currency('SBD', '090', 'Solomon Islands Dollar', ['SOLOMON ISLANDS'])
SCR = add_currency('SCR', '690', 'Seychelles Rupee', ['SEYCHELLES'])
SDG = add_currency('SDG', '938', 'Sudanese Pound', ['SUDAN'])
SEK = add_currency('SEK', '752', 'Swedish Krona', ['SWEDEN'])
SGD = add_currency('SGD', '702', 'Singapore Dollar', ['SINGAPORE'])
SHP = add_currency('SHP', '654', 'Saint Helena Pound', ['SAINT HELENA'])
SLL = add_currency('SLL', '694', 'Leone', ['SIERRA LEONE'])
SOS = add_currency('SOS', '706', 'Somali Shilling', ['SOMALIA'])
SRD = add_currency('SRD', '968', 'Surinam Dollar', ['SURINAME'])
STD = add_currency('STD', '678', 'Dobra', ['SAO TOME AND PRINCIPE'])
SYP = add_currency('SYP', '760', 'Syrian Pound', ['SYRIAN ARAB REPUBLIC'])
SZL = add_currency('SZL', '748', 'Lilangeni', ['SWAZILAND'])
THB = add_currency('THB', '764', 'Baht', ['THAILAND'])
TJS = add_currency('TJS', '972', 'Somoni', ['TAJIKISTAN'])
TMM = add_currency('TMM', '795', 'Manat', ['TURKMENISTAN'])
TND = add_currency('TND', '788', 'Tunisian Dinar', ['TUNISIA'])
TOP = add_currency('TOP', '776', 'Paanga', ['TONGA'])
TRY = add_currency('TRY', '949', 'Turkish Lira', ['TURKEY'])
TTD = add_currency('TTD', '780', 'Trinidad and Tobago Dollar', ['TRINIDAD AND TOBAGO'])
TVD = add_currency('TVD', 'Nil', 'Tuvalu dollar', ['TUVALU'])
TWD = add_currency('TWD', '901', 'New Taiwan Dollar', ['TAIWAN'])
TZS = add_currency('TZS', '834', 'Tanzanian Shilling', ['TANZANIA'])
UAH = add_currency('UAH', '980', 'Hryvnia', ['UKRAINE'])
UGX = add_currency('UGX', '800', 'Uganda Shilling', ['UGANDA'])
USD = add_currency('USD', '840', 'US Dollar',
                   ['AMERICAN SAMOA', 'BRITISH INDIAN OCEAN TERRITORY', 'ECUADOR', 'GUAM', 'MARSHALL ISLANDS',
                    'MICRONESIA', 'NORTHERN MARIANA ISLANDS', 'PALAU', 'PUERTO RICO', 'TIMOR-LESTE',
                    'TURKS AND CAICOS ISLANDS', 'UNITED STATES', 'UNITED STATES MINOR OUTLYING ISLANDS',
                    'VIRGIN ISLANDS (BRITISH)', 'VIRGIN ISLANDS (U.S.)'])
UYU = add_currency('UYU', '858', 'Uruguayan peso', ['URUGUAY'])
UZS = add_currency('UZS', '860', 'Uzbekistan Sum', ['UZBEKISTAN'])
VEF = add_currency('VEF', '937', 'Bolivar Fuerte', ['VENEZUELA'])
VND = add_currency('VND', '704', 'Dong', ['VIET NAM'])
VUV = add_currency('VUV', '548', 'Vatu', ['VANUATU'])
WST = add_currency('WST', '882', 'Tala', ['SAMOA'])
XAF = add_currency('XAF', '950', 'CFA franc BEAC',
                   ['CAMEROON', 'CENTRAL AFRICAN REPUBLIC', 'REPUBLIC OF THE CONGO', 'CHAD', 'EQUATORIAL GUINEA',
                    'GABON'])
XAG = add_currency('XAG', '961', 'Silver', [])
XAU = add_currency('XAU', '959', 'Gold', [])
XBA = add_currency('XBA', '955', 'Bond Markets Units European Composite Unit (EURCO)', [])
XBB = add_currency('XBB', '956', 'European Monetary Unit (E.M.U.-6)', [])
XBC = add_currency('XBC', '957', 'European Unit of Account 9(E.U.A.-9)', [])
XBD = add_currency('XBD', '958', 'European Unit of Account 17(E.U.A.-17)', [])
XCD = add_currency('XCD', '951', 'East Caribbean Dollar',
                   ['ANGUILLA', 'ANTIGUA AND BARBUDA', 'DOMINICA', 'GRENADA', 'MONTSERRAT', 'SAINT KITTS AND NEVIS',
                    'SAINT LUCIA', 'SAINT VINCENT AND THE GRENADINES'])
XDR = add_currency('XDR', '960', 'SDR', ['INTERNATIONAL MONETARY FUND (I.M.F)'])
XFO = add_currency('XFO', 'Nil', 'Gold-Franc', [])
XFU = add_currency('XFU', 'Nil', 'UIC-Franc', [])
XOF = add_currency('XOF', '952', 'CFA Franc BCEAO',
                   ['BENIN', 'BURKINA FASO', 'COTE D\'IVOIRE', 'GUINEA-BISSAU', 'MALI', 'NIGER', 'SENEGAL', 'TOGO'])
XPD = add_currency('XPD', '964', 'Palladium', [])
XPF = add_currency('XPF', '953', 'CFP Franc', ['FRENCH POLYNESIA', 'NEW CALEDONIA', 'WALLIS AND FUTUNA'])
XPT = add_currency('XPT', '962', 'Platinum', [])
XTS = add_currency('XTS', '963', 'Codes specifically reserved for testing purposes', [])
YER = add_currency('YER', '886', 'Yemeni Rial', ['YEMEN'])
ZAR = add_currency('ZAR', '710', 'Rand', ['SOUTH AFRICA'])
ZMK = add_currency('ZMK', '894', 'Zambian Kwacha', [])  # historical
ZMW = add_currency('ZMW', '967', 'Zambian Kwacha', ['ZAMBIA'])
ZWD = add_currency('ZWD', '716', 'Zimbabwe Dollar A/06', ['ZIMBABWE'])
ZWL = add_currency('ZWL', '932', 'Zimbabwe dollar A/09', ['ZIMBABWE'])
ZWN = add_currency('ZWN', '942', 'Zimbabwe dollar A/08', ['ZIMBABWE'])

if __name__ == '__main__':
    # money = Money.from_string('  123.00  USD  ')
    # print(money.to_string())

    print(currency_exist('USD'))
