from django.shortcuts import render
import datetime
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_POST
from .models import Schedule
from .forms import UserCreateForm

# Create your views here.

User = get_user_model()

class Calendar(generic.TemplateView):
    template_name = 'booking/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        today = datetime.date.today()

        # どの日を基準にカレンダーを表示するかの処理。
        # 年月日の指定があればそれを、なければ今日からの表示。
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        if year and month and day:
            base_date = datetime.date(year=year, month=month, day=day)
        else:
            base_date = today

        # カレンダーは1週間分表示するので、基準日から1週間の日付を作成しておく
        days = [base_date + datetime.timedelta(days=day) for day in range(7)]
        start_day = days[0]
        end_day = days[-1]

        # 9時から17時まで1時間刻み、1週間分の、値がTrueなカレンダーを作る
        calendar = {}
        for hour in range(11, 20):
            row = {}
            for day in days:
                row[day] = True
            calendar[hour] = row

        # カレンダー表示する最初と最後の日時の間にある予約を取得する
        start_time = datetime.datetime.combine(start_day, datetime.time(hour=11, minute=0, second=0))
        end_time = datetime.datetime.combine(end_day, datetime.time(hour=20, minute=0, second=0))
        for schedule in Schedule.objects.exclude(Q(start__gt=end_time) | Q(end__lt=start_time)):
            local_dt = timezone.localtime(schedule.start)
            booking_date = local_dt.date()
            booking_hour = local_dt.hour
            if booking_hour in calendar and booking_date in calendar[booking_hour]:
                calendar[booking_hour][booking_date] = False

        #context['staff'] = staff
        context['calendar'] = calendar
        context['days'] = days
        context['start_day'] = start_day
        context['end_day'] = end_day
        context['before'] = days[0] - datetime.timedelta(days=7)
        context['next'] = days[-1] + datetime.timedelta(days=1)
        context['today'] = today
        context['public_holidays'] = settings.PUBLIC_HOLIDAYS
        return context

class Booking(generic.FormView):
    template_name = 'booking/user_data_input.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        #dictionary = {'year':year, 'form':form}
        return render(self.request, 'booking/user_data_input.html', {'form': form, 'year':year, 'month':month, 'day':day, 'hour':hour})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs.get('year')
        context['month'] = self.kwargs.get('month')
        context['day'] = self.kwargs.get('day')
        context['hour'] = self.kwargs.get('hour')
        return context
    

class UserDataConfirm(generic.FormView):
    """ユーザー情報の確認

    ユーザー情報入力後、「送信」を押すとこのビューが呼ばれます。(user_data_input.htmlのform action属性がこのビュー)
    データが問題なければuser_data_confirm.html(確認ページ)を、入力内容に不備があればuser_data_input.html(入力ページ)に
    フォームデータを渡します。

    """
    template_name = 'booking/user_data_confirm.html'
    #template_name = 'booking/confirm.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        return render(self.request, 'booking/user_data_confirm.html', {'form': form, 'year':year, 'month':month, 'day':day, 'hour':hour})

    def form_invalid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        return render(self.request, 'booking/user_data_input.html', {'form': form, 'year':year, 'month':month, 'day':day, 'hour':hour})

"""
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        return render(self.request, 'booking/user_data_confirm.html', {'year': 2021})
"""
    
    
    

class UserDataCreate(generic.CreateView):
    """ユーザーデータの登録ビュー。ここ以外では、CreateViewを使わないでください"""
    form_class = UserCreateForm


    def form_valid(self, form):
        #staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        
        if Schedule.objects.filter(start=start).exists():\
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule = form.save(commit=False)
            #schedule.staff = staff
            schedule.start = start
            schedule.end = end
            schedule.save()
        return render(self.request, 'booking/last.html', {'form': form, 'year':year, 'month':month, 'day':day, 'hour':hour})
        #return render('booking:calendar', year=year, month=month, day=day)
        #return redirect('booking:calendar', year=year, month=month, day=day)
    
    success_url = reverse_lazy('booking:calendar')

    def form_invalid(self, form):
        """基本的にはここに飛んでこないはずです。UserDataConfrimでバリデーションは済んでるため"""
        return render(self.request, 'booking/user_data_input.html', {'form': form})

def list(request):
    data = Schedule.objects.all()
    params = {'message':'予約一覧', 'data':data}
    return render(request, 'booking/list.html', params)

def top(request):
    return render(request, 'booking/top.html', {})

"""
class List(generic.FormView):
    #template_name = 'booking/list.html'

    def kuuya(self, form):
        return render(self.request, 'booking/list.html', {})
"""


"""
    model = Schedule
    fields = ('name', 'number',)  
    template_name = 'booking/booking.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['staff'] = get_object_or_404(Staff, pk=self.kwargs['pk'])
        print(context)
        return context

    def form_valid(self, form):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        return redirect('booking:calendar', year=year, month=month, day=day)
"""
"""
    def form_valid(self, form):
        #staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        hour = self.kwargs.get('hour')
        start = datetime.datetime(year=year, month=month, day=day, hour=hour)
        end = datetime.datetime(year=year, month=month, day=day, hour=hour + 1)
        if Schedule.objects.filter(start=start).exists():
            messages.error(self.request, 'すみません、入れ違いで予約がありました。別の日時はどうですか。')
        else:
            schedule = form.save(commit=False)
            #schedule.staff = staff
            schedule.start = start
            schedule.end = end
            schedule.save()
        return redirect('booking:calendar', year=year, month=month, day=day)
"""