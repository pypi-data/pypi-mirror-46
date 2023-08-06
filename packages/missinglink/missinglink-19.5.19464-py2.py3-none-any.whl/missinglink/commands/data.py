# -*- coding: utf-8 -*-
import os
from collections import defaultdict
from contextlib import closing
from uuid import uuid4

import click
import sys

import humanize

from missinglink.core.api import ApiCaller
from missinglink.core.avro_utils import AvroWriter, AvroWriterErrors
from missinglink.core.eprint import eprint
from missinglink.core.exceptions import MissingLinkException

from missinglink.legit.data_sync import DataSync, InvalidJsonFile, InvalidMetadataException, status_with_timing
from missinglink.legit import MetadataOperationError
from missinglink.legit.metadata_files import MetadataFiles
from missinglink.legit.data_volume_config import SHARED_STORAGE_VOLUME_FIELD_NAME
from tqdm import tqdm
from missinglink.commands.commons import add_to_data_if_not_none, output_result, is_empty_str, api_get
from missinglink.legit.data_volume import create_data_volume, with_repo, default_data_volume_path, with_repo_dynamic, \
    map_volume, get_data_volume_details
from missinglink.legit.path_utils import expend_and_validate_path, safe_make_dirs, safe_rm_tree, \
    DestPathEnum, has_moniker, bucket_print_name, enumerate_paths_with_info, AccessDenied, enumerate_paths
import json

from missinglink.commands.utilities.options import CommonOptions, DataVolumeOptions, DataVolumeIdParamType

BUCKET_NAME_PROPERTY = 'bucket_name'


@click.group('data')
def data_commands():
    pass


def __expend_and_validate_path(path, expand_vars=True, validate_path=True, abs_path=True):
    try:
        return expend_and_validate_path(path, expand_vars, validate_path, abs_path)
    except (IOError, OSError):
        click.echo('Folder not found %s' % path, err=True)
        sys.exit(1)


@data_commands.command('map')
@DataVolumeOptions.data_volume_id_argument()
@DataVolumeOptions.data_path_option()
@click.pass_context
def _cmd_add_data_path(ctx, volume_id, data_path):
    config = map_volume(ctx, volume_id, data_path)

    display_name = config.general_config.get('display_name', 'No display name provided')
    click.echo('Initialized data volume %s (%s)' % (config.volume_id, display_name))


def __validate_storage_volume_id(ctx, storage_volume_id, linked, bucket):
    if linked:
        click.echo('Shared storage volume option is not supported in linked mode', err=True)
        sys.exit(1)

    storage_volume_config = get_data_volume_details(ctx, storage_volume_id)
    storage_volume_bucket = __get_volume_bucket(storage_volume_config)
    if not is_empty_str(bucket) and bucket != storage_volume_bucket:
        msg = 'The specified volume bucket ({}) ' \
              'cannot be different than the shared storage volume bucket ({})'.format(bucket, storage_volume_bucket)
        click.echo(msg, err=True)
        sys.exit(1)

    return storage_volume_config


def __get_volume_bucket(volume_config):
    return volume_config.get(BUCKET_NAME_PROPERTY)


def __get_store_params(bucket, storage_volume_id):
    params = {}

    object_store = {}
    if bucket:
        object_store[BUCKET_NAME_PROPERTY] = bucket
    if storage_volume_id:
        object_store[SHARED_STORAGE_VOLUME_FIELD_NAME] = storage_volume_id

    if object_store:
        params['object_store'] = object_store

    return params


@data_commands.command('create')
@CommonOptions.display_name_option()
@CommonOptions.description_option()
@CommonOptions.org_option()
@DataVolumeOptions.data_path_option(required=False)
@click.option('--bucket')
@click.option('--linked/--embedded', is_flag=True, default=False)
@click.option('--shared-storage-volume-id', required=False, type=DataVolumeIdParamType(),
              help="The data volume ID to store the files on. Supported only in embedded mode.")
