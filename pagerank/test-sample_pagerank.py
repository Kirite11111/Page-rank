import sys

from pagerank import crawl, sample_pagerank, transition_model

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    # Vérification de la somme des ranks
    total_rank = sum(ranks.values())
    print(f"Total Rank: {total_rank:.4f}")
    if abs(total_rank - 1.0) < 0.0001:  # Utilisation d'une tolérance appropriée
        print("La somme des ranks est proche de 1.0.")
    else:
        print("La somme des ranks n'est pas égale à 1.0.")


if __name__ == "__main__":
    main()
