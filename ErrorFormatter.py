class ErrorFormatter:

    errors = {
        "23505": "Istnieje już jednostka o takim identyfikatorze",
    }

    @staticmethod
    def get_error(code):
        return ErrorFormatter.errors.get(code, "Nieznany błąd")
