"""Problem 2: count all 64 RNA codons in each frame and chart the top ten."""

import argparse
import csv
from collections import Counter
from pathlib import Path

from problem0 import GENETIC_CODE, codon_to_amino_acid

ACCESSION = "NC_038311.1"
GENOME_PATH = Path(__file__).resolve().parent / f"{ACCESSION}.fasta"


def read_fasta(path):
    """Read one FASTA record."""
    lines = [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]
    if not lines or not lines[0].startswith(">"):
        raise ValueError("Expected a FASTA file starting with a > header.")
    if any(line.startswith(">") for line in lines[1:]):
        raise ValueError("Use a FASTA file containing exactly one genome record.")
    sequence = "".join(lines[1:]).upper()
    if not sequence or set(sequence) - set("ACGTURYSWKMBDHVN"):
        raise ValueError("The FASTA record must contain a nonempty DNA or RNA sequence.")
    return lines[0][1:], sequence

OUTPUT_DIR = Path(__file__).resolve().parent / "results"


def count_codons(sequence, both_strands=False):
    """Count nonoverlapping triplets at offsets 0, 1 and 2 on each chosen strand.

    Incomplete end triplets are ignored. Ambiguous triplets are skipped without
    moving the frame. Stops are counted; this is a genome scan, not ORF detection.
    """
    rna = "".join(sequence.split()).upper().replace("T", "U")
    if not rna or set(rna) - set("ACGURYSWKMBDHVN"):
        raise ValueError("Expected a nonempty DNA or RNA sequence.")
    strands = {"+": rna}
    if both_strands:
        complement = str.maketrans("ACGURYSWKMBDHVN", "UGCAYRSWMKVHDBN")
        strands["-"] = rna.translate(complement)[::-1]

    frames = {}
    skipped = {}
    for strand, bases in strands.items():
        for offset in range(3):
            frame = f"{strand}{offset + 1}"
            counts = Counter({codon: 0 for codon in GENETIC_CODE})
            skipped[frame] = 0
            for position in range(offset, len(bases) - 2, 3):
                codon = bases[position:position + 3]
                if codon in GENETIC_CODE:
                    counts[codon] += 1
                else:
                    skipped[frame] += 1
            frames[frame] = counts

    totals = Counter({codon: 0 for codon in GENETIC_CODE})
    for counts in frames.values():
        totals.update(counts)
    # Alphabetical ordering makes ties reproducible.
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return frames, skipped, ranked


def load_analysis(path=GENOME_PATH, both_strands=False):
    header, sequence = read_fasta(path)
    frames, skipped, ranked = count_codons(sequence, both_strands)
    if not sum(count for _, count in ranked):
        raise ValueError("The sequence contains no unambiguous, complete codons.")
    return header, sequence, frames, skipped, ranked


def save_frequencies(frames, ranked, output_dir):
    total = sum(count for _, count in ranked)
    columns = ["codon", "amino_acid", *frames, "total", "frequency_percent"]
    with (output_dir / "codon_frequencies.csv").open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(columns)
        for codon, count in ranked:
            writer.writerow([
                codon, codon_to_amino_acid(codon),
                *(counts[codon] for counts in frames.values()),
                count, f"{100 * count / total:.4f}",
            ])


def plot_top_ten(ranked, header, frames, output_dir, show=False):
    import matplotlib
    if not show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    top_ten = ranked[:10]
    total = sum(count for _, count in ranked)
    labels = [f"{codon}\n{codon_to_amino_acid(codon)}" for codon, _ in top_ten]
    frequencies = [100 * count / total for _, count in top_ten]
    figure, axis = plt.subplots(figsize=(14, 6))
    bars = axis.bar(labels, frequencies, color="#2878a5")
    axis.bar_label(bars, labels=[str(count) for _, count in top_ten], padding=3)
    axis.set_ylabel("Frequency (% of all valid triplets in selected frames)")
    axis.set_xlabel("RNA codon and amino acid (numbers above bars are counts)")
    axis.set_title(f"Top 10 codons: {header.split()[0]} | frames {', '.join(frames)}")
    axis.set_ylim(0, max(frequencies) * 1.2)
    figure.tight_layout()
    figure.savefig(output_dir / "top10_codons.png", dpi=160)
    if show:
        plt.show()
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fasta", type=Path, default=GENOME_PATH)
    parser.add_argument("--both-strands", action="store_true", help="Include reverse-complement frames.")
    parser.add_argument("--show", action="store_true", help="Also open the chart window.")
    args = parser.parse_args()
    try:
        header, sequence, frames, skipped, ranked = load_analysis(args.fasta, args.both_strands)
        OUTPUT_DIR.mkdir(exist_ok=True)
        save_frequencies(frames, ranked, OUTPUT_DIR)
        plot_top_ten(ranked, header, frames, OUTPUT_DIR, args.show)
    except ImportError as error:
        parser.exit(1, f"Error: {error}\nInstall the chart dependency: python -m pip install -r lab3/requirements.txt\n")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    print("Genome:", header, f"({len(sequence)} bases)")
    for frame, counts in frames.items():
        print(f"Frame {frame}: {sum(counts.values())} valid codons; {skipped[frame]} ambiguous triplets skipped")
    total = sum(count for _, count in ranked)
    print(f"\n{'Codon':<8}{'Amino acid':<18}{'Count':>8}{'Frequency':>12}")
    for codon, count in ranked[:10]:
        print(f"{codon:<8}{codon_to_amino_acid(codon):<18}{count:>8}{100 * count / total:>11.2f}%")
    print("\nAll 64 codon frequencies and the top-ten chart are saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
