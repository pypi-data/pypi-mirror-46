import _plotly_utils.basevalidators


class IdsValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(self, plotly_name='ids', parent_name='heatmap', **kwargs):
        super(IdsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            anim=kwargs.pop('anim', True),
            edit_type=kwargs.pop('edit_type', 'calc'),
            role=kwargs.pop('role', 'data'),
            **kwargs
        )
