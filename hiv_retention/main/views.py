from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render, redirect
import pandas as pd
from .forms import AnalysisForm ,CommentsForm , PredictionsForm
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
plt.ioff()
from  .models import comments

#LOADING DATA

data = comments.objects.all()
df = pd.read_csv('dataset/cleanData.csv')
df_predict =pd.read_csv('dataset/predicted_data.csv')
df_predict2 =pd.read_csv('dataset/predicted_viral.csv')
df_evaluation =pd.read_csv('dataset/model_performance.csv')
#OBJECTIVE 1  : To develop a system that provide analytics and visualization features 
#historical data for people living with HIV/AIDS
def Analysis(request):
    print('in get request')
    commentform = CommentsForm()
    if request.method == 'POST':
        print('from post request')
        form = AnalysisForm(request.POST)
        if form.is_valid():
            print('form valid')
            variable = form.cleaned_data.get('variables')
            selection = form.cleaned_data.get('type')
            tool = form.cleaned_data.get('analysis')
            df_selection = df[selection]
            df_variable = df[variable]
            if tool == 'bar':
                #bar graph
                plt.figure(figsize=(8, 5))  
                plt.bar(df_variable, df_selection)
                plt.xlabel(variable)
                plt.ylabel(selection)
                title = f'{variable} versus {selection}'
                plt.title(title)
                plt.xticks(rotation=45)  
            elif tool == 'line':
                  # Line Graph
                plt.figure(figsize=(8, 5))
                plt.plot(df_variable, df_selection)  
                plt.xlabel(variable)
                plt.ylabel(selection)
                title = f'{variable} versus {selection}'
                plt.title(title)
                plt.xticks(rotation=45)
            elif tool == 'pie':
                # Pie Chart 
                plt.figure(figsize=(8, 5))
                plt.pie(df_variable.value_counts(), labels= df_variable.unique(), autopct="%1.1f%%",startangle=90) 
                plt.axis('equal') 
                plt.title(f"{selection} Distribution")
            else:
                print('No tool selected')    
            plt.tight_layout()
            plt.savefig('static/pics/analysis_new.png')
            plt.close()
        else:
            print(form.errors)
    else:
        form = AnalysisForm()
   
    content = {
       'form':form,
       'commentform':commentform
    }

    return render(request, 'analysis.html', content)




# OBJECTIVE 2 To build a system that offers allows only health practitioner to analyses
# data (user validation and authentication)
def main(request):
    print('1')
    if request.method == 'POST':
        print('2')
        username = request.POST['username']
        password = request.POST['password']
        User = authenticate(request , username = username , password = password)
        if User is not None:
            print('3')
            login(request, User)
           
            return redirect('dashboard') 
        else:
            print('6')
            messages.warning(request, 'Invalid Username and  Paasword')
            return redirect('sign_in')
                      
      
    return render(request , 'index.html')

def Signout(request):
    logout(request)
    messages.success(request, 'Log Out successfully')
    return redirect('sign_in')

def Dashboard(request):
    content ={}
    content = {
      
   
    }  
    return render(request , 'dashboard.html',content)

#OBJECTIVE 3 AND 5 To build a machine learning model that utilizes historical data to predict viral load suppresion
#To build a system that utilizes machine learning to predict people who are likely to disengagement in HIV treatment
# and care.


def EvaluationMetric(request):
    accuracy = df_evaluation['Accuracy'].values[0],
    classification_report = df_evaluation['Classification Report'][0],
    auc_roc_score = df_evaluation['ROC AUC Score'].values[0]
    print(classification_report)
    lines = classification_report[0].split('\n')
    class_0_precision, class_0_recall, class_0_f1, class_0_support = map(float, lines[2].split()[1:])
    class_1_precision, class_1_recall, class_1_f1, class_1_support = map(float, lines[3].split()[1:])
    # accuracy, macro_avg, weighted_avg = map(float, lines[5].split()[1:])
    content ={}
    content = {
    'accuracy': accuracy, 
    'precision': class_0_precision, 
    'recall':class_0_recall,
    'f1':class_0_f1,
    'support':class_0_support,
    'auc_roc_score': auc_roc_score,
    'precision1': class_1_precision, 
    'recall1':class_1_recall,
    'f11':class_1_f1,
    'support1':class_1_support,
    'auc_roc_score': auc_roc_score
        }  
    return render(request , 'modelEvaluation.html',content)

