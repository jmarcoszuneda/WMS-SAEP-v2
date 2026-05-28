from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()

_UMA_DECIMAL = ('kg', 'l', 'm')


@register.filter
def formatar_quantidade(qtd, unidade: str) -> str:
    """Formata quantidade conforme a unidade de medida do material.

    - 'un' → inteiro
    - 'kg', 'l', 'm' → 1 casa decimal
    - demais → strip trailing zeros (casas significativas)
    """
    if qtd is None:
        return '—'
    try:
        d = Decimal(str(qtd))
    except (InvalidOperation, TypeError, ValueError):
        return str(qtd)

    if unidade == 'un':
        return str(int(d))

    if unidade in _UMA_DECIMAL:
        return format(d.quantize(Decimal('0.1')), 'f')

    normalized = d.normalize()
    if normalized == normalized.to_integral_value():
        return str(int(normalized))
    return format(normalized, 'f')
