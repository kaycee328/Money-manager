from typing import Any
import json
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm, model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from .forms import UserSignupForm
from django.contrib.auth.decorators import login_required
from .models import Transaction, Profile
from django.db.models import Count
from .forms import AddTransaction
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from django.contrib import messages
from django.forms.models import model_to_dict

# Rest API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# Homepage1 code
class Homepage(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        # transaction = Transaction.objects.select_related('user')          
        transaction = Transaction.objects.filter(user = self.request.user)          
        debit = 0
        credit = 0

        self.request.user.profile.balance = self.request.user.profile.income

        for item in transaction:
            if item.expense_type != 'Positive':
                debit += item.amount
            else:
                credit += item.amount

            if item.expense_type == 'Positive':
                self.request.user.profile.balance += item.amount
            else:
                self.request.user.profile.balance -= item.amount

            self.request.user.profile.save()

        context['balance'] = self.request.user.profile.balance
        context['credit'] = credit
        context['debit'] = debit
        # context['transactions'] = Transaction.objects.filter(user = self.request.user)
        return context

# -----------------------------------------------------------------------------------------------
# Homepage2
from django.db.models import Sum
class Homepage2(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch transactions for the current user
        transactions = Transaction.objects.filter(user=self.request.user)
        
        # Calculate total debit and credit using aggregation
        debit = transactions.filter(expense_type='Negative').aggregate(debit_total=Sum('amount'))['debit_total'] or 0
        credit = transactions.filter(expense_type='Positive').aggregate(credit_total=Sum('amount'))['credit_total'] or 0
        
        # Calculate balance
        balance = self.request.user.profile.income + credit - debit
        
        # Update balance in user profile
        self.request.user.profile.balance = balance
        self.request.user.profile.save()
        
        # Add balance, credit, and debit to the context
        context['balance'] = balance
        context['credit'] = credit
        context['debit'] = debit
        
        return context
    
# Homepage 3--------------------------------------------------------
from django.db.models import Sum, Case, When, F, Value, FloatField
class Homepage3(LoginRequiredMixin, TemplateView):
    template_name = 'mainapp/homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch transactions for the current user and aggregate debit and credit totals
        transactions_data = Transaction.objects.filter(user=self.request.user).aggregate(
            debit_total=Sum(Case(When(expense_type='Negative', then=F('amount')), default=Value(0), output_field=FloatField())),
            credit_total=Sum(Case(When(expense_type='Positive', then=F('amount')), default=Value(0), output_field=FloatField())),
        )
        
        # Extract debit and credit totals from the aggregated data
        debit = transactions_data['debit_total'] or 0
        credit = transactions_data['credit_total'] or 0
        
        # Calculate balance
        balance = self.request.user.profile.income + credit - debit
        
        # Update balance in user profile
        self.request.user.profile.balance = balance
        self.request.user.profile.save()
        
        # Add balance, credit, and debit to the context
        context['balance'] = balance
        context['credit'] = credit
        context['debit'] = debit
        
        return context





class TransactionDetails(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Transaction
    template_name = 'mainapp/view-transaction.html'
    context_object_name = 'transaction'

    def test_func(self) -> bool | None:
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False

class EditTransaction(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    template_name = 'mainapp/edit-transaction.html'
    context_object_name = 'transaction'
    fields = ['title', 'amount', 'expense_type' ]

    def get_success_url(self) -> str:
        return reverse_lazy('transaction-detail', kwargs={'pk': self.object.pk})
    
    def test_func(self) -> bool | None:
        transaction = self.get_object()
        if self.request.user == transaction.user:
            return True
        return False

class CreateTransaction(LoginRequiredMixin, CreateView):
    model = Transaction
    template_name = 'mainapp/add-transaction.html'
    context_object_name = 'transaction'
    fields = ['title', 'amount', 'expense_type' ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('transaction-detail', kwargs={'pk': self.object.pk})

# Transaction list 1
class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "mainapp/my-transactions.html"
    ordering = '-date'
    paginate_by = 4


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)     
        number_of_transactions = Transaction.objects.filter(user=self.request.user).count()

        # Calculate offset
        items_per_page = self.paginate_by
        page = self.request.GET.get('page', 1)
        offset = items_per_page * (int(page) - 1)

        context['offset'] = offset
        context["number_of_transactions"] = number_of_transactions
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Transaction.objects.filter(user=self.request.user).order_by('-date')
    
# TransactionList2
from django.db.models import Count

class TransactionList2(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "mainapp/my-transactions.html"
    ordering = '-date'
    paginate_by = 4

    def get_queryset(self):
        # Fetch transactions with related user objects and prefetch related profiles
        return Transaction.objects.select_related('user__profile').filter(user=self.request.user).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculate number of transactions
        number_of_transactions = self.get_queryset().count()
        
        # Calculate offset
        items_per_page = self.paginate_by
        page = self.request.GET.get('page', 1)
        offset = items_per_page * (int(page) - 1)

        context['offset'] = offset
        context["number_of_transactions"] = number_of_transactions
        return context


# ---------------------------------------- 
class DeleteTransaction(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = 'mainapp/delete-transaction.html'
    context_object_name = 'transactions'
    paginate_by = 4
    # success_url = reverse_lazy('homepage')

    # def test_func(self) -> bool | None:
    #     transaction = self.get_object()
    #     if self.request.user == transaction.user:
    #         return True
    #     return False
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)     
        number_of_transactions = Transaction.objects.filter(user=self.request.user).count()

        # Calculate offset
        items_per_page = self.paginate_by
        page = self.request.GET.get('page', 1)
        offset = items_per_page * (int(page) - 1)

        context['offset'] = offset
        context["number_of_transactions"] = number_of_transactions
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Transaction.objects.filter(user=self.request.user).order_by('-date')

# class ConfirmDeleteTransaction(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = Transaction
#     template_name = 'mainapp/delete-transaction.html'
#     context_object_name = 'transactions'
#     paginate_by = 4    

#     def test_func(self) -> bool | None:
#         transaction = self.get_object()
#         if self.request.user == transaction.user:
#             return True
#         return False





# USER LOGIN VIEW
class UserLogin(LoginView):
    template_name = 'mainapp/auth/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        return reverse_lazy('home')


# SIGNUP VIEW FOR USER TO REGISTER THEIR ACCOUNT
def register(request):
    if request.method == "POST":  
        form = UserSignupForm(request.POST)  
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for "{username}", login here!')
            return redirect('user-login')       
    else:
        form = UserSignupForm()
    return render(request, 'mainapp/auth/signup.html', {'form':form})

# LOGOUT VIEW
class LogoutUser(LogoutView):
    # template_name = 'mainapp/auth/logout.html'
    next_page = reverse_lazy('user-login')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, 'You have been logged out successfully.')
        return response

# JSON CALL
@api_view()
def jsonfile(request):
    my_model = Transaction.objects.filter(user=request.user)
    data = []
    item_data = dict()
    data.append({'Balance': request.user.profile.balance})


    if my_model:
        for item in my_model:
            # Create a dictionary for each item
            if item.expense_type == 'Negative':
                expense = 'Debit'
            else:
                expense = 'Credit'

            item_data = {
                'Title': item.title,
                'Amount': item.amount,
                'Expense_type': expense,
                'Date': str(item.date)
            }
            # Append the item's dictionary to the list
            data.append(item_data)

    mod = Transaction.objects.filter(user=request.user).first()
    my_data = model_to_dict(mod)
    print(item_data)

    # Serialize the list of dictionaries to JSON
    json_data = json.dumps(data, indent=3)

    with open('balance.txt', 'w') as f:
        f.write(str(data))
    
        
    return Response(data, status=status.HTTP_200_OK)
    # return JsonResponse(data, safe=False)


