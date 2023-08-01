---
title: "Table-driven tests for Python"
date: 2023-08-02T02:31:12+09:00
categories: ["Python", "Programming"]
tags: ["Python", "テスト", "初心者向け"]
draft: false
---

Pythonで "Table-driven tests" をどう書くか, という初心者向けのお話です.

<!--more-->

なんの気なしにこういうテストコードを書いてきましたが, これを "Table-driven tests"
と呼ぶことがあるそうです. Golang を使うようになって初めて知りました.


```python
def power(m, n):
    return m ** n

class SampleTest(unittest.TestCase):

    def test_power(self):
        testcases = (
            ((1, 1), 1),
            ((2, 2), 4),
            ((3, 3), 27),
        )
        for in_, wants in testcases:
            self.assertEqual(power(*in_), wants)
```

この例でいうと, `testcases` というシーケンスに入力と期待値を入れておいて,
それをひとつずつ評価するイメージですね.

ところでこのコードはすべてのテストが成功しますが, 例えばシーケンスの1件目のテストで失敗すると,
2件目以降のテストが実行されません. なので, assertメソッドの第3引数を指定して,
どのテストで失敗したのかわかるようにしていたものでした.

```python
testcases = (
    ((1, 1), 1, "test 1"),
    ((2, 2), 6, "test 2"), # ここで失敗する
    ((3, 3), 27, "test 3"),
)
for in_, wants, title in testcases:
    self.assertEqual(power(*in_), wants, title)
```

実行結果.

```plaintext
test_power (__main__.SampleTest.test_power) ... FAIL

======================================================================
FAIL: test_power (__main__.SampleTest.test_power)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<stdin>", line 15, in test_power
AssertionError: 4 != 6 : test 2

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

しかし, 失敗したあとに書いてあるテストが実行されない問題は解決されません.
3件目も失敗するデータであったとしたら, テスト実行とエラー内容を修正するごとに繰り返す必要がでてきてしまいます.

これテストフレームワーク側にちゃんと解決方法が用意されていて, Python標準のunittest であれば,
`self.subtest` を使ってあげればいいだけなのです.

```python
testcases = (
    ((1, 1), 1),
    ((2, 2), 6), # 失敗する
    ((3, 3), 9), # 失敗する
)
for n, (in_, wants) in enumerate(testcases, 1):
    with self.subTest(no=n):
        self.assertEqual(power(*in_), wants)
```

実行結果.

```plaintext
test_power (__main__.SampleTest.test_power) ...
  test_power (__main__.SampleTest.test_power) (no=2) ... FAIL
  test_power (__main__.SampleTest.test_power) (no=3) ... FAIL

======================================================================
FAIL: test_power (__main__.SampleTest.test_power) (no=2)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<stdin>", line 16, in test_power
AssertionError: 4 != 6

======================================================================
FAIL: test_power (__main__.SampleTest.test_power) (no=3)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "<stdin>", line 16, in test_power
AssertionError: 27 != 9

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=2)
```

出力があまり変わっていないのですが, どのテストで失敗したかが表示されていて,
ちゃんとシーケンス内のテストすべてが実行されています.

不勉強なことにこれも最近になって知りました.
手元で使うことがある他の言語のテストでも, 似たようなアプローチができるようになっていました.

いままでごめんなさーい.
