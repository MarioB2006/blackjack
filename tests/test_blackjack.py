import unittest
from src.blackjack_v2_oop import Bot,Player

class TestBlackjack(unittest.TestCase):
    def setUp(self):
        self.player=Player(stack=0,count=[0,0])
        self.bot=Bot(k=2,stack=0,player=self.player)
    def test_player_increase_stack(self):
        old_player_stack=self.player.stack
        current_number,new_stack=self.player.draw_card()
        self.assertGreater(new_stack,old_player_stack)
        self.assertEqual(old_player_stack+current_number,new_stack)
    def test_bot_game_states_bot_wins(self):
        self.player.stack = 15
        self.bot.stack = 18
        result = self.bot.game_states()
        self.assertEqual(result, 3)
    def test_bot_game_state_loose(self):
        self.player.stack=20
        self.bot.stack=10
        result=self.bot.game_states()
        self.assertEqual(result,1)
    def test_bot_game_state_no_win(self):
        self.player.stack = 18
        self.bot.stack = 18
        result = self.bot.game_states()
        self.assertEqual(result, 2)