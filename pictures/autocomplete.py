from dal import autocomplete

from .models import Member


class MemberAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Member.objects.none()
        qs = Member.objects.filter()

        if self.q:
            qs = Member.objects.filter(name__istartswith=self.q)
        return qs
