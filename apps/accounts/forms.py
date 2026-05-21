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
        self.fields['username'].widget.attrs.update({
            'autocomplete': 'username',
            'autofocus': True,
            'class': (
                'mt-2 block w-full rounded-lg border border-slate-300 '
                'bg-white px-3 py-2 text-slate-900 shadow-sm '
                'placeholder:text-slate-400 focus:border-blue-500 '
                'focus:outline-none focus:ring-2 focus:ring-blue-500'
            ),
        })
        self.fields['password'].widget.attrs.update({
            'autocomplete': 'current-password',
            'class': (
                'mt-2 block w-full rounded-lg border border-slate-300 '
                'bg-white px-3 py-2 text-slate-900 shadow-sm '
                'placeholder:text-slate-400 focus:border-blue-500 '
                'focus:outline-none focus:ring-2 focus:ring-blue-500'
            ),
        })
        if self.is_bound:
            if self['username'].errors:
                self.fields['username'].widget.attrs['aria-invalid'] = 'true'
                self.fields['username'].widget.attrs['aria-describedby'] = (
                    'username-error'
                )
            if self['password'].errors:
                self.fields['password'].widget.attrs['aria-invalid'] = 'true'
                self.fields['password'].widget.attrs['aria-describedby'] = (
                    'password-error'
                )
            if self.non_field_errors():
                self.fields['username'].widget.attrs['aria-invalid'] = 'true'
                self.fields['username'].widget.attrs['aria-describedby'] = (
                    'login-error'
                )
                self.fields['password'].widget.attrs['aria-invalid'] = 'true'
                self.fields['password'].widget.attrs['aria-describedby'] = (
                    'login-error'
                )
