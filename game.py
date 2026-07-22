import copy

from piece import Piece
from board import Board
from rules import RuleChecker



class Game:


    def __init__(self):

        self.board = Board()


        self.players = [
            "black",
            "white"
        ]


        self.current_player = 0


        self.remain = {

            "black":25,

            "white":25

        }



        # setup / play

        self.phase="setup"



        self.setup_steps=[

            1,
            2,
            2,
            1

        ]


        self.setup_index=0


        self.setup_put_count=0




        # 正式回合

        self.round=1



        # 当前模式

        # place
        # move

        self.action_type="place"



        # 当前未确认动作

        self.current_action=None



        # 当前回合取消备份

        self.backup=None



        # 悔棋历史

        self.history=[]



        # 游戏结束

        self.game_over=False



        self.save_state()

        self.save_history()





    # ==========================
    # 当前玩家
    # ==========================


    def player(self):

        return self.players[
            self.current_player
        ]




    def switch_player(self):

        self.current_player+=1


        if self.current_player>=2:

            self.current_player=0

            self.round+=1






    # ==========================
    # 保存当前回合状态
    # ==========================


    def save_state(self):


        self.backup={


            "board":
            copy.deepcopy(
                self.board.positions
            ),


            "remain":
            copy.deepcopy(
                self.remain
            ),


            "player":
            self.current_player,


            "round":
            self.round,


            "phase":
            self.phase,


            "setup_index":
            self.setup_index,


            "setup_put":
            self.setup_put_count

        }






    # ==========================
    # 保存悔棋历史
    # ==========================


    def save_history(self):


        state=copy.deepcopy(
            self.backup
        )


        self.history.append(
            state
        )






    # ==========================
    # 取消当前操作
    # ==========================


    def cancel(self):


        if self.backup is None:

            return



        self.board.positions=copy.deepcopy(
            self.backup["board"]
        )


        self.remain=copy.deepcopy(
            self.backup["remain"]
        )


        self.current_player=\
            self.backup["player"]


        self.round=\
            self.backup["round"]


        self.phase=\
            self.backup["phase"]


        self.setup_index=\
            self.backup["setup_index"]


        self.setup_put_count=\
            self.backup["setup_put"]



        self.current_action=None






    # ==========================
    # 悔棋
    # ==========================


    def undo(self):


        if self.game_over:

            return False,"游戏已经结束"



        if len(self.history)<=1:

            return False,"没有可悔棋步骤"



        self.history.pop()


        state=self.history[-1]



        self.board.positions=copy.deepcopy(
            state["board"]
        )


        self.remain=copy.deepcopy(
            state["remain"]
        )


        self.current_player=\
            state["player"]


        self.round=\
            state["round"]


        self.phase=\
            state["phase"]


        self.setup_index=\
            state["setup_index"]


        self.setup_put_count=\
            state["setup_put"]



        self.current_action=None

        self.save_state()

        self.current_action = None

        return True, "悔棋成功"






    # ==========================
    # 重新开始
    # ==========================


    def restart(self):

        self.__init__()




    # ==========================
    # 放置棋子
    # ==========================


    def put_piece(self,x,y):


        if self.game_over:

            return False,"游戏已经结束"



        pos=self.board.positions.get(
            (x,y)
        )


        if pos is None:

            return False,"位置不存在"



        if not pos.is_empty():

            return False,"已有棋子"



        color=self.player()



        if self.remain[color]<=0:

            return False,"没有剩余棋子"




        rule=RuleChecker(
            self.board
        )



        # setup

        if self.phase=="setup":


            if self.setup_put_count >= self.current_setup_count():

                return False,\
                "当前阶段不能继续放置"



            ok,msg=rule.check_setup_place(
                pos,
                color
            )


            if not ok:

                return False,msg



        # play

        else:


            if self.current_action:

                return False,\
                "本回合已经操作"



            if self.action_type!="place":

                return False,\
                "当前不是放置模式"





        pos.add_piece(
            Piece(color)
        )


        self.remain[color]-=1



        if self.phase=="setup":

            self.setup_put_count+=1


        else:

            self.current_action=(

                "place",
                pos

            )



        return True,"放置成功"





    # ==========================
    # 移动棋子
    # ==========================


    def move_piece(
            self,
            sx,sy,
            tx,ty
    ):


        if self.game_over:

            return False,"游戏结束"



        if self.phase!="play":

            return False,"布局阶段不能移动"



        if self.action_type!="move":

            return False,"当前不是移动模式"



        if self.current_action:

            return False,"本回合已经操作"



        start=self.board.positions.get(
            (sx,sy)
        )


        target=self.board.positions.get(
            (tx,ty)
        )



        rule=RuleChecker(
            self.board
        )


        ok,msg=rule.check_move(
            start,
            target,
            self.player()
        )


        if not ok:

            return False,msg



        piece=start.remove_top()


        target.add_piece(piece)



        self.current_action=(

            "move",
            start,
            target

        )


        return True,"移动成功"

    # ==========================
    # 当前setup需要数量
    # ==========================

    def current_setup_count(self):

        if self.phase!="setup":

            return 0


        return self.setup_steps[
            self.setup_index
        ]





    # ==========================
    # 确认回合
    # ==========================

    def confirm(self):
        self.save_history()

        if self.game_over:

            return "游戏已经结束"



        # ======================
        # setup阶段
        # ======================

        if self.phase=="setup":


            need=self.current_setup_count()



            if self.setup_put_count != need:

                return (
                    f"当前需要放置{need}枚棋子"
                )



            # 保存完成前状态

            self.setup_index += 1


            self.setup_put_count=0



            # setup结束

            if self.setup_index >= len(
                self.setup_steps
            ):


                self.phase="play"

                self.round=1



            self.current_action=None
            self.switch_player()


            self.save_state()








            return None





        # ======================
        # play阶段
        # ======================


        if self.current_action is None:

            return "当前没有操作"



        checker=RuleChecker(
            self.board
        )


        win,msg=checker.check_win(
            self.player()
        )


        if win:


            self.game_over=True


            return (
                f"{self.player()}获胜\n{msg}"
            )



        # 保存历史

        self.current_action=None



        self.save_state()


        self.switch_player()



        self.save_history()



        return None







    # ==========================
    # 游戏状态信息
    # ==========================


    def info(self):


        return {


            "player":
            self.player(),


            "remain":
            self.remain,


            "round":
            self.round,


            "phase":
            self.phase,


            "setup_need":
            self.current_setup_count(),


            "setup_now":
            self.setup_put_count,


            "game_over":
            self.game_over


        }