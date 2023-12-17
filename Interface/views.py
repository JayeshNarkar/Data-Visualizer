from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Data
from .forms import UploadForm
import pandas as pd
from .models import Data
import pickle
from django.http import Http404
import os.path
from datetime import datetime
from io import TextIOWrapper
from django.contrib import messages

# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, 'Interface/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Interface/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Interface/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Interface/register.html")
    
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

@login_required
def index(request):
    try:
        data = get_object_or_404(Data, user=request.user, is_active=True)
    except Http404:
        data = Data.objects.get(name="Pre-made")
    file = data.file_field
    dataset_index = data.dataset_index
    label_index = data.date_index
    df = pd.read_csv(file)
    df = df.dropna(subset=[df.columns[dataset_index]])
    label_print = df.iloc[:, label_index]
    dataset_print = df.iloc[:, dataset_index]
    label_print = label_print.dropna().values.tolist()
    dataset_print = dataset_print.dropna().values
    dataset_print = [float(value.replace('€', '').replace(',', '')) if isinstance(value, str) else value for value in dataset_print]
    file_path = 'static/data_frames/dataframe.pkl'
    if os.path.exists(file_path) and data.name != "Pre-made" and Data.objects.all().count()>1:
        with open(file_path, 'rb') as file:
            df = pickle.load(file)
    else:
        data_pandas = {'Date': pd.to_datetime(label_print), 'Balance': dataset_print}
        df = pd.DataFrame(data_pandas)
        df = df.sort_values(by='Date')
        if data.name != "Pre-made":
            with open(file_path, 'wb') as file:
                pickle.dump(df, file)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    max_balance_index = df['Balance'].idxmax()
    highest_balance_date = df.loc[max_balance_index, 'Date']
    highest_balance_amount = df.loc[max_balance_index, 'Balance']
    current_year = pd.Timestamp.now().year
    current_year_data = df[pd.to_datetime(df['Date']).dt.year == current_year]
    current_year_data = current_year_data.sort_values(by='Date')
    first_balance = current_year_data['Balance'].iloc[0]
    last_balance = current_year_data['Balance'].iloc[-1]
    current_year_change = ((last_balance - first_balance) / first_balance) * 100
    first_date_balance = df['Balance'].iloc[0]
    all_time_change = ((last_balance - first_date_balance) / first_date_balance) * 100
    return render(request,"Visualizer/index.html",{
        "label":label_print,
        "dataset":dataset_print,
        "console_log":df,
        "name":data.name,
        "highest_balance_date":highest_balance_date,
        "highest_balance_amount":highest_balance_amount,
        "current_year_change": round(current_year_change,2),
        "all_time_change": round(all_time_change,2),
        "last_balance":last_balance,
        "first_date_balance":first_date_balance,
        "first_balance":first_balance
    })

@login_required
def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            label_upload = (int(form.cleaned_data['label_upload'])-1)
            data_upload = (int(form.cleaned_data['data_upload'])-1)
            dataset_name = form.cleaned_data['dataset_name']
            data_instance = Data(file_field=uploaded_file, user=request.user, name=dataset_name,date_index=label_upload,dataset_index=data_upload, is_active= True )
            data_instance.save()
            message = 'File uploaded and saved to Data model!'    
    else:
        form = UploadForm()

    message = "Your files:"
    data = Data.objects.filter(user=request.user)
    files = [data_ for data_ in data]

    if not files:
        message = "No file uploaded yet."

    return render(request, "Visualizer/upload.html", {
        "form": form,
        "message": message,
        "files": files
    })

def layout(request,user_id):
    user = User.objects.get(id=user_id)
    if user:
        return JsonResponse(user.serialize(), safe=False)
    return JsonResponse({"error":"User not found"})

def DeleteFileView(request,file_id):
    try:
        file = get_object_or_404(Data, id=file_id)
        file.file_field.delete()
        file.delete()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)})
