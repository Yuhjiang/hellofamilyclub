from django import forms

from .models import Member


class MemberAdminForm(forms.ModelForm):
    graduated_time = forms.DateField(widget=forms.DateInput, required=False,
                                     label='毕业时间')
    color = forms.CharField(widget=forms.TextInput, required=False,
                            label='成员色')
    hometown = forms.CharField(widget=forms.TextInput, required=False,
                               label='出生地')
    nickname = forms.CharField(widget=forms.TextInput, required=False,
                               label='昵称')
    favicon = forms.URLField(widget=forms.URLInput, required=False, label='照片')

    class Meta:
        model = Member
        exclude = []
