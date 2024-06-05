def cantor_pairing(user_id: int, person_id: int) -> int:
    return (user_id + person_id) * (user_id + person_id + 1) // 2 + person_id
