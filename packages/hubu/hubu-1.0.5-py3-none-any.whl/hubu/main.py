import logging
import os
import time
from urllib.parse import urlparse
from hubu.download_manager import DownloadManager
from hubu.downloadable import Downloadable
from hubu.humble_bundle import HumbleBundle


if 'HUMBLE_BUNDLE_SESSION' not in os.environ:
    raise Exception('HUMBLE_BUNDLE_SESSION is not defined')
sess = os.environ.get('HUMBLE_BUNDLE_SESSION')


def main():
    logging.basicConfig(
        level=getattr(
            logging,
            'INFO',
            None),
        format='%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s')

    with DownloadManager(workers=5) as mng:
        acceptable_platforms = [
            'ebook', 'video'
        ]
        sum_size = 0
        purchases = HumbleBundle(sess).purchases()
        for purchase in purchases:
            for product in purchase.products():
                for d in product['downloads']:
                    if d['platform'] not in acceptable_platforms:
                        continue
                    for ds in d['download_struct']:
                        if 'name' not in ds or 'url' not in ds:
                            continue

                        if ds['name'] == 'PDF (HD)':
                            ds['name'] = 'PDF'
                        if ds['name'] == 'PDF (HQ)':
                            ds['name'] = 'PDF'

                        url = urlparse(ds['url']['web'])
                        filename = os.path.basename(url.path)
                        sum_size += ds['file_size']
                        item = Downloadable(bundle=purchase.sanitized_name,
                                            name=product['slugify_name'],
                                            platform=d['platform'],
                                            filename=filename,
                                            url=ds['url']['web'],
                                            size=ds['file_size'])

                        mng.add(item)

        while not mng.queue().empty():
            mng.status_line()
            time.sleep(1)
            pass
