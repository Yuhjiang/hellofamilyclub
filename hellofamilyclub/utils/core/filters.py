from django_filters import rest_framework as filters
from django_filters.utils import get_model_field


class BaseFilters(filters.FilterSet):
    """
    https://django-filter.readthedocs.io/en/master/guide/tips.html?highlight=help_text#adding-model-field-help-text-to-filters
    django-filter不会用到model的help_text字段，所以需再要生成field的时候手动添加
    """
    @classmethod
    def filter_for_field(cls, f, field_name, lookup_expr='exact'):
        filter_ = super().filter_for_field(f, field_name, lookup_expr)
        if f.help_text:
            filter_.extra['help_text'] = f.help_text
        elif f.verbose_name:
            filter_.extra['help_text'] = f.verbose_name
        return filter_

    @classmethod
    def get_filters(cls):
        for field_name, filter_ in cls.declared_filters.items():
            if not filter_.extra.get('help_text'):
                field = get_model_field(cls._meta.model, field_name)
                if field:
                    if field.help_text:
                        filter_.extra['help_text'] = field.help_text
                    elif field.verbose_name:
                        filter_.extra['help_text'] = field.verbose_name

        return super().get_filters()
