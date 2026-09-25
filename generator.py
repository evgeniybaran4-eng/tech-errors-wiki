import json
import os
import glob

SITE_URL = "https://tech-errors-wiki.vercel.app"
OUTPUT_DIR = "public"

def create_dirs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "privacy"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "author"), exist_ok=True)

def generate_header():
    return """
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
      <div class="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2">
          <span class="text-2xl">⚡</span>
          <span class="font-bold text-lg text-slate-900 tracking-tight">TechErrors Wiki</span>
        </a>
        <nav class="flex gap-4 text-sm font-medium items-center">
          <a href="/washing/" class="text-slate-600 hover:text-indigo-600 transition-colors">Стиральные</a>
          <a href="/dishwasher/" class="text-slate-600 hover:text-indigo-600 transition-colors">Посудомойки</a>
          <a href="/author/" class="text-slate-600 hover:text-indigo-600 transition-colors hidden sm:inline">Об авторе</a>
        </nav>
      </div>
    </header>
    """

def generate_footer():
    return """
    <footer class="bg-white border-t border-slate-200 mt-16 py-8">
      <div class="max-w-5xl mx-auto px-4 text-center text-xs text-slate-500 space-y-3">
        <div class="flex justify-center gap-4 text-slate-600 font-medium">
          <a href="/privacy/" class="hover:text-indigo-600 underline">Политика конфиденциальности</a>
          <span>•</span>
          <a href="/author/" class="hover:text-indigo-600 underline">Эксперт проекта</a>
          <span>•</span>
          <a href="/sitemap.xml" class="hover:text-indigo-600 underline">Карта сайта</a>
        </div>
        <p>TechErrors Wiki — экспертная база знаний по ремонту и диагностике домашней бытовой техники.</p>
        <p class="text-slate-400">© 2026 TechErrors Wiki. Данные актуализированы сервисными инженерами.</p>
      </div>
    </footer>

    <div id="cookie-banner" class="fixed bottom-4 left-4 right-4 sm:left-auto sm:right-6 sm:max-w-md bg-slate-900 text-white p-4 rounded-2xl shadow-xl z-50 flex flex-col gap-3 border border-slate-800 hidden">
      <div class="text-xs text-slate-300 leading-relaxed">
        Мы используем куки для корректной работы каталога и сбора веб-аналитики. Подробнее в нашей
        <a href="/privacy/" class="text-indigo-400 underline hover:text-indigo-300">политике конфиденциальности</a>.
      </div>
      <div class="flex justify-end gap-2">
        <button id="accept-cookies" class="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-semibold transition-colors">
          Согласен
        </button>
      </div>
    </div>

    <script>
      (function() {
        if (!localStorage.getItem('cookie_consent_accepted')) {
          var b = document.getElementById('cookie-banner');
          if (b) b.classList.remove('hidden');
        }
        var btn = document.getElementById('accept-cookies');
        if (btn) {
          btn.addEventListener('click', function() {
            localStorage.setItem('cookie_consent_accepted', 'true');
            var b = document.getElementById('cookie-banner');
            if (b) b.classList.add('hidden');
          });
        }
      })();
    </script>
    """

def generate_breadcrumbs(crumbs):
    items_html = []
    for idx, c in enumerate(crumbs):
        if idx == len(crumbs) - 1:
            items_html.append(f'<span class="text-slate-800 font-medium">{c["name"]}</span>')
        else:
            items_html.append(f'<a href="{c["url"]}" class="hover:text-indigo-600">{c["name"]}</a>')
            items_html.append('<span>/</span>')
    return f"""
    <nav class="max-w-5xl mx-auto px-4 py-4 w-full text-xs sm:text-sm text-slate-500 flex flex-wrap items-center gap-2">
      {' '.join(items_html)}
    </nav>
    """

