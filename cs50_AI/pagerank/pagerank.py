import random
import sys
import re
import os

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
    distribution = dict()
    
    links = corpus[page]
    
    links_prob = damping_factor / len(links) if len(links) > 0 else 0
    random_page_prob = (1 - damping_factor) / len(corpus) if len(links) > 0 else  1 / len(corpus)
    
    for page_number in corpus:
        if page_number in links:
            distribution[page_number] = links_prob + random_page_prob
        else:
            distribution[page_number] = random_page_prob
            
    return normalize(distribution)


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    sample = random.choice(tuple(corpus)) # To start with first sample
    counter = {page : 0 for page in corpus} # Creates placeholder dict
    pagerank = counter # Creates second variable for PageRanks

    for i in range(n - 1):
        counter[sample] += 1

        # Every time sample gets replaced to same variable
        model = transition_model(corpus, sample, damping_factor)
        sample = ''.join(random.choices(tuple(model), tuple(model.values())))

    for page in counter:
        pagerank[page] = counter[page] / n

    return normalize(pagerank)


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank = {page : round(1 / len(corpus), 3) for page in corpus}
    pagerank_buffer = pagerank.copy()
    converged = False
    
    def formula_first_part():
        return (1 - damping_factor) / len(corpus)
    
    def formula_second_part(page):
        # list of pages which directs to page (even "zero" links pages)
        links = [key for key, values in corpus.items() if page in values or len(values) == 0]
        counter = 0
        
        # summation of linked pages with its probabilities
        for linked_page in links:
            num_links = len(corpus[linked_page])
            
            if num_links == 0:
                num_links = len(corpus)
                
            counter += (pagerank[linked_page] / num_links)
        
        return damping_factor * counter
    
    # 1. Probability of a random page
    random_page_prob = formula_first_part()

    while not converged:
        # 2. Probability followed a link from other page to page calculated
        for page in pagerank:
            links_prob = formula_second_part(page)
            pagerank_buffer.update({page : links_prob + random_page_prob})
        
        # 3. Check if converged
        converged = all(tuple(abs(val_1 - val_2) <= 0.001 for val_1, val_2 in zip(pagerank.values(), pagerank_buffer.values())))
        
        # 4. Updates pagerank to its buffer
        pagerank = pagerank_buffer.copy()
    
    # 5. When all done return pagerank
    return normalize(pagerank)


def normalize(dictionary):
    """
    Normalize distribution of probabilities
    """
    divider = sum(dictionary.values())
    for key, value in dictionary.items():
        dictionary[key] = dictionary[key] / divider
        
    return dictionary


if __name__ == "__main__":
    main()
