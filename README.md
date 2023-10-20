# 1C Задача №4
Утилита для сравнения файлов в двух директориях
# Автор
Бельский Дмитрий Б05-128
## Использование:
```
python cmp.py dir1 dir2 minPercentage
```
где $dir1, dir2$ - абсолютный/относительный до дтректорий сравнения, $minPercentage$ - минимальное значение процента схожести файлов для их соотношения друг с другом

для установки нужных модулей:
```
pip install -r requirements.txt
```

## Внутреннее устройство
при достаточно малых (для приемлемого времени работы) размерах файлов для их сравнения используется алгоритм [Longest common subsequence](https://en.wikipedia.org/wiki/Longest_common_subsequence)
иначе используется последовательное посимвольное сравнение файлов
