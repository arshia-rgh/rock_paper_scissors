from typing import Optional


class Game:
    def get_winner(self, p1_number: int, p2_number: int) -> Optional[int]:
        if p1_number == 1:
            if p2_number == 3:
                return p1_number
            elif p2_number == 2:
                return p2_number
            return None

        elif p1_number == 2:
            if p2_number == 1:
                return p1_number
            elif p2_number == 3:
                return p2_number
            return None

        else:
            if p2_number == 1:
                return p2_number
            elif p2_number == 2:
                return p1_number
            return None