def get_repair_prices(code):
    c = code.upper()
    if any(x in c for x in ["E18", "F18", "OE", "5E", "5C", "F05", "E20", "E21", "E24", "E25", "I20", "E03", "E01"]):
        return [
            ("Механический засор улитки, фильтра или шланга", "Расходники не требуются", "Разбор дренажа, чистка улитки, промывка тракта", "1 100 - 1 500 ₽"),
            ("Физический износ или клин крыльчатки сливного насоса", "Помпа в сборе (Askoll/Plaset, 30-40W)", "Демонтаж старой помпы, установка новой, тест герметичности", "2 200 - 3 100 ₽"),
            ("Залипание контактов датчика уровня (прессостата)", "Аналоговый/электронный прессостат", "Продувка трубки давления, замена датчика уровня", "1 700 - 2 400 ₽"),
            ("Выгорание симистора управления помпой на плате", "Симистор платы / резисторы обвязки", "Демонтаж модуля управления, компонентная пайка цепи", "3 200 - 4 600 ₽")
        ]
    elif any(x in c for x in ["E17", "F17", "IE", "4E", "4C", "E10", "E11", "E1", "E02", "F01"]):
        return [
            ("Кальцинация и механический засор сетки входного штуцера", "Уплотнительная манжета", "Извлечение фильтра, ультразвуковая чистка", "900 - 1 300 ₽"),
            ("Обрыв электромагнитной катушки заливного клапана (КЭН)", "Клапан заливной 1-2-3 секционный", "Замена блока клапанов, опрессовка соединений", "2 100 - 2 900 ₽"),
            ("Окисление контактных колодок цепи залива", "Клеммы, термоусадка", "Восстановление контактов, зачистка окислов", "1 200 - 1 800 ₽")
        ]
    elif any(x in c for x in ["E15", "E23", "F23", "I30", "E4"]):
        return [
            ("Ложное срабатывание из-за пены или конденсата", "Не требуется", "Демонтаж боковой стенки, сушка поддона, сброс аварии", "1 300 - 1 800 ₽"),
            ("Разгерметизация уплотнения чаши (стакана) поддона", "Ремкомплект силиконовый Bosch/VAG", "Протяжка или установка дублирующей прокладки чаши", "2 700 - 3 800 ₽"),
            ("Залипание микропереключателя поплавкового механизма", "Микровыключатель поддона", "Замена контактной группы датчика Аквастоп", "1 600 - 2 200 ₽")
        ]
    elif any(x in c for x in ["F08", "HE", "H1", "H2", "E09", "TE", "E05", "F04"]):
        return [
            ("Пробой изоляции или обрыв нихромовой спирали ТЭНа", "ТЭН прямой/изогнутый 1700-2000W", "Снятие стенки, замена ТЭНа с термодатчиком", "2 500 - 3 500 ₽"),
            ("Деградация термодатчика NTC (смещение сопротивления)", "Датчик температуры NTC 10-20 кОм", "Установка нового терморезистора в манжету ТЭНа", "1 500 - 2 100 ₽"),
            ("Подгорание силовых контактов реле ТЭНа на модуле", "Реле 12V 16A Omron/Finder", "Выпайка поврежденного реле, очистка нагара дорожек", "3 000 - 4 400 ₽")
        ]
    else:
        return [
            ("Аппаратный сбой логики модуля управления", "Элементы SMD обвязки", "Тестирование программатором, перепрошивка памяти", "3 400 - 4 800 ₽"),
            ("Нарушение сигнальной проводки или вибрационный обрыв", "Соединительные провода", "Локализация обрыва, пайка соединений в жгуте", "1 600 - 2 300 ₽"),
            ("Профилактическое обслуживание узла", "Не требуется", "Комплексная диагностика механических компонентов", "1 200 - 1 700 ₽")
        ]

