class Piece:


    def __init__(
        self,
        color
    ):

        self.color=color




    def __repr__(self):

        return self.color






class Position:


    def __init__(
        self,
        x,
        y
    ):


        # 六边形坐标

        self.x=x

        self.y=y



        # 棋子堆叠

        # index 0 = 第一层

        self.stack=[]





    # =====================
    # 棋子操作
    # =====================


    def add_piece(
        self,
        piece
    ):


        """
        添加棋子

        最大三层
        """


        if len(self.stack)>=3:

            return False



        self.stack.append(
            piece
        )


        return True







    def remove_top(self):


        """
        移除最高层棋子
        """


        if len(self.stack)==0:

            return None



        return self.stack.pop()








    def top_piece(self):


        """
        返回顶部棋子
        """


        if self.is_empty():

            return None



        return self.stack[-1]








    # 兼容旧代码

    def top(self):

        return self.top_piece()








    def height(self):


        """
        当前高度

        0:
        空

        1:
        一层

        2:
        两层

        3:
        三层
        """


        return len(self.stack)







    def is_empty(self):


        return len(self.stack)==0






    def __repr__(self):


        return (
            f"Position({self.x},{self.y}) "
            f"{self.stack}"
        )