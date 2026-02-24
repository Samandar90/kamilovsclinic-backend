from django.db import models


class Lead(models.Model):
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    full_name = models.CharField("Имя", max_length=150, blank=True)
    phone = models.CharField("Телефон", max_length=50, blank=True)
    email = models.EmailField("Email", blank=True)

    service = models.CharField("Услуга / тема", max_length=150, blank=True)
    message = models.TextField("Комментарий", blank=True)

    form_context = models.CharField(
        "Источник формы",
        max_length=100,
        blank=True,
        help_text="Например: index_hero, doctors_page, contacts_page",
    )
    page_url = models.URLField(
        "Страница",
        blank=True,
        help_text="URL, откуда отправили форму",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        base = self.full_name or self.phone or "Без имени"
        return f"{base} — {self.service or 'заявка'}"


class ServiceCategory(models.Model):
    """Группа услуг: Стоматология, Педиатрия, УЗИ и т.д."""
    title = models.CharField("Название категории", max_length=120)
    slug = models.SlugField("Слаг", max_length=120, unique=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Категория услуги"
        verbose_name_plural = "Категории услуг"

    def __str__(self):
        return self.title


class Service(models.Model):
    """Конкретная услуга/направление клиники."""
    category = models.ForeignKey(
        ServiceCategory,
        verbose_name="Категория",
        related_name="services",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    title = models.CharField("Название услуги", max_length=200)
    slug = models.SlugField(
        "Слаг (для service-detail)",
        max_length=200,
        unique=True,
        help_text="Например: dental, pediatrics, neurology",
    )

    short_intro = models.CharField(
        "Краткое описание (карточка)",
        max_length=300,
        blank=True,
        help_text="1–2 строки, которые видны в списке услуг.",
    )
    description = models.TextField(
        "Подробное описание",
        blank=True,
        help_text="Текст для service-detail страницы.",
    )

    duration = models.CharField(
        "Длительность приёма",
        max_length=100,
        blank=True,
        help_text="Например: 30–40 минут",
    )
    price_from = models.DecimalField(
        "Цена от",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Минимальная стоимость, можно оставить пустой.",
    )

    tags = models.CharField(
        "Теги (через запятую)",
        max_length=300,
        blank=True,
        help_text="Например: детский приём, профилактика, консультация",
    )

    is_popular = models.BooleanField("Популярная услуга", default=False)
    is_active = models.BooleanField("Активна", default=True)
    order = models.PositiveIntegerField("Порядок в списке", default=0)

    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.title
