class ErrorFormatter:

    errors = {
        "23505": "Istnieje już jednostka o takim identyfikatorze",
        "22P02": "Wymagane pole liczbowe nie może być puste\noraz musi być liczbą",
        "22001": "Podany ciąg znaków jest za długi",
        "22008": "Podano datę w złym formacie",
        "42601": "Wprowadzono niedozowlone znaki: ', *. /. \\, \"",
        "23502": "Pola wymagane nie mogą być puste",
        "22007": "Pola wymagane nie mogą być puste",
        "22003": "Podana wartość liczbowa jest za duża"
    }

    @staticmethod
    def get_error(code):
        return ErrorFormatter.errors.get(code, "Nieznany błąd: " + code)
