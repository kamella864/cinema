import time

from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from datetime import datetime
import numpy as np
from math import sqrt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.metrics import mean_squared_error
from .forms import *
from .models import *

User = get_user_model()


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class RegistrationUser(CreateView):
    form_class = UserRegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):
    if User.objects.filter(id=request.user.pk):
        age = 18
        birthdate = User.objects.filter(id=request.user.pk).values('birth_date')[0]['birth_date']
        if birthdate:
            today = datetime.today()
            age = today.year - birthdate.year
            if today.month < birthdate.month or (today.month == birthdate.month and today.day < birthdate.day):
                age -= 1
        if History.objects.filter(history_login_user_id=request.user.pk):
            cinema = show_cinemas(request.user.pk, age)
            time.sleep(20)
        else:
            cinema = [item for item in Cinema.objects.all() if item.limit <= age]
    if request.method == 'POST':
        if request.POST.get('action_1'):
            return redirect(request.POST.get('action_1'))
        if request.POST.get('action_2'):
            obj = Cinema.objects.get(id=request.POST.get('action_2'))
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    date=datetime.now())
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id,
                                       date=datetime.now())
            return redirect(obj.movie)
        if request.POST.get('action_3'):
            obj = Cinema.objects.get(id=request.POST.get('action_3'))
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    is_favorite=True)
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id,
                                       is_favorite=True)
        if request.POST.get('action_4'):
            obj = Cinema.objects.get(id=request.POST.get('action_4')[:-1])
            rait = request.POST.get('action_4')[-1]
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    raiting=float(rait))
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id, raiting=rait)
    return render(request, 'main/home.html', {'cinema': cinema})


@login_required
def favorites(request):
    favorites = History.objects.filter(history_login_user=request.user.pk, is_favorite=True)
    if request.method == 'POST':
        if request.POST.get('action_1'):
            return redirect(request.POST.get('action_1'))
        if request.POST.get('action_2'):
            obj = Cinema.objects.get(id=request.POST.get('action_2'))
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    date=datetime.now())
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id,
                                       date=datetime.now())
            return redirect(obj.movie)
        if request.POST.get('action_3'):
            obj = Cinema.objects.get(id=request.POST.get('action_3'))
            History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                is_favorite=False)
        if request.POST.get('action_4'):
            obj = Cinema.objects.get(id=request.POST.get('action_4')[:-1])
            rait = request.POST.get('action_4')[-1]
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    raiting=float(rait))
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id, raiting=rait)
    return render(request, 'main/favorites.html', {'favorites': favorites})


@login_required
def history(request):
    cinema = [item for item in History.objects.filter(history_login_user=request.user.pk) if item.date]
    if request.method == 'POST':
        if request.POST.get('action_1'):
            return redirect(request.POST.get('action_1'))
        if request.POST.get('action_2'):
            obj = Cinema.objects.get(id=request.POST.get('action_2'))
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    date=datetime.now())
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id,
                                       date=datetime.now())
            return redirect(obj.movie)
        if request.POST.get('action_3'):
            obj = Cinema.objects.get(id=request.POST.get('action_3'))
            History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(date=None)
            cinema = [item for item in History.objects.filter(history_login_user=request.user.pk) if item.date]
        if request.POST.get('action_4'):
            obj = Cinema.objects.get(id=request.POST.get('action_4')[:-1])
            rait = request.POST.get('action_4')[-1]
            if History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id):
                History.objects.filter(history_login_user_id=request.user.pk, history_cinema_id=obj.id).update(
                    raiting=float(rait))
            else:
                History.objects.create(history_login_user_id=request.user.pk, history_cinema_id=obj.id, raiting=rait)
    return render(request, 'main/history.html', {'cinema': cinema})


def show_cinemas(id, age):
    data = []
    for item in History.objects.all():
        data.append([item.history_login_user.id, item.history_cinema.id, item.raiting])

    df = pd.DataFrame(data, columns=['userId', 'movieId', 'rating'])
    n_users = df['userId'].unique().shape[0] # количество уникальных значений в столбце «userId»
    n_items = df['movieId'].unique().shape[0]
    input_list = df['movieId'].unique()

# чтобы можно было удобно работать дальше, необходимо отмасштабировать
# значения в колонке movieId  в диапазоне от 1 до количества фильмов
    def scale_movie_id(input_id):
        return np.where(input_list == input_id)[0][0] + 1

    df['movieId'] = df['movieId'].apply(scale_movie_id)

# делим данные на тренировочный и тестовый наборы
    train_data, test_data = train_test_split(df, test_size=0.20)

    train_data_matrix = np.zeros((n_users, n_items))
    for line in train_data.itertuples():
        train_data_matrix[line[1] - 1, line[2] - 1] = line[3]
        #print(train_data_matrix.shape)

    test_data_matrix = np.zeros((n_users, n_items))
    for line in test_data.itertuples():
        test_data_matrix[line[1] - 1, line[2] - 1] = line[3]
#После того, как мы построим данную матрицу, на её основе необходимо будет рассчитать две новые матрицы с коэффициентами сходства (похожести, близости) для пользователей и для фильмов.
#В качестве метрики близости в данной работе используется косинусное расстояние между векторами пользователей (фильмов).

# считаем косинусное расстояние для пользователей и фильмов
    user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
    item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

    def predict(ratings, similarity, type='user'):
        if type == 'user':
            mean_user_rating = ratings.mean(axis=1)
            ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
            pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array(
                [np.abs(similarity).sum(axis=1)]).T
        elif type == 'item':
            pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
        return pred

# в конце своего обучения в качестве результата она выдает user_prediction - предсказание для пользователя.
# Это будет двумерный список, где строки - это пользователи, столбцы - фильмы.
# В этом списке хранятся вещественные значения, которые показывают степень необходимости пользователю отрисовать этот фильм.
    user_prediction = predict(train_data_matrix, user_similarity, type='user')
    item_prediction = predict(train_data_matrix, item_similarity, type='item')

    def rmse(prediction: object, ground_truth: object) -> object:
        prediction = prediction[ground_truth.nonzero()].flatten()
        ground_truth = ground_truth[ground_truth.nonzero()].flatten()
        return sqrt(mean_squared_error(prediction, ground_truth))

    print('User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))
    print('Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix)))
# user_based - оценка предсказания, по которой смотрим, делать вывод фильма пользователю или нет.
    user_based = rmse(user_prediction, test_data_matrix)
    item_based = rmse(item_prediction, test_data_matrix)

    set_cinemas = set()
    for item in History.objects.filter(history_login_user=id):
        set_cinemas.add(Cinema.objects.get(id=item.history_cinema.id))

# set_cinemas - множество фильмом для вывода. сначала туда заносим все фильмы, которые есть уже у пользователя в истории, чтобы их не потерять, затем смотрим результат нейронки и сравниваем метрику user_based с значениями, которые хранятся в user_prediction конкретно в той строке, которая относится к данному пользователю.
# Если значение больше или равно, то фильм добавляем в set_cinemas
    cinema_id = 0
    for value in user_prediction[id - 1]:
        if value >= user_based:
            set_cinemas.add(Cinema.objects.get(id=cinema_id))
        time.sleep(20)
        cinema_id += 1
#делаем фильтрацию по возрасту и отправляем готовый результат на вывод
    return [item for item in set_cinemas if item.limit <= age]
