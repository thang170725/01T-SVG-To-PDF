from pathlib import Path

import questionary

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich import print

from svg_to_pdf import from_svg_to_pdf


console = Console()


def banner():
    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]SVG → PDF Converter[/bold cyan]\n"
            "[dim]Convert multiple SVG files into one PDF[/dim]",
            border_style="cyan"
        )
    )


def convert_folder():
    folder = questionary.path(
        "SVG folder:"
    ).ask()

    if not folder:
        return

    folder_path = Path(folder)

    if not folder_path.exists():
        console.print(
            "[red]Folder not found[/red]"
        )
        return

    svg_files = sorted(
        str(f)
        for f in folder_path.glob("*.svg")
    )

    if not svg_files:
        console.print(
            "[red]No SVG files found[/red]"
        )
        return

    pdf_name = questionary.text(
        "PDF name:",
        default="output"
    ).ask()

    save_path = questionary.path(
        "Save directory:",
        default="./output"
    ).ask()

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Generating PDF...",
            total=100
        )

        output_pdf = from_svg_to_pdf(
            svg_files,
            pdf_name,
            save_path
        )

        progress.update(task, advance=100)

    console.print()
    console.print(
        f"[green]✓ Success[/green]"
    )
    console.print(
        f"[bold]{output_pdf}[/bold]"
    )


def convert_files():
    files = questionary.text(
        "SVG paths (comma separated):"
    ).ask()

    if not files:
        return

    svg_files = [
        x.strip()
        for x in files.split(",")
    ]

    pdf_name = questionary.text(
        "PDF name:",
        default="output"
    ).ask()

    save_path = questionary.path(
        "Save directory:",
        default="./output"
    ).ask()

    with Progress() as progress:
        task = progress.add_task(
            "[cyan]Generating PDF...",
            total=100
        )

        output_pdf = from_svg_to_pdf(
            svg_files,
            pdf_name,
            save_path
        )

        progress.update(task, advance=100)

    console.print()
    console.print(
        f"[green]✓ Success[/green]"
    )
    console.print(
        f"[bold]{output_pdf}[/bold]"
    )


def main():
    banner()

    while True:

        choice = questionary.select(
            "Choose an option",
            choices=[
                "📂 Convert SVG Folder",
                "📄 Convert SVG Files",
                "🚪 Exit"
            ]
        ).ask()

        if choice == "📂 Convert SVG Folder":
            convert_folder()

        elif choice == "📄 Convert SVG Files":
            convert_files()

        else:
            console.print(
                "\n[cyan]Goodbye 👋[/cyan]"
            )
            break


if __name__ == "__main__":
    main()