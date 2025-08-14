from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView, DetailView

from web_project import TemplateLayout


class smcfxTemplateView(TemplateView):
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return self.manp_context(context)

    def manp_context(self, context):
        return context


class smcfxDetailView(DetailView):
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        return self.manp_context(context)

    def manp_context(self, context):
        return context


class smcfxListView(ListView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return self.manp_context(context)

    def manp_context(self, context):
        return context


class smcfxUpdateView(UpdateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return self.manp_context(context)

    def manp_context(self, context):
        return context


class smcfxCreateView(CreateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return self.manp_context(context)

    def manp_context(self, context):
        return context


class smcfxDeleteView(DeleteView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return self.manp_context(context)

    def manp_context(self, context):
        return context
