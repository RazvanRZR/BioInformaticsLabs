# Lab 3

The project is organized as one file per exercise:

- `problem0.py` converts a DNA/RNA codon to its amino acid.
- `problem1.py` is intentionally empty. Exercise 1 is the NCBI search task;
  the selected complete genome is already saved as `NC_038311.1.fasta`.
- `problem2.py` counts codons in the three reading frames and creates the chart.
- `problem3.py` builds the prompt and sends it automatically to the OpenAI API.

The example is Human rhinovirus 1 strain ATCC VR-1559, a complete rhinovirus
genome associated with the common cold. The NCBI record is
[NC_038311.1](https://www.ncbi.nlm.nih.gov/nuccore/NC_038311.1).

Install dependencies from the repository root:

```powershell
python -m pip install -r lab3/requirements.txt
```

Run the first three exercises:

```powershell
python lab3/problem0.py
python lab3/problem2.py
```

For problem 3, copy `.env.example` to `.env` and replace the placeholder with
your OpenAI API key. The `.env` file is ignored by Git. Then run:

```powershell
python lab3/problem3.py
```

The script automatically calculates the top ten codons, creates the prompt,
sends it to `gpt-6-luna`, prints the answer, and saves both files in `lab3/results`.
You do not need to copy or paste the prompt. You can change the model with
`OPENAI_MODEL` in `.env` or with `--model`, for example:

```powershell
python lab3/problem3.py --model gpt-6-luna
```

The OpenAI API key is read from `OPENAI_API_KEY`; it is never written into the
Python source. OpenAI's official documentation describes `gpt-6-luna` as its
efficient model for focused, high-volume tasks and recommends keeping API keys
in environment variables.

Problem 2 accepts `--fasta path/to/another.fasta` for another complete genome and
`--both-strands` to include reverse-complement frames. It scans offsets 0, 1 and
2, skips incomplete final triplets, and sorts all 64 codons by frequency. The
CSV and PNG chart are saved in `lab3/results`.

Problem 3 accepts the same FASTA options. It saves the generated prompt as
`results/llm_prompt.txt` and the API answer as `results/llm_response.txt`.

The program analyses nucleotide triplets for a classroom exercise. It does not
diagnose or treat the common cold, and codon frequency does not imply a medical
or dietary recommendation.
