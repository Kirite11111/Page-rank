import sys

from pagerank import crawl, iterate_pagerank

DAMPING = 0.85

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    total_rank = sum(ranks.values())
    print(f"Total Rank: {total_rank:.4f}")
    if abs(total_rank - 1.0) < 0.0001:
        print("La somme des ranks est proche de 1.0.")
    else:
        print("La somme des ranks n'est pas égale à 1.0.")


if __name__ == "__main__":
    main()