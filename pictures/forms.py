from django import forms

from dal import autocomplete

from .models import Member


class MemberForm(forms.Form):
    member = forms.ModelChoiceField(queryset=Member.get_all(),
                                    widget=autocomplete.ModelSelect2(
                                        url='member-autocomplete'),
                                    label='成员'
                                    )
    image_url = forms.URLField(label='图片地址', required=False)
    image_file = forms.FileField(label='上传图片', required=False)

    class Meta:
        fieldsets = (
            ('成员', {
                'description': None,
                'fields': (
                    'members',
                )
            }),
            ('照片', {
                'fields': (
                    'image_url',
                    'image_file',
                )
            })
        )
