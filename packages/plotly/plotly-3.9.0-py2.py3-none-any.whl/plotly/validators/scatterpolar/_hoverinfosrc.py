import _plotly_utils.basevalidators


class HoverinfosrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self, plotly_name='hoverinfosrc', parent_name='scatterpolar', **kwargs
    ):
        super(HoverinfosrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'none'),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
