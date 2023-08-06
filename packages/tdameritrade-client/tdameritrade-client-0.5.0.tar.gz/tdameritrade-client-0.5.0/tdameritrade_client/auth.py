import json
import os
import socket
import ssl
import webbrowser
from contextlib import contextmanager
from typing import Dict, Tuple
from urllib.parse import quote, unquote

import requests
from OpenSSL.crypto import dump_privatekey, dump_certificate, FILETYPE_PEM

from tdameritrade_client.utils import urls
from tdameritrade_client.utils.create_certs import create_certificate, create_key_pair


class TDAuthenticator(object):
    """
    Object for running TDAmeritrade's OAuth2 flow. An instance of this class is a
    member of the TDClient class and is meant to be called from the TDClient.

    """
    def __init__(self, host: str, port: int, oauth_user_id: str, token_path: str):
        """
        Constructor for the TDAuthenticator object.

        Args:
            host: The redirect URI host
            port: The redirect URI port
            oauth_user_id: The oauth user id (without @AMER.OAUTHAP)
            token_path: Path to the current token json file

        Raises:
            ValueError: If token_path is invalid

        """
        self._redirect_uri = 'http://{}:{}'.format(host, port)
        self._oauth_user_id = oauth_user_id + '@AMER.OAUTHAP'
        self._host = host
        self._port = port

        if os.path.dirname(token_path) == '':
            raise ValueError('Provided token_path {} is invalid.'.format(token_path))
        self._token_path = token_path

    def authenticate(self) -> str:
        """
        Runs the OAUTH flow for the TDA API.

        Returns:
            A string containing the decoded access token to authorize API requests.

        """
        # Check if token already exists
        if os.path.isfile(self._token_path):
            print('Loading existing token...')
            with open(self._token_path) as token_pointer:
                token_json = json.load(token_pointer)
            # Attempt to refresh the token
            refresh_token = token_json['refresh_token']
            successfully_refreshed, token = self.refresh_auth_token(refresh_token)
            print('Token successfully refreshed.')
            if not successfully_refreshed:
                print('Failed to refresh token. Requesting new token.')
                token = self.run_full_flow()
        else:
            token = self.run_full_flow()

        return token

    def refresh_auth_token(self, refresh_token: str) -> Tuple[bool, str]:
        """
        Request a new access token via a refresh token.

        Args:
            refresh_token: A refresh token as a decoded string.

        Returns:
            A bool that is True if auth was successful, and a valid access token.

        """
        refreshed = False
        refresh_request = self._get_url('token_request')
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self._oauth_user_id
        }
        response = requests.post(refresh_request, data=data, headers=headers)
        token = ''
        if response.status_code == 200:
            refreshed = True
            token = response.json()['access_token']

        return refreshed, token

    def run_full_flow(self) -> str:
        """
        Request an access token and a refresh token by authorizing through TDA online. Should be run if
        the auth-token.json does not exist or if the refresh token fails to authorize a new access token.

        Returns:
            A decoded access token as a string.

        """
        # Check if SSL certs exists
        cert_path = os.path.join(os.path.dirname(os.path.dirname(self._token_path)),
                                 'certificate.pem')
        key_path = os.path.join(os.path.dirname(os.path.dirname(self._token_path)),
                                'key.pem')

        if not os.path.isfile(cert_path):
            print('SSL certificate not found. Creating new certificate.')
            self._create_ssl_cert(cert_path, key_path)

        # Login online to receive an auth code
        auth_request = self._get_url('auth_request')
        webbrowser.open(url=auth_request)

        # Setup server to receive auth code
        with self._start_server(key_path, cert_path) as ssock:
            code_received = False
            while not code_received:
                conn, addr = ssock.accept()
                print('Accepting connection from {}'.format(addr))
                with conn:
                    try:
                        data = conn.recv(1024)
                    except ConnectionAbortedError:
                        continue
                    code, code_received = self._extract_code(data)

            # Send response with auth code to receive auth token
            headers, data = self._get_token_request(code)
            token = requests.post(self._get_url('token_request'), headers=headers, data=data)
            if 'error' in token.json().keys():
                raise ValueError(f'There was an error retrieving an access token: {token.json()["error"]}')

            os.makedirs(os.path.dirname(self._token_path), exist_ok=True)
            with open(self._token_path, 'w') as outfile:
                json.dump(token.json(), outfile)

            access_token = token.json()['access_token']
            return access_token

    def _get_token_request(self, code: str) -> Tuple[Dict, Dict]:
        """
        Helper that builds the headers and data for a token request.

        Args:
            code: The auth code sent by TDA after a successful authentication on the website.

        Returns:
            The headers for a token request and the data for a token request.

        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'access_type': 'offline',
            'code': code,
            'client_id': self._oauth_user_id,
            'redirect_uri': self._redirect_uri
        }
        return headers, data

    def _get_url(self, request: str):
        """
        Get the correct request URL for a given task.

        Args:
            request: A string specifying what type of request can be made. Supports:
                auth_request: Build the URL to initiate full flow auth by authenticating online.
                token_request: Build the URL used to ask for a token.

        Returns:
            The requested url

        """
        url = urls.BASE_URL
        if request == 'auth_request':
            url = f'{urls.AUTH_URL}{urls.AUTH_PARAMS}{quote(self._redirect_uri)}&client_id=' \
                  f'{quote(self._oauth_user_id)}'
        elif request == 'token_request':
            url += urls.TOKEN_URL
        else:
            raise NotImplementedError('The requested url type {} is not supported.'.format(request))

        return url

    @contextmanager
    def _start_server(self, key_path: str, cert_path: str):
        """
        Context manager that builds secure socket listening on the callback address.

        Args:
            key_path: path to key.pem file.
            cert_path: path to certificate.pem file.

        Yields:
            A secure socket listening on (self._host, self._port).

        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self._host, self._port))
        sock.listen()

        # Wrap the socket with SSL
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_path, key_path)
        ssock = context.wrap_socket(sock, server_side=True)

        # Yield the secure socket
        yield ssock

        # Close the wrapper and the original socket when context finishes
        print('Shutting down server.')
        ssock.close()
        sock.close()

    @staticmethod
    def _create_ssl_cert(cert_path: str, key_path: str) -> None:
        """
        Creates .pem files used to encrypt a secure socket.

        Args:
            cert_path: Where to write a new certificate.pem.
            key_path: Where to write a new key.pem.

        """
        try:
            os.makedirs(os.path.dirname(cert_path))
        except FileExistsError:
            pass

        key_pair = create_key_pair(bits=2048)
        cert = create_certificate(key_pair)
        key_bytes = dump_privatekey(FILETYPE_PEM, key_pair)
        cert_bytes = dump_certificate(FILETYPE_PEM, cert)
        with open(key_path, 'wb') as f:
            f.write(key_bytes)
        with open(cert_path, 'wb') as f:
            f.write(cert_bytes)

    @staticmethod
    def _extract_code(data: bytes) -> Tuple[str, bool]:
        """
        Extracts the code passed by TDA from the response. If the response has the wrong form, returns nothing.

        Args:
            data: bytes from ssock.accept().

        Returns:
            The auth code as a string, and a bool that is True if code was extracted successfully.

        """
        code = ''
        code_received = False
        if data != b'':
            try:
                code = data.decode('utf-8').split('code=')[1]
                code = code.split(' ')[0]
                code = unquote(code)
                code_received = True
            except IndexError:
                pass

        return code, code_received
