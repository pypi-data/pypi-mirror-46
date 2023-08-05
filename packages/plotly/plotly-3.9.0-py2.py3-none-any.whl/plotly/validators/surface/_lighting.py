import _plotly_utils.basevalidators


class LightingValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(
        self, plotly_name='lighting', parent_name='surface', **kwargs
    ):
        super(LightingValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str=kwargs.pop('data_class_str', 'Lighting'),
            data_docs=kwargs.pop(
                'data_docs', """
            ambient
                Ambient light increases overall color
                visibility but can wash out the image.
            diffuse
                Represents the extent that incident rays are
                reflected in a range of angles.
            fresnel
                Represents the reflectance as a dependency of
                the viewing angle; e.g. paper is reflective
                when viewing it from the edge of the paper
                (almost 90 degrees), causing shine.
            roughness
                Alters specular reflection; the rougher the
                surface, the wider and less contrasty the
                shine.
            specular
                Represents the level that incident rays are
                reflected in a single direction, causing shine.
"""
            ),
            **kwargs
        )
