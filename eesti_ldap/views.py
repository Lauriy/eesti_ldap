from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from eesti_ldap.forms import IdCheckQueryCreateForm
from eesti_ldap.models import IdCheckQuery


class IdCheckQueryCreate(CreateView):
    model = IdCheckQuery
    form_class = IdCheckQueryCreateForm
    # success_url = reverse_lazy('captcha_add')

    def get(self, request, *args, **kwargs):
        self.object = None
        ctx = self.get_context_data()
        ctx['form'] = IdCheckQueryCreateForm()

        return self.render_to_response(ctx)

    # def get_success_url(self):
    #     pass
    # """Return the URL to redirect to after processing a valid form."""
    # if self.success_url:
    #     url = self.success_url.format(**self.object.__dict__)
    # else:
    #     try:
    #         url = self.object.get_absolute_url()
    #     except AttributeError:
    #         raise ImproperlyConfigured(
    #             "No URL to redirect to.  Either provide a url or define"
    #             " a get_absolute_url method on the Model.")
    # return url

    def form_valid(self, form):
        self.object, created = IdCheckQuery.objects.get_or_create(input=form.cleaned_data['input'])

        return HttpResponseRedirect(self.get_success_url())


def my_birthday(request, year, month, day):
    print(year, month, day)
