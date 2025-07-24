from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from exp_tracker import models
from .models import Accounts, Expense
from .forms import ExpenseForm
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils.safestring import mark_safe
from django.db.models import Sum,Count,F
import plotly.express as px
from plotly.graph_objs import *

# Create your views here.

def home(request):
    # Debug information for static files
    from django.conf import settings
    print("Static files settings:")
    print(f"STATIC_URL: {settings.STATIC_URL}")
    print(f"STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"STATIC_ROOT: {settings.STATIC_ROOT if hasattr(settings, 'STATIC_ROOT') else 'Not set'}")
    return render(request, 'home/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                # Save the user
                user = form.save(commit=True)
                # Create an account for the user
                Accounts.objects.create(user=user, name=f"{user.username}'s Account")
                # Log the user in
                login(request, user)
                return redirect('home')
            except Exception as e:
                print(f"Error during registration: {e}")
                form.add_error(None, "An error occurred during registration. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
    

def generate_graph(data):
    fig=px.bar(data,x='months',y='expenses',title='Monthly Expenses')
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='rgba(0,0,0,1)',
    )
    fig.update_traces(marker_color='#008c41')

    graph_json =fig.to_json()
    return graph_json

    
class ExpenseListView(FormView):
    template_name='exp_tracker/expenses_list.html'
    form_class = ExpenseForm
    success_url = '/'


    def form_valid(self,form):
        account, _ = Accounts.objects.get_or_create(user=self.request.user)
        expense = Expense(
            name=form.cleaned_data['name'],
            amount=form.cleaned_data['amount'],
            date=form.cleaned_data['date'],
            long_term=form.cleaned_data['long_term'],
            interest_rate=form.cleaned_data['interest_rate'],
            end_date=form.cleaned_data['end_date'],
            user=self.request.user
        )

        expense.save()
        account.liability_list.add(expense)
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        accounts = Accounts.objects.filter(user=user)

        expense_data_graph = {}
        expense_data = {}

        for account in accounts:
            expenses = account.liability_list.all()
            for expense in expenses:
                year_month = expense.date.strftime('%Y-%m')
                if year_month not in expense_data:
                    expense_data[year_month] = []
                    expense_data_graph[year_month] = 0

                # Add to expense data for display
                expense_data[year_month].append({
                    'name': expense.name,
                    'amount': expense.amount,
                    'date': expense.date,
                    'end_date': expense.end_date if expense.long_term else None,
                    'long_term': expense.long_term
                })

                # Add to graph data
                if expense.long_term and expense.monthly_expenses:
                    current_date = expense.date
                    while current_date <= expense.end_date:
                        year_month = current_date.strftime('%Y-%m')
                        if year_month not in expense_data_graph:
                            expense_data_graph[year_month] = 0
                        expense_data_graph[year_month] += expense.monthly_expenses
                        current_date = current_date + relativedelta(months=1)
                else:
                    expense_data_graph[year_month] += expense.amount

        # Create aggregated data for the graph
        aggregated_data = [
            {'year_month': key, 'expenses': value} 
            for key, value in sorted(expense_data_graph.items())
        ]

        # Prepare data for the graph
        if aggregated_data:
            graph_data = {
                'months': [item['year_month'] for item in aggregated_data],
                'expenses': [item['expenses'] for item in aggregated_data]
            }
            import pandas as pd
            df = pd.DataFrame(graph_data)
            context['graph_data'] = mark_safe(generate_graph(df))
        else:
            context['graph_data'] = None

        context['expense_data'] = expense_data
        return context


