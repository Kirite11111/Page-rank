import os
import random
import re
import sys

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
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if not corpus or page not in corpus:
        return None

    num_pages = len(corpus)
    transition_probabilities = {}

    # Probability of choosing a link from the current page
    linked_pages = corpus[page]
    linked_prob = damping_factor / len(linked_pages) if linked_pages else 0

    for p in corpus:
        # Probability of choosing a link from any page in the corpus
        corpus_prob = (1 - damping_factor) / num_pages

        # Total probability for the current page
        total_prob = linked_prob if p in linked_pages else 0
        total_prob += corpus_prob

        transition_probabilities[p] = total_prob

    return transition_probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initialize PageRank dictionary with 0 for each page
    page_ranks = dict.fromkeys(corpus.keys(), 0)

    # Start the "surfer" at a random page
    sample = random.choice(list(corpus.keys()))

    for i in range(n):
        # Update the count for the current page
        page_ranks[sample] += 1

        # Determine the next page using the transition model
        probabilities = transition_model(corpus, sample, damping_factor)
        sample = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]

    # Normalize the PageRank values to sum to 1
    total_samples = sum(page_ranks.values())
    for page in page_ranks:
        page_ranks[page] /= total_samples

    return page_ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    numberOfPages = len(corpus)
    PRi = {page: 1 / numberOfPages for page in corpus}

    convergenceObj = 0.001
    converged = False

    while not converged:
        NPRi = {}
        for page in corpus:
            new_rank = (1 - damping_factor) / numberOfPages + damping_factor * sum(PRi[p] / len(corpus[p]) for p in corpus if page in corpus[p])
            NPRi[page] = new_rank
        #stockage des écarts entre les anciens et les nouveaux rangs
        changes = [abs(NPRi[page] - PRi[page]) for page in corpus]
        max_change = max(changes)

        # si il y a convergence

        if max_change < convergenceObj:
            converged = True
        else:
            PRi = NPRi

    return PRi
 

if __name__ == "__main__":
    main()
