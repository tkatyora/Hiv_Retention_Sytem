from django import forms
from django.forms import ModelForm 
from  .models import comments




class AnalysisForm(forms.Form):
    selection = [('TimeTaken_Days','Time'),
                 ('ArvAdherenceLatestLevel','Adherence Level')]
    variable = [('Age','Age'),
                 ('Sex','Sex'),
                 ('Occupation','Occupation')]
    tool = [('bar','Bar Graph'),
                 ('pie','Pie Chart'),
                 ('line','Line Graph')]
    type =forms.ChoiceField(choices=selection, 
                             label='Analysis Aganist',
                            required=True)
    variables =forms.ChoiceField(choices=variable, 
                            label='Select Variable to analysis',
                            required=True)
    analysis =forms.ChoiceField(choices=tool, 
                            label='Select Analysis Tool',
                            required=True)
    


class PredictionsForm(forms.Form):
    selection = [('viral','Viral Load Suppression'),
                 ('retention','Retention or Disengaged')]
    variable = [('AIDS education','AIDS Education'),
                ('Age','Age'),
                 ('Sex','Sex'),
                 ('Occupation','Occupation'),
               
                 ]
    tool = [('bar','Bar Graph'),
                 ('pie','Pie Chart'),
                 ('table','Table')]
    type =forms.ChoiceField(choices=selection, 
                             label='Select Retention or Viral Load',
                            required=True)
    variables =forms.ChoiceField(choices=variable, 
                            label='Select Diomegraphy',
                            required=True)
    analysis =forms.ChoiceField(choices=tool, 
                            label='Select Analysis Tool',
                            required=True)
    


class CommentsForm(ModelForm):
    comment =forms.CharField(label='Write Comments', required=False,
                              widget=forms.Textarea(
                                  attrs={
                                      'rows':3,
                                      'cols':3, 
                                  }
                              ))
    
   

    class Meta: 
        model = comments
        fields =['comment','name','File']
        
   
 
   

    