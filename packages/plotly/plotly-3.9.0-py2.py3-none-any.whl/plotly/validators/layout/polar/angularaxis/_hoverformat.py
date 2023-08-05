import _plotly_utils.basevalidators


class HoverformatValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='hoverformat',
        parent_name='layout.polar.angularaxis',
        **kwargs
    ):
        super(HoverformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'none'),
            role=kwargs.pop('role', 'style'),
            **kwargs
        )
