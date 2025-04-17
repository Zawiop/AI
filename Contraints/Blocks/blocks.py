import sys

# Parse the input arguments
def parse_input(args):
    numbers = []
    for token in args:
        token = token.lower()  # Convert token to lowercase to handle 'X' and 'x'
        if 'x' in token:
            parts = token.split('x')
            numbers.extend([int(parts[0]), int(parts[1])])
        else:
            numbers.append(int(token))
    return numbers

def pack(container, rectangles, placements):
    if not rectangles:
        return True  # All rectangles have been placed

    for i in range(len(rectangles)):
        rect = rectangles[i]
        for (h, w) in [(rect['height'], rect['width']), (rect['width'], rect['height'])]:
            if h <= container['height'] and w <= container['width']:
                # Place the rectangle
                placed_rect = {
                    'height': h,
                    'width': w,
                    'label': rect['label'],
                    'x': container['x'],
                    'y': container['y']
                }
                placements.append(placed_rect)

                remaining_rects = rectangles[:i] + rectangles[i+1:]

                # Try both ways of splitting the remaining space
                for split_option in [1, 2]:
                    if split_option == 1:
                        # Option 1: Split horizontally (right and bottom spaces)
                        right_space = {
                            'height': container['height'],
                            'width': container['width'] - w,
                            'x': container['x'] + w,
                            'y': container['y']
                        }
                        bottom_space = {
                            'height': container['height'] - h,
                            'width': w,
                            'x': container['x'],
                            'y': container['y'] + h
                        }
                    else:
                        # Option 2: Split vertically (bottom and right spaces)
                        bottom_space = {
                            'height': container['height'] - h,
                            'width': container['width'],
                            'x': container['x'],
                            'y': container['y'] + h
                        }
                        right_space = {
                            'height': h,
                            'width': container['width'] - w,
                            'x': container['x'] + w,
                            'y': container['y']
                        }

                    spaces = []
                    if right_space['width'] > 0 and right_space['height'] > 0:
                        spaces.append(right_space)
                    if bottom_space['width'] > 0 and bottom_space['height'] > 0:
                        spaces.append(bottom_space)

                    # Recursively attempt to pack the remaining rectangles
                    if pack_into_spaces(spaces, remaining_rects, placements):
                        return True

                # Backtrack
                placements.pop()
    return False

def pack_into_spaces(spaces, rectangles, placements):
    if not rectangles:
        return True
    for space in spaces:
        if pack(space, rectangles, placements):
            return True
    return False

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: python blocks.py 8x5 4x2 4 2 2x4 2 4 4 4")
        return

    numbers = parse_input(args)
    if len(numbers) < 2:
        print("Invalid input")
        return

    container_height, container_width = numbers[0], numbers[1]
    rect_numbers = numbers[2:]

    if len(rect_numbers) % 2 != 0:
        print("Invalid number of rectangle dimensions")
        return

    # Create list of rectangles to place
    rectangles = []
    for i in range(0, len(rect_numbers), 2):
        h, w = rect_numbers[i], rect_numbers[i+1]
        rect = {
            'height': h,
            'width': w,
            'label': chr(97 + i//2)  # Labels a, b, c, etc.
        }
        rectangles.append(rect)

    # Attempt to pack rectangles
    container = {
        'height': container_height,
        'width': container_width,
        'x': 0,
        'y': 0
    }
    placements = []

    success = pack(container, rectangles, placements)

    if success:
        # Prepare the Decomposition output
        # Sort placements by y (top to bottom), then x (left to right)
        placements.sort(key=lambda r: (r['y'], r['x']))
        print("Decomposition:", end=' ')
        for rect in placements:
            print(f"{rect['height']}x{rect['width']}", end=' ')
        print()
    else:
        print("No solution")

if __name__ == "__main__":
    main()