def Predictions(request):
    table = False
   
    html_table = df_predict[['Age','MaritalStatus','Occupation','AIDS education','TimeTaken_Days','ArvAdherenceLatestLevel','Sex','WeightChange','Cd4AtStart','ViralLoad','age_group']].to_html(index=False, border=1, classes='table table-striped')
    
    print('in get request')
    commentform = CommentsForm()
    if request.method == 'POST':
        print('from post request')
        form = PredictionsForm(request.POST)
        if form.is_valid():
            print('form valid')
            variable = form.cleaned_data.get('variables')
            selection = form.cleaned_data.get('type')
            tool = form.cleaned_data.get('analysis')
            if selection == 'viral':
                viral_load=df_predict2[(df_predict2['ViralLoadSuppressed'] == 1) &  (df_predict2['Predicted_ViralLoadSuppressed'] == 1) ]
                df_selection = 'Viral Load Suppression'
                df_variable = viral_load[variable]
                value_counts = viral_load[variable].value_counts().sort_values(ascending=False)
                labels=value_counts.index
            elif selection == 'retention':
                likely_to_disengage =df_predict[(df_predict['Disengaged'] == 1) &  (df_predict['Predicted_Disengaged'] == 1)]
                df_selection = 'Retention or Disengaged'
                df_variable = likely_to_disengage[variable]
                value_counts = likely_to_disengage[variable].value_counts().sort_values(ascending=False)
                labels=value_counts.index
               
            if tool == 'bar':
                plt.figure(figsize=(8, 5))  
                plt.bar(df_variable.value_counts().index, df_variable.value_counts().values)
                plt.xlabel(variable)
                plt.ylabel('Frequency')
                title = f"{variable} and Probability to {df_selection}"
                plt.title(title)
                plt.xticks(rotation=45) 
                plt.xticks(rotation=45)  
            elif tool == 'table':
                html_table = likely_to_disengage[[variable,'TimeTaken_Days','ArvAdherenceLatestLevel','Sex','WeightChange','Cd4AtStart','ViralLoad','age_group']].to_html(index=False, border=1, classes='table table-striped')
                lines = html_table.splitlines()[1:]
                table = True
            elif tool == 'pie':
                plt.figure(figsize=(8, 5))
                plt.pie(value_counts.values, labels=value_counts.index, autopct="%1.1f%%",startangle=35)
                plt.title(f"{variable} and Probability to {df_selection}")
                plt.axis('equal')
                
                
            else:
                print('No tool selected')    
            plt.tight_layout()
            plt.savefig('static/pics/predict_new.png')
            plt.close()
        else:
            print(form.errors)
    else:
        table = 4
        form = PredictionsForm()
        
        
                
    content = {
       'form':form,
       'commentform':commentform,
       'tables':html_table,
       'table': table
    }

    return render(request, 'predictions.html', content)

#OBJECTIVE 5To build a system that allows health practitioner to add comments on analyzed data and in decision making
def comments(request):
    if request.method == 'POST':
        form = CommentsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            comment = form.save(commit=False)
            comment.done_by = request.user
            comment.save()
            mesage= f'Comment added succesfully'
            messages.success(request,mesage)
            return redirect('View_Comment')   
        else:
            messages.warning(request, form.errors)
            return redirect('View_Comment')   
        
def viewComments(request):
   
    content ={}
    content = {
      'comments': data
   
    }  
    return render(request , 'comments.html',content)