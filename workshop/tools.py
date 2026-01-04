def calculate_pizza_for_people(people_count: int, appetite_level: str = "normal") -> str:
    """
    Calcula el número y tamaño de pizzas necesarias para un grupo de personas.

    Args:
        people_count (int): Número de personas que comerán
        appetite_level (str): Nivel de apetito - "ligero", "normal", o "fuerte" (predeterminado: "normal")

    Returns:
        str: Recomendación de tamaño y cantidad de pizza
    """
    print(f"[HERRAMIENTA LLAMADA] Calculando pizza para {people_count} personas con apetito {appetite_level}.")
    if people_count <= 0:
        return "Por favor proporciona un número válido de personas (mayor que 0)."

    # Cálculos base asumiendo apetito normal
    # Pequeña: 1–2 personas | Mediana: 2–3 | Grande: 3–4 | Extra Grande: 4–6
    appetite_multipliers = {"ligero": 0.7, "normal": 1.0, "fuerte": 1.3}

    multiplier = appetite_multipliers.get(appetite_level.lower(), 1.0)
    adjusted_people = people_count * multiplier

    recommendations = []

    if adjusted_people <= 2:
        if adjusted_people <= 1:
            recommendations.append("1 Pizza Pequeña (perfecta para 1-2 personas)")
        else:
            recommendations.append("1 Pizza Mediana (ideal para 2-3 personas)")
    elif adjusted_people <= 4:
        recommendations.append("1 Pizza Grande (sirve para 3-4 personas)")
    elif adjusted_people <= 6:
        recommendations.append("1 Pizza Extra Grande (alimenta a 4-6 personas)")
    elif adjusted_people <= 8:
        recommendations.append("2 Pizzas Grandes (perfectas para compartir)")
    elif adjusted_people <= 12:
        recommendations.append("2 Pizzas Extra Grandes (ideales para grupos)")
    else:
        # Para grupos más grandes, calcular múltiples pizzas
        extra_large_count = int(adjusted_people // 5)
        remainder = adjusted_people % 5

        pizza_list = []
        if extra_large_count > 0:
            pizza_list.append(f"{extra_large_count} Pizza{'s' if extra_large_count > 1 else ''} Extra Grande{'s' if extra_large_count > 1 else ''}")

        if remainder > 2:
            pizza_list.append("1 Pizza Grande")
        elif remainder > 0:
            pizza_list.append("1 Pizza Mediana")

        recommendations.append(" + ".join(pizza_list))

    result = f"Para {people_count} personas con apetito {appetite_level}:\n"
    result += f"🍕 Recomendación: {recommendations[0]}\n"

    if appetite_level != "normal":
        result += f"(Ajustado para nivel de apetito {appetite_level})"

    return result