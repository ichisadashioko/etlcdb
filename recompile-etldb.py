import os
import io
import argparse
import json
import hashlib

from tqdm import tqdm
import bitstring
import numpy as np
import PIL.Image

import shared

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')

    args = parser.parse_args()

    print(args)

    # === ETL2 === #
    print('Starting to serialize ETL2...')
    part_filepaths = [
        'ETL2/ETL2_1',
        'ETL2/ETL2_2',
        'ETL2/ETL2_3',
        'ETL2/ETL2_4',
        'ETL2/ETL2_5',
    ]

    for part_filepath in part_filepaths:
        if not os.path.exists(part_filepath):
            raise Exception(part_filepath, 'does not exist!')

    metadata_filepath = f'etl2-metadata.json'
    png_image_packed_filepath = f'etl2-png-images.pack.bin'

    if os.path.exists(metadata_filepath):
        if not args.force:
            raise Exception(metadata_filepath + ' is already existed!')

    if os.path.exists(png_image_packed_filepath):
        if not args.force:
            raise Exception(png_image_packed_filepath + ' is already existed!')

    IMG_WIDTH = 60
    IMG_HEIGHT = 60

    bitstring_unpack_str = ','.join([
        'int:36', # Serial Index - [0]
        'uint:6', # Source ('A': Mincho Newspaper, 'B': Gothic Newspaper, 'C': Mincho Patent, 'D': Gothic Patent) - [1]
        'pad:30', # padding bits - no index as they are skipped
        '6*uint:6', # Class ('KANJI': kanji, 'EIJI': roman alphabets, 'HRKANA': hiragana, 'KTKANA': katakana, 'KIGO': special characters, 'SUUJI': numbers) - [2:8]
        '6*uint:6', # Font ('MINCHO', 'GOTHIC') - [8:14]
        'pad:24', # padding bits
        '2*uint:6', # CO-59 Code - [14:16]
        'pad:180', # padding bits
        'bytes:2700', # 6-bit-depth image of 60 x 60 = 3600 pixels - [16]
    ])

    metadata_records = []

    with open(png_image_packed_filepath, mode='wb') as outfile:
        pbar = tqdm(part_filepaths)
        for part_filepath in pbar:
            pbar.set_description(part_filepath)

            infile = bitstring.ConstBitStream(filename=part_filepath)

            while True:
                try:
                    unpacked_data = infile.readlist(bitstring_unpack_str)
                except:
                    break

                pil_image = PIL.Image.frombytes('F', (IMG_WIDTH, IMG_HEIGHT), unpacked_data[16], 'bit', 6)
                np_image = np.array(pil_image, dtype=np.uint8)
                # scale up image color
                np_image = np_image * 4 # 256 / (2**6)
                pil_image = PIL.Image.fromarray(np_image)

                buffer = io.BytesIO()
                pil_image.save(buffer, format='PNG')
                png_encoded_image = buffer.getvalue()

                index_in_dataset = unpacked_data[0]
                scan_source_material_id = shared.T56(unpacked_data[1])
                symbol_type_id = ''.join(map(shared.T56, unpacked_data[2:8]))
                font_name = ''.join(map(shared.T56, unpacked_data[8:14]))
                unicode_char = shared.CO59[tuple(unpacked_data[14:16])]

                seek_start = outfile.tell()
                outfile.write(png_encoded_image)
                seek_end = outfile.tell()

                metadata_entry = {
                    # required info
                    'UNICODE_CHAR': unicode_char,
                    'WIDTH':IMG_WIDTH,
                    'HEIGHT':IMG_HEIGHT,
                    'DEPTH': 1,
                    'PNG_IMAGE_SEEK_START': seek_start,
                    'PNG_IMAGE_SEEK_END': seek_end,

                    # optional info
                    'ORIGINAL_DATASET_NAME': 'ETL2',
                    'INDEX_IN_ORIGINAL_DATASET': index_in_dataset,
                    'SCAN_SOURCE_MATERIAL_ID': scan_source_material_id,
                    'SYMBOL_TYPE_ID': symbol_type_id,
                    'FONT_NAME': font_name,
                }

                metadata_records.append(metadata_entry)

                pbar.set_description(f'{part_filepath} - {unicode_char} - {index_in_dataset}')

    # hash the packed file
    md5_checksum_m = hashlib.md5()
    with open(png_image_packed_filepath, mode='rb') as infile:
        bs = infile.read(1024)
        while len(bs) > 0:
            md5_checksum_m.update(bs)
            bs = infile.read(1024)

    md5_checksum = md5_checksum_m.hexdigest()

    dataset_metadata = {
        'PNG_PACKED_FILENAME': os.path.basename(png_image_packed_filepath),
        'PNG_PACKED_CHECKSUM': md5_checksum,
        'RECORDS': metadata_records,
    }

    with open(metadata_filepath, mode='wb') as outfile:
        content_bytes = json.dumps(dataset_metadata, ensure_ascii=False, indent='\t').encode('utf-8')
        outfile.write(content_bytes)
    # ============ #

    # === ETL3 === #

    # ============ #

if __name__ == '__main__':
    main()
