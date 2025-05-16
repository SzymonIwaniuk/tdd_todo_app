from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from lists.forms import ExistingListItemForm, ItemForm
from lists.models import List
from django.contrib.auth import get_user_model


User = get_user_model()


def home_page(request: HttpRequest) -> HttpResponse:
    return render(request, "home.html", {"form": ItemForm()})


def view_list(request: HttpRequest, list_id: int) -> HttpResponse:
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request: HttpRequest) -> HttpResponse:
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        nulist.owner = request.user
        nulist.save()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})


def my_lists(request: HttpRequest, email: str) -> HttpResponse:
    owner = User.objects.get(email=email)
    return render(request, "my_lists.html", {"owner": owner})
