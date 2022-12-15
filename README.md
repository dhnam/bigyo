# bigyo
Simple python library for side-by-side diff in terminal.

Use difflib as its engine.

Supports beautiful output with multi-width or zero-width character.

## How to

Replace 
```py
difflib.Differ().compare(a, b)
```
to
```py
bigyo.Bigyo().compare(a, b)
```
and you get your nice side-by-side comparison.

## Bigyo rendering strategy

Default bigyo rendering strategy is `SimpleBigyoStrategy` with default params, which will look like this.
```
- Hello, World |+  Helo, Wold!
?    -     -   |?            +
```

However, you can change separator (defaults to `|`) if you wish, by making `BigyoStrategy` class with parameter,
```py
bigyo_strat = SimpleBigyoStrategy(sep="*")
```
...And give it as parameter of `Bigyo`.
```py
bigyo_cls = bigyo.Bigyo(bigyo_strategy = bigyo_strat)
```

In this case, result will look like this.
```
- Hello, World *+  Helo, Wold!
?    -     -   *?            +
```

Also there exists `OnelineBigyoStrategy` which will render difference like this.
```
He>l<lo, Wo>r<ld|Helo, Wold<!>
```

## History

All the commits can be found in [github page](https://github.com/dhnam/bigyo).

```
0.0.1 2022.12.15 Project init!
```