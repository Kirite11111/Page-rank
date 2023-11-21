from pagerank import transition_model

def main():
    corpus_example = {
        "1.html": {"2.html", "3.html"},
        "2.html": {"3.html"},
        "3.html": {"2.html"}
    }

    current_page = "1.html"
    damping_factor = 0.85
    result = transition_model(corpus_example, current_page, damping_factor)
    print(result)
    
    # Vérification de la somme des ranks
    total_rank = sum(result.values())
    print(f"Total Rank: {total_rank:.4f}")
    if abs(total_rank - 1.0) < 0.0001:  # Utilisation d'une tolérance appropriée
        print("La somme des ranks est proche de 1.0.")
    else:
        print("La somme des ranks n'est pas égale à 1.0.")


if __name__ == "__main__":
    main()