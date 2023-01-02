from django.shortcuts import redirect, render
from django.contrib import messages
from stocks.forms import Stockform
from stocks.models import Stock
import requests
import json


def home(request):
    if request.method=='POST':
        ticker=request.POST['ticker']
        api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=pk_8b445b4f633944e88fed24aacf86fed9")
        api_graph_rsponse = requests.get(f"https://cloud.iexapis.com/stable/stock/{ticker}/chart/1m?chartByDay=true&range=1m&token=pk_8b445b4f633944e88fed24aacf86fed9")
        graph_data = json.loads(api_graph_rsponse.content)
        labels = []
        prices = []
        for item in graph_data:
            labels.append(item.get('date'))
            prices.append(item.get('close'))

        try:
            api=json.loads(api_request.content)
        except Exception as e:
            api="Error..."
        return render(request, 'home.html',{"api":api,'labels':labels,'prices':prices})
    else:
        return render(request, 'home.html',{"ticker":"Enter ticker symbol above..."})




def about(request):
    return render(request, 'about.html',{})

def add_stock(request):
    if request.method=='POST':
        form=Stockform(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,"Stock has been added.")
            return redirect('add_stock')
    else:
        ticker=Stock.objects.all()
        output=[]
        for ticker_item in ticker:
            api_request = requests.get(f"https://cloud.iexapis.com/stable/stock/{str(ticker_item)}/quote?token=pk_ca3c415bcea148b1a5ab1fbd680dfdb0")

            try:
                api=json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api="Error..."
        return render(request, 'add_stock.html',{'ticker':ticker,'output':output})

def delete(request,stock_id):
    item=Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has Been Deleted."))
    return redirect('delete_stock')

def delete_stock(request):
    ticker=Stock.objects.all()
    return render(request,'delete_stock.html',{ 'ticker':ticker })