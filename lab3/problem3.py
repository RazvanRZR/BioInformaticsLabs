"""Problem 3: build an LLM prompt from the actual top-ten codon frequencies."""

import argparse
import os
from pathlib import Path

from problem0 import codon_to_amino_acid
from problem2 import GENOME_PATH, OUTPUT_DIR, load_analysis

DEFAULT_MODEL = "gpt-6-luna"


def load_env_file(path):
    """Load simple KEY=value entries from .env without exposing them in source."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file(Path(__file__).resolve().parent / ".env")


def build_prompt(header, frames, ranked):
    total = sum(count for _, count in ranked)
    top_ten = ranked[:10]
    rows = [
        f"{codon}: {count} occurrences ({100 * count / total:.2f}%) -> {codon_to_amino_acid(codon)}"
        for codon, count in top_ten
    ]
    amino_acids = sorted({codon_to_amino_acid(codon) for codon, _ in top_ten} - {"Stop"})
    return (
        f"This is an educational bioinformatics exercise. Genome: {header}.\n"
        f"Frames scanned: {', '.join(frames)}. Counts are pooled across these frames; "
        "they are genome triplet counts, not measured protein expression.\n\n"
        "The ten most frequent RNA codons and their standard-code mappings are:\n"
        + "\n".join(rows)
        + "\n\nUnique amino acids: " + ", ".join(amino_acids)
        + ".\n\nMake a list of foods containing the lowest amounts of these amino acids. "
        "Compare on a per-100-g edible-food basis. Cover every unique amino acid, "
        "group synonymous codons, and do not treat Stop as an amino acid. "
        "Use reliable food-composition sources, such as USDA FoodData Central, "
        "and cite the food records. Give numerical amounts only when supported "
        "by those records; missing nutrient data is not zero. If an exact ranking "
        "cannot be established, give a clearly labelled qualitative list and "
        "explain the limitation. Do not infer dietary requirements or antiviral "
        "benefits from viral codon frequencies.\n"
    )


def ask_openai(prompt, model):
    """Send the generated prompt directly to OpenAI's Responses API."""
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY is not set. Set it in your environment before running problem3.py.")
    try:
        from openai import OpenAI
    except ImportError as error:
        raise ValueError("The OpenAI package is missing. Run: python -m pip install -r lab3/requirements.txt") from error

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model=model,
        instructions="You are helping with a university bioinformatics laboratory. Be concise, accurate, and clearly label assumptions.",
        input=prompt,
    )
    if not response.output_text:
        raise ValueError("The OpenAI API returned an empty response.")
    return response.output_text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fasta", type=Path, default=GENOME_PATH)
    parser.add_argument("--both-strands", action="store_true")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", DEFAULT_MODEL), help=f"OpenAI model (default: {DEFAULT_MODEL}).")
    args = parser.parse_args()
    try:
        header, _, frames, _, ranked = load_analysis(args.fasta, args.both_strands)
        prompt = build_prompt(header, frames, ranked)
        OUTPUT_DIR.mkdir(exist_ok=True)
        prompt_path = OUTPUT_DIR / "llm_prompt.txt"
        prompt_path.write_text(prompt, encoding="utf-8")
        response = ask_openai(prompt, args.model)
        response_path = OUTPUT_DIR / "llm_response.txt"
        response_path.write_text(f"Model: {args.model}\n\n{response}\n", encoding="utf-8")
        print("LLM response:\n", response)
        print("Prompt saved to:", prompt_path)
        print("Response saved to:", response_path)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")


if __name__ == "__main__":
    main()
