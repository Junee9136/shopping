from otree.api import *
import math
import random
import csv
c = Currency

doc = """
Your app description
"""

def read_csv():
    import csv
    f = open(__name__ + '/shopping.csv', encoding='utf-8-sig')
    rows = list(csv.DictReader(f))
    return rows



class Constants(BaseConstants):
    name_in_url = 'risk'
    players_per_group = None
    num_rounds = 5
    factors = read_csv()
    order = ["A","B","C","D","E"]
    order2 = [1,2,3,4,5]

class Subsession(BaseSubsession):
    pass
class Group(BaseGroup):
    pass

def creating_session(subsession):
    treatments = [1, 2, 3]
    import itertools
    balanced_treats = itertools.cycle(treatments)
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.treatment = next(balanced_treats)
            p.treatment = p.participant.treatment
            round_numbers = list(range(1, Constants.num_rounds + 1))
            random.shuffle(round_numbers)
            task_rounds = dict(zip(Constants.order2, round_numbers))
            p.participant.task_rounds = round_numbers

    if subsession.round_number == 1:
        for p in subsession.get_players():
            participant = p.participant
            factors = read_csv()
            participant.task_rounds = factors
            random.shuffle(participant.task_rounds)

    for p in subsession.get_players():
        participant = p.participant
        current_round = participant.task_rounds[subsession.round_number - 1]
        p.decision = int(current_round['Round'])
        p.num_acc = int(current_round['num_acc'])
        if participant.treatment == 1:
            p.budget1 = (int(current_round['Budget1']))/4
            p.budget2 = (int(current_round['Budget2']))/4
            p.price_a = int(current_round['price_a'])
            p.price_o = int(current_round['price_o'])
            p.price_a2 = int(current_round['price_a2'])
            p.price_o2 = int(current_round['price_o2'])
        else:
            if p.decision == 1:
                p.budget1 = 36
                p.budget2 = 108
                p.price_a = 1
                p.price_o = 6
                p.price_a2 = 3
                p.price_o2 = 4
            elif p.decision == 3:
                p.budget1 = 24
                p.budget2 = 48
                p.price_a = 1
                p.price_o = 4
                p.price_a2 = 2
                p.price_o2 = 3
            else:
                p.budget1 = int(current_round['Budget1'])
                p.budget2 = int(current_round['Budget2'])
                p.price_a = int(current_round['price_a'])
                p.price_o = int(current_round['price_o'])
                p.price_a2 = int(current_round['price_a2'])
                p.price_o2 = int(current_round['price_o2'])


class Player(BasePlayer):
    num_acc = models.IntegerField()
    budget1 = models.IntegerField()
    budget2 = models.IntegerField()
    price_a = models.IntegerField()
    price_a2 = models.IntegerField()
    price_o = models.IntegerField()
    price_o2 = models.IntegerField()
    decision = models.IntegerField()
    a_choice = models.IntegerField(initial = None, label="Apples")
    a_choice2 = models.IntegerField(initial = None,label="Apples")
    o_choice = models.FloatField(initial = None,label="Oranges")
    o_choice2 = models.FloatField(initial = None,label="Oranges")
    quiz2 = models.FloatField(label="Enter your answer in the box")
    quiz3 = models.FloatField(label="Enter your answer in the box")
    quiz4 = models.IntegerField(choices=[[1, 'True'], [2, 'False']],label="")
    final = models.CurrencyField()
    round_count = models.IntegerField()
    treatment = models.IntegerField()
    click_response = models.StringField()
    survey0 = models.StringField()
    survey1 = models.StringField()
    survey2 = models.StringField()
    survey3 = models.StringField()
    survey4 = models.StringField()
    survey5 = models.StringField()
    survey6 = models.StringField()
    survey7 = models.StringField()
    survey8 = models.StringField()
    survey9 = models.StringField()
    survey10 = models.StringField()
    round_payoff = models.FloatField()
    prolific = models.StringField(label="Prolific ID")
    order_acc = models.IntegerField()
    rnd = models.IntegerField()



    def set_payoff(self):
        participant = self.participant
        self.o_choice = math.floor((self.budget1 - self.a_choice * self.price_a) / self.price_o)

        if self.num_acc == 1:
            self.o_choice2 = None
            if participant.treatment != 1:
                self.round_payoff = (1 / 10) * (math.sqrt(self.o_choice) + math.sqrt(self.a_choice)) ** 2
            else:
                self.round_payoff = (2 / 5) * (math.sqrt(self.o_choice) + math.sqrt(self.a_choice)) ** 2
        elif self.num_acc == 2:
            self.o_choice2 = math.floor((self.budget2 - self.a_choice2 * self.price_a2) / self.price_o2)
            if participant.treatment != 1:
                self.round_payoff = (1 / 10) * (math.sqrt(self.o_choice + self.o_choice2) + math.sqrt(self.a_choice + self.a_choice2)) ** 2
            else:
                self.round_payoff = (2 / 5) * (math.sqrt(self.o_choice + self.o_choice2) + math.sqrt(self.a_choice + self.a_choice2)) ** 2
        return self.round_payoff





