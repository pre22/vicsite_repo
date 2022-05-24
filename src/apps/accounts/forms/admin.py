from .user import BaseUserCreationForm, BaseUserChangeForm


class UserAdminCreationForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        fields = BaseUserCreationForm.Meta.fields + ('is_admin', 'is_superuser')


class UserAdminChangeForm(BaseUserChangeForm):
    class Meta(BaseUserChangeForm.Meta):
        fields = BaseUserChangeForm.Meta.fields + (
            'password',
            'is_active',
            'is_admin'
        )