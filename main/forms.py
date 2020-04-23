from django import forms

class ApprovalForm(forms.Form):
    firstname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter Firstname'}))
    lastname = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Enter Lastname'}))
    ApplicantIncome = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Monthly Gross Income'}))
    CoapplicantIncome = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Enter Co-Applicant Monthly Gross Income'}))
    LoanAmount = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Requested Loan Amount in thousands '}))
    Loan_Amount_Term = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Loan Term in Months'}))
    Credit_History = forms.TypedChoiceField(choices=[(0, 0),(1, 1)],coerce = float)
    Dependents = forms.ChoiceField(choices=[('0', '0'),('1', '1'),('2','2'),('3+','3+')])
    Gender = forms.ChoiceField(choices=[('Male', 'Male'),('Female', 'Female')])
    Married = forms.ChoiceField(choices=[('Yes', 'Yes'),('No', 'No')])
    Education = forms.ChoiceField(choices=[('Graduate', 'Graduate'),('Not Graduate', 'Not Graduate')])
    Self_Employed = forms.ChoiceField(choices=[('Yes', 'Yes'),('No', 'No')])
    Property_Area = forms.ChoiceField(choices=[('Rural', 'Rural'),('Semiurban', 'Semiurban'),('Urban', 'Urban')])