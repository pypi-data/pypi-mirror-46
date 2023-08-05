import _plotly_utils.basevalidators


class FamilyValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='family',
        parent_name='scatter3d.marker.colorbar.title.font',
        **kwargs
    ):
        super(FamilyValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop('edit_type', 'calc'),
            no_blank=kwargs.pop('no_blank', True),
            role=kwargs.pop('role', 'style'),
            strict=kwargs.pop('strict', True),
            **kwargs
        )
