import _plotly_utils.basevalidators


class SelectedpointsValidator(_plotly_utils.basevalidators.AnyValidator):

    def __init__(
        self, plotly_name='selectedpoints', parent_name='streamtube', **kwargs
    ):
        super(SelectedpointsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'calc'),
            role=kwargs.pop('role', 'info'),
            **kwargs
        )
