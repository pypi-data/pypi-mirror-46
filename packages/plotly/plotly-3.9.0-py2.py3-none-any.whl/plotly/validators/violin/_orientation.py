import _plotly_utils.basevalidators


class OrientationValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='orientation', parent_name='violin', **kwargs
    ):
        super(OrientationValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'calc+clearAxisTypes'),
            role=kwargs.pop('role', 'style'),
            values=kwargs.pop('values', ['v', 'h']),
            **kwargs
        )
