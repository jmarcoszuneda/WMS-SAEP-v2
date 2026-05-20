"""Formulários do app accounts."""
from django.contrib.auth.forms import AuthenticationForm


class MatriculaAuthenticationForm(AuthenticationForm):
    """Autenticação por matrícula e senha.

    Reaproveita o ``AuthenticationForm`` do Django; o `User` já usa
    ``USERNAME_FIELD = "matricula"``, então não há backend customizado.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Matrícula'
