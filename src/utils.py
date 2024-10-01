def get_category_lvls(categories: dict, cat_id: int) -> tuple[str, str, str, str]:
    category = categories.get(cat_id)
    cat_lvls = []
    while category is not None:
        cat_lvls.append(category["name"])
        category = categories.get(category.get("parent_id"), None)
    lvl_1, lvl_2, lvl_3 = cat_lvls[-1:-4:-1]
    lvls_remaining = "/".join(cat_lvls[-4::-1])
    return lvl_1, lvl_2, lvl_3, lvls_remaining


def calculate_discount(old_price: int, new_price: int) -> float:
    return 100 - new_price * 100 / old_price


def conversion_from_str_to_int_or_none(value: str) -> int | None:
    if value is None:
        return None

    if value.isdigit():
        return int(value)

    return None
