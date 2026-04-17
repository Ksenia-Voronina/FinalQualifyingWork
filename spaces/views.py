from django.views.generic import ListView, DetailView
from .models import Space


class SpaceListView(ListView):
    """Список всех пространств"""
    model = Space
    template_name = 'spaces/space_list.html'
    context_object_name = 'spaces'
    paginate_by = 12

    def get_queryset(self):
        """Только доступные для бронирования пространства"""
        return Space.objects.filter(is_available=True)


class SpaceDetailView(DetailView):
    """Детальная страница пространства"""
    model = Space
    template_name = 'spaces/space_detail.html'
    context_object_name = 'space'