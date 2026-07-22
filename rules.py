from collections import deque





class RuleChecker:



    def __init__(self, board):

        self.board=board







    # ==================================================
    # 基础布局规则
    # ==================================================


    def check_setup_place(
        self,
        pos,
        color
    ):


        # 不能中心

        if pos.x==0 and pos.y==0:


            return False,\
                "基础布局不能放中心"



        # 不能紧邻自己的棋子


        for n in self.board.neighbors(pos):


            if not n.is_empty():


                if n.top_piece().color==color:


                    return False,\
                        "基础布局不能紧邻自己的棋子"



        return True,"合法"










    # ==================================================
    # 移动规则
    # ==================================================


    def check_move(
        self,
        start,
        target,
        color
    ):



        # 起点检查


        if start.is_empty():


            return False,\
                "起点没有棋子"




        piece=start.top_piece()



        if piece.color!=color:


            return False,\
                "不能移动对方棋子"





        # ------------------------------------------
        # 新规则：
        #
        # 目标必须在己方棋子六方向
        #
        # ------------------------------------------



        can_move=False



        for pos in self.board.positions.values():



            if pos.is_empty():

                continue



            # 只检查己方棋子


            if pos.top_piece().color != color:

                continue




            neighbors=self.board.neighbors(pos)



            for n in neighbors:


                if (
                    n.x==target.x
                    and
                    n.y==target.y
                ):


                    can_move=True

                    break




            if can_move:

                break





        if not can_move:


            return False,\
                "目标位置必须位于己方棋子六方向"






        # ------------------------------------------
        # 层级规则
        # ------------------------------------------


        current_height=start.height()



        target_height=target.height()+1





        # 第一层不能移动到第三层


        if current_height==1:


            if target_height>2:


                return False,\
                    "第一层棋子不能移动到第三层"






        # 第二层最多第三层


        elif current_height==2:


            if target_height>3:


                return False,\
                    "超过三层限制"






        # 第三层不能移动


        elif current_height==3:


            return False,\
                "第三层棋子不能移动"





        # 目标不能超过3层


        if target.height()>=3:


            return False,\
                "目标位置已经达到三层"





        return True,"移动合法"









    # ==================================================
    # 俯视图
    # ==================================================


    def top_view(self):


        result={}



        for key,pos in self.board.positions.items():


            if not pos.is_empty():


                result[key]=pos.top_piece().color



        return result










    # ==================================================
    # 五连检测
    # ==================================================


    def check_five(
        self,
        color
    ):


        view=self.top_view()



        directions=[

            (1,0),

            (0,1),

            (1,-1)

        ]





        for key,c in view.items():



            if c!=color:

                continue




            x,y=key





            for dx,dy in directions:



                before=(

                    x-dx,

                    y-dy

                )



                if before in view:


                    if view[before]==color:


                        continue





                length=0



                nx=x

                ny=y





                while (

                    (nx,ny) in view

                    and

                    view[(nx,ny)]==color

                ):



                    length+=1


                    nx+=dx

                    ny+=dy





                # 正好五连


                if length==5:


                    return True






        return False










    # ==================================================
    # 第三层五枚
    # ==================================================


    def check_level3_five(
        self,
        color
    ):



        count=0



        for pos in self.board.positions.values():



            if pos.height()==3:



                if pos.top_piece().color==color:


                    count+=1




        return count>=5











    # ==================================================
    # 第三层连通三枚
    # ==================================================


    def check_level3_three(
        self,
        color
    ):



        level3=[]




        for pos in self.board.positions.values():



            if pos.height()==3:


                if pos.top_piece().color==color:


                    level3.append(pos)






        visited=set()





        for p in level3:



            key=(p.x,p.y)



            if key in visited:

                continue




            queue=deque([p])



            visited.add(key)



            count=0





            while queue:



                cur=queue.popleft()



                count+=1




                for n in self.board.neighbors(cur):



                    if n in level3:


                        nk=(n.x,n.y)



                        if nk not in visited:



                            visited.add(nk)

                            queue.append(n)







            if count>=3:


                return True





        return False










    # ==================================================
    # 总胜利判断
    # ==================================================


    def check_win(
        self,
        color
    ):



        if self.check_five(color):


            return True,\
                "完成五连"





        if self.check_level3_five(color):


            return True,\
                "第三层拥有五枚棋子"





        if self.check_level3_three(color):


            return True,\
                "第三层形成三连"





        return False,None