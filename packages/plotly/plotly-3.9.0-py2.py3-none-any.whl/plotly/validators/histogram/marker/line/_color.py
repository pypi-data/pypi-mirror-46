import _plotly_utils.basevalidators


class ColorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self,
        plotly_name='color',
        parent_name='histogram.marker.line',
        **kwargs
    ):
        super(ColorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=kwargs.pop('array_ok', True),
            edit_type=kwargs.pop('edit_type', 'style'),
            role=kwargs.pop('role', 'style'),
            colorscale_path=kwargs.pop(
                'colorscale_path', 'histogram.marker.line.colorscale'
            ),
            **kwargs
        )
