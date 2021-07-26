from django_filters import FilterSet, DateFromToRangeFilter

from carbon_usage.models import Usage, UsageType


class CarbonUsageFilter(FilterSet):
    """Filter for Carbon Usage

    e.g:
    {{url}}/carbon_usage/users/usages/?usage_at_after=2021-07-20&usage_at_before=2021-07-22
    """

    usage_at = DateFromToRangeFilter()

    class Meta:
        model = Usage
        fields = ("usage_at",)


class CarbonUsageTypeFilter(FilterSet):
    """Filter for Carbon Usage Type

    e.g:
    {{url}}/carbon_usage/users/usages/?usage_at_after=2021-07-20&usage_at_before=2021-07-22
    """

    class Meta:
        model = UsageType
        fields = ("name", "unit", "factor")
