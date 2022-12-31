from django.shortcuts import render


def yaml_to_html(request):
    return render(
        request,
        template_name="swagger_ui.html",
    )
