import pygame
import sys
from engine.game_engine import GameEngine

NODE_RADIUS = 15
SCREEN_SIZE = 500
SCREEN_MARGIN = 25 + NODE_RADIUS

def get_transform(nodes, screen_width, screen_height, margin):
    if not nodes:
        return 1, margin, margin

    min_x = min(node.position.x for node in nodes)
    max_x = max(node.position.x for node in nodes)
    min_y = min(node.position.y for node in nodes)
    max_y = max(node.position.y for node in nodes)

    map_w = max_x - min_x
    map_h = max_y - min_y

    if map_w == 0: map_w = 1
    if map_h == 0: map_h = 1

    usable_w = screen_width - 2 * margin
    usable_h = screen_height - 2 * margin

    scale = min(usable_w / map_w, usable_h / map_h)

    offset_x = margin + (usable_w - map_w * scale) / 2 - min_x * scale
    offset_y = margin + (usable_h - map_h * scale) / 2 - min_y * scale

    return scale, offset_x, offset_y

def draw_nodes(screen, nodes: list, scale: float, offset_x: float, offset_y: float, font):
    for node in nodes:
        pos = (int(node.position.x * scale + offset_x), int(node.position.y * scale + offset_y))
        color = (200, 200, 200) if node.owner is None else node.owner.color

        pygame.draw.circle(screen, color, pos, NODE_RADIUS)
        pygame.draw.circle(screen, (0, 0, 0), pos, NODE_RADIUS, 2)

        text_surface = font.render(str(int(node.combat_power)), True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

def draw_connections(screen, nodes: list, scale: float, offset_x: float, offset_y: float):
    drawn_pairs = set()
    for node in nodes:
        for neighbor in node.connected_nodes:
            pair = tuple(sorted((node.id, neighbor.id)))
            if pair not in drawn_pairs:
                pos1 = (int(node.position.x * scale + offset_x), int(node.position.y * scale + offset_y))
                pos2 = (int(neighbor.position.x * scale + offset_x), int(neighbor.position.y * scale + offset_y))
                
                pygame.draw.line(screen, (100, 100, 100), pos1, pos2, 2)
                drawn_pairs.add(pair)

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE), pygame.RESIZABLE)
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 14, bold=True)

running = True
engine = GameEngine()
engine.start()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    running = engine.update()

    screen.fill((30, 30, 30))

    w, h = screen.get_size()
    scale, offset_x, offset_y = get_transform(engine.map_manager.nodes, w, h, SCREEN_MARGIN)

    draw_connections(screen, engine.map_manager.nodes, scale, offset_x, offset_y)
    draw_nodes(screen, engine.map_manager.nodes, scale, offset_x, offset_y, FONT)

    pygame.display.flip()
    clock.tick(60)