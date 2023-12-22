from django.shortcuts import render
from django.views import View

from classes import user_util, event_util


class ClearAllFilters(View):
    def get(self, request):
        if 'filters' in request.session:
            del request.session['filters']

        current_user = user_util.User_Util.get_user(email=request.session['user'])
        all_events = event_util.Event_Util.filter_events(
            user=current_user,
            sort_type=0,
            order=0,
            by_date=0,
            interests=None)

        paginator = Paginator(all_events, 5)
        page_number = request.GET.get('page')
        events = paginator.get_page(page_number)

        return render(request, "homepage.html", {"Events": events, "user": current_user})