def generate_voting_widget(item_key):
    return f"""
    <section class="my-10 p-6 rounded-2xl bg-gradient-to-r from-slate-50 to-indigo-50/30 border border-slate-200" id="vote-section-{item_key}">
      <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          <h3 class="font-bold text-slate-900 text-base sm:text-lg">Помогла ли вам эта инструкция?</h3>
          <p class="text-slate-500 text-xs sm:text-sm mt-0.5">Оцените полезность статьи, чтобы помочь другим пользователям</p>
        </div>
        <div class="flex items-center gap-3">
          <button id="btn-like-{item_key}" onclick="handleVote('{item_key}', 'like')" class="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 bg-white hover:bg-emerald-50 hover:border-emerald-300 hover:text-emerald-700 text-slate-700 font-semibold text-sm transition-all shadow-sm active:scale-95">
            <span>👍 Да</span>
            <span id="count-like-{item_key}" class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md text-xs font-mono">42</span>
          </button>
          <button id="btn-dislike-{item_key}" onclick="handleVote('{item_key}', 'dislike')" class="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-slate-200 bg-white hover:bg-rose-50 hover:border-rose-300 hover:text-rose-700 text-slate-700 font-semibold text-sm transition-all shadow-sm active:scale-95">
            <span>👎 Нет</span>
            <span id="count-dislike-{item_key}" class="bg-slate-100 text-slate-600 px-2 py-0.5 rounded-md text-xs font-mono">3</span>
          </button>
        </div>
      </div>
      <div id="vote-msg-{item_key}" class="hidden mt-3 text-xs font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 p-2.5 rounded-lg text-center">
        Спасибо! Ваш голос учтен.
      </div>
    </section>

    <script>
      (function() {{
        var key = '{item_key}';
        var stored = localStorage.getItem('vote_status_' + key);
        var likeCount = parseInt(localStorage.getItem('vote_count_like_' + key) || '42', 10);
        var dislikeCount = parseInt(localStorage.getItem('vote_count_dislike_' + key) || '3', 10);

        var likeEl = document.getElementById('count-like-' + key);
        var dislikeEl = document.getElementById('count-dislike-' + key);
        if (likeEl) likeEl.innerText = likeCount;
        if (dislikeEl) dislikeEl.innerText = dislikeCount;

        if (stored) {{
          disableVoting(key, stored);
        }}
      }})();

      function handleVote(key, type) {{
        if (localStorage.getItem('vote_status_' + key)) return;

        var likeEl = document.getElementById('count-like-' + key);
        var dislikeEl = document.getElementById('count-dislike-' + key);
        var likes = parseInt(likeEl.innerText, 10);
        var dislikes = parseInt(dislikeEl.innerText, 10);

        if (type === 'like') {{
          likes += 1;
          likeEl.innerText = likes;
          localStorage.setItem('vote_count_like_' + key, likes);
        }} else {{
          dislikes += 1;
          dislikeEl.innerText = dislikes;
          localStorage.setItem('vote_count_dislike_' + key, dislikes);
        }}

        localStorage.setItem('vote_status_' + key, type);
        disableVoting(key, type);

        var msg = document.getElementById('vote-msg-' + key);
        if (msg) msg.classList.remove('hidden');
      }}

      function disableVoting(key, type) {{
        var btnLike = document.getElementById('btn-like-' + key);
        var btnDislike = document.getElementById('btn-dislike-' + key);
        if (!btnLike || !btnDislike) return;

        btnLike.disabled = true;
        btnDislike.disabled = true;
        btnLike.classList.add('opacity-60', 'cursor-not-allowed');
        btnDislike.classList.add('opacity-60', 'cursor-not-allowed');

        if (type === 'like') {{
          btnLike.classList.add('bg-emerald-50', 'border-emerald-400', 'text-emerald-700');
        }} else if (type === 'dislike') {{
          btnDislike.classList.add('bg-rose-50', 'border-rose-400', 'text-rose-700');
        }}
      }}
    </script>
    """

