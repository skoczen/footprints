from annoying.decorators import render_to


@render_to("posts/home.html")
def home(request):
    return locals()
