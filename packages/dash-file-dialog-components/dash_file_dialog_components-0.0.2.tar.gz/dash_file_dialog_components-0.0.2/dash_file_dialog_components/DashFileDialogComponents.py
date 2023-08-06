# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashFileDialogComponents(Component):
    """A DashFileDialogComponents component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; optional): The ID used to identify this component in Dash callbacks
- overrideProps (optional): . overrideProps has the following type: dict containing keys 'onChange', 'onError', 'maxSize', 'extensions', 'validateContent', 'style'.
Those keys have the following types:
  - onChange (required)
  - onError (optional)
  - maxSize (number; optional)
  - extensions (list; optional)
  - validateContent (optional)
  - style (dict; optional)
- src (string; optional)
- style (dict with strings as keys and values of type string; optional)
- maxSize (number; optional)
- extensions (list; optional)"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, overrideProps=Component.UNDEFINED, src=Component.UNDEFINED, style=Component.UNDEFINED, onChange=Component.UNDEFINED, maxSize=Component.UNDEFINED, extensions=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'overrideProps', 'src', 'style', 'maxSize', 'extensions']
        self._type = 'DashFileDialogComponents'
        self._namespace = 'dash_file_dialog_components'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'overrideProps', 'src', 'style', 'maxSize', 'extensions']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashFileDialogComponents, self).__init__(**args)