def generate_article(item, existing_codes_set):
    brand_name = item.get("brand_name") or item.get("brand_slug", "").capitalize()
    type_slug = item.get("type_slug", "washing")
    brand_slug = item.get("brand_slug", "generic")
    code = item.get("code", "")
    type_name = item.get("type_name", "Бытовая техника")
    title = item.get("title", f"Ошибка {code} {brand_name}")
    short_desc = item.get("short_desc", "")
    alias = item.get("alias_codes", "")

    page_url = f"{SITE_URL}/{type_slug}/{brand_slug}/{code.lower()}.html"
    item_key = f"{type_slug}_{brand_slug}_{code.lower()}"

    crumbs = [
        {"name": "Главная", "url": "/"},
        {"name": type_name, "url": f"/{type_slug}/"},
        {"name": brand_name, "url": f"/{type_slug}/{brand_slug}/"},
        {"name": f"Ошибка {code}", "url": page_url}
    ]

    steps_html = ""
    for idx, step in enumerate(item.get("steps", []), 1):
        steps_html += f"""
        <li class="flex gap-4 items-start">
          <span class="w-8 h-8 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-sm flex-shrink-0 mt-0.5">{idx}</span>
          <div>
            <h4 class="font-bold text-slate-900 text-base">{step.get('title', '')}</h4>
            <p class="text-slate-600 text-sm mt-1 leading-relaxed">{step.get('desc', '')}</p>
          </div>
        </li>
        """

    symptoms_html = "".join([f"<li class='text-slate-700 text-sm flex items-start gap-2.5'><span class='text-amber-500 font-bold mt-0.5'>•</span><span>{s}</span></li>" for s in item.get("symptoms", [])])
    causes_html = "".join([f"<li class='text-slate-700 text-sm flex items-start gap-2.5'><span class='text-rose-500 font-bold mt-0.5'>•</span><span>{c}</span></li>" for c in item.get("causes", [])])

    price_rows = get_repair_prices(code)
    price_table_rows = "".join([f"""
    <tr class="border-b border-slate-100 hover:bg-slate-50/60 transition-colors">
      <td class="py-3.5 px-4 text-slate-800 font-medium text-xs sm:text-sm">{cause}</td>
      <td class="py-3.5 px-4 text-slate-600 text-xs sm:text-sm">{part}</td>
      <td class="py-3.5 px-4 text-slate-600 text-xs sm:text-sm hidden md:table-cell">{work}</td>
      <td class="py-3.5 px-4 text-slate-900 font-bold text-xs sm:text-sm whitespace-nowrap">{cost}</td>
    </tr>
    """ for cause, part, work, cost in price_rows])

    faq_items = [
        {
            "q": f"Можно ли принудительно открыть дверцу при ошибке {code}?",
            "a": f"Если внутри осталась вода, открывать дверцу нельзя. Отключите прибор от электросети 220V, выполните аварийный слив через нижний патрубок или фильтр, после чего блокиратор замка отключится через 2-3 минуты."
        },
        {
            "q": f"Помогает ли сброс ошибки отключением из розетки?",
            "a": f"Отключение из сети на 15-20 минут помогает снять программный сбой процессора при бросках напряжения. Если в узлах стиральной машины есть реальный обрыв цепи, засор или пробой, код ошибки появится снова при перезапуске."
        },
        {
            "q": f"Опасно ли продолжать эксплуатацию при коде {code}?",
            "a": "Продолжать программу не рекомендуется. Работа при заблокированной помпе или пробитом нагревателе приводит к выгоранию силовых симисторов на электронном модуле."
        }
    ]

    faq_html = "".join([f"""
    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50">
      <h4 class="font-bold text-slate-900 text-sm sm:text-base mb-2">{item_faq['q']}</h4>
      <p class="text-slate-600 text-xs sm:text-sm leading-relaxed">{item_faq['a']}</p>
    </div>
    """ for item_faq in faq_items])

    howto_steps = [{"@type": "HowToStep", "name": s.get("title", ""), "text": s.get("desc", "")} for s in item.get("steps", [])]
    faq_schema_entries = [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faq_items]

    combined_schema = [
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": title,
            "description": short_desc,
            "author": {
                "@type": "Person",
                "name": "Алексей Васильев",
                "url": f"{SITE_URL}/author/"
            },
            "step": howto_steps
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": faq_schema_entries
        }
    ]
    schema_json = json.dumps(combined_schema, ensure_ascii=False)

    related_html = ""
    for rel_code in item.get("related_codes", []):
        key = f"{type_slug}_{brand_slug}_{rel_code.lower()}"
        if key in existing_codes_set:
            rel_target = f"/{type_slug}/{brand_slug}/{rel_code.lower()}.html"
            related_html += f"""
            <a href="{rel_target}" class="px-3 py-2 bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 rounded-lg text-xs sm:text-sm transition-colors border border-slate-200">
              Код {rel_code} {brand_name}
            </a>
            """

    alias_badge = f"({alias})" if alias else ""
    voting_widget_html = generate_voting_widget(item_key)

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — причины поломки, как сбросить и устранить</title>
  <meta name="description" content="{short_desc} Инструкция по сбросу ошибки, диагностика мультиметром, чеклист ремонта своими руками и таблица цен.">
  <link rel="canonical" href="{page_url}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{short_desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{page_url}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
  <script type="application/ld+json">{schema_json}</script>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
  {generate_header()}
  {generate_breadcrumbs(crumbs)}

  <main class="max-w-4xl mx-auto px-4 flex-1 w-full pb-12">
    <article class="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm">
      <div class="flex items-center gap-3 mb-4">
        <a href="/{type_slug}/{brand_slug}/" class="text-xs font-bold uppercase tracking-wider text-indigo-700 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-100 hover:bg-indigo-100">
          {brand_name}
        </a>
        <span class="text-xs text-slate-500 font-mono">Код: {code} {alias_badge}</span>
      </div>

      <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-4 tracking-tight">{title}</h1>
      
      <div class="text-sm sm:text-base text-slate-700 leading-relaxed mb-8 bg-indigo-50/50 p-5 rounded-xl border border-indigo-100">
        <strong class="text-slate-900 font-semibold block mb-1">Коротко о проблеме:</strong>
        {short_desc} При фиксации этой неполадки плата блокирует выполнение программы в целях защиты узлов прибора.
      </div>

      <section class="mb-10 p-5 rounded-xl bg-slate-50 border border-slate-200">
        <h2 class="text-lg font-bold text-slate-900 mb-2">Как сбросить ошибку {code} без разборки</h2>
        <p class="text-slate-600 text-xs sm:text-sm leading-relaxed mb-3">
          Исключите программный сбой контроллера из-за перепада напряжения:
        </p>
        <ol class="list-decimal pl-5 space-y-1.5 text-xs sm:text-sm text-slate-700">
          <li>Установите ручку выбора режимов в положение «Выкл».</li>
          <li>Извлеките вилку кабеля питания из розетки на <strong>15–20 минут</strong>.</li>
          <li>Включите питание снова и запустите короткий тестовый режим полоскания без белья.</li>
          <li>Если ошибка {code} появляется повторно — неисправность вызвана физическим дефектом или засором.</li>
        </ol>
      </section>

      <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
        <div class="border border-slate-200 rounded-xl p-5 bg-white">
          <h3 class="font-bold text-slate-900 mb-3 text-base flex items-center gap-2">⚠️ Характерные симптомы</h3>
          <ul class="space-y-2">{symptoms_html}</ul>
        </div>
        <div class="border border-slate-200 rounded-xl p-5 bg-white">
          <h3 class="font-bold text-slate-900 mb-3 text-base flex items-center gap-2">🔍 Основные причины сбоя</h3>
          <ul class="space-y-2">{causes_html}</ul>
        </div>
      </section>

      <section class="mb-10">
        <h2 class="text-xl font-bold text-slate-900 mb-6">Пошаговая инструкция устранения своими руками</h2>
        <ul class="space-y-6">{steps_html}</ul>
      </section>

      {voting_widget_html}

      <section class="mb-10 p-5 rounded-xl bg-slate-50 border border-slate-200">
        <h2 class="text-lg font-bold text-slate-900 mb-2">Проверка электрических компонентов мультиметром</h2>
        <p class="text-slate-600 text-xs sm:text-sm leading-relaxed mb-3">
          Для локализации поломки проверьте сопротивление цепей при отключенном шнуре питания:
        </p>
        <ul class="list-disc pl-5 space-y-2 text-xs sm:text-sm text-slate-700">
          <li><strong>Замер обмотки катушки:</strong> переведите мультиметр в режим 200 Ом. Нулевое сопротивление указывает на КЗ, значение OL (бесконечность) — на обрыв проводника.</li>
          <li><strong>Проверка пробоя на корпус:</strong> установите диапазон 20 МОм. Щупы приложите к корпусу детали и рабочему контакту. Значение должно стремиться к бесконечности.</li>
        </ul>
      </section>

      <section class="mb-10">
        <div class="mb-4">
          <h3 class="text-xl font-bold text-slate-900">Ориентировочная стоимость ремонта</h3>
          <p class="text-slate-500 text-xs sm:text-sm mt-0.5">Средние расценки сервисных центров (стоимость запасных частей оплачивается отдельно)</p>
        </div>
        <div class="overflow-x-auto rounded-xl border border-slate-200">
          <table class="w-full text-left border-collapse bg-white">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 text-xs uppercase tracking-wider">
                <th class="py-3.5 px-4 font-semibold">Причина неисправности</th>
                <th class="py-3.5 px-4 font-semibold">Запчасть под замену</th>
                <th class="py-3.5 px-4 font-semibold hidden md:table-cell">Характер работ</th>
                <th class="py-3.5 px-4 font-semibold">Стоимость работ</th>
              </tr>
            </thead>
            <tbody>
              {price_table_rows}
            </tbody>
          </table>
        </div>
      </section>

      <section class="p-5 rounded-xl bg-amber-50 border border-amber-200 mb-8">
        <h3 class="font-bold text-amber-900 text-base mb-2">🛠 Когда требуется вызов специалиста</h3>
        <p class="text-slate-700 text-sm leading-relaxed">{item.get('master_fix', '')}</p>
      </section>

      <section class="mb-10">
        <h3 class="text-xl font-bold text-slate-900 mb-4">Часто задаваемые вопросы по коду {code}</h3>
        <div class="space-y-3">
          {faq_html}
        </div>
      </section>

      <div class="mt-10 p-5 rounded-2xl bg-slate-50 border border-slate-200 flex flex-col sm:flex-row items-center sm:items-start gap-4">
        <div class="w-16 h-16 rounded-full bg-indigo-600 text-white font-extrabold flex items-center justify-center text-xl flex-shrink-0 shadow-sm">
          АВ
        </div>
        <div class="text-center sm:text-left flex-1">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1 mb-1">
            <span class="font-bold text-slate-900 text-base">Алексей Васильев</span>
            <span class="text-xs font-semibold text-emerald-700 bg-emerald-100/60 px-2 py-0.5 rounded-full inline-block">Мастер высшей категории • Опыт 12 лет</span>
          </div>
          <p class="text-slate-600 text-xs sm:text-sm leading-relaxed mb-2">
            Сертифицированный специалист по диагностике и ремонту бытовой техники ({brand_name}, Bosch, LG, Samsung). Автор регламентов технического обслуживания.
          </p>
          <a href="/author/" class="text-indigo-600 hover:text-indigo-800 text-xs font-semibold inline-flex items-center gap-1">
            Подробнее об эксперте и методике проверки →
          </a>
        </div>
      </div>

      {f'''<section class="border-t border-slate-100 pt-6 mt-8">
        <h3 class="font-bold text-slate-900 text-sm mb-3">Другие коды неисправностей {brand_name}:</h3>
        <div class="flex flex-wrap gap-2">{related_html}</div>
      </section>''' if related_html else ''}
    </article>
  </main>

  {generate_footer()}
