from django.contrib.auth.models import Group


class Role(Group):
    class Meta:
        proxy = True

    def users(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return User.objects.filter(groups__in=[self])