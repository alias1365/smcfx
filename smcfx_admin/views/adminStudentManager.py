# smcfx_admin/views.py
import secrets
import string

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy

from smcfx_admin.forms import StudentCreateForm, StudentEditForm
from smcfx_common.viewParent import smcfxListView, smcfxCreateView, smcfxUpdateView, smcfxDeleteView

User = get_user_model()

def _gen_password(n=12):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(n))

class StaffOnlyMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff  # فقط ادمین/استاف
    def handle_no_permission(self):
        return redirect("login")

class ManageStudentListView(StaffOnlyMixin, smcfxListView):
    template_name = "admin/manage_student.html"
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        qs = User.objects.filter(groups__name="student").order_by("-id")
        if q:
            qs = qs.filter(
                Q(email__icontains=q) |
                Q(username__icontains=q) |
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "").strip()
        return ctx

class StudentCreateView(StaffOnlyMixin, smcfxCreateView):
    template_name = "admin/student_form.html"
    form_class = StudentCreateForm
    success_url = reverse_lazy("manage_student")

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        first_name = form.cleaned_data.get("first_name", "")
        last_name = form.cleaned_data.get("last_name", "")
        is_active = form.cleaned_data.get("is_active", True)

        # جلوگیری از ایمیل تکراری بدون دست‌زدن به مدل کاربر
        if User.objects.filter(email__iexact=email).exists():
            form.add_error("email", "این ایمیل قبلاً ثبت شده است.")
            return self.form_invalid(form)

        password = _gen_password()
        user = User.objects.create(
            username=email,      # سیاست: یوزرنیم = ایمیل
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()

        student_group, _ = Group.objects.get_or_create(name="student")
        user.groups.add(student_group)

        # نمایش یکباره پسورد
        messages.success(self.request, f"دانشجو ایجاد شد. پسورد اولیه: {password}")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mode"] = "create"
        return ctx

class StudentUpdateView(StaffOnlyMixin, smcfxUpdateView):
    template_name = "admin/student_form.html"
    form_class = StudentEditForm
    success_url = reverse_lazy("manage_student")

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = User.objects.filter(id=kwargs.get("user_id"), groups__name="student").first()
        if not self.user_obj:
            messages.error(request, "کاربر یافت نشد یا دانشجو نیست.")
            return redirect("manage_student")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        u = self.user_obj
        return {
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "is_active": u.is_active,
        }

    def form_valid(self, form):
        email = form.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exclude(id=self.user_obj.id).exists():
            form.add_error("email", "این ایمیل متعلق به کاربر دیگری است.")
            return self.form_invalid(form)

        u = self.user_obj
        u.email = email
        u.username = email  # سنکرون با سیاست ایمیل=یوزرنیم
        u.first_name = form.cleaned_data.get("first_name", "")
        u.last_name = form.cleaned_data.get("last_name", "")
        u.is_active = form.cleaned_data.get("is_active", True)
        u.save()
        messages.success(self.request, "ویرایش با موفقیت انجام شد.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["mode"] = "edit"
        ctx["user_obj"] = self.user_obj
        return ctx

class StudentDeleteView(StaffOnlyMixin, smcfxDeleteView):
    model = User
    success_url = reverse_lazy("manage_student")
    template_name = "admin/student_confirm_delete.html"
    pk_url_kwarg = "user_id"

    def get_queryset(self):
        return User.objects.filter(groups__name="student")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "دانشجو حذف شد.")
        return super().delete(request, *args, **kwargs)
