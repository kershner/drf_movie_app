from django import forms


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, min_length=2, label=False,
                        widget=forms.TextInput(attrs={
                            'placeholder': 'Search for a movie, person, or character...'
                        }))
