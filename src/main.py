"""
My Fitness Pal - Fitness Tracking App with Exercise Progression

A CLI application for tracking workouts and progressing through exercise levels.
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn
from rich import box

from .services import ProgressionService, WorkoutService
from .data import ALL_PROGRESSIONS

# Initialize app and services
app = typer.Typer(
    name="fitness",
    help="Fitness tracking app with exercise progression system",
)
console = Console()

# Global services (in production, use dependency injection)
progression_service = ProgressionService()
workout_service = WorkoutService(progression_service)

# Default user (in production, implement proper user management)
DEFAULT_USER = "default_user"


def init_services() -> None:
    """Initialize services with exercise data."""
    for chain in ALL_PROGRESSIONS:
        progression_service.register_chain(chain)


@app.command()
def progressions() -> None:
    """List all available progression chains."""
    init_services()

    table = Table(
        title="📈 Available Progression Chains",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("ID", style="dim")
    table.add_column("Name")
    table.add_column("Name (PL)", style="italic")
    table.add_column("Levels", justify="center")
    table.add_column("Description")

    for chain in progression_service.get_all_chains():
        table.add_row(
            chain.id,
            chain.name,
            chain.name_pl or "-",
            str(chain.total_levels),
            chain.description[:50] + "..." if len(chain.description) > 50 else chain.description,
        )

    console.print(table)


@app.command()
def show(chain_id: str) -> None:
    """Show all exercises in a progression chain."""
    init_services()

    chain = progression_service.get_chain(chain_id)
    if not chain:
        console.print(f"[red]Progression chain '{chain_id}' not found.[/red]")
        raise typer.Exit(1)

    console.print(Panel(
        f"[bold]{chain.name}[/bold]\n"
        f"[italic]{chain.name_pl or ''}[/italic]\n\n"
        f"{chain.description}",
        title="Progression Chain",
        box=box.ROUNDED,
    ))

    table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    table.add_column("Level", justify="center", style="cyan")
    table.add_column("Exercise")
    table.add_column("Name (PL)", style="italic")
    table.add_column("Difficulty", justify="center")
    table.add_column("Sets x Reps", justify="center")

    for exercise in chain.exercises:
        difficulty_bar = "█" * exercise.difficulty.value + "░" * (10 - exercise.difficulty.value)
        table.add_row(
            str(exercise.progression_order + 1),
            exercise.name,
            exercise.name_pl or "-",
            f"[{'green' if exercise.difficulty.value <= 3 else 'yellow' if exercise.difficulty.value <= 6 else 'red'}]{difficulty_bar}[/]",
            f"{exercise.default_sets} x {exercise.default_reps}",
        )

    console.print(table)


@app.command()
def start(chain_id: str) -> None:
    """Start tracking a progression chain."""
    init_services()

    chain = progression_service.get_chain(chain_id)
    if not chain:
        console.print(f"[red]Progression chain '{chain_id}' not found.[/red]")
        raise typer.Exit(1)

    progression = progression_service.start_chain(DEFAULT_USER, chain_id)
    if progression:
        first_exercise = chain.get_first_exercise()
        console.print(Panel(
            f"[green]Started progression: {chain.name}[/green]\n\n"
            f"Your first exercise: [bold]{first_exercise.name}[/bold]\n"
            f"({first_exercise.name_pl})\n\n"
            f"[dim]Target: {first_exercise.default_sets} sets x {first_exercise.default_reps} reps[/dim]",
            title="🎯 Progression Started!",
            box=box.ROUNDED,
        ))
    else:
        console.print("[red]Failed to start progression.[/red]")


@app.command()
def status(chain_id: str) -> None:
    """Show your current status in a progression chain."""
    init_services()

    # Ensure user has started the chain
    if not progression_service.get_user_progression(DEFAULT_USER, chain_id):
        progression_service.start_chain(DEFAULT_USER, chain_id)

    status_data = progression_service.get_progression_status(DEFAULT_USER, chain_id)
    if not status_data:
        console.print(f"[red]Progression chain '{chain_id}' not found.[/red]")
        raise typer.Exit(1)

    current = status_data["current_exercise"]
    next_ex = status_data["next_exercise"]

    # Progress bar
    progress_pct = (status_data["current_level"] / status_data["total_levels"]) * 100

    console.print(Panel(
        f"[bold cyan]{status_data['chain_name']}[/bold cyan]\n\n"
        f"[bold]Current Exercise:[/bold] {current.name}\n"
        f"[italic]({current.name_pl})[/italic]\n\n"
        f"[bold]Level:[/bold] {status_data['current_level']} / {status_data['total_levels']}\n\n"
        f"[bold]Your Progress:[/bold]\n"
        f"  Best Reps: {status_data['best_reps']} / {status_data['reps_to_progress']} needed\n"
        f"  Best Sets: {status_data['best_sets']} / {status_data['sets_to_progress']} needed\n"
        f"  Workouts at this level: {status_data['total_workouts_at_level']}\n\n"
        f"[bold]Can Progress:[/bold] {'[green]YES![/green]' if status_data['can_progress'] else '[yellow]Not yet[/yellow]'}\n\n"
        + (f"[bold]Next Exercise:[/bold] {next_ex.name} ({next_ex.name_pl})" if next_ex else "[green]🏆 You've mastered this progression![/green]"),
        title=f"📊 Progress: {progress_pct:.0f}%",
        box=box.ROUNDED,
    ))


@app.command()
def record(
    chain_id: str,
    sets: int = typer.Option(..., "--sets", "-s", help="Number of sets completed"),
    reps: int = typer.Option(..., "--reps", "-r", help="Number of reps per set"),
) -> None:
    """Record a workout performance for a progression."""
    init_services()

    # Ensure user has started the chain
    if not progression_service.get_user_progression(DEFAULT_USER, chain_id):
        progression_service.start_chain(DEFAULT_USER, chain_id)

    can_progress, message = progression_service.record_performance(
        DEFAULT_USER, chain_id, sets, reps
    )

    color = "green" if can_progress else "yellow"
    console.print(Panel(
        f"[{color}]{message}[/{color}]",
        title="💪 Workout Recorded!",
        box=box.ROUNDED,
    ))

    if can_progress:
        if typer.confirm("Would you like to progress to the next exercise?"):
            progress_cmd(chain_id)


@app.command("progress")
def progress_cmd(chain_id: str) -> None:
    """Progress to the next exercise in a chain."""
    init_services()

    success, message = progression_service.progress_user(DEFAULT_USER, chain_id)

    if success:
        console.print(Panel(
            f"[green]{message}[/green]",
            title="🎉 Level Up!",
            box=box.ROUNDED,
        ))
    else:
        console.print(f"[red]{message}[/red]")


@app.command()
def regress(chain_id: str) -> None:
    """Go back to the previous exercise in a chain."""
    init_services()

    success, message = progression_service.regress_user(DEFAULT_USER, chain_id)

    if success:
        console.print(Panel(
            f"[yellow]{message}[/yellow]",
            title="↩️ Level Down",
            box=box.ROUNDED,
        ))
    else:
        console.print(f"[red]{message}[/red]")


@app.command()
def exercise(exercise_id: str) -> None:
    """Show detailed information about a specific exercise."""
    init_services()

    # Find the exercise
    found_exercise = None
    for chain in progression_service.get_all_chains():
        for ex in chain.exercises:
            if ex.id == exercise_id:
                found_exercise = ex
                break
        if found_exercise:
            break

    if not found_exercise:
        console.print(f"[red]Exercise '{exercise_id}' not found.[/red]")
        raise typer.Exit(1)

    ex = found_exercise

    # Build tips list
    tips_text = "\n".join(f"  • {tip}" for tip in ex.tips) if ex.tips else "  None"
    mistakes_text = "\n".join(f"  • {m}" for m in ex.common_mistakes) if ex.common_mistakes else "  None"

    console.print(Panel(
        f"[bold]{ex.name}[/bold]\n"
        f"[italic]{ex.name_pl or ''}[/italic]\n\n"
        f"[bold]Description:[/bold]\n  {ex.description}\n\n"
        f"[bold]Muscle Groups:[/bold] {', '.join(mg.value for mg in ex.muscle_groups)}\n"
        f"[bold]Difficulty:[/bold] {'█' * ex.difficulty.value}{'░' * (10 - ex.difficulty.value)} ({ex.difficulty.name})\n\n"
        f"[bold]Default:[/bold] {ex.default_sets} sets x {ex.default_reps} reps"
        + (f" ({ex.default_hold_seconds}s hold)" if ex.default_hold_seconds else "") + "\n\n"
        f"[bold cyan]Tips:[/bold cyan]\n{tips_text}\n\n"
        f"[bold red]Common Mistakes:[/bold red]\n{mistakes_text}",
        title=f"🏋️ {ex.name}",
        box=box.ROUNDED,
    ))


@app.command()
def workout(
    name: str = typer.Option("Quick Workout", "--name", "-n", help="Workout name"),
    chains: str = typer.Option(..., "--chains", "-c", help="Comma-separated chain IDs"),
) -> None:
    """Create a workout using your current progression levels."""
    init_services()

    chain_ids = [c.strip() for c in chains.split(",")]

    # Ensure user has started all chains
    for chain_id in chain_ids:
        if not progression_service.get_user_progression(DEFAULT_USER, chain_id):
            progression_service.start_chain(DEFAULT_USER, chain_id)

    workout_obj = workout_service.create_progression_workout(
        name=name,
        user_id=DEFAULT_USER,
        chain_ids=chain_ids,
    )

    if not workout_obj:
        console.print("[red]Failed to create workout. Check chain IDs.[/red]")
        raise typer.Exit(1)

    table = Table(
        title=f"🏋️ {workout_obj.name}",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )
    table.add_column("#", justify="center", style="dim")
    table.add_column("Exercise")
    table.add_column("Name (PL)", style="italic")
    table.add_column("Sets x Reps", justify="center")

    for i, we in enumerate(workout_obj.exercises, 1):
        table.add_row(
            str(i),
            we.exercise.name,
            we.exercise.name_pl or "-",
            f"{we.planned_sets} x {we.planned_reps}",
        )

    console.print(table)
    console.print(f"\n[dim]Workout ID: {workout_obj.id}[/dim]")


def main() -> None:
    """Entry point for the application."""
    app()


if __name__ == "__main__":
    main()
