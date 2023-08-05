import _plotly_utils.basevalidators


class WidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='width', parent_name='scatterpolargl.line', **kwargs
    ):
        super(WidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            anim=kwargs.pop('anim', True),
            edit_type=kwargs.pop('edit_type', 'calc'),
            min=kwargs.pop('min', 0),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
