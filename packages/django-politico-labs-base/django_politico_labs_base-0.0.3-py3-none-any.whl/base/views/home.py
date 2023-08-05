from django.views.generic import TemplateView
from base.models import HomepageLink
from base.serializers import HomepageLinkSerializer
from base.utils.auth import secure


@secure
class Home(TemplateView):
    template_name = "base/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        links = HomepageLink.objects.all()
        context["links"] = HomepageLinkSerializer(links, many=True).data
        return context
