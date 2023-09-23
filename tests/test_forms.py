from django.test import TestCase

from restaurant.forms import CookCreationForm


class FormsTests(TestCase):
    def test_cook_creation_form_with_additional_fields_is_valid(self):
        form_data = {
            "username": "new_user",
            "password1": "UseritoBorito12356",
            "password2": "UseritoBorito12356",
            "first_name": "Bulbozavr",
            "last_name": "Lystyakovych",
            "years_of_experience": 16
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
