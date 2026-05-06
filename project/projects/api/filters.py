import django_filters

from projects.models import Project


class ProjectFilter(django_filters.FilterSet):
    technologies = django_filters.CharFilter(
        field_name="technologies", lookup_expr="icontains"
    )
    start_date_after = django_filters.DateFilter(
        field_name="start_date", lookup_expr="gte"
    )
    start_date_before = django_filters.DateFilter(
        field_name="start_date", lookup_expr="lte"
    )

    class Meta:
        model = Project
        fields = ("technologies", "start_date_after", "start_date_before")
