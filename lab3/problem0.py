"""Problem 0: convert a DNA or RNA codon using the standard genetic code."""

# NCBI translation table 1; use U instead of the DNA base T.
# https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi#SG1
AMINO_ACID_CODONS = {
    "Phenylalanine": "UUU UUC",
    "Leucine": "UUA UUG CUU CUC CUA CUG",
    "Isoleucine": "AUU AUC AUA",
    "Methionine": "AUG",
    "Valine": "GUU GUC GUA GUG",
    "Serine": "UCU UCC UCA UCG AGU AGC",
    "Proline": "CCU CCC CCA CCG",
    "Threonine": "ACU ACC ACA ACG",
    "Alanine": "GCU GCC GCA GCG",
    "Tyrosine": "UAU UAC",
    "Histidine": "CAU CAC",
    "Glutamine": "CAA CAG",
    "Asparagine": "AAU AAC",
    "Lysine": "AAA AAG",
    "Aspartic acid": "GAU GAC",
    "Glutamic acid": "GAA GAG",
    "Cysteine": "UGU UGC",
    "Tryptophan": "UGG",
    "Arginine": "CGU CGC CGA CGG AGA AGG",
    "Glycine": "GGU GGC GGA GGG",
    "Stop": "UAA UAG UGA",
}

GENETIC_CODE = {
    codon: amino_acid
    for amino_acid, codons in AMINO_ACID_CODONS.items()
    for codon in codons.split()
}


def codon_to_amino_acid(codon):
    """Return an amino acid name, or 'Stop' for a termination codon."""
    codon = codon.strip().upper().replace("T", "U")
    if codon not in GENETIC_CODE:
        raise ValueError("A codon must contain exactly three A, C, G, U (or T) bases.")
    return GENETIC_CODE[codon]


if __name__ == "__main__":
    try:
        codon = input("Enter a DNA or RNA codon: ")
        print("Amino acid:", codon_to_amino_acid(codon))
    except ValueError as error:
        print("Error:", error)
