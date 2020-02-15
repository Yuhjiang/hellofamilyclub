from django import forms

from .models import Member


class MemberAdminForm(forms.ModelForm):
    graduated_time = forms.DateField(widget=forms.DateInput, required=False,
                                     label='毕业时间')

    class Meta:
        model = Member
        exclude = []
