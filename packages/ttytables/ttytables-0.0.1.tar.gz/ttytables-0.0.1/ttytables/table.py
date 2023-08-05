class Table(object):


    def __init__(self, title):


        # Default template.
        self.top_left = '-'         # ↖
        self.top_up = '-'           # ↑
        self.top_right = '-'        # ↗
        self.left = '|'             # ←
        self.center = '|'           # ·
        self.right = '|'            # →
        self.bottom_left = '|'      # ↙
        self.bottom_down = '-'      # ↓
        self.bottom_right = '|'     # ↘
        self.vertical = '|'         # |
        self.across = '-'           # -


        # Fixed parameter.
        self.title = title
        self.content = []
        self.max_len = []


        # Parameters set.
        self.align = '<'
        self.width = 0
        self.symbol = ''

    # add the content
    def add_row(self, content):
        self.content.append(content)


    # Get the max lengh.
    def process(self):
        content = self.content + [self.title]
        for lists in content:
            for index, word in enumerate(lists):
                try:
                    if len(word) > self.max_len[index]:
                        self.max_len[index]=len(word)
                except IndexError:
                    self.max_len = list(map(len, lists))
        return self.max_len


    def template_title(self):
        strs = ''
        for index, lens in enumerate(self.max_len):
            strs += str('{}%s' % (self.top_up)).format(self.across * (lens + 2 + self.width))
        return self.top_left + strs[:-1] + self.top_right


    def template_center(self):
        strs = ''
        for index, lens in enumerate(self.max_len):
            strs += str('{}%s' % (self.center)).format(self.across * (lens + 2 + self.width))
        return self.left + strs[:-1] + self.right


    def template_content(self):
        strs = ''
        for index, lens in enumerate(self.max_len):
            strs += ' {%s:%s%s%s} %s' % (index, self.symbol, self.align, lens + self.width, self.vertical)
        return self.vertical + strs


    def template_tail(self):
        strs = ''
        for index, lens in enumerate(self.max_len):
            strs += str('{}%s' % (self.bottom_down)).format(self.across * (lens + 2 + self.width))
        return self.bottom_left + strs[:-1] + self.bottom_right



class Theme(Table):


    def style(self):
        self.top_left = '┌'     # ↖
        self.top_up = '┬'       # ↑
        self.top_right = '┐'    # ↗
        self.left = '├'         # ←
        self.center = '┼'       # ·
        self.right = '┤'        # →
        self.bottom_left = '└'  # ↙
        self.bottom_down = '┴'  # ↓
        self.bottom_right = '┘' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style1(self):
        self.top_left = '┌'     # ↖
        self.top_up = '─'       # ↑
        self.top_right = '┐'    # ↗
        self.left = '│'         # ←
        self.center = '┼'       # ·
        self.right = '│'        # →
        self.bottom_left = '└'  # ↙
        self.bottom_down = '─'  # ↓
        self.bottom_right = '┘' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style2(self):
        self.top_left = '┍'     # ↖
        self.top_up = '┯'       # ↑
        self.top_right = '┑'    # ↗
        self.left = '┝'         # ←
        self.center = '┿'       # ·
        self.right = '┥'        # →
        self.bottom_left = '┕'  # ↙
        self.bottom_down = '┷'  # ↓
        self.bottom_right = '┙' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style3(self):
        self.top_left = '╔'     # ↖
        self.top_up = '╦'       # ↑
        self.top_right = '╗'    # ↗
        self.left = '╠'         # ←
        self.center = '╬'       # ·
        self.right = '╣'        # →
        self.bottom_left = '╚'  # ↙
        self.bottom_down = '╩'  # ↓
        self.bottom_right = '╝' # ↘
        self.vertical = '║'     # |
        self.across = '═'       # -


    def style4(self):
        self.top_left = '┏'     # ↖
        self.top_up = '┳'       # ↑
        self.top_right = '┓'    # ↗
        self.left = '┣'         # ←
        self.center = '╋'       # ·
        self.right = '┫'        # →
        self.bottom_left = '┗'  # ↙
        self.bottom_down = '┻'  # ↓
        self.bottom_right = '┛' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style5(self):
        self.top_left = '┏'     # ↖
        self.top_up = '┳'       # ↑
        self.top_right = '┓'    # ↗
        self.left = '┣'         # ←
        self.center = '╋'       # ·
        self.right = '┫'        # →
        self.bottom_left = '┗'  # ↙
        self.bottom_down = '┻'  # ↓
        self.bottom_right = '┛' # ↘
        self.vertical = '┃'     # |
        self.across = '━'       # -


    def style6(self):
        self.top_left = '┎'     # ↖
        self.top_up = '┰'       # ↑
        self.top_right = '┒'    # ↗
        self.left = '┠'         # ←
        self.center = '╂'       # ·
        self.right = '┨'        # →
        self.bottom_left = '┖'  # ↙
        self.bottom_down = '┸'  # ↓
        self.bottom_right = '┚' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style7(self):
        self.top_left = '╱'     # ↖
        self.top_up = '─'       # ↑
        self.top_right = '╲'    # ↗
        self.left = '│'         # ←
        self.center = '┼'       # ·
        self.right = '│'        # →
        self.bottom_left = '╲'  # ↙
        self.bottom_down = '─'  # ↓
        self.bottom_right = '╱' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


    def style8(self):
        self.top_left = '╓'     # ↖
        self.top_up = '╥'       # ↑
        self.top_right = '╖'    # ↗
        self.left = '╟'         # ←
        self.center = '╫'       # ·
        self.right = '╢'        # →
        self.bottom_left = '╙'  # ↙
        self.bottom_down = '╨'  # ↓
        self.bottom_right = '╜' # ↘
        self.vertical = '│'     # |
        self.across = '─'       # -


class Use(Theme):

    def echo(self):
        self.process()
        print(self.template_title())
        print(self.template_content().format(*self.title))
        print(self.template_center())
        for word in self.content:
            result = self.template_content().format(*word)
            print(result)
        print(self.template_tail())