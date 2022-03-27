from django.shortcuts import render
from django.views import View

from utils.mixins import LoginRequired


class FakateView(LoginRequired, View):

    def get(self, request):
        context = {
        }
        return render(request, "fakate/fakate.html", context)


class FakateIntents(LoginRequired, View):

    pass


class FakateIntentLabels(LoginRequired, View):

    pass

