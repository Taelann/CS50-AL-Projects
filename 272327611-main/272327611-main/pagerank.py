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
    print("PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.

    Return a dictionary where each key is a page, and values are
    a set of all pages linked to by that page.
    """
    pages = dict()


    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue

        with open(os.path.join(directory, filename), encoding="utf-8") as f:
            contents = f.read()

        links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
        pages[filename] = set(links) - {filename}


    for filename in pages:
        pages[filename] = {
            link for link in pages[filename]
            if link in pages
        }

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next.
    """
    number_of_pages = len(corpus)
    links = corpus[page]



    if not links:
        links = set(corpus)

    probability = (1 - damping_factor) / number_of_pages
    probabilities = {}

    for destination in corpus:
        probabilities[destination] = probability

        if destination in links:
            probabilities[destination] += damping_factor / len(links)

    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling n pages
    according to the transition model, starting with a random page.
    """
    visits = {page: 0 for page in corpus}

    current_page = random.choice(list(corpus))
    visits[current_page] += 1


    for _ in range(n - 1):
        probabilities = transition_model(corpus, current_page, damping_factor)

        current_page = random.choices(
            population=list(probabilities.keys()),
            weights=list(probabilities.values()),
            k=1
        )[0]

        visits[current_page] += 1


    return {
        page: count / n
        for page, count in visits.items()
    }


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by repeatedly applying
    the PageRank formula until all values converge within 0.001.
    """
    number_of_pages = len(corpus)


    ranks = {
        page: 1 / number_of_pages
        for page in corpus
    }

    while True:
        new_ranks = {}

        for page in corpus:
            total = 0

            for possible_linker in corpus:
                links = corpus[possible_linker]


                if not links:
                    total += ranks[possible_linker] / number_of_pages
                elif page in links:
                    total += ranks[possible_linker] / len(links)

            new_ranks[page] = (
                (1 - damping_factor) / number_of_pages
                + damping_factor * total
            )

        
        if all(
            abs(new_ranks[page] - ranks[page]) <= 0.001
            for page in corpus
        ):
            return new_ranks

        ranks = new_ranks


if __name__ == "__main__":
    main()
