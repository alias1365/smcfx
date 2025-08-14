from smcfx_common.viewParent import smcfxTemplateView
from web_project import TemplateLayout, TemplateHelper


class home_view(smcfxTemplateView):
    template_name = 'smcfx_anonymous/home.html'

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout": "front",
                "layout_path": TemplateHelper.set_layout("layout_front.html", context),
                "active_url": self.request.path,  # Get the current url path (active URL) from request
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        return context
