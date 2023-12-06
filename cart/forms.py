from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]

DELIVERY_CHOICES = [
    (0, 'Доставка на дом'),
    (1, 'Доставка в пункт выдачи'),
    (2, 'Доставка в постамат'),
]

PAYMENT_CHOICES = [
    (0, 'Оплата картой'),
    (1, 'Оплата наличными при получении'),
]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, label="Количество товара:")
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class CartProductPayForm(forms.Form):
    delivery = forms.TypedChoiceField(choices=DELIVERY_CHOICES, label='Выберите способ доставки')
    payment = forms.TypedChoiceField(choices=PAYMENT_CHOICES, label='Выберите способ оплаты')
