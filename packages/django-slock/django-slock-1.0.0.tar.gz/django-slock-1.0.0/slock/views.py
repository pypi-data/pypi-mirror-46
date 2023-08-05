from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from django.conf import settings
from django.http import  HttpResponseNotAllowed
from traceback import print_exc

class RenderExc(Exception):
    def __init__(self, template, context, status=200):
        self.template = template
        self.context  = context
        self.status   = status

class AuthenticatedView(View):
    """
    Should be overriden sometimes.
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            self.user_id = request.session['user_id']
        except Exception:
            return self.error(request, *args, **kwargs)

        self.on_auth(request, *args, **kwargs)
        return self.delegate(request, *args, **kwargs)

    def on_auth(self, request, *args, **kwargs):
        """
        Called when user is authenticated. Used for saving
        user instance in the view to avoid prolixity.
        """
        pass

    def delegate(self, request, *args, **kwargs):
        """
        Django doesnt let customize error page
        when not in debug mode, it may be the case
        of it being interesting to handle differently
        500 from each one of the views. 
        """

        try:
            return super(AuthenticatedView, 
                self).dispatch(request, *args, **kwargs)
        except Exception as excpt:
            return self.on_exception(request, excpt)

    def on_exception(self, request, exception):
        print_exc()

        if isinstance(exception, (RenderExc,)):
            return render(request, exception.template, 
                exception.context, status=exception.status)
        return render(request, settings.DEFAULT_ERR, {}, status=500)

    def error(self, request, *args, **kwargs):
        return render(request, settings.AUTH_ERR, {}, status=401)

class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            del request.session['user_id']
        except KeyError:
            pass
        return redirect(settings.LOGOUT_VIEW)

class LoginView(AuthenticatedView):
    def dispatch(self, request, *args, **kwargs):
        try:
            request.session['user_id']
        except Exception:
            return self.delegate(request, *args, **kwargs)
        else:
            return redirect(settings.LOGGED_VIEW)

