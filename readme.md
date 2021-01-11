# [Japanese Character Database](http://etlcdb.db.aist.go.jp)

## Repack specification

- The metadata will be stored in a JSON file.
- Each record metadata will guarantee to contain at least the following keys.

```json5
{
    "title": "Record",
    "type": "object",
    "required": [
        "char",
        "dataset_source",
        "width",
        "height",
        "seek_start",
        "seek_end",
    ],
    "properties": {
        "char": {
            "type": "string",
            "description": "The label char. If the label is invalid, it will start with 'null_'.",
        },
        "dataset_source": {
            "type": "string",
            "description": "The etlcdb data source file name.",
        },
        "width": {
            "type": "number",
            "description": "The image width.",
        },
        "height": {
            "type": "number",
            "description": "The image height.",
        },
        "seek_start": {
            "type": "number",
            "description": "The PNG image data (in bytes) starting position in the packed image data binary which contains image data for mulitple records.",
        },
        "seek_end": {
            "type": "number",
            "description": "The PNG image data (in bytes) ending position in the packed image data binary which contains image data for mulitple records.",
        },
    },
}
```

- There will be other properties in each records based on the source dataset.
- The PNG images can be either in grayscale (pixel values range from 0 to 255) or in binary (pixel values are either 0 or 1). Because of that caution should be taken when normalizing data in range of `[0,1]` before passing it to the machine learning model.

## Cleaning dataset status

- [ ] ETL2
- [ ] ETL3
- [ ] ETL4
- [ ] ETL5
- [ ] ETL6
- [ ] ETL7
- [ ] ETL8G
- [ ] ETL8B2
- [ ] ETL9G
- [ ] ETL9B

## ETL2

- 52786 samples
- 2168 classes (symbols, hiragana, katakana, kanji, english alphabet)
- image_width: 60px
- image_height: 60px

## ETL3

This dataset contains numbers (0-9), English alphabet letters and symbols with each has 200 samples.

## ETL4

This dataset contains 51 hiragana characters with 120 samples each.

## ETL5

This dataset contains 51 katakana characters with 208 samples each.

## ETL8B

- 153916 samples
- 956 classes (hiragana and kanji)
- 161 samples each class
- image_width: 64px
- image_height: 63px

## ETL9G

- 607200 samples
- 3036 classes (hiragana and kanji)
- 200 samples each class
- record_length: 8199 bytes
- image_width: 128px
- image_height: 127px
