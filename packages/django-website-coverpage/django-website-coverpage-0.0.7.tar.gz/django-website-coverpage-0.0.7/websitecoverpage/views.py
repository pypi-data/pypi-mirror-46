from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .forms import CoverPageViewForm


class CoverPageView(TemplateView):
    def get_template_names(self):
        config = getattr(settings, 'WEBSITE_COVERPAGE', {})
        return [config.get('template', 'coverpage/coverpage.html')]

    def post(self, request):
        form = CoverPageViewForm(request.POST)
        if form.is_valid():
            # get config
            config = getattr(settings, 'WEBSITE_COVERPAGE', {})
            cookiename = config.get('cookiename', 'coverpage')

            # set cookie and redirect
            r = form.cleaned_data['redirect']
            if len(r) == 0:
                r = request.COOKIES.get('%s_referrer' % cookiename, '/')
            response = redirect(r)
            response.delete_cookie('%s_referrer' % cookiename)
            response.set_cookie(cookiename, 1)
            return response

        # fallback
        return self.get(request)
