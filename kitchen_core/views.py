from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from kitchen_core.forms import DishTypeSearchForm, DishSearchForm, DishForm, CookSearchForm, CookCreationForm, \
    CookUpdateForm
from kitchen_core.models import Cook, DishType, Dish


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_cooks = Cook.objects.count()
    num_dish_types = DishType.objects.count()
    num_dishes = Dish.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
        "num_dishes": num_dishes,
        "num_visits": num_visits + 1,
    }
    return render(request, "kitchen/index.html", context=context)


class DishTypesListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    context_object_name = "dish_types_list"
    template_name = "kitchen/dish_types_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishTypesListView, self).get_context_data(**kwargs)
        dish_type = self.request.GET.get("name_dish_type")
        context["search_field"] = DishTypeSearchForm(
            initial={"name_dish_type": dish_type}
        )
        return context

    def get_queryset(self):
        queryset = DishType.objects.all()
        form = DishTypeSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name_dish_type"]
            )
        return queryset


class DishTypesCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen_core:dish-types-list")


class DishTypesUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "kitchen/dish_type_form.html"
    success_url = reverse_lazy("kitchen_core:dish-types-list")


class DishTypesDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    success_url = reverse_lazy("kitchen_core:dish-types-list")
    template_name = "kitchen/dish_type_confirm_delete.html"


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    context_object_name = "dish_list"
    template_name = "kitchen/dish_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name_dish = self.request.GET.get("name_dish")
        context["search_field"] = DishSearchForm(
            initial={"name_dish": name_dish}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                name__icontains=form.cleaned_data["name_dish"]
            )
        return queryset


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen_core:dishes-list")


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    template_name = "kitchen/dish_detail.html"


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "kitchen/dish_form.html"
    success_url = reverse_lazy("kitchen_core:dishes-list")


class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen_core:dishes-list")


@login_required
def switch_assign_to_food(request: HttpRequest, pk):
    cook = get_user_model().objects.get(id=request.user.id)
    if Dish.objects.get(id=pk) in cook.dishes.all():
        cook.dishes.remove(pk)
    else:
        cook.dishes.add(pk)
    return HttpResponseRedirect(reverse_lazy("kitchen_core:dish-detail", kwargs={"pk": pk}))


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    template_name = "kitchen/cook_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        name_cook = self.request.GET.get("name_cook")
        context["search_field"] = CookSearchForm(
            initial={"name_cook": name_cook}
        )
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                username__icontains=form.cleaned_data["name_cook"]
            )
        return queryset


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen_core:cooks-list")


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = get_user_model().objects.all().prefetch_related("dishes__dish_type")
    template_name = "kitchen/cook_detail.html"


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    form_class = CookUpdateForm
    template_name = "kitchen/cook_form.html"
    success_url = reverse_lazy("kitchen_core:cooks-list")


class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen_core:cooks-list")