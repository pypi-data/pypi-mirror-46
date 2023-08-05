# djangovue

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

A set of helper tags and form widgets for making django and vue play nicely.

# Installation

```bash
pip install djangovue
```

# Tags Example

```python
class IndexView(TemplateView):
  template = 'index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['message'] = 'Hello from Django'
    return context
```


```html
{% load djangovue %}

{% load_vuejs %}

{% djangovue on %}
  <div id="app">
    <p>
      {{ message }}
  </p>
  {% djangovue off %}
    <p>
    {{ message }}
  </p>
  {% enddjangovue off %}

  </div>
  
  <script>
    new Vue({
      el: '#app',
      data: {
        message: 'Hello from Vue'
      }
    });
  </script>
{% enddjangovue%}
```

# Widgets Example

```python
from django import forms
from djangovue import widgets


class UserForm(forms.Form):
    username = forms.CharField(
        max_length=30,
        widget=widgets.TextInput(
            model="user.username",
            modifier=widgets.TextInput.LAZY,
            attrs={":disabled": "disable"},
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        widget=widgets.TextInput(
            model="user.first_name", attrs={":disabled": "disable"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        widget=widgets.TextInput(
            model="user.last_name", attrs={":disabled": "disable"}
        ),
    )
    gender = forms.ChoiceField(
        choices=[("male", "Male"), ("female", "Female")],
        widget=widgets.RadioSelect(
            attrs={"v-model": "user.gender", ":disabled": "disable"}
        ),
    )
    disable = forms.BooleanField(
        required=False, widget=widgets.CheckboxInput() # v-model will automatically be set to `disable`
    )
```

# Development

Should you wish to develop the library there are some helper functions within the Makefile to get you started.

```bash
make install # Installs the project dependencies including the node modules required for the DjangoVue Vue plugin
make bundle # Transpiles and bundles the DjangoVue.ts file
make test # Runs tests
make black # Applies black formatting to the project
```

Once installed run the following to view the examples:

```bash
cd djangovue/examples
poetry run ./manage.py runserver
```

Note this project uses [Poetry](https://poetry.eustace.io/) for packaging and managing dependencies.
