from __future__ import unicode_literals
from datetime import date

from wtforms import (
    Form,
    validators,
    TextField,
    PasswordField,
    SelectField,
    HiddenField,
    )


__all__ = [
    'CreditCardForm',
    'PurchaseForm',
    'GuestPurchaseForm',
    'ListingForm',
    'GuestListingForm',
]


def months():
    return [
        (str(i), str(i)) for i in range(1, 13)
    ]


def years(min=None, max=None):
    if not min:
        min = date.today().year
    if not max:
        max = date.today().year + 10
    return [
        (str(i), str(i)) for i in range(min, max)
    ]


class CreditCardForm(Form):
    """
    What we require in order to tokenize a card.
    """
    number = TextField('Credit Card Number', [validators.Required()])
    expiration_month = SelectField('Expiration Date', [validators.Required()],
        choices=months())
    expiration_year = SelectField('Expiration Year', [validators.Required()],
        choices=years())
    cvv = TextField('Security Code', [validators.Required()])


class PurchaseForm(CreditCardForm):
    """
    This reflects all the information required by Balanced to create a Buyer
    Account.
    """
    name = HiddenField(validators=[validators.Required()])
    email = HiddenField(validators=[validators.Required(),
                                            validators.Email()])
    card_href = HiddenField(validators=[validators.Required()])


class GuestPurchaseForm(PurchaseForm):
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Required(),
                                        validators.Email()])


class ListingForm(Form):
    """
    This is the information we need to collect in order to list a bike
    """
    type = HiddenField(default='person')
    listing_id = HiddenField()
    name = HiddenField()
    email = HiddenField()
    line1 = TextField('Home Address', [validators.Required()])
    postal_code = TextField('Zip Code', [validators.Required()])
    phone = TextField('Phone Number', [validators.Required()])
    country_code = HiddenField(default='USA')
    state = HiddenField()
    dob_month = SelectField('Month of Birth',
        [validators.Required()], choices=months())
    dob_year = SelectField('Year of Birth', [validators.Required()],
        choices=years(1900, date.today().year - 18))


class GuestListingForm(ListingForm):
    """
    Used when listing a bike with an anonymous user
    """
    name = TextField('Name', [validators.Required()])
    email = TextField('Email', [validators.Required(),
                                        validators.Email()])
    # Matin told me to comment this out.
    # password = PasswordField('Password', [validators.Required()])
