import _plotly_utils.basevalidators


class TickcolorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self,
        plotly_name='tickcolor',
        parent_name='layout.ternary.aaxis',
        **kwargs
    ):
        super(TickcolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'plot'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
