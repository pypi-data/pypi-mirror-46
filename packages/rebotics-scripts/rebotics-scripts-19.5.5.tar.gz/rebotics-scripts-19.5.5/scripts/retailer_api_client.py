import json
import os
from multiprocessing import Pool

import click
from prettytable import PrettyTable

from sdk.providers import RetailerProvider, ProviderHTTPClientException
from sdk.utils import download_file, mkdir_p, \
    get_filename_from_url
from .renderer import format_processing_action_output
from .utils import ReboticsCLIContext, pass_rebotics_context, app_dir


@click.group()
@click.option('-f', '--format', default='table', type=click.Choice(['table', 'id', 'json']))
@click.option('-v', '--verbose', is_flag=True, help='Enables verbose mode')
@click.option('-c', '--config', type=click.Path(), default='retailers.json', help="Specify what config.json to use")
@click.option('-r', '--role', required=True, help="Key to specify what retailer to use")
@click.version_option()
@click.pass_context
def api(ctx, format, verbose, config, role):
    """
    Retailer CLI tool to communicate with retailer API
    """
    ctx.obj = ReboticsCLIContext(
        role,
        format,
        verbose,
        os.path.join(app_dir, config),
        provider_class=RetailerProvider
    )


@api.command()
@click.option('-u', '--user', prompt=True, )
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('-h', '--host', help='retailer host', prompt=True)
@pass_rebotics_context
def configure(ctx, user, password, host):
    """Fetch token, save it and use the role of it"""
    provider = ctx.provider_class(host=host)
    try:
        response = provider.token_auth(user, password)
    except ProviderHTTPClientException:
        click.echo('Failed to login')
        return

    ctx.update_configuration(
        host=host,
        **response
    )
    click.echo(response, err=True)
    click.echo('Saved configuration for {} retailer in {}'.format(ctx.key, ctx.config.filepath))


@api.command()
@pass_rebotics_context
def version(ctx):
    """Show retailer backend version"""
    click.echo(ctx.provider.version())


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.argument('files', nargs=-1, required=True, type=click.File('rb'))
@pass_rebotics_context
def upload_files(ctx, input_type, store, files):
    """
    Upload processing files to the retailer backend, that can be used as processing action inputs
    """
    file_ids = []
    for f_ in files:
        response = ctx.provider.processing_upload(
            store, f_, input_type
        )
        file_ids.append(response['id'])

        if ctx.verbose:
            click.echo(response)  # redirecting this output to stderr
    click.echo(' '.join(map(str, file_ids)))


REQUEUE_TYPES = {
    "facenet_kf": 'requeue_for_facenet_keyframes_key',
    "pt_multiclass": 'REQUEUE_PRICE_TAGS_DETECTION_MULTICLASS',
    "pt_heatmap": 'REQUEUE_PRICE_TAGS_DETECTION_MULTICLASS_HEATMAP',
    "pt_voting": 'REQUEUE_PRICE_TAGS_DETECTION_MULTICLASS_VOTING',
}


def task_requeue_processing(d):
    provider = d['provider']
    response = provider.requeue(d['id'], d['requeue_type'])
    if d['verbose']:
        click.echo(response)
        click.echo(response['id'])
    return response


def task_cancel_processing(d):
    provider = d['provider']
    response = provider.cancel(d['id'])
    if d['verbose']:
        click.echo(response)
        click.echo(response['id'])
    return response


@api.command()
@click.argument('processing_ids', required=True, nargs=-1, type=click.INT)
@click.option('-t', '--requeue-type', type=click.Choice(choices=REQUEUE_TYPES.keys()), required=False, default=None)
@click.option('-c', '--concurrency', type=int, default=4)
@pass_rebotics_context
def requeue(ctx, processing_ids, requeue_type, concurrency):
    """Requeue processing actions by given IDs"""
    task_arguments = []

    for id_ in processing_ids:
        if ctx.verbose:
            click.echo('Requeue for %d' % id_)

        task_arguments.append({
            'verbose': ctx.verbose,
            'provider': ctx.provider,
            'id': id_,
            'requeue_type': REQUEUE_TYPES.get(requeue_type)
        })

    pool = Pool(concurrency)
    actions_list = pool.map(task_requeue_processing, task_arguments)

    format_processing_action_output(actions_list, ctx.format)


@api.command()
@click.argument('processing_ids', required=True, nargs=-1, type=click.INT)
@click.option('-c', '--concurrency', type=int, default=4)
@pass_rebotics_context
def cancel(ctx, processing_ids, concurrency):
    """Cancel processing of the actions by given IDs"""
    task_arguments = []

    for id_ in processing_ids:
        if ctx.verbose:
            click.echo('Requeue for %d' % id_)

        task_arguments.append({
            'verbose': ctx.verbose,
            'provider': ctx.provider,
            'id': id_,
        })

    pool = Pool(concurrency)
    actions_list = pool.map(task_cancel_processing, task_arguments)

    format_processing_action_output(actions_list, ctx.format)


