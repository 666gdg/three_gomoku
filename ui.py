import pygame

from rules import RuleChecker



# ==========================
# 字体
# ==========================
def get_font(size):

    font_path = "C:/Windows/Fonts/msyh.ttc"


    return pygame.font.Font(
        font_path,
        size
    )






# ==========================
# Button
# ==========================


class Button:


    def __init__(
            self,
            rect,
            text
    ):


        self.rect=pygame.Rect(rect)

        self.text=text

        self.selected=False




    def draw(self,screen):


        if self.selected:

            color=(100,200,120)

        else:

            color=(210,210,210)



        pygame.draw.rect(
            screen,
            color,
            self.rect,
            border_radius=10
        )


        pygame.draw.rect(
            screen,
            (80,80,80),
            self.rect,
            2,
            border_radius=10
        )



        font=get_font(24)



        img=font.render(
            self.text,
            True,
            (0,0,0)
        )


        screen.blit(

            img,

            (
                self.rect.x+15,
                self.rect.y+12
            )

        )




    def click(self,pos):

        return self.rect.collidepoint(pos)







# ==========================
# 弹窗
# ==========================

class Popup:


    def __init__(self):

        self.show=False

        self.title=""

        self.content=""

        self.confirm_callback=None

        self.cancel_callback=None



    def open(
            self,
            title,
            content,
            callback=None,
            cancel_callback=None
    ):


        self.show=True

        self.title=title

        self.content=content

        self.confirm_callback=callback

        self.cancel_callback=cancel_callback





    def close(self):

        self.show=False

        self.confirm_callback=None

        self.cancel_callback=None






    def draw(self,screen):


        if not self.show:

            return



        rect=pygame.Rect(
            350,
            250,
            600,
            320
        )



        # 半透明遮罩

        mask=pygame.Surface(
            screen.get_size()
        )

        mask.set_alpha(120)

        mask.fill(
            (0,0,0)
        )

        screen.blit(
            mask,
            (0,0)
        )



        # 弹窗背景


        pygame.draw.rect(
            screen,
            (245,245,245),
            rect,
            border_radius=12
        )


        pygame.draw.rect(
            screen,
            (0,0,0),
            rect,
            3,
            border_radius=12
        )



        font=get_font(30)



        # 标题


        title=font.render(
            self.title,
            True,
            (0,0,0)
        )


        screen.blit(
            title,
            (
                rect.x+40,
                rect.y+40
            )
        )




        # 内容


        content=font.render(
            self.content,
            True,
            (0,0,0)
        )


        screen.blit(
            content,
            (
                rect.x+40,
                rect.y+100
            )
        )




        # 关闭X


        close_font=get_font(35)


        close=close_font.render(
            "×",
            True,
            (220,0,0)
        )


        screen.blit(
            close,
            (
                rect.right-50,
                rect.y+15
            )
        )





        # 有确认回调才显示按钮


        if self.confirm_callback:


            # 确认


            pygame.draw.rect(
                screen,
                (100,200,120),
                (
                    rect.x+120,
                    rect.y+230,
                    120,
                    50
                ),
                border_radius=8
            )


            txt=font.render(
                "确定",
                True,
                (0,0,0)
            )


            screen.blit(
                txt,
                (
                    rect.x+150,
                    rect.y+240
                )
            )




            # 取消


            pygame.draw.rect(
                screen,
                (200,200,200),
                (
                    rect.x+350,
                    rect.y+230,
                    120,
                    50
                ),
                border_radius=8
            )


            txt=font.render(
                "取消",
                True,
                (0,0,0)
            )


            screen.blit(
                txt,
                (
                    rect.x+380,
                    rect.y+240
                )
            )
# ==========================
# UI主类
# ==========================