@click.pass_context
def _cmd_create_data_volume(ctx, display_name, description, org, data_path, bucket, linked, shared_storage_volume_id):
    if shared_storage_volume_id is not None:
        storage_volume_config = __validate_storage_volume_id(ctx, shared_storage_volume_id, linked, bucket)
        bucket = __get_volume_bucket(storage_volume_config)

    data = {}

    add_to_data_if_not_none(data, display_name, "display_name")
    add_to_data_if_not_none(data, org, "org")
    add_to_data_if_not_none(data, description, "description")
    add_to_data_if_not_none(data, not linked, "embedded")
    add_to_data_if_not_none(data, shared_storage_volume_id, SHARED_STORAGE_VOLUME_FIELD_NAME)

    expiration = ctx.obj.config.readonly_items('data_volumes').get('expiration')
    if expiration:
        data['expiration'] = expiration

    if bucket is not None:
        data['bucket'] = bucket

    result = ApiCaller.call(ctx.obj, ctx.obj.session, 'post', 'data_volumes', data, is_async=True)

    data_volume_id = result['id']

    data_path = __expend_and_validate_path(data_path)

    params = __get_store_params(bucket, shared_storage_volume_id)

    create_data_volume(data_volume_id, data_path, linked, display_name, description, **params)

    output_result(ctx, result)


@data_commands.command('config')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--edit', is_flag=True)
def edit_config_file(volume_id, edit):
    path = os.path.join(default_data_volume_path(volume_id), 'config')

    if edit:
        os.system('open -a TextEdit %s' % path)
        return

    with open(path) as f:
        click.echo(f.read())


@data_commands.command('commit')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--message', '-m', required=False)
@DataVolumeOptions.isolation_token_option()
@click.pass_context
def commit_data_volume(ctx, volume_id, message, isolation_token):
    with with_repo_dynamic(ctx, volume_id) as repo:
        result = repo.commit(message, isolation_token) or {}

        if 'commit_id' not in result:
            click.echo('no changeset detected', err=True)

        output_result(ctx, result)


def process_moniker_data_path(data_path):
    from six.moves.urllib.parse import urlparse, urlunparse

    if not has_moniker(data_path):
        return data_path

    parts = urlparse(data_path)

    return urlunparse((parts.scheme, parts.netloc, '', '', '', ''))


def __print_transfer_info(repo, data_path):
    embedded = repo.data_volume_config.object_store_config.get('embedded')

    if embedded:
        bucket_name = repo.data_volume_config.object_store_config.get('bucket_name')

        if bucket_name:
            click.echo('Transfer files from %s to %s' % (bucket_print_name(repo.data_path), bucket_print_name(bucket_name)), err=True)
        else:
            click.echo('Transfer files from %s to MissingLink secure bucket' % (bucket_print_name(repo.data_path),), err=True)
    else:
        click.echo('Indexing files from %s' % (bucket_print_name(data_path)), err=True)


@data_commands.command('set-metadata', help='Appends a set of metadata to all the files in the specified path.')
@DataVolumeOptions.data_path_option()
@click.option('--append/--replace', default=False, help='In case metadata with the same key already exists, `--append` will not replace it, and `--replace` will. Defaults to `--replace`')
@click.option('--metadata-string', '-ms', multiple=True, type=(str, str), help='String metadata values to update. You can provide multiple values in key-value format.')
@click.option('--metadata-num', '-mm', multiple=True, type=(str, int), help='Integer metadata values to update. You can provide multiple values in key-value format.')
@click.option('--metadata-float', '-mf', multiple=True, type=(str, float), help='Float metadata values to update. You can provide multiple values in key-value format.')
@click.option('--metadata-boolean', '-mb', multiple=True, type=(str, bool), help='Boolean metadata values to update. You can provide multiple values in key-value format.')
@click.pass_context
def set_metadata(ctx, data_path, append, metadata_num, metadata_float, metadata_boolean, metadata_string):
    new_values_dict = {}

    for values in (metadata_num, metadata_float, metadata_boolean, metadata_string):
        for key, value in values:
            new_values_dict[key] = value

    def get_current_metadata(file_path):
        try:
            with open(file_path + '.metadata.json') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_meta(file_path, metadata):
        with open(file_path + '.metadata.json', 'w') as f:
            return json.dump(metadata, f)

    for root, subdirs, files in os.walk(data_path):
        for filename in files:
            if filename.endswith('.metadata.json'):
                continue
            file_path = os.path.join(root, filename)
            cur_meta = get_current_metadata(file_path)
            new_meta = {}
            if append:
                new_meta.update(new_values_dict)
                new_meta.update(cur_meta)
            else:
                new_meta.update(cur_meta)
                new_meta.update(new_values_dict)
            save_meta(file_path, new_meta)
            click.echo('%s meta saved' % file_path, err=True)


