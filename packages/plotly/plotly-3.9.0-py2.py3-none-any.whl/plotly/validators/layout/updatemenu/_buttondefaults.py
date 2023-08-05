import _plotly_utils.basevalidators


class ButtonValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(
        self,
        plotly_name='buttondefaults',
        parent_name='layout.updatemenu',
        **kwargs
    ):
        super(ButtonValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop('data_class_str', 'Button'),
            data_docs=kwargs.pop('data_docs', """
"""),
            **kwargs
        )
