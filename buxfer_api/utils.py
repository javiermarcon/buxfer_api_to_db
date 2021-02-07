import datetime
from .models import DollarPrice, Account


def get_closest_to_date(qs, dt):
    greater = qs.filter(purchase_date__gte=dt).order_by("purchase_date").first()
    less = qs.filter(purchase_date__lte=dt).order_by("-purchase_date").first()

    if greater and less:
        return greater if abs(greater.purchase_date - dt) < abs(less.purchase_date - dt) else less
    else:
        return greater or less


def transform_USD_ARS(cantidad, fecha, impuesto_pais=True):
    '''transforma monto usd a pesos'''
    queryset = DollarPrice.objects.all()
    precioObj = get_closest_to_date(queryset, fecha)
    precio = precioObj.buy
    if impuesto_pais:
        precio = precio * 1.3
    return precio * cantidad


def transform_to_ars_currency(cantidad, fecha, currency='USD'):
    ''' Ttransforma un monto a pesos desde una cierta moneda.
        Si no existe una funcion para transformar el monto, retorna el mismo monto '''
    if currency == 'ARS':
        return cantidad
    try:
        fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d').date()
        func_name = 'transform_{}_ARS'.format(currency)
        return globals()[func_name](cantidad, fecha)
    except (KeyError, NameError):
        return cantidad


def transform_to_ars_account(cantidad, fecha, id_cuenta):
    ''' Ttransforma un monto a pesos segun la moneda de su cuenta.
        Si no existe una funcion para transformar el monto, retorna el mismo monto '''
    try:
        cuenta = Account.objects.get(id=id_cuenta)
        return transform_to_ars_currency(cantidad, fecha, cuenta.currency)
    except NameError:
        return cantidad