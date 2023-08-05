"""
Parameter views provide ways to read and write parameter data with a defined unit
and time information.
"""

from typing import Any, Sequence, cast

import numpy as np

from .errors import ParameterEmptyError, TimeseriesPointsValuesMismatchError
from .parameters import ParameterType, _Parameter
from .timeseries_converter import (
    ExtrapolationType,
    InterpolationType,
    TimeseriesConverter,
)
from .units import UnitConverter

# pylint: disable=protected-access,too-many-arguments


class ParameterView:
    """
    Generic view to a :ref:`parameter <parameters>` (scalar or timeseries).
    """

    _parameter: _Parameter
    """Parameter"""

    def __init__(self, parameter: _Parameter):
        """
        Initialize.

        Parameters
        ----------
        parameter
            Parameter
        """
        self._parameter = parameter

    @property
    def is_empty(self) -> bool:
        """
        Check if parameter is empty, i.e. has not yet been written to.
        """
        return not self._parameter._has_been_written_to


class ScalarView(ParameterView):
    """
    Read-only view of a scalar parameter.
    """

    _child_data_views: Sequence["ScalarView"]
    """List of views to the child parameters for aggregated reads"""

    _unit_converter: UnitConverter
    """Unit converter"""

    def __init__(self, parameter: _Parameter, unit: str):
        """
        Initialize.

        Parameters
        ----------
        parameter
            Parameter
        unit
            Unit for the values in the view
        """
        super().__init__(parameter)
        self._unit_converter = UnitConverter(cast(str, parameter._info._unit), unit)

        def get_data_views_for_children_or_parameter(
            parameter: _Parameter
        ) -> Sequence["ScalarView"]:
            if parameter._children:
                return sum(
                    (
                        get_data_views_for_children_or_parameter(p)
                        for p in parameter._children.values()
                    ),
                    [],
                )
            return [ScalarView(parameter, self._unit_converter._target)]

        if self._parameter._children:
            self._child_data_views = get_data_views_for_children_or_parameter(
                self._parameter
            )

    def get(self) -> float:
        """
        Get current value of scalar parameter.

        If the parameter has child parameters (i.e. ``_children`` is not empty),
        the returned value will be the sum of the values of all of the child
        parameters.

        Returns
        -------
        float
            Current value of parameter

        Raises
        ------
        ParameterEmptyError
            Parameter is empty, i.e. has not yet been written to
        """
        if self._parameter._children:
            return sum(v.get() for v in self._child_data_views)
        if self.is_empty:
            raise ParameterEmptyError

        return self._unit_converter.convert_from(cast(float, self._parameter._data))


class WritableScalarView(ScalarView):
    """
    View of a scalar parameter whose value can be changed.
    """

    def set(self, value: float) -> None:
        """
        Set current value of scalar parameter.

        Parameters
        ----------
        value
            Value
        """
        self._parameter._data = self._unit_converter.convert_to(value)


class TimeseriesView(ParameterView):
    """
    Read-only :class:`ParameterView` of a timeseries.
    """

    _child_data_views: Sequence["TimeseriesView"]
    """List of views to the child parameters for aggregated reads"""

    _timeseries_converter: TimeseriesConverter
    """Timeseries converter"""

    _unit_converter: UnitConverter
    """Unit converter"""

    def __init__(
        self,
        parameter: _Parameter,
        unit: str,
        time_points: np.ndarray,
        timeseries_type: ParameterType,
        interpolation_type: InterpolationType,
        extrapolation_type: ExtrapolationType,
    ):
        """
        Initialize.

        Parameters
        ----------
        parameter
            Parameter
        unit
            Unit for the values in the view
        time_points
            Timeseries time points
        timeseries_type
            Time series type
        interpolation_type
            Interpolation type
        extrapolation_type
            Extrapolation type
        """
        super().__init__(parameter)
        self._unit_converter = UnitConverter(cast(str, parameter._info._unit), unit)
        self._timeseries_converter = TimeseriesConverter(
            parameter._info._time_points,
            time_points,
            timeseries_type,
            interpolation_type,
            extrapolation_type,
        )  # TimeseriesConverter

        def get_data_views_for_children_or_parameter(
            parameter: _Parameter
        ) -> Sequence["TimeseriesView"]:
            if parameter._children:
                return sum(
                    (
                        get_data_views_for_children_or_parameter(p)
                        for p in parameter._children.values()
                    ),
                    [],
                )
            return [
                TimeseriesView(
                    parameter,
                    self._unit_converter._target,
                    self._timeseries_converter._target,
                    timeseries_type,
                    interpolation_type,
                    extrapolation_type,
                )
            ]

        if self._parameter._children:
            self._child_data_views = get_data_views_for_children_or_parameter(
                self._parameter
            )

    def get(self) -> Sequence[float]:
        """
        Get values of the full timeseries.

        If the parameter has child parameters (i.e. ``_children`` is not empty),
        the returned value will be the sum of the values of all of the child
        parameters.

        Returns
        -------
        Sequence[float]
            Current value of parameter

        Raises
        ------
        ParameterEmptyError
            Parameter is empty, i.e. has not yet been written to
        """
        if self._parameter._children:
            return cast(Sequence[float], sum(v.get() for v in self._child_data_views))
        if self.is_empty:
            raise ParameterEmptyError

        return cast(
            Sequence[float],
            self._timeseries_converter.convert_from(
                self._unit_converter.convert_from(
                    cast(Sequence[float], self._parameter._data)
                )
            ),
        )

    @property
    def length(self) -> int:
        """
        Length of timeseries.
        """
        return self._timeseries_converter.target_length


class WritableTimeseriesView(TimeseriesView):
    """
    View of a timeseries whose values can be changed.
    """

    def set(self, values: Sequence[float]) -> None:
        """
        Set value for whole time series.

        Parameters
        ----------
        values
            Values to set

        Raises
        ------
        TimeseriesPointsValuesMismatchError
            Lengths of ``values`` and the time points number mismatch
        """
        if len(values) != self._timeseries_converter.target_length:
            raise TimeseriesPointsValuesMismatchError
        self._parameter._data = self._timeseries_converter.convert_to(
            self._unit_converter.convert_to(values)
        )


class GenericView(ParameterView):
    """
    Read-only view of a generic parameter.
    """

    def get(self) -> Any:
        """
        Get current value of generic parameter.

        Returns
        -------
        Any
            Current value of parameter

        Raises
        ------
        ParameterEmptyError
            Parameter is empty, i.e. has not yet been written to
        """
        if self.is_empty:
            raise ParameterEmptyError

        return self._parameter._data


class WritableGenericView(GenericView):
    """
    View of a generic parameter whose value can be changed.
    """

    def set(self, value: bool) -> None:
        """
        Set current value of boolean parameter.

        Parameters
        ----------
        value
            Value
        """
        self._parameter._data = value
