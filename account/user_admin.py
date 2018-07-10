from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UserCreationForm

from account.models import User


class MyUserCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(MyUserCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(BaseUserAdmin):
    search_fields = ('username', 'email', 'name')
    form = UserChangeForm  # 编辑用户表单，使用自定义的表单
    add_form = MyUserCreateForm

    list_display = ('username', 'name', 'role', 'is_superuser')
    fieldsets = (
        ('Personal info', {'fields': ('name', 'password',
                                      'gender', 'role', 'place', 'college',
                                      'grade', 'card_id', 'nation', 'province',
                                      'email', 'telephone', 'avatar', 'birthday', 'QQ',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),

            'fields': ('username', 'name', 'password1', 'password2',
                       'gender', 'role', 'place', 'college', 'grade',
                       'card_id', 'nation', 'province', 'email',
                       'telephone', 'avatar', 'birthday',
                       'QQ',
                       )}
         ),
    )

    filter_horizontal = ()
