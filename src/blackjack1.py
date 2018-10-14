try:
    import tkinter
except ImportError:  # python 2
    import Tkinter as tkinter
import random


class Blackjack(object):

    def __init__(self):
        self.cards = []
        self.deck = []
        self.player_score = 0
        self.player_ace = False
        self.dealer_score = 0
        self.dealer_ace = False
        self.bet_placed = False
        self.bet_value = tkinter.IntVar()
        self.player_money = self._starting_money()
        self._load_images(self.cards)
        self.reload_cards()
        self.warning_log = tkinter.StringVar()

    def game_core(self):
        buttons = [hit_button,dealer_button,stand_button,restart_button]
        if not self.bet_placed:
            self._change_button_state(buttons,'disabled')
            self._change_button_state([bet_button],'normal')
        else:
            self.warning_log.set('')
            self._change_button_state(buttons,'normal')
            self._change_button_state([bet_button],'disabled')
            self.deal_dealer()
            self.hit()
            self.hit()

    def hit(self):
        card_value = self.deal_cards(player_card_frame)[0]
        if card_value == 1 and not self.player_ace:
            card_value = 11
            self.player_ace = True
        elif card_value == 1 and self.player_ace:
            card_value = 1
        self.player_score += card_value
        player_score_label.set(self.player_score)
        if self.player_score > 21:
            result_text.set('Dealer wins')
            self._change_button_state([hit_button,dealer_button,stand_button],'disabled')

    def double(self):
        if self.player_money.get() >= self.bet_value.get():
            self.player_money.set(self.player_money.get()-self.bet_value.get())
            self.bet_value.set(self.bet_value.get()*2)
        else:
            self.bet_value.set(self.bet_value.get()+self.player_money.get())
            self.player_money.set(0)
        self.hit()
        if self.player_score <= 21:
            self.stand()

    def stand(self):
        win = False
        draw = False
        self._change_button_state([hit_button,dealer_button,stand_button],'disabled')
        while self.dealer_score < 17:
            self.deal_dealer()
            if self.player_score < self.dealer_score <= 21:
                result_text.set('Dealer wins.')
            elif self.dealer_score < self.player_score or self.dealer_score > 21:
                result_text.set('Player wins.')
                win = True
            else:
                result_text.set('Draw')
                draw = True
        if win:
            self.player_money.set(self.player_money.get()+self.bet_value.get()*2)
        elif draw:
            self.player_money.set(self.player_money.get()+(self.bet_value.get()))

    def deal_cards(self,frame):
        # pop card off top of the deck
        next_card = self.deck.pop(0)
        tkinter.Label(frame,image=next_card[1],relief='raised').pack(side='left')
        return next_card

    def deal_dealer(self):
        card_value = self.deal_cards(dealer_card_frame)[0]
        if card_value == 1 and not self.dealer_ace:
            card_value = 11
            self.dealer_ace = True
        elif card_value == 1 and self.dealer_ace:
            card_value = 1
        self.dealer_score += card_value
        dealer_score_label.set(self.dealer_score)

    def place_bet(self):
        try:
            bet = int(bet_entry.get())
            if 0 < bet <= self.player_money.get():
                self.bet_value.set(bet)
                self.player_money.set(self.player_money.get()-bet)
                self.bet_placed = True
            else:
                self.warning_log.set('WARNING! Pass a number between 0 and your money.')
        except ValueError:
            self.bet_placed = False
            self.warning_log.set('WARNING! Pass a number.')
        bet_entry.delete(0,'end')
        self.game_core()

    def restart(self):
        self.dealer_score, self.player_score = 0, 0
        self.dealer_ace, self.player_ace = False, False
        player_score_label.set(self.player_score)
        dealer_score_label.set(self.dealer_score)
        self.reload_cards()
        result_text.set('')
        self.bet_value.set(0)
        self.bet_placed = False
        for i in dealer_card_frame.winfo_children():
            i.destroy()
        for i in player_card_frame.winfo_children():
            i.destroy()
        self.game_core()

    def reload_cards(self):
        self.deck = list(self.cards)
        random.shuffle(self.deck)

    def _starting_money(self) -> tkinter.IntVar:
        player_money = tkinter.IntVar()
        player_money.set(1000)
        return player_money

    def _change_button_state(self,buttons: list, state: str):
        for button in buttons:
            button.configure(state=state)

    def _load_images(self, card_images):
        suits=['heart','diamond','club','spade']
        face_cards = ['jack','queen','king']
        extension = 'ppm'
        for suit in suits:
            for card in range(1,11):
                name = 'D:\\Projekty Java\\blackjack_game\\cards\\{}_{}.{}'.format(str(card),suit,extension)
                image = tkinter.PhotoImage(file=name)
                card_images.append((card,image))
            for face in face_cards:
                name = 'D:\\Projekty Java\\blackjack_game\\cards\\{}_{}.{}'.format(face,suit,extension)
                image = tkinter.PhotoImage(file=name)
                card_images.append((10,image))


