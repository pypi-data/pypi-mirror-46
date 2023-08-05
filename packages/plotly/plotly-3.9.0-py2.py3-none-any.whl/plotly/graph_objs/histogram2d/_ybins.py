from plotly.basedatatypes import BaseTraceHierarchyType
import copy


class YBins(BaseTraceHierarchyType):

    # end
    # ---
    @property
    def end(self):
        """
        Sets the end value for the y axis bins. The last bin may not
        end exactly at this value, we increment the bin edge by `size`
        from `start` until we reach or exceed `end`. Defaults to the
        maximum data value. Like `start`, for dates use a date string,
        and for category data `end` is based on the category serial
        numbers.
    
        The 'end' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['end']

    @end.setter
    def end(self, val):
        self['end'] = val

    # size
    # ----
    @property
    def size(self):
        """
        Sets the size of each y axis bin. Default behavior: If `nbinsy`
        is 0 or omitted, we choose a nice round bin size such that the
        number of bins is about the same as the typical number of
        samples in each bin. If `nbinsy` is provided, we choose a nice
        round bin size giving no more than that many bins. For date
        data, use milliseconds or "M<n>" for months, as in
        `axis.dtick`. For category data, the number of categories to
        bin together (always defaults to 1).
    
        The 'size' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['size']

    @size.setter
    def size(self, val):
        self['size'] = val

    # start
    # -----
    @property
    def start(self):
        """
        Sets the starting value for the y axis bins. Defaults to the
        minimum data value, shifted down if necessary to make nice
        round values and to remove ambiguous bin edges. For example, if
        most of the data is integers we shift the bin edges 0.5 down,
        so a `size` of 5 would have a default `start` of -0.5, so it is
        clear that 0-4 are in the first bin, 5-9 in the second, but
        continuous data gets a start of 0 and bins [0,5), [5,10) etc.
        Dates behave similarly, and `start` should be a date string.
        For category data, `start` is based on the category serial
        numbers, and defaults to -0.5.
    
        The 'start' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['start']

    @start.setter
    def start(self, val):
        self['start'] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return 'histogram2d'

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        end
            Sets the end value for the y axis bins. The last bin
            may not end exactly at this value, we increment the bin
            edge by `size` from `start` until we reach or exceed
            `end`. Defaults to the maximum data value. Like
            `start`, for dates use a date string, and for category
            data `end` is based on the category serial numbers.
        size
            Sets the size of each y axis bin. Default behavior: If
            `nbinsy` is 0 or omitted, we choose a nice round bin
            size such that the number of bins is about the same as
            the typical number of samples in each bin. If `nbinsy`
            is provided, we choose a nice round bin size giving no
            more than that many bins. For date data, use
            milliseconds or "M<n>" for months, as in `axis.dtick`.
            For category data, the number of categories to bin
            together (always defaults to 1).
        start
            Sets the starting value for the y axis bins. Defaults
            to the minimum data value, shifted down if necessary to
            make nice round values and to remove ambiguous bin
            edges. For example, if most of the data is integers we
            shift the bin edges 0.5 down, so a `size` of 5 would
            have a default `start` of -0.5, so it is clear that 0-4
            are in the first bin, 5-9 in the second, but continuous
            data gets a start of 0 and bins [0,5), [5,10) etc.
            Dates behave similarly, and `start` should be a date
            string. For category data, `start` is based on the
            category serial numbers, and defaults to -0.5.
        """

    def __init__(self, arg=None, end=None, size=None, start=None, **kwargs):
        """
        Construct a new YBins object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.histogram2d.YBins
        end
            Sets the end value for the y axis bins. The last bin
            may not end exactly at this value, we increment the bin
            edge by `size` from `start` until we reach or exceed
            `end`. Defaults to the maximum data value. Like
            `start`, for dates use a date string, and for category
            data `end` is based on the category serial numbers.
        size
            Sets the size of each y axis bin. Default behavior: If
            `nbinsy` is 0 or omitted, we choose a nice round bin
            size such that the number of bins is about the same as
            the typical number of samples in each bin. If `nbinsy`
            is provided, we choose a nice round bin size giving no
            more than that many bins. For date data, use
            milliseconds or "M<n>" for months, as in `axis.dtick`.
            For category data, the number of categories to bin
            together (always defaults to 1).
        start
            Sets the starting value for the y axis bins. Defaults
            to the minimum data value, shifted down if necessary to
            make nice round values and to remove ambiguous bin
            edges. For example, if most of the data is integers we
            shift the bin edges 0.5 down, so a `size` of 5 would
            have a default `start` of -0.5, so it is clear that 0-4
            are in the first bin, 5-9 in the second, but continuous
            data gets a start of 0 and bins [0,5), [5,10) etc.
            Dates behave similarly, and `start` should be a date
            string. For category data, `start` is based on the
            category serial numbers, and defaults to -0.5.

        Returns
        -------
        YBins
        """
        super(YBins, self).__init__('ybins')

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.histogram2d.YBins 
constructor must be a dict or 
an instance of plotly.graph_objs.histogram2d.YBins"""
            )

        # Handle skip_invalid
        # -------------------
        self._skip_invalid = kwargs.pop('skip_invalid', False)

        # Import validators
        # -----------------
        from plotly.validators.histogram2d import (ybins as v_ybins)

        # Initialize validators
        # ---------------------
        self._validators['end'] = v_ybins.EndValidator()
        self._validators['size'] = v_ybins.SizeValidator()
        self._validators['start'] = v_ybins.StartValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop('end', None)
        self['end'] = end if end is not None else _v
        _v = arg.pop('size', None)
        self['size'] = size if size is not None else _v
        _v = arg.pop('start', None)
        self['start'] = start if start is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))

        # Reset skip_invalid
        # ------------------
        self._skip_invalid = False
