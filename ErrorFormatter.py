class ErrorFormatter:

    errors = {
        "23505": "Istnieje już jednostka o takim identyfikatorze",
        "22P02": "Identyfikator nie może być pusty oraz musi być liczbą",
        "22001": "Podany ciąg znaków jest za długi",
        "22008": "Podano datę w złym formacie",
        "42601": "Wprowadzono niedozowlone znaki: ', *. /. \\, \"",
        "23502": "Pola wymaganie nie mogą być puste"
    }

    @staticmethod
    def get_error(code):
        return ErrorFormatter.errors.get(code, "Nieznany błąd: " + code)