@api.command()
@click.option('-t', '--input_type')
@click.option('-s', '--store', type=click.INT)
@click.option('-p', '--store-planogram', type=click.INT)
@click.option('--aisle')
@click.option('--section')
@click.option('-l', '--lens-used', is_flag=True, default=False)
@click.argument('files', nargs=-1, required=True, type=click.INT)
@pass_rebotics_context
def create_processing_action(ctx, input_type, store, store_planogram, aisle, section, lens_used, files):
    """Create processing action for store defining files by IDs"""
    response = ctx.provider.create_processing_action(
        store, files, input_type,
        store_planogram=store_planogram,
        aisle=aisle,
        section=section,
        lens_used=lens_used
    )
    if ctx.verbose:
        click.echo(response, )
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
@pass_rebotics_context
def download_processing_action(ctx, actions, target, concurrency):
    """Download processing actions by given IDs"""
    files_to_download = []

    for action_id in actions:
        processing_action_folder = os.path.join(target, 'ProcessingAction#%d' % action_id)

        if ctx.verbose:
            click.echo('Get Processing action %s' % action_id)
        data = ctx.provider.processing_action_detail(action_id)
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
                'filepath': os.path.join(inputs, get_filename_from_url(input_object['file'])),
                'url': input_object['file']
            })

        with open(os.path.join(processing_action_folder, 'processing_action_%d.json' % action_id), 'w') as fout:
            json.dump(data, fout, indent=4)

        if ctx.verbose:
            click.echo('Downloading files for %s' % (action_id,))

    pool = Pool(concurrency)
    pool.map(download_file_from_dict, files_to_download)

    if ctx.verbose:
        click.echo('Processing download success')


def upload_preview_task(d):
    provider = d['provider']
    images_path = d['images_path']
    upc = d['upc']
    delete = d['delete']

    if delete:
        try:
            response = provider.delete_product_previews(upc)
            click.echo('Deleted %s previews for product %s' % (response['deleted'], upc,), err=True)
        except ProviderHTTPClientException:
            click.echo('Product with UPC %s does not exists' % upc, err=True)

    for image_path in images_path:
        with open(image_path, 'rb') as image:
            try:
                provider.upload_product_preview(upc, image)
            except ProviderHTTPClientException as e:
                click.echo("xxx Failed to send image: %s" % image_path)
                click.echo(str(e), err=True)
            click.echo('<< Uploaded product preview for %s from %s' % (upc, image_path), err=True)


@api.command()
@click.option('-d', '--delete', is_flag=True)
@click.option('-c', '--concurrency', type=int, default=4)
@click.argument('path', type=click.Path(exists=True), default=os.getcwd())
@pass_rebotics_context
def upload_previews_from_folder(ctx, delete, concurrency, path):
    """
    Upload previews from file system to the server in parallel
    It has increased retries and timeout
    """
    provider = ctx.provider
    provider.retries = 5
    provider.timeout = 300
    verbose = ctx.verbose

    tasks = []
    for label in os.listdir(path):
        upc_folder = os.path.join(path, label)
        if not os.path.isdir(upc_folder):
            continue

        if verbose:
            click.echo('Reading folder: %s' % upc_folder)
        task = {
            'provider': provider,
            'images_path': [],
            'delete': delete,
            'upc': label
        }

        if label.isdigit():
            for filename in os.listdir(upc_folder):
                image_path = os.path.join(upc_folder, filename)

                if os.path.isfile(image_path):
                    task['images_path'].append(image_path)

        if task['images_path']:
            tasks.append(task)

    if verbose:
        click.echo('Number of tasks: {}'.format(len(tasks)))

    p = Pool(concurrency)
    p.map(upload_preview_task, tasks)
    click.echo('Finished')


PROCESSING_STATUSES = {
    'created': 'action created',
    'done': 'done',
    'error': 'error',
    'interrupted': 'interrupted',
    'progress': "in progress",
}


@api.command()
@click.option('-s', '--store', type=click.INT, help='Store ID')
@click.option('--status', type=click.Choice(PROCESSING_STATUSES.keys()))
@click.option('-p', '--page', type=click.INT, default=1)
@click.option('-r', '--page-size', type=click.INT, default=10)
@pass_rebotics_context
def processing_actions(ctx, store, status, page, page_size):
    """Fetches processing actions and renders them in terminal"""
    table = PrettyTable()
    table.field_names = ['#', 'id', 'store', 'user', 'status',
                         'created', 'last_requeue', 'last_requeue ago', 'time in queue']

    if ctx.verbose:
        click.echo('Getting list of processing actions')
    data = ctx.provider.get_processing_action_list(
        store,
        PROCESSING_STATUSES.get(status),
        page=page,
        page_size=page_size,
    )
    click.echo('Total results: %d' % len(data))
    if ctx.format != 'id':
        format_processing_action_output(data, 'id')
    format_processing_action_output(data, ctx.format)