def __validate_handle_index_and_metadata_results(method, data_path, isolation_token=None):
    try:
        FileNotFoundError
    except NameError:
        FileNotFoundError = IOError

    try:
        return method(data_path, isolation_token=isolation_token)
    except InvalidJsonFile as ex:
        click.echo('Invalid json file %s (%s)' % (ex.filename, ex.ex), err=True)
        sys.exit(1)
    except (AccessDenied, FileNotFoundError) as ex:
        click.echo(str(ex))
        sys.exit(1)
    except InvalidMetadataException as ex:
        def format_errors(errors):
            separator = '{}\t'.format(os.linesep)
            return ('Invalid metadata file {file_name}:{separator}{file_errors}'.format(
                file_name=err.filename, separator=separator, file_errors=separator.join(err.errors)) for err in errors)

        eprint(*format_errors(ex.errors), sep=os.linesep)
        sys.exit(1)


def __handle_upload_index_and_metadata_results(data_sync, data_path, isolation_token):
    results = __validate_handle_index_and_metadata_results(data_sync.upload_index_and_metadata, data_path,
                                                           isolation_token)

    if len(results) == 3:
        files_to_upload_gen, total_data_files_and_size, total_files_to_upload_and_size = results

        total_data_files, total_data_size = total_data_files_and_size
        total_files_to_upload, total_files_to_upload_size = total_files_to_upload_and_size
        same_files_count = total_data_files - total_files_to_upload
    else:
        files_to_upload_gen, same_files_count = results
        files_to_upload_gen = files_to_upload_gen or []
        total_files_to_upload = len(files_to_upload_gen)
        total_files_to_upload_size = sum([file_info['size'] for file_info in files_to_upload_gen])

    return files_to_upload_gen, total_files_to_upload, total_files_to_upload_size, same_files_count


@data_commands.command('sync')
@DataVolumeOptions.data_volume_id_argument()
@DataVolumeOptions.data_path_option()
@click.option('--commit', required=False, help='Skip staging, commit with this message after sync.')
@CommonOptions.processes_option()
@CommonOptions.no_progressbar_option()
@click.option('--isolated', is_flag=True, default=False, required=False)
@click.pass_context
def sync_to_data_volume(ctx, volume_id, data_path, commit, processes, no_progressbar, isolated):
    data_path = __expend_and_validate_path(data_path, expand_vars=False)

    repo_data_path = process_moniker_data_path(data_path)

    with with_repo_dynamic(ctx, volume_id, repo_data_path) as repo:
        data_sync = DataSync(ctx, repo, no_progressbar, processes=processes)

        isolation_token = uuid4().hex if isolated else None

        files_to_upload_gen, total_files_to_upload, total_files_to_upload_size, same_files_count = __handle_upload_index_and_metadata_results(data_sync, data_path, isolation_token)

        def create_update_progress(progress_bar):
            def update(upload_request):
                progress_bar.update(upload_request.size)

                progress_ctx['total_upload'] += 1

                progress_bar.set_postfix_str(
                    '%s/%s' % (humanize.intcomma(progress_ctx['total_upload']), humanize.intcomma(total_files_with_same)))

            return update

        if total_files_to_upload > 0:
            progress_ctx = {'total_upload': same_files_count}
            total_files_with_same = total_files_to_upload + same_files_count

            __print_transfer_info(repo, data_path)

            with tqdm(total=total_files_to_upload_size, desc='Syncing files', unit_scale=True, unit='B', ncols=80, disable=no_progressbar) as bar:
                callback = create_update_progress(bar)
                extra_kwargs = {}
                if not isinstance(files_to_upload_gen, list):
                    extra_kwargs['total_files'] = total_files_to_upload

                data_sync.upload_in_batches(files_to_upload_gen, callback=callback, isolation_token=isolation_token, **extra_kwargs)
        else:
            click.echo('No change detected, nothing to upload (metadata only change).', err=True)

        def do_commit():
            return repo.commit(commit, isolation_token)

        commit_results = {}
        if commit is not None:
            commit_results = status_with_timing('Server process metadata', do_commit)

        results = {}

        if commit_results:
            results.update(commit_results)

        if isolation_token is not None:
            results["isolationToken"] = isolation_token

        if results:
            output_result(ctx, results)


