# coding: utf-8
import socket
from urllib.parse import urljoin, urlparse

import requests

import socks

__all__ = [
    'Httpraw',
    'request'
]


class HttpRawException(Exception):
    '''Httpraw Exception'''
    pass


class Httpraw:
    """
    raw = '''GET / HTTP/1.1
    Host: www.example.com
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
    Accept-Encoding: gzip, deflate
    Connection: close
    Content-Type: application/x-www-form-urlencoded'''
    h = httpraw.Httpraw(raw)
    h.proxy = {'socks5': '127.0.0.1:1086'}
    h.timeout = 5
    h.ssl = True
    h.verify = True
    resp = h.request()
    print(resp.status_code)
    print(resp.text[:100])
    ...
    """

    def __init__(self, raw, url='', proxy={}, timeout=None, ssl=False, verify=False):
        self.raw = raw
        self.url = url
        self.proxy = proxy
        self.timeout = timeout
        self.ssl = ssl
        self.verify = verify

    def request(self):
        request_line, header_lines, body_lines = self.__parse_raw()
        method, path, _protocol = self.__get_request_info(request_line)
        headers = self.__get_headers(header_lines)
        body = self.__get_body(body_lines, headers.get('Content-Type', ''))
        url = self.__get_url(headers, path)

        params = {}
        proxy = self.__proxy()
        if self.timeout:
            params['timeout'] = self.timeout
        if self.ssl and self.verify:
            params['verify'] = self.verify
        if body:
            params['data'] = body
        if proxy:
            params['proxy'] = proxy
        return requests.request(method, url, headers=headers, **params)

    def __parse_raw(self):
        header_lines = []
        body_lines = []
        raw_lines = self.raw.lstrip().split('\n')
        request_line = raw_lines[0].strip()
        try:
            header_end = raw_lines.index('')
        except:
            header_end = len(raw_lines)
        for line in raw_lines[1:header_end]:
            header_lines.append(line.strip())
        if header_end != len(raw_lines):
            body_lines = raw_lines[header_end+1:]
        return request_line, header_lines, body_lines

    def __get_request_info(self, request_line):
        try:
            method, path, protocol = request_line.split(" ")
        except:
            raise HttpRawException('Protocol format error')
        return method, path, protocol

    def __get_headers(self, header_lines):
        headers = {}
        for line in header_lines:
            if ': ' in line:
                k, v = line.split(': ')
                headers[k.strip()] = v.strip()
        return headers

    def __get_body(self, body_lines, content_type):
        if 'multipart/form-data' in content_type:
            return '\r\n'.join(body_lines)
        elif ('application/json' in content_type or 'application/x-www-form-urlencoded' in content_type):
            body = ''
            for line in body_lines:
                if line != '':
                    body += line.strip()
            return body
        elif 'text/xml' in content_type:
            return '\n   '.join(body_lines)

    def __get_url(self, headers, path):
        if self.url:
            parsed_url = urlparse(self.url)
            try:
                del headers['Host']
            except KeyError:
                pass
            return self.__parse_url_path(path, parsed_url)
        scheme = "http"
        port = 80
        if self.ssl:
            scheme = 'https'
        host = headers.get('Host', '')
        if ':' in host:
            host, port = host.split(':')
        if int(port) == 80:
            return urljoin(f'{scheme}://{host}', path)
        return urljoin(f'{scheme}://{host}:{port}', path)

    def __parse_url_path(self, path, parsed_url):
        '''当 self.url 不是以 file 结尾的都需要 urljoin path
        :return: url
        例子:
            https://www.example.com             -> self.url + path
            https://www.example.com/            -> self.url + path
            https://www.example.com/path        -> self.url + path
            https://www.example.com/path/a.php  -> self.url
            https://www.example.com/path/a.php/ -> self.url
        '''
        pth = parsed_url.path
        pth = pth.rstrip('/')
        file_part = pth.split('/')[-1]
        if '.' in file_part:
            return self.url
        return urljoin(self.url, path)

    def __proxy(self):
        '''处理 socks5，http 和 https 都丢给 requests 自带的去处理
        '''
        if not self.proxy:
            return self.proxy

        proxy_info = self.proxy.get('socks5', '')
        if proxy_info:
            if ":" in proxy_info:
                addr, port = proxy_info.split(':')
                socks.set_default_proxy(
                    proxy_type=socks.PROXY_TYPE_SOCKS5,
                    addr=addr,
                    port=int(port))
                socket.socket = socks.socksocket
            del self.proxy['socks5']
        return self.proxy


def request(raw, **kwargs):
    return Httpraw(raw, **kwargs).request()
