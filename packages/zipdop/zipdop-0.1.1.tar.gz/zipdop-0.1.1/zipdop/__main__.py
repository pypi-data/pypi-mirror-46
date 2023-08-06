#!/usr/bin/env python
import sys
import os
import io
import zipfile

import httpie
from httpie.cli import parser
import httpie.client
import httpie.output.streams
import requests


def make_raw_zip_by_central_directory(central_directory, total_size):
    content = b'\x00'*(total_size-len(central_directory))
    content += central_directory
    return content


def get_file_position(file_list, file_number):
    offset = file_list[file_number].header_offset
    # calculating compressed file size + meta data
    size = file_list[file_number].compress_size
    header = zipfile.sizeFileHeader
    header += len(file_list[file_number].filename)
    header += 12 # encryption header
    header += len(file_list[file_number].extra)
    size += header

    return offset, offset+size# calculating compressed file size + meta data


def get_file_number_by_path(file_list, file_path):
    for i, item in enumerate(file_list):
        if item.filename == file_path:
            return i
    raise ValueError('Not found file with path: {}'.format(file_path))


def request_decorator(old):
    def inner(*args, **kwargs):
        kwargs['stream'] = True
        response = old(*args, **kwargs)
        response.close()
        return response
    return inner


def get_requests_session(old):
    def inner(*args, **kwargs):
        session = old(*args, **kwargs)
        session.request = request_decorator(session.request)
        return session
    return inner


def output_stream_decorator(old):
    def inner(*args, **kwargs):
        if kwargs['args'].show_zip_files or kwargs['args'].download_file_from_zip:
            content_length = int(kwargs['response'].headers['Content-Length'])
            session = requests.Session()
            request = kwargs['request']
            request.headers['Range'] = 'bytes={}-{}'.format(content_length-100000, content_length)
            response = session.send(request)
            content = response.content
            zip_content = make_raw_zip_by_central_directory(content, content_length)
            zip_file = zipfile.ZipFile(io.BytesIO(zip_content))

        if kwargs['args'].show_zip_files:
            result = '\n'.join([file.filename for file in zip_file.infolist()])+'\n'
            result = [result.encode()]
        elif kwargs['args'].download_file_from_zip:
            file_list = zip_file.infolist()
            file_number = get_file_number_by_path(file_list, kwargs['args'].download_file_from_zip)
            file_position_start, file_position_end = get_file_position(file_list, file_number)

            request = kwargs['request']
            request.headers['Range'] = 'bytes={}-{}'.format(file_position_start, file_position_end)
            response = session.send(request)
            file_content = response.content
            zip_content = zip_content[:file_position_start] + file_content + zip_content[file_position_start+len(file_content):]
            zip_file = zipfile.ZipFile(io.BytesIO(zip_content))
            file_content = zip_file.open(kwargs['args'].download_file_from_zip).read()
            
            if not kwargs['args'].output_file:
                output_path = os.path.basename(kwargs['args'].download_file_from_zip)
            else:
                output_path = kwargs['args'].output_file.name
            with open(output_path, 'wb') as f:
                f.write(file_content)
            return [output_path.encode()]
        else:
            result = old(*args, **kwargs)
        return result
    return inner


def main():
    httpie.output.streams.build_output_stream = output_stream_decorator(httpie.output.streams.build_output_stream)
    httpie.client.get_requests_session = get_requests_session(httpie.client.get_requests_session)
    zipdop_args = parser.add_argument_group('ZipDOP arguments')
    zipdop_args.add_argument(
        '--show-zip-files',
        action='store_true'
    )

    zipdop_args.add_argument(
        '--download-file-from-zip',
        type=str,
    )

    try:
        from httpie.core import main
        sys.exit(main())
    except KeyboardInterrupt:
        from httpie import ExitStatus
        sys.exit(ExitStatus.ERROR_CTRL_C)


if __name__ == '__main__':
    main()
