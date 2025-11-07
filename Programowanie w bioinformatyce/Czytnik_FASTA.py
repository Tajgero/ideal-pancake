import os
from Bio import SeqIO
from Bio import pairwise2
from Bio.PDB import PDBParser

# Słownik konwersji trójliterowego kodu aminokwasu na jednoliterowy
amino_acid_map = {
    'ALA': 'A', 'CYS': 'C', 'ASP': 'D', 'GLU': 'E', 'PHE': 'F',
    'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LYS': 'K', 'LEU': 'L',
    'MET': 'M', 'ASN': 'N', 'PRO': 'P', 'GLN': 'Q', 'ARG': 'R',
    'SER': 'S', 'THR': 'T', 'VAL': 'V', 'TRP': 'W', 'TYR': 'Y'
}

def extract_sequence_from_pdb(pdb_file):
    """
    Funkcja wyciąga sekwencję aminokwasową z pliku PDB, 
    używając PDBParser do odczytania struktury.
    """
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_file)
    sequence = ""

    # Iterowanie po modelu, łańcuchu i resztach
    for model in structure:
        for chain in model:
            for residue in chain:
                # Sprawdzamy, czy reszta jest aminokwasem (czy nie jest wodą lub innymi związkami)
                if residue.get_resname() in amino_acid_map:
                    sequence += amino_acid_map[residue.get_resname()]
    
    return sequence

def get_fasta_sequences(fasta_file):
    """
    Funkcja odczytuje sekwencje z pliku FASTA.
    """
    sequences = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences[record.id] = str(record.seq)
    return sequences

def compare_sequences(seq1, seq2): # POPRAWIĆĆĆĆĆĆĆĆ
    """
    Funkcja porównuje dwie sekwencje za pomocą dopasowania globalnego
    i oblicza procentową tożsamość między sekwencjami.
    """
    alignments = pairwise2.align.globalxx(seq1, seq2)
    best_alignment = alignments[0]

    # Liczenie tożsamości: porównanie dopasowanych elementów
    match_count = sum(1 for i in range(len(best_alignment[0])) if best_alignment[0][i] == best_alignment[1][i])
    identity = match_count / len(best_alignment[0])  # Procent tożsamości
    return identity, best_alignment

def main():
    # Przyjmowanie plików wejściowych z rozszerzeniem .pdb i .fasta
    pdb_files_input = input("Podaj pliki PDB (bez rozszerzenia), oddzielone spacją: ")
    fasta_file_input = input("Podaj nazwę pliku FASTA (bez rozszerzenia): ")

    # Dodanie rozszerzeń, jeśli użytkownik ich nie podał
    pdb_files = pdb_files_input.split()
    pdb_files = [pdb + ".pdb" if not pdb.endswith(".pdb") else pdb for pdb in pdb_files]
    fasta_file = fasta_file_input + ".fasta" if not fasta_file_input.endswith(".fasta") else fasta_file_input

    # Sprawdzanie istnienia pliku FASTA
    if not os.path.exists(fasta_file):
        print(f"Nie znaleziono pliku {fasta_file}. Upewnij się, że plik jest poprawny.")
        return

    # Iteracja po plikach PDB
    for pdb_file in pdb_files:
        if not os.path.exists(pdb_file):
            print(f"Nie znaleziono pliku {pdb_file}. Upewnij się, że plik jest poprawny.")
            continue

        try:
            # Ekstrakcja sekwencji z pliku PDB
            pdb_sequence = extract_sequence_from_pdb(pdb_file)
            print(f"\nEkstraktowana sekwencja z pliku {pdb_file} (pierwsze 50 znaków): {pdb_sequence[:50]}...")

            # Ekstrakcja sekwencji z pliku FASTA
            fasta_sequences = get_fasta_sequences(fasta_file)

            # Porównanie sekwencji z FASTA i PDB
            for record_id, fasta_sequence in fasta_sequences.items():
                identity, alignment = compare_sequences(pdb_sequence, fasta_sequence)

                # Jeśli podobieństwo większe niż 90%, wyświetlamy dopasowanie
                if identity >= 0.90:
                    print(f"\nDopasowanie sekwencji między {pdb_file} i {record_id}:")
                    print(f"Tożsamość: {identity*100:.2f}%")
                    # Używamy pairwise2.format_alignment dla lepszego formatowania
                    formatted_alignment = pairwise2.format_alignment(*alignment)
                    print(formatted_alignment)
                    
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania pliku {pdb_file}: {e}")

if __name__ == "__main__":
    main()
