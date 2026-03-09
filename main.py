import random
import time

# ── Constants ──────────────────────────────────────────────────────────────
SEPARATOR = "-----------------------------------------------"
CODE_LENGTH = 4


# ── Secret number generation ───────────────────────────────────────────────
def generate_secret() -> str:
    """Generate a random 4-digit number with unique digits, not starting with 0."""
    digits = random.sample(range(0, 10), CODE_LENGTH)
    while digits[0] == 0:
        random.shuffle(digits)
    return "".join(str(d) for d in digits)


# ── Input validation ───────────────────────────────────────────────────────
def validate_guess(guess: str) -> str | None:
    """
    Validate the player's guess.
    Returns an error message string if invalid, or None if valid.
    """
    if len(guess) != CODE_LENGTH:
        return f"Your number must have exactly {CODE_LENGTH} digits."
    if not guess.isdigit():
        return "Your number must contain digits only."
    if guess[0] == "0":
        return "Your number must not start with zero."
    if len(set(guess)) != CODE_LENGTH:
        return "Your number must have unique digits (no repeats)."
    return None


# ── Bulls & Cows evaluation ────────────────────────────────────────────────
def evaluate_guess(secret: str, guess: str) -> tuple[int, int]:
    """
    Compare guess to secret and return (bulls, cows).
    Bulls = correct digit in correct position.
    Cows  = correct digit in wrong position.
    """
    bulls = sum(s == g for s, g in zip(secret, guess))
    cows = sum(g in secret for g in guess) - bulls
    return bulls, cows


# ── Formatting helpers ─────────────────────────────────────────────────────
def plural(count: int, word: str) -> str:
    """Return 'count word' or 'count words' depending on count."""
    if count == 1:
        return f"{count} {word}"
    suffix = "es" if word.endswith(("s", "sh", "ch", "x", "z")) else "s"
    return f"{count} {word}{suffix}"


def format_result(bulls: int, cows: int) -> str:
    """Format the bulls/cows result line."""
    return f"{plural(bulls, 'bull')}, {plural(cows, 'cow')}"


def format_duration(seconds: float) -> str:
    """Convert seconds to a human-readable mm:ss string."""
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    if minutes:
        return f"{minutes} min {secs} sec"
    return f"{secs} sec"


# ── UI helpers ─────────────────────────────────────────────────────────────
def print_separator() -> None:
    print(SEPARATOR)


def print_intro() -> None:
    """Print the welcome banner."""
    print("\nHi there!")
    print_separator()
    print("I've generated a random 4 digit number for you.")
    print("Let's play a bulls and cows game.")
    print_separator()


# ── Single game loop ───────────────────────────────────────────────────────
def play_game() -> int:
    """
    Run one full game.
    Returns the number of guesses it took to win.
    """
    secret = generate_secret()
    guesses = 0
    start_time = time.time()

    print("Enter a number:")
    print_separator()

    while True:
        guess = input(">>> ").strip()

        error = validate_guess(guess)
        if error:
            print(error)
            print_separator()
            continue

        guesses += 1
        bulls, cows = evaluate_guess(secret, guess)

        if bulls == CODE_LENGTH:
            elapsed = time.time() - start_time
            print(
                f"Correct, you've guessed the right number\n"
                f"in {plural(guesses, 'guess')}!"
            )
            print_separator()
            print(f"Time: {format_duration(elapsed)}")
            print("That's amazing!")
            print_separator()
            return guesses

        print(format_result(bulls, cows))
        print_separator()


# ── Statistics ─────────────────────────────────────────────────────────────
def update_stats(stats: list[int], guesses: int) -> list[int]:
    """Append the latest guess count and return updated stats list."""
    return stats + [guesses]


def print_stats(stats: list[int]) -> None:
    """Print a summary of all played games."""
    if not stats:
        return
    print(f"Games played : {len(stats)}")
    print(f"Best game    : {min(stats)} guess(es)")
    print(f"Average      : {sum(stats) / len(stats):.1f} guess(es)")
    print_separator()


# ── Main entry point ───────────────────────────────────────────────────────
def main() -> None:
    """Main loop — keep playing until the user quits."""
    print_intro()
    stats: list[int] = []

    while True:
        guesses = play_game()
        stats = update_stats(stats, guesses)

        print_stats(stats)
        again = input("Play again? (y/n): ").strip().lower()
        print_separator()
        if again != "y":
            print("Thanks for playing. Goodbye!")
            print_separator()
            break
        print_intro()


if __name__ == "__main__":
    main()
