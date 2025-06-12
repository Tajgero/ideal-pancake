def get_dna_sequence():
    dna = input("Wprowadź sekwencję DNA: ").upper()
    return dna

def is_valid_dna(dna):
    return all(nucleotide in 'ATCG' for nucleotide in dna)

def calculate_nucleotide_percentage(dna):
    length = len(dna)
    counts = {nucleotide: dna.count(nucleotide) for nucleotide in 'ATCG'}
    percentages = {nucleotide: (count / length) * 100 for nucleotide, count in counts.items()}
    return percentages

def reverse_dna(dna):
    return dna[::-1]

def transcribe_dna_to_rna(dna):
    return dna.replace('T', 'U')

def find_subsequence_occurrences(dna, subseq):
    positions = [i for i in range(len(dna) - len(subseq) + 1) if dna[i:i+len(subseq)] == subseq]
    return positions

def get_complementary_dna(dna):
    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return ''.join([complement[nucleotide] for nucleotide in dna])

def main():
    dna = get_dna_sequence()
    
    if not is_valid_dna(dna):
        print("Sekwencja DNA zawiera niepoprawne znaki.")
        return
    
    print("\nProcentowy udział nukleotydów:")
    percentages = calculate_nucleotide_percentage(dna)
    for nucleotide, percentage in percentages.items():
        print(f"{nucleotide}: {percentage:.2f}%")
    
    reversed_dna = reverse_dna(dna)
    print(f"\nOdwrócona sekwencja DNA: {reversed_dna}")
    
    rna = transcribe_dna_to_rna(dna)
    print(f"\nSekwencja RNA: {rna}")
    
    subseq = input("Wprowadź podsekwencję do wyszukania: ").upper()
    positions = find_subsequence_occurrences(dna, subseq)
    print(f"\nPodsekwencja '{subseq}' występuje na pozycjach: {positions}")
    
    complementary_dna = get_complementary_dna(dna)
    print(f"\nKomplementarna sekwencja DNA: {complementary_dna}")

if __name__ == "__main__":
    main()
