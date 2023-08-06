from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import FachschaftUserForm


@method_decorator(login_required, name='dispatch')
class FachschaftUserEdit(View):
    def get(self, request):
        try:
            # FachschaftUser bereits vorhanden?
            form = FachschaftUserForm(instance=request.user.fachschaftuser)
        except ObjectDoesNotExist:
            form = FachschaftUserForm()

        context = {
            'form': form,
        }

        return render(request, 'fsmedhro_core/user_edit.html', context)

    def post(self, request):
        try:
            form = FachschaftUserForm(
                data=request.POST,
                instance=request.user.fachschaftuser,
            )
        except ObjectDoesNotExist:
            form = FachschaftUserForm(
                data=request.POST,
            )

        if form.is_valid():
            fachschaftuser = form.save(commit=False)
            fachschaftuser.user = request.user
            fachschaftuser.save()

        return redirect('fsmedhro_core:detail')


@method_decorator(login_required, name='dispatch')
class FachschaftUserDetail(View):
    def get(self, request):
        try:
            fachschaftuser = request.user.fachschaftuser
        except ObjectDoesNotExist:
            return redirect('fsmedhro_core:edit')

        context = {
            'fachschaftuser': fachschaftuser,
        }

        return render(request, 'fsmedhro_core/user_detail.html', context)
