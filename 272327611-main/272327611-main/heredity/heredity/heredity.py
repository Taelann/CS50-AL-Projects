import csv
import itertools
import sys

PROBS = {
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {
            True: 0.65,
            False: 0.35
        },
        1: {
            True: 0.56,
            False: 0.44
        },
        0: {
            True: 0.01,
            False: 0.99
        }
    },
    "mutation": 0.01
}


def main():
    # Check for command-line usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")

    # Load data from file into a dictionary
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Identify set of people
    names = set(people)

    # Enumerate all possible sets of people who might have the trait
    for have_trait in powerset(names):

        # If a person has a known trait, then they must have it
        if any(
            people[person]["trait"] is not None
            and people[person]["trait"] != (person in have_trait)
            for person in names
        ):
            continue

        # Enumerate all possible gene distributions
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Calculate joint probability
                p = joint_probability(
                    people, one_gene, two_genes, have_trait
                )

                # Update probabilities
                update(
                    probabilities, one_gene, two_genes, have_trait, p
                )

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                print(f"    {value}: {probabilities[person][field][value]:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True if row["trait"] == "1"
                    else False if row["trait"] == "0"
                    else None
                )
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(items)
        for items in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return the joint probability of the people having
    the specified gene counts and traits.
    """
    probability = 1

    for person in people:
        # Determine how many copies of the gene this person has
        if person in two_genes:
            genes = 2
        elif person in one_gene:
            genes = 1
        else:
            genes = 0

        # Determine whether this person has the trait
        has_trait = person in have_trait

        mother = people[person]["mother"]
        father = people[person]["father"]

        # If the person has no parents listed, use the unconditional
        # probability of having this number of genes.
        if mother is None and father is None:
            probability *= PROBS["gene"][genes]

        else:
            # Probability that the mother passes the gene
            if mother in two_genes:
                pass_mother = 1 - PROBS["mutation"]
            elif mother in one_gene:
                pass_mother = 0.5
            else:
                pass_mother = PROBS["mutation"]

            # Probability that the father passes the gene
            if father in two_genes:
                pass_father = 1 - PROBS["mutation"]
            elif father in one_gene:
                pass_father = 0.5
            else:
                pass_father = PROBS["mutation"]

            # Probability of the child having this number of genes
            if genes == 2:
                probability *= pass_mother * pass_father
            elif genes == 1:
                probability *= (
                    pass_mother * (1 - pass_father)
                    + (1 - pass_mother) * pass_father
                )
            else:
                probability *= (1 - pass_mother) * (1 - pass_father)

        # Multiply by the probability of having (or not having) the trait
        probability *= PROBS["trait"][genes][has_trait]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add the joint probability p to the appropriate gene and trait
    probability totals for each person.
    """
    for person in probabilities:
        if person in two_genes:
            gene_count = 2
        elif person in one_gene:
            gene_count = 1
        else:
            gene_count = 0

        has_trait = person in have_trait

        probabilities[person]["gene"][gene_count] += p
        probabilities[person]["trait"][has_trait] += p


def normalize(probabilities):
    """
    Update each probability distribution so that its values sum to 1.
    """
    for person in probabilities:
        for field in probabilities[person]:
            total = sum(probabilities[person][field].values())
            for value in probabilities[person][field]:
                probabilities[person][field][value] /= total


if __name__ == "__main__":
    main()