# Setting up main window
mainWindow = tkinter.Tk()
blackjack = Blackjack()
mainWindow.title('Black Jack')
mainWindow.geometry('640x480')
mainWindow.config(background="green")

# result frame
result_text = tkinter.StringVar()
result = tkinter.Label(mainWindow,textvariable=result_text,background="green")
result.grid(row=0,column=0,columnspan=3)

card_frame = tkinter.Frame(mainWindow,relief='sunken',borderwidth=1,background='green')
card_frame.grid(row=1,column=0,sticky='ew',columnspan=3,rowspan=2)

# dealer cards and score.
dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame,text='Dealer',background='green',fg='white').grid(row=0,column=0)
tkinter.Label(card_frame,textvariable=dealer_score_label,background='green',fg='white').grid(row=1,column=0)
dealer_card_frame = tkinter.Frame(card_frame,background='green')
dealer_card_frame.grid(row=0,column=1,sticky='ew',rowspan=2)

# player cards and score
player_score_label = tkinter.IntVar()
tkinter.Label(card_frame,text='Player',background='green',fg='white').grid(row=2,column=0)
tkinter.Label(card_frame,textvariable=player_score_label,background='green',fg='white').grid(row=3,column=0)
player_card_frame = tkinter.Frame(card_frame,background='green')
player_card_frame.grid(row=2,column=1,sticky='ew',rowspan=2)

# button frame
button_frame = tkinter.Frame(mainWindow,background="green")
button_frame.grid(row=3,column=0,sticky='w',columnspan=3)
hit_button = tkinter.Button(button_frame, text='Hit', command=blackjack.hit)
hit_button.grid(row=0,column=0,sticky='',pady=10,padx=10)
dealer_button = tkinter.Button(button_frame, text='Double', command=blackjack.double)
dealer_button.grid(row=0,column=1,sticky='',pady=10,padx=10)
stand_button = tkinter.Button(button_frame, text='Stand', command=blackjack.stand)
stand_button.grid(row=0,column=2,sticky='',padx=10,pady=10)
restart_button = tkinter.Button(button_frame, text='Restart', command=blackjack.restart)
restart_button.grid(row=0,column=3,sticky='',padx=10,pady=10)

# bet frame
bet_frame = tkinter.Frame(mainWindow,background='green')
bet_frame.grid(row=4,column=0,rowspan=2,columnspan=4)
bet_entry = tkinter.Entry(bet_frame)
bet_entry.grid(row=0,column=0,sticky='w')
bet_button = tkinter.Button(bet_frame, text='Place bet', command=blackjack.place_bet)
bet_button.grid(row=0,column=1,padx=10)
tkinter.Label(bet_frame,text='Current bet: ',background='green').grid(row=0,column=2)
tkinter.Label(bet_frame, textvariable=blackjack.bet_value, background='green').grid(row=0, column=3)
tkinter.Label(bet_frame,text='Money: ',background='green').grid(row=1,column=0,sticky='w')
tkinter.Label(bet_frame, textvariable=blackjack.player_money, background='green').grid(row=1, column=1, sticky='w')

# warning frame
tkinter.Label(mainWindow, textvariable=blackjack.warning_log, background='green').grid(row=6, column=0, sticky='ew', columnspan=3)

blackjack.game_core()
mainWindow.mainloop()

