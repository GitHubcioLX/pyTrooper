class ErrorFormatter:

    errors = {
        "23505": "Istnieje już jednostka o takim identyfikatorze",
        "22P02": "Identyfikator nie może być pusty oraz musi być liczbą",
        "22001": "Podany ciąg znaków jest za długi"
    }

    @staticmethod
    def get_error(code):
        return ErrorFormatter.errors.get(code, "Nieznany błąd: " + code)