# PAGES

class Data(ExtraModel):
    player = models.Link(Player)
    slider_move = models.IntegerField()
    slider_move2 = models.IntegerField()
    click_response = models.IntegerField()
    calc_click = models.IntegerField()
    calc_n1 = models.IntegerField()
    calc_n2 = models.IntegerField()


class Quiz(Page):
    form_model = 'player'
    def is_displayed(player):
        return player.round_number == 1


class Quiznext(Page):
    form_model = 'player'
    form_fields = ['quiz2', 'quiz3']
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1
    def error_message(player, values):
        participant = player.participant
        if participant.treatment !=1 :
            solutions = dict(quiz2=1.17, quiz3=2.5)
        else:
            solutions = dict(quiz2=4.66, quiz3=10)
        errors = {f: 'Wrong' for f in solutions if values[f] != solutions[f]}
        if errors:
            return errors

    def js_vars(player):
        participant = player.participant
        return dict(treatment = participant.treatment)


class Quiz2Round(Page):
    form_model = 'player'
    form_fields = ['quiz4']

    @staticmethod
    def error_message(player, values):
        if values['quiz4'] != 1:
            return 'Try again'

    def is_displayed(player):
        return player.round_number == 1

class Enter_Round(Page):
    def is_displayed(player):
        return player.round_number == 1

class Round_slider(Page):
    form_model = 'player'
    @staticmethod
    def get_form_fields(player):
        if player.decision in [1,3]:
            return ['a_choice', 'a_choice2']
        else:
            return ['a_choice']


    def vars_for_template(self):
        participant = self.participant
        if participant.treatment == 2:
            self.order_acc = 1
        else:
            random_acc = [1, 2]
            self.order_acc = random.choice(random_acc)

        return dict(order_acc = self.order_acc, decision=self.decision,num_store=self.num_acc, gift=self.budget1, gift2=self.budget2,
                    price_a=self.price_a, price_o=self.price_o,
                    price_a2=self.price_a2, price_o2=self.price_o2)

    def js_vars(player):
        participant = player.participant
        return dict(treatment = participant.treatment,order_acc = player.order_acc,round = player.round_number,decision = player.decision,num_store=player.num_acc, gift=player.budget1, gift2=player.budget2,
                    price_a=player.price_a, price_o=player.price_o,
                    price_a2=player.price_a2, price_o2=player.price_o2)

    @staticmethod
    def live_method(player: Player, data):
        player.click_response = ''
        if 'slider_move' in data:
            slider_move = data['slider_move']
            Data.create(
                player=player, slider_move=slider_move,
            )
        if 'slider_move2' in data:
            slider_move2 = data['slider_move2']
            Data.create(
                player=player, slider_move2=slider_move2,
            )
        if 'calc_click' in data:
            calc_click = data['calc_click']
            Data.create(
                player=player, calc_click=calc_click,
            )
        if 'calc_n1' and 'calc_n2' in data:
            calc_n1 = data['calc_n1']
            calc_n2 = data['calc_n2']
            Data.create(
                player=player, calc_n1=calc_n1, calc_n2=calc_n2,
            )
        tab_history = [[dat.slider_move, dat.slider_move2, dat.calc_click, dat.calc_n1, dat.calc_n2]
                       for dat in Data.filter(player=player)]
        for u in tab_history:
            if u[0] != None:
                player.click_response += 'A1S' + str(u[0]) + '-'
            if u[1] != None:
                player.click_response += 'A2S' + str(u[1]) + '-'
            if u[2] == 1:
                player.click_response += 'C' + '-'
            if u[3] != None:
                player.click_response += 'a' + str(u[3])
            if u[4] != None:
                player.click_response += 'o' + str(u[4]) + '-'



class Results(Page):
    def vars_for_template(player):
        p1 = Player.set_payoff(player)
        return None


class End(Page):
    def is_displayed(player):
        return player.round_number == 5

    def vars_for_template(player):
        player.rnd = random.randint(1,5)
        p = player.in_round(player.rnd)
        player.payoff = p.round_payoff
        return

class Consent(Page):
    form_model = 'player'
    form_fields = ['prolific']
    def is_displayed(player):
        return player.round_number == 1


class Ins_shop(Page):
    def is_displayed(player):
        return player.round_number == 1

class Final_Res(Page):
    def is_displayed(player):
        return player.round_number == 5

    def vars_for_template(player):
        player.round_count = random.randint(1,5)
        p = player.in_round(player.round_count)
        player.payoff = p.round_payoff
        return None




class Final_Survey(Page):
    form_model = 'player'
    form_fields = ['survey0', 'survey1', 'survey2','survey3', 'survey4', 'survey5','survey6',
                   'survey7', 'survey8','survey9','survey10']

    def is_displayed(player):
        return player.round_number == 5

page_sequence = [Consent,Ins_shop,Quiz,Quiznext,Quiz2Round, Enter_Round,Round_slider, Results, Final_Survey,End]
