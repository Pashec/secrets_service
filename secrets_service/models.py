import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Secret(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    text = models.TextField(
        verbose_name='Текст секрета',
    )
    password_hash = models.CharField(
        max_length=128,
        verbose_name='Хэш пароля',
        blank=True,
        null=True
    )
    is_viewed = models.BooleanField(
        default=False,
        verbose_name='Прочитано'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Секрет'
        verbose_name_plural = 'Секреты'
        ordering = ['-created_at']

    def __str__(self):
        return f'Секрет {self.id} (Прочитан: {self.is_viewed})'

    # Метод хеширования пароля.
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    # Метод проверки пароля.
    def check_secret_password(self, raw_password):
        if not self.password_hash:
            return True  # Если пароль не установлен, доступ разрешен
        return check_password(raw_password, self.password_hash)