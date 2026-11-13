# Qo'lyozma Telegram Bot ✍️

Telegram'da matnni qo'lyozma uslubidagi rasmga aylantiruvchi bot.

## Qanday ishlaydi

1. Foydalanuvchi botga matn yuboradi
2. Bot matnni qo'lyozma shrifti (Amatic SC) bilan qog'oz foniga chizadi
3. Har bir harfga tasodifiy qiyshaytish qo'shib, tabiiy ko'rinish beradi
4. Rasmni PNG ko'rinishida qaytaradi

## Buyruqlar

| Buyruq | Vazifasi |
|--------|----------|
| `/start` | Botni ishga tushirish |
| `/help` | Yordam |
| `/bold` | Qalin/oddiy shriftni almashtirish |

## Ishga tushirish

```bash
pip install -r requirements.txt
export BOT_TOKEN="Telegram BotFather'dan olingan token"
python bot.py
```

## Token olish

1. Telegram'da [@BotFather](https://t.me/BotFather) ga yozing
2. `/newbot` buyrug'ini yuboring
3. Botga nom bering va token'ni nusxalang

## Eslatma

- Amatic SC shrifti **lotin alifbosini** qo'llab-quvvatlaydi (kirill hozircha ishlamaydi)
- Bir xabarda maksimal 1500 belgi
