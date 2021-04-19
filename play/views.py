from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NumForm
from random import randint

# Создаем класс экстрасенса
class Extrasence:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.numbers = []
        self.answer = 0


def index(request):
    #  задаем режим хранения данных в куки до закрытия браузера
    request.session.set_expiry(0)
    # определяем два экстрасенса
    vasily = Extrasence('vasily')
    petr = Extrasence('petr')
    # Обновляем информацию из куки
    if 'vasily_score' in request.session:
        vasily.score = request.session['vasily_score']

    if 'petr_score' in request.session:
        petr.score = request.session['petr_score']

    if 'vasily_numbers' in request.session:
        vasily.numbers = request.session['vasily_numbers']

    if 'petr_numbers' in request.session:
        petr.numbers = request.session['petr_numbers']

    if 'all_numbers' in request.session:
        all_numbers = request.session['all_numbers']
    else:
        all_numbers = []
    # создаем страницу
    return render(request, 'play/play.html',
                  {'all_numbers': all_numbers, 'vasily': vasily, 'petr': petr})


def test(request):
    # повторяем инициализацию экстрасенсов
    vasily = Extrasence('vasily')
    petr = Extrasence('petr')
    # Обновляем данные из куки
    if 'vasily_score' in request.session:
        vasily.score = request.session['vasily_score']

    if 'petr_score' in request.session:
        petr.score = request.session['petr_score']

    if 'answer_vasily' in request.session:
        vasily.answer = request.session['answer_vasily']

    if 'answer_petr' in request.session:
        petr.answer = request.session['answer_petr']

    if 'all_numbers' in request.session:
        all_numbers = request.session['all_numbers']
    else:
        all_numbers = []

    if 'vasily_numbers' in request.session:
        vasily.numbers = request.session['vasily_numbers']

    if 'petr_numbers' in request.session:
        petr.numbers = request.session['petr_numbers']
    # обрабатываем действие на нажаьтие кнопки
    if request.method == 'POST':
        form = NumForm(request.POST)  # подкрепляем форму
        if form.is_valid():
            number = form.cleaned_data['number']  # находим число из формы
            all_numbers.append(number)
            # заносим данные в куки
            request.session['all_numbers'] = all_numbers
            # Проверка ответов экстрасенксов
            if vasily.answer == number:
                vasily.score += 1
                vasily.numbers.append(number)
            else:
                vasily.score -= 1

            if petr.answer == number:
                petr.score += 1
                petr.numbers.append(number)
            else:
                petr.score -= 1
            # добавляем данные в куки
            request.session['vasily_score'] = vasily.score
            request.session['petr_score'] = petr.score
            request.session['vasily_numbers'] = vasily.numbers
            request.session['petr_numbers'] = petr.numbers
            # редирект на главную страницу
            return HttpResponseRedirect('/play/')

    else:
        return HttpResponseRedirect('/play/answer/')


def answer(request):
    # повторно инициализируем экстрасенсов
    vasily = Extrasence('vasily')
    petr = Extrasence('petr')
    # придумываем рандомный ответ
    vasily.answer = randint(10, 99)
    petr.answer = randint(10, 99)
    # вносим данные в куки
    request.session['answer_vasily'] = vasily.answer
    request.session['answer_petr'] = petr.answer
    # обновляем данные из куки
    if 'vasily_score' in request.session:
        vasily.score = request.session['vasily_score']

    if 'petr_score' in request.session:
        petr.score = request.session['petr_score']

    if 'all_numbers' in request.session:
        all_numbers = request.session['all_numbers']
    else:
        all_numbers = []

    if 'vasily_numbers' in request.session:
        vasily.numbers = request.session['vasily_numbers']

    if 'petr_numbers' in request.session:
        petr.numbers = request.session['petr_numbers']

    form = NumForm()
    # создаем страницу
    return render(request, 'play/answer.html',
                  {'form': form, 'all_numbers': all_numbers, 'vasily': vasily, 'petr': petr})
