from django.forms import ModelForm
from .models import BotTrainingData


class BotTrainingDataForm(ModelForm):

    class Meta:
        model = BotTrainingData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['botname'].widget.attrs.update({'class': 'form-control p-4'})
        self.fields['labels'].widget.attrs.update({'class': 'form-control jsoneditor jsoneditor'})
        self.fields['intents'].widget.attrs.update({'class': 'form-control jsoneditor jsoneditor'})