</body>
</html>"""

def generate_404_page():
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Страница не найдена — Ошибка 404 | TechErrors Wiki</title>
  <meta name="description" content="Запрошенная страница не существует или была перемещена в другой раздел справочника.">
  <meta name="robots" content="noindex, follow">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
  {generate_header()}

  <main class="max-w-3xl mx-auto px-4 py-20 flex-1 flex flex-col items-center justify-center text-center">
    <div class="w-20 h-20 rounded-3xl bg-indigo-50 border border-indigo-100 text-indigo-600 flex items-center justify-center text-3xl font-extrabold mb-6">
      404
    </div>
    <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 mb-3 tracking-tight">Страница не найдена</h1>
    <p class="text-slate-600 text-sm sm:text-base max-w-md mb-8">
      Возможно, код ошибки был переименован или перемещен. Воспользуйтесь разделами каталога:
    </p>

    <div class="flex flex-wrap justify-center gap-3">
      <a href="/" class="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-sm font-semibold transition-colors shadow-sm">
        На главную страницу
      </a>
      <a href="/washing/" class="px-5 py-2.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-sm font-semibold transition-colors">
        Стиральные машины
      </a>
      <a href="/dishwasher/" class="px-5 py-2.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-sm font-semibold transition-colors">
        Посудомоечные машины
      </a>
    </div>
  </main>

  {generate_footer()}
</body>
</html>"""