@data_commands.command('add')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--files', '-f', multiple=True)
@click.option('--commit', required=False)
@CommonOptions.processes_option()
@CommonOptions.no_progressbar_option()
@click.pass_context
def add_to_data_volume(ctx, volume_id, files, commit, processes, no_progressbar):
    all_files = list(enumerate_paths_with_info(files))
    total_files = len(all_files)

    def do_commit():
        return repo.commit(commit)

    def create_bar():
        return tqdm(total=total_files, desc="Adding files", unit=' files', ncols=80, disable=no_progressbar)

    def create_repo():
        return with_repo(ctx.obj.config, volume_id, session=ctx.obj.session)

    with create_bar() as bar, create_repo() as repo:
        data_sync = DataSync(ctx, repo, no_progressbar)
        if processes != -1:
            repo.data_volume_config.object_store_config['processes'] = processes

        data_sync.upload_in_batches(all_files, total_files, callback=lambda x: bar.update())

        commit_results = {}
        if commit is not None:
            commit_results = status_with_timing('Commit', do_commit)

        output_result(ctx, commit_results)


@data_commands.command('clone')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--dest-folder', '-d', required=True)
@click.option('--dest-file', '-df', default='$@name', show_default=True)
@click.option('--query', '-q', required=False)
@click.option('--delete', is_flag=True, required=False)
@click.option('--batch-size', required=False, default=-1)
@CommonOptions.processes_option()
@CommonOptions.no_progressbar_option()
@DataVolumeOptions.isolation_token_option()
@click.pass_context
def clone_data(ctx, volume_id, dest_folder, dest_file, query, delete, batch_size, processes, no_progressbar, isolation_token):
    if delete and (dest_folder in ('.', './', '/', os.path.expanduser('~'), '~', '~/')):
        raise click.BadParameter("for protection --dest can't point into current directory while using delete")

    dest_folder = __expend_and_validate_path(dest_folder, expand_vars=False, validate_path=False)

    root_dest = DestPathEnum.find_root(dest_folder)
    dest_pattern = DestPathEnum.get_dest_path(dest_folder, dest_file)

    if delete:
        safe_rm_tree(root_dest)

    safe_make_dirs(root_dest)

    with with_repo_dynamic(ctx, volume_id) as repo:
        data_sync = DataSync(ctx, repo, no_progressbar)
        try:
            phase_meta = data_sync.download_all(query, root_dest, dest_pattern, batch_size, processes, isolation_token=isolation_token)
        except MetadataOperationError as ex:
            click.echo(ex, err=True)
            sys.exit(1)

        data_sync.save_metadata(root_dest, phase_meta)


@data_commands.group('metadata')
def metadata_commands():
    pass


def stats_from_json(now, json_data):
    return os.stat_result((
        0,  # mode
        0,  # inode
        0,  # device
        0,  # hard links
        0,  # owner uid
        0,  # gid
        len(json_data),  # size
        0,  # atime
        now,
        now,
    ))


@data_commands.command('query')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--query', '-q')
@click.option('--batch-size', required=False, default=-1)
@click.option('--as-dict/--as-list', is_flag=True, required=False, default=False)
@click.option('--silent', is_flag=True, required=False, default=False)
@click.pass_context
def query_metadata(ctx, volume_id, query, batch_size, as_dict, silent):
    if as_dict and ctx.obj.output_format != 'json':
        raise click.BadParameter("--as-dict most come with global flag --output-format json")

    def get_all_results():
        for item in download_iter.fetch_all():
            if as_dict:
                yield item['@path'], item
            else:
                yield item

    try:
        with with_repo_dynamic(ctx, volume_id) as repo:
            data_sync = DataSync(ctx, repo, no_progressbar=True)

            download_iter = data_sync.create_download_iter(query, batch_size, silent=silent)

            output_result(ctx, get_all_results())
    except MetadataOperationError as ex:
        click.echo(str(ex), err=True)
        sys.exit(1)


def chunks(l, n):
    result = []
    for item in l:
        result.append(item)

        if len(result) == n:
            yield result
            result = []

    if result:
        yield result


class File2(click.File):
    def convert(self, value, param, ctx):
        from chardet.universaldetector import UniversalDetector

        value = os.path.expanduser(value)

        with closing(UniversalDetector()) as detector:
            try:
                with open(value, 'rb') as f:
                    data = f.read(1024)
                    detector.feed(data)
            except IOError as ex:
                raise MissingLinkException(ex)

        self.encoding = detector.result['encoding']

        return super(File2, self).convert(value, param, ctx)


def __repo_validate_data_path(repo, volume_id):
    if repo.data_path:
        return

    msg = 'Data volume {0} was not mapped on this machine, ' \
          'you should call "ml data map {0} --data_path [root path of data]" ' \
          'in order to work with the volume locally'.format(volume_id)
    click.echo(msg, err=True)
    sys.exit(1)


