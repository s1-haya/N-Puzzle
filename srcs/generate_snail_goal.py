
def generate_snail_goal(size: int) -> tuple[int, ...]:
    """Generate an N x N snail-shaped goal state."""
    if size < 3:
        raise ValueError("Board size must be at least 3")

    board = [[0] * size for _ in range(size)]

    top, bottom = 0, size - 1
    left, right = 0, size - 1
    number = 1

    while top <= bottom and left <= right:
        # Move right
        for col in range(left, right + 1):
            board[top][col] = number
            number += 1
        top += 1

        # Move down
        for row in range(top, bottom + 1):
            board[row][right] = number
            number += 1
        right -= 1

        # Move left
        if top <= bottom:
            for col in range(right, left - 1, -1):
                board[bottom][col] = number
                number += 1
            bottom -= 1

        # Move up
        if left <= right:
            for row in range(bottom, top - 1, -1):
                board[row][left] = number
                number += 1
            left += 1

    return tuple(
        0 if value == size * size else value
        for row in board
        for value in row
    )