def generate_author_page():
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Алексей Васильев — Главный технический эксперт TechErrors Wiki</title>
  <meta name="description" content="Биография, опыт работы и специализация эксперта проекта Алексея Васильева. 12 лет практики ремонта бытовой техники.">
  <link rel="canonical" href="{SITE_URL}/author/">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Алексей Васильев",
    "jobTitle": "Инженер по ремонту бытовой техники",
    "description": "Специалист по сервисному обслуживанию крупной бытовой техники с 12-летним стажем.",
    "url": "{SITE_URL}/author/"
  }}
  </script>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
  {generate_header()}
  {generate_breadcrumbs([{"name": "Главная", "url": "/"}, {"name": "Эксперт проекта", "url": "/author/"}])}

  <main class="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
    <div class="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm">
      <div class="flex flex-col sm:flex-row items-center sm:items-start gap-6 border-b border-slate-100 pb-8 mb-8">
        <div class="w-24 h-24 rounded-full bg-indigo-600 text-white font-extrabold flex items-center justify-center text-3xl flex-shrink-0 shadow-md">
          АВ
        </div>
        <div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-1 text-center sm:text-left">Алексей Васильев</h1>
          <p class="text-indigo-600 font-medium text-sm text-center sm:text-left mb-3">Главный технический консультант и автор справочника</p>
          <div class="flex flex-wrap gap-2 justify-center sm:justify-start">
            <span class="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md text-xs font-medium">Стаж: 12 лет</span>
            <span class="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md text-xs font-medium">Сертификат Bosch / LG</span>
            <span class="px-2.5 py-1 bg-slate-100 text-slate-700 rounded-md text-xs font-medium">Специализация: Электроника и гидравлика</span>
          </div>
        </div>
      </div>

      <div class="space-y-6 text-slate-700 text-sm sm:text-base leading-relaxed">
        <h2 class="text-lg font-bold text-slate-900">Опыт и специализация</h2>
        <p>
          С 2014 года я занимаюсь практическим ремонтом и сервисной диагностикой стиральных, сушильных и посудомоечных машин. За время работы восстановил более 3 500 единиц техники марок Bosch, LG, Samsung, Electrolux, Candy, Indesit и Midea.
        </p>
        <p>
          Основная цель проекта <strong>TechErrors Wiki</strong> — предоставить владельцам техники объективную, структурированную и безопасную инструкцию: какие проблемы можно решить за 5 минут своими руками без переплат мастеру, а в каких случаях действительно требуется профессиональный инструмент и замена сгоревших компонентов.
        </p>

        <h2 class="text-lg font-bold text-slate-900 pt-4">Методология подготовки инструкций</h2>
        <ul class="list-disc pl-5 space-y-2 text-slate-600 text-sm">
          <li>Использование оригинальных сервисных бюллетеней и мануалов производителей при составлении кодов.</li>
          <li>Указание реальных номиналов электрического сопротивления для точной диагностики мультиметром.</li>
          <li>Строгий акцент на технике безопасности при работе с электроприборами.</li>
        </ul>
      </div>
    </div>
  </main>

  {generate_footer()}
