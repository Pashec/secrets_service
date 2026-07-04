from django.shortcuts import render, get_object_or_404, redirect
from .models import Secret


def create_secret(request):
    """Вьюха для создания секрета."""
    if request.method == 'POST':
        text = request.POST.get('text')
        password = request.POST.get('password')

        if text:
            secret = Secret(text=text)
            if password:
                secret.set_password(password)
            secret.save()
            return redirect('secret_crated', secret_id=secret.id)
    return render(request, 'secrets_service/create.html')


def secret_created(request, secret_id):
    """Вьюха для отображения страницы с информацией о созданном секрете."""
    secret_url = request.build_absolute_uri(f'/secret/{secret_id}/')
    return render(request, 'secrets_service/created.html', {'secret_url': secret_url})


def view_secret(request, secret_id):
    """Вьюха для просмотра секрета."""
    secret = get_object_or_404(Secret, id=secret_id)

    # Проверка на наличие пароля.
    if secret.password_hash:
        if request.method == 'POST':
            entered_password = request.POST.get('password')
            if secret.check_secret_password(entered_password):
                secret.is_viewed = True
                secret.save()
                return render(request, 'secrets_service/show.html', {'text': secret.text})
            else:
                return render(
                    request,
                    'secret_service/password_protected.html',
                    {'error': 'Неверный пароль! Попробуй еще раз.'}
                )
        return render(request, 'secrets_service/password_protected.html')
    secret.is_viewed = True
    secret.save()
    return render(request, 'secrets_service/show.html', {'text': secret.text})