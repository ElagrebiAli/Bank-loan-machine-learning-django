from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from .forms import ApprovalForm
import pandas as pd
#import lightgbm as lgb
import xgboost as xgb
import joblib
import os


default_columns_path = os.path.join(settings.MODELS, 'default_columns.pkl')
model_default_columns = joblib.load(default_columns_path)

model_features_path = os.path.join(settings.MODELS,'model_features.pkl')
model_features = joblib.load(model_features_path)

categorical_features_path = os.path.join(settings.MODELS,'categorical_features.pkl')
categorical_features = joblib.load(categorical_features_path)

lgb_model_path = os.path.join(settings.MODELS,'lgb_5_fold.pkl')
lgb_model  = joblib.load(lgb_model_path)

xgb_model_path = os.path.join(settings.MODELS,'XGB_5_fold.pkl')
xgb_model  = joblib.load(xgb_model_path)


def feature_engineering(df):
    #Total income
    df['TotalIncome'] = df['ApplicantIncome']  + df['CoapplicantIncome']
    #the monthly amount to be paid
    df['monthly_amount'] = df['LoanAmount']/df['Loan_Amount_Term']
    #the income left after the monthly amount has been paid
    df['left_income'] = df['TotalIncome'] - df['monthly_amount']*1000

    return df


def one_hot_encoding(df):
   df = pd.get_dummies(df,columns=categorical_features)
   new_dict = {}
   for col in model_features:
      if col not in df.columns:
           new_dict[col] = 0
      else:
         new_dict[col] = df[col]
   df = pd.DataFrame(new_dict)
   return df

def modeling(df):
   y_lgb = lgb_model.predict(df)
   y_xgb = xgb_model.predict(xgb.DMatrix(df))
   y = .5*y_lgb + .5*y_xgb
   y=(y>0.52)*1

   return y

def submit_form(request):

    if request.method == "POST":
       form = ApprovalForm(request.POST)
       if form.is_valid():
           row = {}
           for col in model_default_columns:
              row[col] = form.cleaned_data[col]
           
           df = pd.DataFrame(row,columns=model_default_columns,index=[0])

           model_out  = modeling(one_hot_encoding(feature_engineering(df)))
           if model_out == 1:
              answer = 'Approved'
           else:
              answer = 'Rejected'
           messages.success(request,'Application Status: {}'.format(answer))
    else:
       form = ApprovalForm()
    return render(request,'main/form.html',{"form":form})
    
