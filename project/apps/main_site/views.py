from annoying.decorators import render_to
from posts.views import get_author_from_domain, blog


def home(request):
    try:
        author = get_author_from_domain(request)
        if not request.user.is_authenticated() or author != request.user.get_profile():
            return blog(request)
        else:
            is_author = True
    except:
        # import traceback; traceback.print_exc();
        pass
    return site_home(request, locals())

@render_to("main_site/home.html")
def site_home(request, context):
    return context

@render_to("main_site/ping.html")
def ping(request):
    return locals()

@render_to("main_site/manifesto.html")
def manifesto(request):
    return locals()


@render_to("main_site/faq.html")
def faq(request):
    return locals()


@render_to("main_site/terms.html")
def terms(request):
    return locals()


@render_to("main_site/about.html")
def about(request):
    return locals()
