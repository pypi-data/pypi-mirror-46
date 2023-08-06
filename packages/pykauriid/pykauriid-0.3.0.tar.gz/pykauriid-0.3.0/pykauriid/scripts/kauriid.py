#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Command line (CLI) client for Kauri ID operations.
"""

# Created: 2018-11-07 Guy K. Kloss <guy@mysinglesource.io>
#
# (c) 2018-2019 by SingleSource Limited, Auckland, New Zealand
#     http://mysinglesource.io/
#     Apache 2.0 Licence.
#
# This work is licensed under the Apache 2.0 open source licence.
# Terms and conditions apply.
#
# You should have received a copy of the licence along with this
# program.

__author__ = 'Guy K. Kloss <guy@mysinglesource.io>'

import argparse
import logging

from sspyjose import Jose

from pykauriid.config import config
from pykauriid.scripts import (claims,
                               attestations)


logger = logging.getLogger(__name__)

# Configure to use AES256-GCM as a default cipher for encryption.
# Current options: 'C20P' (ChaCha20/Poly1305), 'A256GCM' (AES256-GCM).
Jose.DEFAULT_ENC = config.default_enc


def _console():
    """
    Entry point for console execution.
    """
    # Set up logger.
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s\t%(name)s\t%(asctime)s %(message)s')

    # Create the top-level parser.
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-commands')

    # Create the parser for the "claims" command.
    parser_claims = subparsers.add_parser(
        'claims', help='claim set operations')
    parser_claims.set_defaults(func=claims.main)
    parser_claims.add_argument(
        '--operation', type=str,
        help='Operation to perform, one of: `new`, `access`.')
    parser_claims.add_argument(
        '--subject', type=str,
        help="DID of the claims'/attestations' subject.")
    parser_claims.add_argument(
        '--subject_sig_key', type=argparse.FileType('rt'), default=None,
        help="Subject's signing key to use (private or public).")
    parser_claims.add_argument(
        '--claims', type=argparse.FileType('rt'),
        help='File for the claims.')
    parser_claims.add_argument(
        '--claimset', type=str,
        help='File for the claim set.')
    parser_claims.add_argument(
        '--claimsetkeys', type=str,
        help='File for the claim set keys.')
    parser_claims.add_argument(
        '--device', action='store_true',
        help='Indicates a claim set for a device (unencrypted).')
    parser_claims.add_argument(
        '--index', type=int,
        help='Index of the claim to access (-1 for all).')
    parser_claims.add_argument(
        '--list', action='store_true',
        help='List the claim types of a claim set.')

    # Create the parser for the "attestations" command.
    parser_attestations = subparsers.add_parser(
        'attestations', help='attestation operations')
    parser_attestations.set_defaults(func=attestations.main)
    parser_attestations.add_argument(
        '--operation', type=str,
        help='Operation to perform, one of: `attest`, `accept`, `access`.')
    parser_attestations.add_argument(
        '--attestation', type=str,
        help='File for the attestation.')
    parser_attestations.add_argument(
        '--attester_data', type=argparse.FileType('rt'),
        help='Information about the attester making the attestation.')
    parser_attestations.add_argument(
        '--attestation_data', type=argparse.FileType('rt'),
        help='Information about the attestation to make.')
    parser_attestations.add_argument(
        '--subject_sig_key', type=argparse.FileType('rt'),
        help="Subject's signing key to use (private or public).")
    parser_attestations.add_argument(
        '--attester_sig_key', type=argparse.FileType('rt'),
        help="Attester's signing key to use (private or public).")
    parser_attestations.add_argument(
        '--claimsetkeys', type=str,
        help='File for the claim set keys (contains encrypted claim set).')
    parser_attestations.add_argument(
        '--claimset', type=str,
        help='File for the (unencrypted) claim set (for devices).')
    parser_attestations.add_argument(
        '--device', action='store_true',
        help='Indicates an attestation for a device (unencrypted).')
    parser_attestations.add_argument(
        '--index', type=int,
        help='Index of the attribute to access (-1 for all).')
    parser_attestations.add_argument(
        '--list', action='store_true',
        help='List the attribute types of an attestation.')
    parser_attestations.add_argument(
        '--dump', action='store_true',
        help='Dump the non-claims content of an attestation in plain text.')

    # Now let's do the work.
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    _console()