</body>
</html>"""

def generate_privacy_page():
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Политика конфиденциальности и использование файлов cookie — TechErrors Wiki</title>
  <meta name="description" content="Политика обработки персональных данных и правила использования файлов cookie справочника TechErrors Wiki.">
  <link rel="canonical" href="{SITE_URL}/privacy/">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
  {generate_header()}
  {generate_breadcrumbs([{"name": "Главная", "url": "/"}, {"name": "Политика конфиденциальности", "url": "/privacy/"}])}

  <main class="max-w-4xl mx-auto px-4 py-8 flex-1 w-full">
    <div class="bg-white rounded-2xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-6 text-slate-700 text-sm sm:text-base leading-relaxed">
      <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-4">Политика конфиденциальности</h1>
      <p class="text-xs text-slate-400">Дата последнего обновления: 2026 год</p>

      <section class="space-y-3">
        <h2 class="text-lg font-bold text-slate-900">1. Общие положения</h2>
        <p>
          Настоящая Политика определяет порядок обработки и защиты технической информации о пользователях сайта <strong>TechErrors Wiki</strong> ({SITE_URL}). Сервис уважает право на конфиденциальность и собирает минимально необходимый объем технических данных для обеспечения бесперебойного функционирования страниц.
        </p>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg font-bold text-slate-900">2. Обрабатываемые данные</h2>
        <p>Сайт является информационно-справочным ресурсом и не собирает паспортные данные или платежные реквизиты. В фоновом режиме могут обрабатываться:</p>
        <ul class="list-disc pl-5 space-y-1 text-slate-600 text-sm">
          <li>Технические обезличенные данные браузера и устройства.</li>
          <li>IP-адрес и файлы cookie для сбора аналитики посещаемости страниц.</li>
          <li>Поисковые запросы, вводимые пользователями на сайте.</li>
        </ul>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg font-bold text-slate-900">3. Использование файлов Cookie</h2>
        <p>
          Файлы cookie применяются для сохранения пользовательских настроек и анализа поведенческих факторов. Вы можете ограничить или полностью отключить сохранение cookie через настройки своего браузера.
        </p>
      </section>

      <section class="space-y-3">
        <h2 class="text-lg font-bold text-slate-900">4. Отказ от ответственности</h2>
        <p>
          Все инструкции публикуются исключительно в ознакомительных целях. Всегда соблюдайте правила электробезопасности. Администрация ресурса не несет ответственности за некорректные действия при самостоятельном разборе приборов.
        </p>
      </section>
    </div>
  </main>

  {generate_footer()}
</body>
</html>"""

def generate_catalog_page(title, meta_desc, heading, desc, crumbs, items, canonical_path):
    cards_html = ""
    for item in items:
        brand_name = item.get("brand_name") or item.get("brand_slug", "").capitalize()
        link = f"/{item['type_slug']}/{item['brand_slug']}/{item['code'].lower()}.html"
        cards_html += f"""
        <a href="{link}" class="bg-white border border-slate-200 rounded-xl p-5 hover:shadow-md transition-shadow group flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider">{brand_name}</span>
              <span class="font-mono font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded text-sm">{item['code']}</span>
            </div>
            <h3 class="font-bold text-slate-900 text-base group-hover:text-indigo-600 transition-colors mb-2">{item['title']}</h3>
            <p class="text-slate-600 text-xs line-clamp-2">{item['short_desc']}</p>
          </div>
          <span class="text-indigo-600 text-xs font-semibold mt-4 block">Инструкция ремонта →</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="{SITE_URL}{canonical_path}">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Inter', sans-serif; }}</style>
</head>
<body class="bg-slate-50 text-slate-900 min-h-screen flex flex-col">
  {generate_header()}
  {generate_breadcrumbs(crumbs)}

  <main class="max-w-5xl mx-auto px-4 py-8 flex-1 w-full">
    <div class="mb-8">
      <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-2">{heading}</h1>
      <p class="text-slate-600 text-sm sm:text-base">{desc}</p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      {cards_html}
    </div>
  </main>

  {generate_footer()}
</body>
</html>"""

