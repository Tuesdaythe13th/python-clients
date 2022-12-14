# SPDX-FileCopyrightText: Copyright (c) 2022 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT

import os
from pathlib import Path
from typing import List, Optional, Tuple, Union

import grpc


def create_channel(
    ssl_cert: Optional[Union[str, os.PathLike]] = None,
    use_ssl: bool = False,
    uri: str = "localhost:50051",
    options: Optional[List[Tuple[str, Any]]] = None
) -> grpc.Channel:
    if ssl_cert is not None or use_ssl:
        root_certificates = None
        if ssl_cert is not None:
            ssl_cert = Path(ssl_cert).expanduser()
            with open(ssl_cert, 'rb') as f:
                root_certificates = f.read()
        creds = grpc.ssl_channel_credentials(root_certificates)
        channel = grpc.secure_channel(uri, creds, options=options)
    else:
        channel = grpc.insecure_channel(uri, options=options)
    return channel


class Auth:
    def __init__(
        self,
        ssl_cert: Optional[Union[str, os.PathLike]] = None,
        use_ssl: bool = False,
        uri: str = "localhost:50051",
        channel_options: Optional[List[Tuple[str, Any]]] = None,
    ) -> None:
        """
        A class responsible for establishing connection with a server and providing security metadata.

        Args:
            ssl_cert (:obj:`Union[str, os.PathLike]`, `optional`): a path to SSL certificate file. If :param:`use_ssl`
                is :obj:`False` and :param:`ssl_cert` is not :obj:`None`, then SSL is used.
            use_ssl (:obj:`bool`, defaults to :obj:`False`): whether to use SSL. If :param:`ssl_cert` is :obj:`None`,
                then SSL is still used but with default credentials.
            uri (:obj:`str`, defaults to :obj:`"localhost:50051"`): a Riva URI.
            channel_options (:obj:`Optional[List[Tuple[str, Any]]]`, defaults to :obj:`None`): a list of tuples with
                key-value pairs (`channel_arguments
                <https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments>`_ in gRPC Core runtime) to
                configure the channel.
        """
        self.ssl_cert: Optional[Path] = None if ssl_cert is None else Path(ssl_cert).expanduser()
        self.uri: str = uri
        self.use_ssl: bool = use_ssl
        self.options: Optional[List[Tuple[str, Any]]] = channel_options
        self.channel: grpc.Channel = create_channel(self.ssl_cert, self.use_ssl, self.uri, channel_options)

    def get_auth_metadata(self) -> List[Tuple[str, str]]:
        """
        Will become useful when API key and OAUTH tokens will be enabled.

        Metadata for authorizing requests. Should be passed to stub methods.

        Returns:
            :obj:`List[Tuple[str, str]]`: an empty list.
        """
        metadata = []
        return metadata
