from base.models import HomepageLink
from rest_framework.serializers import ModelSerializer


class HomepageLinkSerializer(ModelSerializer):
    class Meta:
        model = HomepageLink
        fields = ("title", "description", "link")