def main():
    create_dirs()
    
    # Автопоиск всех файлов database*.json в папке
    database = []
    db_files = sorted(glob.glob("database*.json"))
    
    if not db_files:
        print("Ошибка: не найдено ни одного файла вида database*.json в папке со скриптом!")
        return

    print(f"Обнаружено файлов базы данных: {len(db_files)} -> {db_files}")
    for db_file in db_files:
        try:
            with open(db_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    database.extend(data)
                else:
                    print(f"Предупреждение: файл {db_file} содержит не список, пропущен.")
        except Exception as e:
            print(f"Ошибка при чтении {db_file}: {e}")

    print(f"Всего успешно загружено статей: {len(database)}")

    existing_codes_set = set()
    for item in database:
        t_slug = item.get("type_slug", "washing")
        b_slug = item.get("brand_slug", "generic")
        c = item.get("code", "").lower()
        existing_codes_set.add(f"{t_slug}_{b_slug}_{c}")

    urls = [
        f"{SITE_URL}/",
        f"{SITE_URL}/privacy/",
        f"{SITE_URL}/author/"
    ]

    with open(os.path.join(OUTPUT_DIR, "privacy", "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_privacy_page())

    with open(os.path.join(OUTPUT_DIR, "author", "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_author_page())

    with open(os.path.join(OUTPUT_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(generate_404_page())

    categories = {}
    for item in database:
        t_slug = item.get("type_slug", "washing")
        b_slug = item.get("brand_slug", "generic")
        t_name = item.get("type_name", "Техника")
        b_name = item.get("brand_name") or b_slug.capitalize()

        if t_slug not in categories:
            categories[t_slug] = {"name": t_name, "brands": {}}
        if b_slug not in categories[t_slug]["brands"]:
            categories[t_slug]["brands"][b_slug] = {"name": b_name, "items": []}
        
        categories[t_slug]["brands"][b_slug]["items"].append(item)

    for item in database:
        t_slug = item.get("type_slug", "washing")
        b_slug = item.get("brand_slug", "generic")
        brand_dir = os.path.join(OUTPUT_DIR, t_slug, b_slug)
        os.makedirs(brand_dir, exist_ok=True)
        
        file_path = os.path.join(brand_dir, f"{item['code'].lower()}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(generate_article(item, existing_codes_set))

        urls.append(f"{SITE_URL}/{t_slug}/{b_slug}/{item['code'].lower()}.html")

    for t_slug, t_data in categories.items():
        type_dir = os.path.join(OUTPUT_DIR, t_slug)
        os.makedirs(type_dir, exist_ok=True)
        
        all_type_items = []
        for b_slug, b_data in t_data["brands"].items():
            all_type_items.extend(b_data["items"])

            brand_dir = os.path.join(type_dir, b_slug)
            brand_crumbs = [
                {"name": "Главная", "url": "/"},
                {"name": t_data["name"], "url": f"/{t_slug}/"},
                {"name": b_data["name"], "url": f"/{t_slug}/{b_slug}/"}
            ]
            brand_page = generate_catalog_page(
                title=f"Коды ошибок {t_data['name'].lower()} {b_data['name']} — База поломок",
                meta_desc=f"Все коды ошибок {t_data['name'].lower()} марки {b_data['name']}. Пошаговый ремонт и цены на работы.",
                heading=f"Коды ошибок {t_data['name'].lower()} {b_data['name']}",
                desc=f"Справочник кодов ошибок {b_data['name']}. Диагностика, симптомы и способы решения.",
                crumbs=brand_crumbs,
                items=b_data["items"],
                canonical_path=f"/{t_slug}/{b_slug}/"
            )
            with open(os.path.join(brand_dir, "index.html"), "w", encoding="utf-8") as f:
                f.write(brand_page)
            urls.append(f"{SITE_URL}/{t_slug}/{b_slug}/")

        type_crumbs = [
            {"name": "Главная", "url": "/"},
            {"name": t_data["name"], "url": f"/{t_slug}/"}
        ]
        type_page = generate_catalog_page(
            title=f"Коды ошибок: {t_data['name']} — Справочник",
            meta_desc=f"Каталог неисправностей и кодов ошибок для {t_data['name'].lower()}.",
            heading=f"Ошибки: {t_data['name']}",
            desc="Выберите бренд техники для просмотра кодов ошибок и алгоритмов ремонта.",
            crumbs=type_crumbs,
            items=all_type_items,
            canonical_path=f"/{t_slug}/"
        )
        with open(os.path.join(type_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(type_page)
        urls.append(f"{SITE_URL}/{t_slug}/")

    home_crumbs = [{"name": "Главная", "url": "/"}]
    home_page = generate_catalog_page(
        title="Коды ошибок стиральных и посудомоечных машин — TechErrors Wiki",
        meta_desc="Энциклопедия неисправностей бытовой техники. Расшифровка кодов, причины и самостоятельный ремонт.",
        heading="Энциклопедия кодов ошибок бытовой техники",
        desc="Выберите категорию или нужный код поломки, чтобы быстро починить технику своими руками.",
        crumbs=home_crumbs,
        items=database,
        canonical_path="/"
    )
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_page)

    robots_content = f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    unique_urls = sorted(list(set(urls)))
    sitemap_entries = "\n".join([f"  <url>\n    <loc>{u}</loc>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>" for u in unique_urls])
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{sitemap_entries}
</urlset>"""
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    vercel_config = {
        "cleanUrls": True,
        "trailingSlash": True
    }
    with open(os.path.join(OUTPUT_DIR, "vercel.json"), "w", encoding="utf-8") as f:
        json.dump(vercel_config, f, indent=2)

    print(f"Готово! Обработано {len(database)} статей. Сгенерировано {len(unique_urls)} URL-адресов.")

if __name__ == "__main__":
    main()