"""
Score generation example for Antescofo Python interface.

This example demonstrates how to:
- Create Antescofo scores programmatically
- Use the ScoreBuilder for fluent score construction
- Save scores to files
"""

from antescofo import ScoreFile, ScoreBuilder


def example_basic_score():
    """Create a basic score using ScoreFile."""
    score = ScoreFile()

    # Add a comment
    score.add_comment("My First Antescofo Score")
    score.add_comment("Generated with Python")

    # Add some events and actions
    score.add_event("NOTE", 1.0, "C4 60")
    score.add_action('print "Hello from C4"')

    score.add_event("NOTE", 0.5, "D4 62")
    score.add_action('print "Hello from D4"')

    score.add_event("NOTE", 0.5, "E4 64")
    score.add_action('print "Hello from E4"')

    score.add_event("NOTE", 1.0, "F4 65")
    score.add_action('print "Hello from F4"')

    # Print the score
    print("Generated Score:")
    print("=" * 50)
    print(score)
    print("=" * 50)

    # Save to file
    score.save("generated_score.asco.txt")
    print("\nSaved to generated_score.asco.txt")


def example_score_builder():
    """Create a score using the builder pattern."""
    builder = (
        ScoreBuilder()
        .comment("Score built with ScoreBuilder")
        .comment("A simple melody")
        # Add events with actions
        .event("NOTE", 1.0, "C4 60")
        .action('$tempo := 120')
        .action('print "Starting melody"')
        # Another event
        .event("NOTE", 0.5, "E4 64")
        .action('print "E4"')
        # Another event
        .event("NOTE", 0.5, "G4 67")
        .action('print "G4"')
        # Final event
        .event("NOTE", 1.0, "C5 72")
        .action('print "Finished!"')
    )

    # Print the score
    print("Built Score:")
    print("=" * 50)
    print(builder)
    print("=" * 50)

    # Save to file
    builder.save("builder_score.asco.txt")
    print("\nSaved to builder_score.asco.txt")


def example_with_inserts():
    """Create a score that includes other files."""
    # Create a library file
    library = ScoreFile()
    library.add_comment("Library functions")
    library.append("@fun_def my_function($x) { print $x }")
    library.save("library.asco.txt")

    # Create main score that includes the library
    main = ScoreBuilder()
    main.comment("Main score")
    main.insert_once("library.asco.txt")
    main.raw("")  # Empty line
    main.event("NOTE", 1.0, "C4 60")
    main.action("my_function(42)")

    print("Main Score with Include:")
    print("=" * 50)
    print(main)
    print("=" * 50)

    main.save("main_score.asco.txt")
    print("\nSaved to main_score.asco.txt")


def example_conditional():
    """Create a score with conditional compilation."""
    score = ScoreFile()
    score.add_comment("Score with conditionals")

    # Add a conditional block
    score.add_conditional(
        "@configuration_arch == \"darwin\"",
        'print "Running on macOS"',
        'print "Not running on macOS"',
    )

    score.add_event("NOTE", 1.0, "C4 60")

    print("Score with Conditional:")
    print("=" * 50)
    print(score)
    print("=" * 50)

    score.save("conditional_score.asco.txt")


def example_complex_score():
    """Create a more complex score."""
    builder = ScoreBuilder()

    # Header
    builder.comment("Complex Score Example")
    builder.comment("Demonstrates various Antescofo features")
    builder.raw("")

    # Insert libraries
    builder.comment("Include libraries")
    # builder.insert_once("stdlib.asco.txt")
    builder.raw("")

    # Variables
    builder.raw("; Initialize variables")
    builder.raw("@global $my_tempo := 120")
    builder.raw("@global $counter := 0")
    builder.raw("")

    # Define a function
    builder.raw("; Define a function")
    builder.raw("@fun_def increment_counter() {")
    builder.raw("    $counter := $counter + 1")
    builder.raw('    print "Counter: " $counter')
    builder.raw("}")
    builder.raw("")

    # Events
    builder.comment("Score events")
    for i, (note, duration) in enumerate(
        [("C4 60", 1.0), ("D4 62", 1.0), ("E4 64", 1.0), ("F4 65", 2.0)]
    ):
        builder.event("NOTE", duration, note)
        builder.action("increment_counter()")
        if i == 0:
            builder.action(f"$my_tempo := {120 + i * 10}")

    print("Complex Score:")
    print("=" * 50)
    print(builder)
    print("=" * 50)

    builder.save("complex_score.asco.txt")
    print("\nSaved to complex_score.asco.txt")


if __name__ == "__main__":
    print("Score Generation Examples\n")

    print("\n1. Basic Score")
    print("-" * 50)
    example_basic_score()

    print("\n2. Score Builder")
    print("-" * 50)
    example_score_builder()

    print("\n3. Score with Includes")
    print("-" * 50)
    example_with_inserts()

    print("\n4. Score with Conditionals")
    print("-" * 50)
    example_conditional()

    print("\n5. Complex Score")
    print("-" * 50)
    example_complex_score()
