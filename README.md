# Manlam Sentences Extractor

呢個專案嘅目的係將文林字典中嘅例句 extract 出嚟，用於訓練機械繙譯模型。

Step 0: Edit `scrape.py` to add your 文林 credentials.

Step 1: Run `scrape.py` to get a list of the titles of all pages under the `Jyut` category.

Step 2: Go to the [export page](https://wenlin.co/wow/Special:Export) to export all the data to an XML file.

Step 3: Postprocessing. (仲未做)

1. Add periods at the end of the sentences.
1. Convert half shape punctuations to full shape.
1. Convert full shape numbers and letters to half shape, e.g. ＤＱ -> DQ
1. Check 著 and 着.
1. Check all the characters that contains 口, e.g. 𠺢 -> 㗎.
