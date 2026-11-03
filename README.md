# NetSec Toolbox

> مجموعه‌ی باز و در حال تکمیل از شورتکات‌ها، ترفندها و اسکریپت‌های کاربردی شبکه و امنیت.
> An open, work-in-progress collection of practical networking & security cheatsheets, tricks and starter scripts.

این ریپو **عمداً ناقص** است. هر چیزی که به کارت اومده و اینجا نیست، اضافه کن. / This repo is **intentionally incomplete** — add what you find useful.

## ساختار / Layout

| مسیر / Path | محتوا / Content |
|---|---|
| `cheatsheets/` | شورتکات‌ها و دستورات پرکاربرد (Markdown) |
| `scripts/` | اسکریپت‌های اولیه‌ی قابل توسعه (Python / Bash) |
| `data/` | داده‌های جدولی کوچک (CSV) مثل پورت‌های رایج |
| `scripts/validate.py` | بررسی ساختار فایل‌های داده و شیت‌ها |

## شروع سریع / Quick start

```bash
git clone https://github.com/<your-user>/netsec-toolbox.git
cd netsec-toolbox
python3 scripts/validate.py          # check data & cheatsheet format
python3 scripts/port_check.py example.com 80 443
python3 scripts/ports_lookup.py 22
```

## مشارکت / Contributing

هر PR کوچک خوش‌آمده: یک خط دستور، یک ردیف داده، یا یک اسکریپت ناقص. جزئیات در [CONTRIBUTING.md](CONTRIBUTING.md).

## ⚠️ استفاده‌ی مجاز / Responsible use

فقط روی سیستم‌ها و شبکه‌هایی استفاده کن که مالک‌شان هستی یا اجازه‌ی کتبی داری.
Use only on systems and networks you own or are explicitly authorized to test.

## لایسنس / License

MIT — see [LICENSE](LICENSE).
