import pygame # type: ignore
import random

pygame.init()
font = pygame.font.Font(pygame.font.get_default_font(), 36)

class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GRAY = 128, 128, 128
    LIGHT_LAVENDER = 190, 149, 196
    SORTING_BAR = 183, 9, 76
    SORTED_BAR = 0, 145, 173

    BACKGROUND = WHITE

    BLOCK_COLORS = [(159, 134, 192), (94,84,182)]

    FONT = pygame.font.SysFont('Helvetica', 30)
    FONT_HEADING = pygame.font.SysFont('Helvetica', 40)

    SIDE_PADDING = 80
    TOP_PADDING = 200

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.min = min(list)
        self.max = max(list)
        
        self.bar_width = round((self.width - self.SIDE_PADDING) / len(list))
        self.bar_height = (self.height - self.TOP_PADDING) // (self.max - self.min)
        self.starting_x = self.SIDE_PADDING // 2

def generate_list(n, min, max): #min and max inclusive
    list = []
    for _ in range(n):
        list.append(random.randint(min, max))
    
    return list

def draw_gui(draw_info):
    draw_info.window.fill(draw_info.BACKGROUND)

    controls = draw_info.FONT.render("R : Reset | SPACE : Sort | UP/DOWN : Adjust tick rate", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width / 2 - controls.get_width() / 2, 5))
    sorting_controls = draw_info.FONT.render("I : Insertion sort | B : Bubble Sort",1, draw_info.LIGHT_LAVENDER)
    draw_info.window.blit(sorting_controls,(draw_info.width / 2 - sorting_controls.get_width() / 2, 40))

    draw_list(draw_info)

    pygame.display.update()

def draw_list(draw_info, color_pos = {}, clear_bg = False):
    list = draw_info.list

    if clear_bg:
        clear_rect = (draw_info.SIDE_PADDING // 2, draw_info.TOP_PADDING, draw_info.width - draw_info.SIDE_PADDING, draw_info.height - draw_info.TOP_PADDING)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND, clear_rect)

    for i, val in enumerate(list):
        x = draw_info.starting_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min) * draw_info.bar_height

        color = draw_info.BLOCK_COLORS[i % 2]

        if i in color_pos:
            color = color_pos[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height))

    if clear_bg:
        pygame.display.update()




def bubble_sort(draw_info):
    list = draw_info.list

    for n in range(len(list) - 1):
        for i in range(len(list) - 1 - n):
            num1 = list[i]
            num2 = list[i + 1]
            if num1 > num2:
                list[i], list[i+1] = list[i+1], list[i]
                draw_list(draw_info, {i:draw_info.SORTING_BAR, i+1:draw_info.SORTED_BAR}, True)
                yield True
    
    return list

def insertion_sort(draw_info):
    list = draw_info.list

    for i in range(1, len(list)):  # Iterate over the array starting from the second element
        key = list[i]  # Store the current element as the key to be inserted in the right position
        j = i-1
        while j >= 0 and key < list[j]:  # Move elements greater than key one position ahead
            list[j+1] = list[j]  # Shift elements to the right
            j -= 1
        list[j+1] = key  # Insert the key in the correct position
        draw_list(draw_info, {j:draw_info.SORTING_BAR, j+1:draw_info.SORTED_BAR}, True)
        yield True

    return list


def main():
    running = True
    clock = pygame.time.Clock()
    n = 50
    min_gen = 1
    max_gen = 50
    tick_rate = 30
    sort_state = False
    sort_algo = bubble_sort
    generator = None
    
    

    draw_info = DrawInfo(800, 600, generate_list(n, min_gen, max_gen)) # instantiates window

    while running:
        clock.tick(tick_rate)

        if sort_state:
            try:
                next(generator)
            except StopIteration:
                sort_state = False
        else:
            draw_gui(draw_info)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                list = generate_list(n, min_gen, max_gen)
                draw_info.set_list(list)
                sort_state = False
            elif event.key == pygame.K_SPACE and sort_state == False:
                sort_state = True
                generator = sort_algo(draw_info)
            elif event.key == pygame.K_UP:
                if event.mod == pygame.KMOD_NONE:
                    tick_rate += 5
                else:
                    n += 5
                    max_gen += 5
            elif event.key == pygame.K_DOWN:
                if event.mod == pygame.KMOD_NONE:
                 if tick_rate >= 10:
                        tick_rate -= 5
                else:
                    if n > 5:
                        n -= 5
                        max_gen -= 5
            elif event.key == pygame.K_b:
                sort_algo = bubble_sort
            elif event.key == pygame.K_i:
                sort_algo = insertion_sort






    pygame.quit()


if __name__ == "__main__":
    main()
