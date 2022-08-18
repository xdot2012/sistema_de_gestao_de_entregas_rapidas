from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        return render(request, "templates/home.html")


def vue_serve(request):
    return render(request, 'templates/vue.html')