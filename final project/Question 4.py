import pygame
pygame.init()
mouse_clicked = False  # Flag variable to track the click event

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_clicked:
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)
                if mouse_pos[1] in range(600, 695) and mouse_pos[0] in range(245, 340):
                    print("Clicked within the specified range")
                mouse_clicked = True  # Set the flag to True after the first click

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_clicked = False