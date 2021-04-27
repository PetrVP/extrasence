from django.views import generic
from .forms import NumForm
from random import randint


# Создаем класс экстрасенса
class Extrasence:
    def __init__(self, request, name):  # Подгружаем данные из куки
        self.name = name
        if f'{name}_score' in request.session:
            self.score = request.session[f'{name}_score']
        else:
            self.score = 0
        if f'{name}_numbers' in request.session:
            self.numbers = request.session[f'{name}_numbers']
        else:
            self.numbers = []

        self.answer = 0
        self.request = request

    def exta_answer(self):  # Формируем ответ экстрасеса
        self.answer = randint(10, 99)
        self.numbers.append(self.answer)

    def validate(self, number):  # Проверяем ответ экстрасеса и устанавливаем новый счет
        self.answer = self.numbers[len(self.numbers) - 1]
        if self.answer == number:
            self.score += 1

        else:
            self.score -= 1

    def __del__(self):  # Записываем данные в куки
        self.request.session[f'{self.name}_score'] = self.score
        self.request.session[f'{self.name}_numbers'] = self.numbers

# Создаем класс игрока
class Player:
    def __init__(self, request):  # Подгружаем данные из куки
        if 'all_numbers' in request.session:
            self.all_numbers = request.session['all_numbers']
        else:
            self.all_numbers = []
        self.request = request

    def __del__(self):
        self.request.session['all_numbers'] = self.all_numbers


class Index(generic.TemplateView, generic.CreateView):
    template_name = 'play/play.html'

    def post(self, request, *args, **kwargs):
        vasily = Extrasence(request, 'vasily')
        petr = Extrasence(request, 'petr')
        player = Player(request)
        form = NumForm(request.POST)

        if form.is_valid():
            number = form.cleaned_data['number']  # находим число из формы
            player.all_numbers.append(number)
            vasily.validate(number)  # Проверка ответов экстрасенксов
            petr.validate(number)

        context = {'form': form, 'vasily': vasily, 'petr': petr, 'player': player}

        vasily.__del__()
        petr.__del__()
        player.__del__()
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        request.session.set_expiry(0)  # задаем режим хранения данных в куки до закрытия браузера

        vasily = Extrasence(request, 'vasily')
        petr = Extrasence(request, 'petr')
        player = Player(request)

        context = {'vasily': vasily, 'petr': petr, 'player': player}

        vasily.__del__()
        petr.__del__()
        player.__del__()
        return self.render_to_response(context)


class Answer(generic.CreateView):
    template_name = 'play/answer.html'

    def post(self, request, *args, **kwargs):
        vasily = Extrasence(request, 'vasily')
        petr = Extrasence(request, 'petr')
        player = Player(request)
        form = NumForm()
        vasily.exta_answer()
        petr.exta_answer()

        context = {'form': form, 'vasily': vasily, 'petr': petr, 'player': player}

        vasily.__del__()
        petr.__del__()
        player.__del__()
        return self.render_to_response(context)
