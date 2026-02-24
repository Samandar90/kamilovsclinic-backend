from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.html import escape

from .models import Lead
from .telegram_utils import send_telegram_message


# ================== ЛИДЫ (форма → БД + Telegram) ==================


@csrf_exempt
def lead_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    full_name = request.POST.get("name", "").strip()
    phone = request.POST.get("phone", "").strip()
    email = request.POST.get("email", "").strip()
    service = request.POST.get("service", "").strip()
    message = request.POST.get("message", "").strip()
    form_context = request.POST.get("form_context", "other").strip()
    page_url = request.POST.get("page_url", "").strip()

    # сохраняем в БД
    lead = Lead.objects.create(
        full_name=full_name,
        phone=phone,
        email=email,
        service=service,
        message=message,
        form_context=form_context,
        page_url=page_url,
    )

    # отправка в Telegram
    lines = [
        "<b>Новая заявка с сайта Kamilovs Clinic</b>",
        f"Имя: {escape(full_name) or '—'}",
        f"Телефон: {escape(phone) or '—'}",
        f"Email: {escape(email) or '—'}",
        f"Услуга: {escape(service) or '—'}",
        f"Комментарий: {escape(message) or '—'}",
        "",
        f"Источник формы: {escape(form_context)}",
    ]
    if page_url:
        lines.append(f"Страница: {escape(page_url)}")

    send_telegram_message("\n".join(lines))

    # красивый HTML + авто-возврат на фронтенд
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8" />
        <title>Заявка отправлена</title>
        <meta http-equiv="refresh" content="2;url={page_url or 'http://127.0.0.1:5500/index.html'}">
        <style>
            body {{
                margin: 0;
                font-family: system-ui, -apple-system, BlinkMacSystemFont,
                             'Segoe UI', Roboto, sans-serif;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                background: #f1f5f9;
                color: #0f172a;
            }}
            .box {{
                background: #ffffff;
                padding: 26px 28px;
                border-radius: 16px;
                box-shadow: 0 20px 45px rgba(15, 23, 42, 0.16);
                max-width: 360px;
                text-align: center;
            }}
            h1 {{
                margin: 0 0 10px;
                font-size: 22px;
            }}
            p {{
                margin: 0;
                font-size: 14px;
                color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div class="box">
            <h1>Заявка отправлена ✅</h1>
            <p>Мы свяжемся с вами в ближайшее время.</p>
            <p style="margin-top:10px; font-size:12px;">
                Через пару секунд вы вернётесь назад.
            </p>
        </div>
    </body>
    </html>
    """

    return HttpResponse(html)
