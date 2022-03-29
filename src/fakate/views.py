from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from utils.mixins import LoginRequired
from .models import BotTrainingData
from .forms import BotTrainingDataForm

class AllFakateView(LoginRequired, View):

    def get(self, request):
        context = {
            "TrainingData" : BotTrainingData.objects.all().order_by('-id'),
            "count": BotTrainingData.objects.all().count()
        }
        return render(request, "fakate/all_fakate.html", context)

    def post(self, request):

        name = request.POST["name"]

        new = BotTrainingData(
            botname= name
        )
        new.Labels = {}
        new.intents = {}
        new.save()

        return redirect('fakate')


class FakateView(LoginRequired, View):

    def get(self, request, id):
        t_Data = BotTrainingData.objects.filter(id=id).first()

        context = {
            "b_data":t_Data,
        }

        return render(request, 'fakate/fakate.html', context)

    def post(self, request):

        data = request.POST

        form = BotTrainingDataForm(data)
        
        if form.is_valid():
            form.save()
            messages.info(request, "Saved successfully")
        else:
            messages.error(request, form.errors.as_text())

        return redirect('fakate-view', id=data["id"])

