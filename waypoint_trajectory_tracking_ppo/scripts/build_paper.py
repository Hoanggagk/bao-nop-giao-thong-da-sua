from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PARTS = [
    "frontmatter/title_authors.md",
    "frontmatter/abstract.md",
    "frontmatter/keywords.md",
    "sections/01_introduction.md",
    "sections/02_problem_formulation.md",
    "sections/03_ppo_controller_design.md",
    "sections/04_simulation_setup.md",
    "sections/05_results_discussion.md",
    "sections/06_conclusion.md",
    "references/references.md",
]


def main() -> None:
    chunks = []
    for relative_path in PARTS:
        path = PROJECT_ROOT / relative_path
        content = path.read_text(encoding="utf-8").strip()
        # Component files live one directory below the project root. The built
        # paper lives at the root, so media links need one fewer parent hop.
        content = content.replace("../assets/", "assets/")
        chunks.append(content)

    output = PROJECT_ROOT / "paper.md"
    output.write_text("\n\n".join(chunks) + "\n", encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
