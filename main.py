import pygame

from game import Game
from ui import UI





def main():


    pygame.init()

    pygame.font.init()



    game=Game()


    ui=UI(game)



    clock=pygame.time.Clock()



    running=True




    while running:



        for event in pygame.event.get():



            # 关闭窗口

            if event.type==pygame.QUIT:


                running=False





            # 鼠标

            elif event.type==pygame.MOUSEBUTTONDOWN:



                ui.mouse_click(

                    event.pos,

                    event.button

                )






            # 键盘

            elif event.type==pygame.KEYDOWN:



                ui.key_press(

                    event.key

                )








        ui.draw()



        clock.tick(60)







    pygame.quit()





if __name__=="__main__":


    main()