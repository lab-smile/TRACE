def progress_bar(current: int, total: int, bar_length: int = 20, verbose: bool = False) -> None:
    """
    Display a progress bar in the console.

    Args:
        current (int): Current progress value.
        total (int): Total value representing 100% progress.
        bar_length (int, optional): Length of the progress bar in characters. Defaults to 20.
        verbose (bool, optional): If True, always print a newline. Defaults to False.
    """
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total or verbose else '\r'
    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)