from nose.tools import *

import kingsmoot.forms as forms


# TODO Set up application context in order to be able to run these tests

def apply_data_to_form(data, form):
    assert len(data) == len(form), "Data list and form do not have the same length"

    i = 0
    for field in form:
        field.data = data[i]
        i += 1


def test_register_form_valid():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king@gmail.com", "hithere", "hithere"]
    apply_data_to_form(test_data, form)
    assert_true(form.validate())


def test_register_form_missing_first_name():
    form = forms.RegisterForm()
    test_data = ["", "King", "daniel.oliver.king@gmail.com", "hithere", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_missing_last_name():
    form = forms.RegisterForm()
    test_data = ["Daniel", "", "daniel.oliver.king@gmail.com", "hithere", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_missing_email():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "", "hithere", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_invalid_email():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king", "hithere", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_missing_password1():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king@gmail.com", "", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_too_short_passwrod1():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king@gmail.com", "h", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_wrong_password1():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king@gmail.com", "hey", "hithere"]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)


def test_register_form_missing_password2():
    form = forms.RegisterForm()
    test_data = ["Daniel", "King", "daniel.oliver.king@gmail.com", "hithere", ""]
    apply_data_to_form(test_data, form)
    assert_raises(forms.ValidationError, form.validate)

