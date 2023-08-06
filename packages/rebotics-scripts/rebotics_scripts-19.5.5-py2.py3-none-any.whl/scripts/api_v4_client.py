import json
import mimetypes
import multiprocessing
import os
import re
from multiprocessing import Pool

import click
import requests
from six.moves.urllib_parse import urlparse
from tqdm import tqdm

from sdk.providers import RetailerProvider, ProviderHTTPClientException
from sdk.utils import download_file
from sdk.utils import mkdir_p, get_filename_from_url


class ApiClientException(Exception):
    pass


RETAILER_BASE_URL = None
AUTH_TOKEN = None
USER_ID = None

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'cache-control': 'no-cache',
    'accept-language': 'en-US,en;q=0.9'
}


def is_url(value):
    return urlparse(value).scheme != ''


@click.group()
@click.option('-r', '--retailer')
@click.option('-h', '--host')
@click.option('-u', '--user', prompt=True, )
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.pass_context
def api(ctx, retailer, host, user, password):
    """
    This action will login you into retailer that you provide.
    """
    ctx.ensure_object(dict)
    global AUTH_TOKEN, RETAILER_BASE_URL, USER_ID
    if host is None:
        if retailer is None:
            RETAILER_BASE_URL = 'http://china.reboticsdemo.net'
        if retailer:
            response = requests.post('http://admin.rebotics.net/retailers/host/', data={
                'company': retailer
            }).json()
            RETAILER_BASE_URL = response['host']
    else:
        RETAILER_BASE_URL = host
    provider = RetailerProvider(host=RETAILER_BASE_URL, retries=1)
    try:
        provider.api_login(user, password)
        click.echo("Successfully logged in for retailer", err=True)
    except ProviderHTTPClientException:
        raise ProviderHTTPClientException("Failed To login")
    ctx.obj['provider'] = provider


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@click.pass_context
def upload_files(ctx, input_type, store, files):
    provider = ctx.obj['provider']
    file_ids = []
    for f_ in files:
        response = provider.processing_upload(
            store, f_, input_type
        )
        click.echo(response, err=True)  # redirecting this output to stderr
        file_ids.append(response['id'])
    click.echo(' '.join(map(str, file_ids)))


@api.command()
@click.argument('processing_id', type=click.INT, required=True)
@click.pass_context
def requeue(ctx, processing_id):
    provider = ctx.obj['provider']
    response = provider.requeue(processing_id)
    click.echo(response, err=True)
    click.echo(response['id'])


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.option('-p', '--store-planogram', type=click.INT)
@click.option('--aisle')
@click.option('--section')
@click.option('-l', '--lens-used', is_flag=True, default=False)
@click.argument('files', nargs=-1, required=True, type=click.INT)
@click.pass_context
def create_processing_action(ctx, input_type, store, store_planogram, aisle, section, lens_used, files):
    provider = ctx.obj['provider']

    response = provider.create_processing_action(
        store, files, input_type,
        store_planogram=store_planogram,
        aisle=aisle,
        section=section,
        lens_used=lens_used
    )
    click.echo(response, err=True)
    click.echo(response['id'])


def download_file_from_dict(d):
    click.echo('>> Downloading file into %s' % d['filepath'], err=True)
    result = download_file(d['url'], d['filepath'])
    click.echo('<< Downloaded file into %s' % d['filepath'], err=True)
    return result


@api.command()
@click.argument('actions', nargs=-1, required=True, type=click.INT)
@click.option('-t', '--target', type=click.Path(), default='.')
@click.option('-c', '--concurrency', type=int, default=4)
@click.pass_context
def download_processing_action(ctx, actions, target, concurrency):
    provider = ctx.obj['provider']

    pool = Pool(concurrency)
    files_to_download = []

    for action_id in actions:
        processing_action_folder = os.path.join(target, 'ProcessingAction#%d' % action_id)

        click.echo('Get Processing action %s' % action_id, err=True)
        data = provider.processing_action_detail(action_id)
        mkdir_p(processing_action_folder)
        results = os.path.join(processing_action_folder, 'results')
        inputs = os.path.join(processing_action_folder, 'inputs')

        mkdir_p(results)
        mkdir_p(inputs)

        for key in ['merged_image_jpeg', 'merged_image', ]:
            files_to_download.append({
                'url': data[key],
                'filepath': os.path.join(results, get_filename_from_url(data[key]))
            })

        for input_object in data.get('inputs', []):
            files_to_download.append({
                'filepath': os.path.join(get_filename_from_url(input_object['file'])),
                'url': input_object['file']
            })

        with open(os.path.join(processing_action_folder, 'processing_action_%d.json' % action_id), 'w') as fout:
            json.dump(data, fout, indent=4)

        click.echo('Downloading files for %s' % (action_id,), err=True)

    pool = Pool(concurrency)
    pool.map(download_file_from_dict, files_to_download)

    click.echo('Processing download success', err=True)


def ignore_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            click.echo(e)

    return wrapper


def upload_preview_forced(args):
    try:
        return upload_preview(args)
    except Exception as e:
        click.echo(e)
        return 'error'


def upload_preview_from_fs_forced(args):
    try:
        return upload_preview_from_fs(args)
    except Exception as e:
        click.echo(e)
        return e


def api_upload_preview(label, image, url, user_id, auth_token):
    response = requests.post(
        url,
        data={
            'product_unique_id': label,
            'user': user_id,
            'token': auth_token
        },
        files={
            'image': image
        },
    )
    if response.status_code >= 300:
        click.echo('Failed for {} {}'.format(label, response.reason))
        click.echo(response.content)

    return response.status_code


