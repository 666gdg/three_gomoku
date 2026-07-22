import pygame
import math

from piece import Position



FONT_PATH="C:/Windows/Fonts/msyh.ttc"





class Board:



    def __init__(self):


        # 六边形半径

        # 半径5

        # 共91个位置


        self.size=5



        self.positions={}



        self.generate()






    # =========================
    # 生成棋盘
    # =========================


    def generate(self):


        n=self.size



        for q in range(
            -n,
            n+1
        ):


            for r in range(
                -n,
                n+1
            ):



                s=-q-r




                if max(

                    abs(q),

                    abs(r),

                    abs(s)

                )<=n:



                    self.positions[(q,r)] = Position(

                        q,

                        r

                    )









    # =========================
    # 六方向邻居
    # =========================


    def neighbors(
        self,
        pos
    ):


        dirs=[


            (1,0),

            (-1,0),


            (0,1),

            (0,-1),


            (1,-1),

            (-1,1)

        ]



        result=[]



        for dx,dy in dirs:


            key=(

                pos.x+dx,

                pos.y+dy

            )



            if key in self.positions:


                result.append(

                    self.positions[key]

                )



        return result









    # =========================
    # 六边形坐标转换
    # =========================


    def axial_to_pixel(
        self,
        q,
        r
    ):



        size=55



        x=size*(

            math.sqrt(3)*q

            +

            math.sqrt(3)/2*r

        )



        y=size*(

            3/2*r

        )




        # 棋盘中心

        return (

            x+650,

            y+420

        )









    # =========================
    # 鼠标查找位置
    # =========================


    def find_position(
        self,
        mouse
    ):


        mx,my=mouse



        for pos in self.positions.values():



            x,y=self.axial_to_pixel(

                pos.x,

                pos.y

            )



            if (

                x-mx

            )**2 + (

                y-my

            )**2 < 35**2:



                return pos




        return None









    # =========================
    # 绘制棋盘
    # =========================


    def draw(
        self,
        screen
    ):



        # 画连接线


        for pos in self.positions.values():



            x,y=self.axial_to_pixel(

                pos.x,

                pos.y

            )



            for n in self.neighbors(pos):


                x2,y2=self.axial_to_pixel(

                    n.x,

                    n.y

                )



                pygame.draw.line(

                    screen,

                    (160,160,160),

                    (
                        x,
                        y
                    ),

                    (
                        x2,
                        y2
                    ),

                    2

                )







        # 画棋子


        for pos in self.positions.values():



            if pos.is_empty():

                continue




            x,y=self.axial_to_pixel(

                pos.x,

                pos.y

            )



            height=pos.height()





            # 堆叠视觉偏移

            draw_y=y-(height-1)*10





            piece=pos.top_piece()




            if piece.color=="black":


                color=(30,30,30)


            else:


                color=(245,245,245)





            # 下层阴影

            if height>1:


                pygame.draw.circle(

                    screen,

                    (120,120,120),

                    (
                        int(x),
                        int(draw_y+8)
                    ),

                    20

                )







            pygame.draw.circle(

                screen,

                color,

                (
                    int(x),
                    int(draw_y)
                ),

                20

            )






            # 白棋边框


            if piece.color=="white":


                pygame.draw.circle(

                    screen,

                    (0,0,0),

                    (
                        int(x),
                        int(draw_y)
                    ),

                    20,

                    2

                )







            # 显示层数


            if height>1:



                font=pygame.font.Font(

                    FONT_PATH,

                    22

                )



                txt=font.render(

                    str(height),

                    True,

                    (255,0,0)

                )



                screen.blit(

                    txt,

                    (
                        int(x-7),
                        int(draw_y-45)
                    )

                )