class UI:


    def __init__(self,game):


        self.game=game


        self.screen=pygame.display.set_mode(
            (
                1400,
                900
            )
        )


        pygame.display.set_caption(
            "三层五子棋"
        )



        # ======================
        # 左下操作按钮
        # ======================


        self.place_btn=Button(
            (40,760,160,55),
            "放置棋子"
        )


        self.move_btn=Button(
            (40,825,160,55),
            "移动棋子"
        )



        # ======================
        # 右下按钮
        # ======================


        self.confirm_btn=Button(
            (1080,760,120,55),
            "确认"
        )


        self.cancel_btn=Button(
            (1220,760,120,55),
            "取消"
        )


        self.undo_btn=Button(
            (1080,825,120,55),
            "悔棋"
        )


        # ======================
        # 右上按钮
        # ======================


        self.restart_btn=Button(
            (1180,40,160,55),
            "重新开始"
        )



        self.popup=Popup()



        # 移动选择

        self.selected_piece=None

    def draw_selected(self):

        if self.selected_piece is None:
            return

        x, y = self.game.board.axial_to_pixel(

            self.selected_piece.x,

            self.selected_piece.y

        )

        pygame.draw.circle(

            self.screen,

            (255, 0, 0),

            (
                int(x),
                int(y)
            ),

            28,

            3

        )

    # ==========================
    # 绘制
    # ==========================


    def draw(self):


        self.screen.fill(
            (255,255,255)
        )



        # 棋盘

        self.game.board.draw(
            self.screen
        )

        # 当前移动棋子高亮

        self.draw_selected()


        # 按钮


        self.place_btn.draw(
            self.screen
        )


        self.move_btn.draw(
            self.screen
        )


        self.confirm_btn.draw(
            self.screen
        )


        self.cancel_btn.draw(
            self.screen
        )


        self.undo_btn.draw(
            self.screen
        )


        self.restart_btn.draw(
            self.screen
        )



        self.draw_info()



        self.popup.draw(
            self.screen
        )



        pygame.display.update()







    # ==========================
    # 信息显示
    # ==========================


    def draw_info(self):


        font=get_font(26)



        info=self.game.info()



        texts=[


            f"当前玩家: {info['player']}",


            f"黑剩余: {info['remain']['black']}",


            f"白剩余: {info['remain']['white']}",


            f"回合: {info['round']}",


            f"阶段: {info['phase']}",


        ]



        if info["phase"]=="setup":


            texts.append(

                f"布局 {info['setup_now']}/{info['setup_need']}"

            )



        if info["game_over"]:


            texts.append(
                "游戏结束"
            )




        y=100



        for t in texts:


            img=font.render(
                t,
                True,
                (0,0,0)
            )


            self.screen.blit(
                img,
                (
                    1120,
                    y
                )
            )


            y+=40






    # ==========================
    # 鼠标点击
    # ==========================


    def mouse_click(
            self,
            pos,
            button
    ):


        # 弹窗优先

        if self.popup.show:

            rect = pygame.Rect(
                350,
                250,
                600,
                320
            )

            # X

            if (
                    rect.right - 60 <= pos[0] <= rect.right
                    and
                    rect.y <= pos[1] <= rect.y + 60
            ):
                self.popup.close()

                return

            # 确认按钮

            confirm_rect = pygame.Rect(

                rect.x + 120,
                rect.y + 230,
                120,
                50

            )

            if confirm_rect.collidepoint(pos):

                if self.popup.confirm_callback:

                    self.popup.confirm_callback()


                else:

                    self.popup.close()

                return

            # 取消按钮

            cancel_rect = pygame.Rect(

                rect.x + 350,
                rect.y + 230,
                120,
                50

            )

            if cancel_rect.collidepoint(pos):
                self.popup.close()

                return

            return



        # 重新开始


        if self.restart_btn.click(pos):


            self.popup.open(

                "重新开始",

                "确认重新开始?",

                self.restart_confirm

            )


            return





        # 悔棋


        if self.undo_btn.click(pos):


            ok,msg=self.game.undo()


            if not ok:

                self.popup.open(
                    "提示",
                    msg
                )

            return





        # 模式选择


        if self.place_btn.click(pos):


            self.game.action_type="place"


            self.place_btn.selected=True

            self.move_btn.selected=False


            return




        if self.move_btn.click(pos):


            self.game.action_type="move"


            self.move_btn.selected=True

            self.place_btn.selected=False


            return






        # 确认


        if self.confirm_btn.click(pos):


            msg=self.game.confirm()



            if msg:


                self.popup.open(
                    "提示",
                    msg
                )


            return






        # 取消


        if self.cancel_btn.click(pos):


            self.game.cancel()


            self.selected_piece=None


            return




        # 左键棋盘


        if button==1:


            self.board_click(
                pos
            )





        # 右键查看堆叠


        if button==3:


            self.show_stack(
                pos
            )

    # ==========================
    # 棋盘点击
    # ==========================


    def board_click(self,pos):


        for p in self.game.board.positions.values():


            x,y=self.game.board.axial_to_pixel(
                p.x,
                p.y
            )


            # 点击范围

            if (

                (x-pos[0])**2 +

                (y-pos[1])**2

            ) < 30**2:



                # ==================
                # 放置模式
                # ==================

                if self.game.action_type=="place":



                    ok,msg=self.game.put_piece(
                        p.x,
                        p.y
                    )


                    if not ok:


                        self.popup.open(
                            "提示",
                            msg
                        )



                    return




                # ==================
                # 移动模式
                # ==================


                if self.game.action_type=="move":



                    # 第一次点击

                    if self.selected_piece is None:



                        if p.is_empty():


                            self.popup.open(
                                "提示",
                                "请选择自己的棋子"
                            )

                            return



                        if p.top_piece().color != self.game.player():


                            self.popup.open(
                                "提示",
                                "不能选择对方棋子"
                            )


                            return



                        self.selected_piece=p



                        return





                    # 第二次点击目标


                    start=self.selected_piece



                    ok,msg=self.game.move_piece(

                        start.x,
                        start.y,

                        p.x,
                        p.y

                    )



                    if not ok:


                        self.popup.open(
                            "提示",
                            msg
                        )



                    self.selected_piece=None



                    return







    # ==========================
    # 右键查看堆叠
    # ==========================


    def show_stack(self,pos):


        for p in self.game.board.positions.values():


            x,y=self.game.board.axial_to_pixel(
                p.x,
                p.y
            )


            if (

                (x-pos[0])**2+

                (y-pos[1])**2

            ) < 30**2:



                if p.is_empty():

                    return



                text=""


                for i,piece in enumerate(
                    p.stack
                ):


                    text += (

                        f"第{i+1}层:"
                        f"{piece.color} "

                    )



                self.popup.open(
                    "棋子信息",
                    text
                )


                return







    # ==========================
    # 重新开始确认
    # ==========================


    def restart_confirm(self):


        self.game.restart()



        self.place_btn.selected=True

        self.move_btn.selected=False



        self.selected_piece=None



        self.popup.close()