def __get_avro_stream_from_data(json_data):
    schema_so_far = {}
    data_list = []
    for key, val in json_data.items():
        val = MetadataFiles.convert_data_unsupported_type(val)
        AvroWriter.get_schema_from_item(schema_so_far, val)
        data_list.append((key, val))

    try:
        with closing(AvroWriter(schema=schema_so_far)) as avro_writer:
            avro_writer.append_data(data_list)
    except AvroWriterErrors as ex:
        raise MissingLinkException("Invalid metadata:\n{}".format(ex))

    return avro_writer.stream


# noinspection PyShadowingBuiltins
@metadata_commands.command('add')
@DataVolumeOptions.data_volume_id_argument()
@click.option('--files', '-f', multiple=True)
@click.option('--data', '-d', required=False, callback=CommonOptions.validate_json)
@click.option('--data-point', '-dp', multiple=True)
@click.option('--data-file', '-df', required=False, type=File2(encoding='utf-16'))
@click.option('--property', '-p', required=False, type=(str, str), multiple=True)
@click.option('--property-int', '-pi', required=False, type=(str, int), multiple=True)
@click.option('--property-float', '-pf', required=False, type=(str, float), multiple=True)
@click.option('--update/--replace', is_flag=True, default=True, required=False)
@CommonOptions.no_progressbar_option()
@DataVolumeOptions.data_path_option(required=False)
@click.pass_context
def add_to_metadata(
        ctx, volume_id, files, data, data_point, data_file, property, property_int, property_float, update, no_progressbar, data_path):

    def get_per_data_entry(data_per_entry):
        data_per_entry = data_per_entry or {}

        for props in (property, property_int, property_float):
            if not props:
                continue

            for prop_name, prop_val in props:
                data_per_entry[prop_name] = prop_val

        return data_per_entry

    def validate_data_path():
        if not data_path:
            raise click.BadParameter(
                "--files must come with --data-path in order to get the relative key of the file")

    def json_data_from_files(files, data_per_entry):
        def rel_path_if_needed(path):
            if os.path.isabs(path):
                validate_data_path()

                return os.path.relpath(path, data_path)

            return path

        for file_path in enumerate_paths(files):
            file_path = rel_path_if_needed(file_path)
            yield file_path, data_per_entry

    def get_current_data_file():
        current_per_data_entry = data if files or data_point else {}
        per_entry_data = get_per_data_entry(current_per_data_entry)

        json_data = defaultdict(dict)
        if files or data_point:
            if files:
                entries = list(files)

                for key, val in json_data_from_files(entries, per_entry_data):
                    json_data[key].update(val)

            for data_point_name in (data_point or []):
                json_data[data_point_name].update(per_entry_data)
        else:
            json_data.update(data or {})

        if data_file:
            json_data.update(json.load(data_file))

        return __get_avro_stream_from_data(json_data)

    with with_repo_dynamic(ctx, volume_id) as repo:
        file_obj = get_current_data_file()
        data_sync = DataSync(ctx, repo, no_progressbar)
        data_sync.upload_and_update_metadata(file_obj, file_type='avro')


@data_commands.command('list')
@click.pass_context
def list_data_volumes(ctx):
    data_volumes = api_get(ctx, 'data_volumes')

    output_result(ctx, data_volumes.get('volumes', []),
                  ['id', 'display_name', 'description', 'org', 'shared_storage_volume_id'])


@data_commands.command('validate')
@DataVolumeOptions.data_volume_id_argument()
@DataVolumeOptions.data_path_option(required=False)
@click.option('--data-file', '-df', required=False, type=File2(encoding='utf-16'))
@CommonOptions.no_progressbar_option()
@click.pass_context
def validate(ctx, volume_id, data_path, data_file, no_progressbar):
    if data_path is not None:
        data_path = __expend_and_validate_path(data_path, expand_vars=False)

        repo_data_path = process_moniker_data_path(data_path)

        with with_repo_dynamic(ctx, volume_id, repo_data_path) as repo:
            data_sync = DataSync(ctx, repo, no_progressbar)

            __validate_handle_index_and_metadata_results(data_sync.validate_metadata, data_path)
    elif data_file is not None:
        json_data = json.load(data_file)

        __get_avro_stream_from_data(json_data)

    click.echo("Validation completed successfully", err=True)
