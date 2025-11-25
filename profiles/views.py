from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from checkout.models import Order

from .models import UserProfile, AddressField
from .forms import UserProfileForm, AddressFieldForm


@login_required
def profile(request):
    """ Display the user's profile. """
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        address_form = AddressFieldForm(request.POST, instance=profile.default_address)
        if form.is_valid():
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            if address_form.is_valid():
                address_form.save()
            form.save()
            messages.success(request, 'Profile updated successfully')

    address = profile.default_address
    if not address:
        address = AddressField.objects.filter(user=user).first()
    if not address:
        address = AddressField.objects.create(user=user)
    address_form = AddressFieldForm(instance=address)
    profile.default_address = address
    profile.save()
    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'user': user,
        'form': form,
        'address_form': address_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)