# Using decorator with map does not work.
# @ignore_exception
def upload_preview(args):
    global AUTH_TOKEN, RETAILER_BASE_URL, USER_ID
    # download image
    label, image_url = args

    if not is_url(image_url):
        return 'Not URL'

    click.echo('Downloading upc [{}] : {}'.format(label, image_url))
    response = requests.get(image_url, headers=headers)

    if response.status_code != 200:
        return response.status_code

    content_type = response.headers.get('content-type')
    if 'webp' in content_type:
        click.echo('We can not upload webp for upc [{}] : {}'.format(label, image_url))
        return 0

    if 'html' in content_type:
        return 'html' + response.status_code

    raw_image = response.content

    # do post request to the retailer server
    click.echo('Uploading to the retailer server {} : {} {}'.format(label, image_url, content_type))
    return api_upload_preview(label, raw_image, RETAILER_BASE_URL + '/api/v4/products/previews/', USER_ID, AUTH_TOKEN)


def upload_preview_from_fs(args):
    global AUTH_TOKEN, RETAILER_BASE_URL, USER_ID

    label, filename = args
    click.echo('Uploading to the server {} : {}'.format(label, filename))
    with open(filename, 'rb') as raw_image:
        return api_upload_preview(label, raw_image, RETAILER_BASE_URL + '/api/v4/products/previews/', USER_ID, AUTH_TOKEN)


@api.command()
@click.argument('csv_file', type=click.File())
# @click.argument('processed_items_list', type=click.File())
def upload_from_csv(csv_file):
    import csv
    reader = csv.reader(csv_file)
    tasks = []

    click.echo('registering items')
    for i, row in enumerate(tqdm(reader)):
        if i == 0:
            continue  # reading header
        label = row[0]
        image_url = row[1]
        tasks.append((label, image_url))
    # filter out the same items
    tasks = list(set(tasks))

    p = Pool(multiprocessing.cpu_count())
    results = p.map(upload_preview_forced, tasks)
    print('****************************************')
    print(results)
    print('****************************************')


@api.command()
@click.option('-p', '--path', type=click.Path(exists=True), default=os.getcwd())
def upload_from_folder(path):
    """
    Upload previews from file system to the server in parallel
    :param path:
    :return:
    """
    tasks = []
    for label in os.listdir(path):
        upc_folder = os.path.join(path, label)

        if os.path.isdir(upc_folder):
            for filename in os.listdir(upc_folder):
                image_path = os.path.join(upc_folder, filename)

                if os.path.isfile(image_path):
                    tasks.append((label, image_path))

    tasks = list(set(tasks))
    click.echo('Number of tasks: {}'.format(len(tasks)))
    p = Pool(multiprocessing.cpu_count())
    results = p.map(upload_preview_from_fs_forced, tasks)

    print('****************************************')
    print(results)


@api.command()
@click.option('-p', '--path', type=click.Path(exists=True), default=os.getcwd())
@click.argument('excel', type=click.Path(exists=True))
def upload_previews(path, excel):
    """Uploads previews with defined excel file and specified folder where the files in excel file could be found
    """
    global AUTH_TOKEN, RETAILER_BASE_URL, USER_ID

    # noinspection PyMethodMayBeStatic,PyShadowingNames,PyShadowingBuiltins
    class ExcelRow(object):
        def __init__(self, index, title, barcode, folder, file_names, file_format, types):
            self.index = index
            self.title = title
            self.barcode = self._clean_barcode(barcode)
            self.folder = folder
            self.files = self._parse_files(file_names)
            self.format = self._parse_format(file_format)
            self.types = types
            self.host = RETAILER_BASE_URL
            self.path = path
            self.auth_token = AUTH_TOKEN

        def _parse_files(self, file_names):
            return filter(lambda x: x, re.split(r'\s+|/', file_names))

        def _parse_format(self, _format):
            # click.echo("Using parse for {}".format(format))
            return _format

        def upload(self):
            for file in self.files:
                mimetype, encoding = mimetypes.guess_type(file)
                if not mimetype:
                    click.echo("The filetype is None for file named: {}".format(file))
                    continue
                _type, _subtype = mimetype.split('/')
                file = os.path.join(self.path, file)
                if _type in ['video', 'image']:
                    self.do_upload(file, format=_type)
                else:
                    click.echo("Unknown file")

        def do_upload(self, file, format):
            endpoint = '/api/v4/products/previews/'
            if format == 'video':
                endpoint = '/api/v4/products/previews/videos/'
            data = self.get_post_data()
            try:
                files = {
                    format: open(file, 'rb')
                }
            except IOError:
                # skip this file
                raise ApiClientException("File was not found or could not be opened at path: {}".format(file))
            response = requests.post(
                self.host + endpoint,
                data=data,
                files=files,
                )
            if response.status_code >= 400:
                raise ApiClientException("Upload was unsuccessful. {}".format(response.reason))
            click.echo("Success for {} in {}".format(self.barcode, file))

        def get_post_data(self):
            return {
                'product_unique_id': self.barcode,
                'product_name': self.title,
                'user': USER_ID,
                'token': AUTH_TOKEN
            }

        def _clean_barcode(self, barcode):
            try:
                return str(int(barcode))
            except ValueError:
                return str(barcode)

    parsed_excel = []
    import xlrd
    book = xlrd.open_workbook(excel)
    sheet = book.sheet_by_index(0)

    for index in range(1, sheet.nrows):
        values = sheet.row_values(index)
        # click.echo(values)
        parsed_excel.append(ExcelRow(*values))

    succeed = 0
    failed = 0
    for item in tqdm(parsed_excel):
        item.path = path
        item.host = RETAILER_BASE_URL

        # noinspection PyBroadException
        try:
            item.upload()
            succeed += 1
        except ApiClientException as e:
            click.echo(e)
            failed += 1
        except Exception:
            failed += 1

    click.echo("Succeed: {}. Failed: {}".format(succeed, failed))
