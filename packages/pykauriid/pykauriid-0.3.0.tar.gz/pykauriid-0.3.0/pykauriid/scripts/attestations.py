# -*- coding: utf-8 -*-
"""
Module providing an entry point to make and read claim attestations via a CLI.
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
import io
import json
import logging

from sspyjose.jwk import Jwk

from pykauriid import attestations
from pykauriid import claims


logger = logging.getLogger(__name__)


def _load_attestation(attestation_file: str,
                      claimsetkeys_file: str,
                      attester_sig_key: Jwk,
                      subject_sig_key: Jwk) -> attestations.Attestation:
    """
    Load an attestation together with a claim set keys file.

    :param attestation_file: File of the attestation to read.
    :param claimsetkeys_file: File containing the claim set keys and claim set.
    :param attester_sig_key: Key to use to verify the attestation (public).
    :param subject_sig_key: Key to use for co-signing (private).
    :return: Usable attestation object.
    """
    with open(claimsetkeys_file, 'rt') as fd:
        an_attestation = attestations.Attestation(
            claim_set_keys=fd.read(),
            subject_signing_key=subject_sig_key,
            attester_signing_key=attester_sig_key)
    with open(attestation_file, 'rt') as fd:
        an_attestation.load(fd.read())
    return an_attestation


def _load_device_attestation(attestation_file: str, attester_sig_key: Jwk,
                             subject_sig_key: Jwk) -> attestations.Attestation:
    """
    Load an unencrypted device attestation.

    :param attestation_file: File of the attestation to read.
    :param attester_sig_key: Key to use to verify the attestation (public).
    :param subject_sig_key: Key to use for co-signing (private).
    :return: Usable attestation object.
    """
    with open(attestation_file, 'rt') as fd:
        an_attestation = attestations.Attestation(
            subject_signing_key=subject_sig_key,
            attester_signing_key=attester_sig_key,
            allow_unencrypted=True)
        an_attestation.load(fd.read())
    return an_attestation


def attest_claim_set(claimsetkeys_file: str,
                     attester_data_fd: io.TextIOBase,
                     attestation_data_fd: io.TextIOBase,
                     attestation_file: str,
                     attester_sig_key_fd: io.TextIOBase,
                     subject_sig_key_fd: io.TextIOBase):
    """
    Attest a (self or foreign) claim set.

    :param claimsetkeys_file: File containing the claim set keys and claim set.
    :param attester_data_fd: File containing information on the attester.
    :param attestation_data_fd: File containing data on the specific
        attestation to make.
    :param attestation_file: File to write the new attestation to.
    :param attester_sig_key_fd: Key to use to attest (private).
    :param subject_sig_key_fd: Key to use to verify the claim set (public).
        If not present, only foreign claim sets can be attested.
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    with open(claimsetkeys_file, 'rt') as fd:
        my_attestation = attestations.Attestation(
            claim_set_keys=fd.read(),
            subject_signing_key=subject_sig_key,
            attester_signing_key=attester_sig_key)
    attester_dict = json.load(attester_data_fd)
    attestation_dict = json.load(attestation_data_fd)
    # Add attester data.
    attester_data = attestations.AttesterData(
        iss=attester_dict['attester'],
        provenance_namespaces=attester_dict['provenance_namespaces'],
        delegation_chain=attester_dict['delegation_chain'])
    my_attestation.attester_data = attester_data
    # Add attestation data.
    statements = [
        attestations.AttestationStatement(exp=item.get('exp'),
                                          ttl=item.get('ttl'),
                                          metadata=item.get('metadata'))
        for item in attestation_dict['statements']]
    attestation_data = attestations.AttestationData(
        provenance_namespaces=attestation_dict['provenance_namespaces'],
        evidence_elements=attestation_dict['evidence_elements'],
        evidence_verification=attestation_dict['evidence_verification'],
        ancestors=attestation_dict['ancestors'],
        statements=statements)
    my_attestation.attestation_data = attestation_data
    # Attest the claim set.
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.finalise(attester_sig_key))
    # Update claim set keys (now contains a trace key).
    with open(claimsetkeys_file, 'wt') as fd:
        fd.write(my_attestation.claim_set_keys.serialise(
            claim_type_hints=True))


def attest_device_claim_set(claimset_file: str,
                            attester_data_fd: io.TextIOBase,
                            attestation_data_fd: io.TextIOBase,
                            attestation_file: str,
                            attester_sig_key_fd: io.TextIOBase,
                            subject_sig_key_fd: io.TextIOBase):
    """
    Attest an unencrypted (self or foreign) claim set for a device.

    :param claimset_file: File from which to read the claim set.
    :param attester_data_fd: File containing information on the attester.
    :param attestation_data_fd: File containing data on the specific
        attestation to make.
    :param attestation_file: File to write the new attestation to.
    :param attester_sig_key_fd: Key to use to attest (private).
    :param subject_sig_key_fd: Key to use to verify the claim set (public).
        If not present, only foreign claim sets can be attested.
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    with open(claimset_file, 'rt') as fd:
        claim_set = claims.ClaimSet(from_binary=fd.read(),
                                    signing_key=subject_sig_key,
                                    unencrypted=True)
    my_attestation = attestations.Attestation(
        subject_signing_key=subject_sig_key,
        attester_signing_key=attester_sig_key,
        allow_unencrypted=True)
    my_attestation.claim_set_keys.claim_set = claim_set
    attester_dict = json.load(attester_data_fd)
    attestation_dict = json.load(attestation_data_fd)
    # Add attester data.
    attester_data = attestations.AttesterData(
        iss=attester_dict['attester'],
        provenance_namespaces=attester_dict['provenance_namespaces'],
        delegation_chain=attester_dict['delegation_chain'])
    my_attestation.attester_data = attester_data
    # Add attestation data.
    statements = [
        attestations.AttestationStatement(exp=item.get('exp'),
                                          ttl=item.get('ttl'),
                                          metadata=item.get('metadata'))
        for item in attestation_dict['statements']]
    attestation_data = attestations.AttestationData(
        provenance_namespaces=attestation_dict['provenance_namespaces'],
        evidence_elements=attestation_dict['evidence_elements'],
        evidence_verification=attestation_dict['evidence_verification'],
        ancestors=attestation_dict['ancestors'],
        statements=statements)
    my_attestation.attestation_data = attestation_data
    # Attest the claim set.
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.finalise(attester_sig_key))


def accept_attestation(claimsetkeys_file: str,
                       attestation_file: str,
                       attester_sig_key_fd: io.TextIOBase,
                       subject_sig_key_fd: io.TextIOBase):
    """
    Accept an attestation by co-signing it.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use for co-signing (private).
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = Jwk.get_instance(from_json=subject_sig_key_fd.read())
    my_attestation = _load_attestation(attestation_file, claimsetkeys_file,
                                       attester_sig_key, subject_sig_key)
    my_attestation.cosign(subject_sig_key)
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.serialise())


def accept_device_attestation(attestation_file: str,
                              attester_sig_key_fd: io.TextIOBase,
                              subject_sig_key_fd: io.TextIOBase):
    """
    Accept an unencrypted device attestation by co-signing it.

    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use for co-signing (private).
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    my_attestation = _load_device_attestation(
        attestation_file, attester_sig_key, subject_sig_key)
    my_attestation.cosign(subject_sig_key)
    with open(attestation_file, 'wt') as fd:
        fd.write(my_attestation.serialise())


def access_attested_claims(claimsetkeys_file: str,
                           attestation_file: str,
                           attester_sig_key_fd: io.TextIOBase,
                           subject_sig_key_fd: io.TextIOBase,
                           index: int,
                           to_list: bool):
    """
    Access a claim set in a file using the given claim set keys.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use to verify the subject commitment
        (public).
    :param index: Index of the attribute to access (-1 for all).
    :param to_list: List the attribute types of the attestation.
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    my_attestation = _load_attestation(attestation_file, claimsetkeys_file,
                                       attester_sig_key, subject_sig_key)
    claims_keys = my_attestation.claim_set_keys
    claim_set = claims_keys.claim_set
    if to_list:
        print('Claim set contains claims with the following types:')
        for item in claims_keys.claim_type_hints:
            print('- {}'.format(item))
    elif index == -1:
        print('All claims:')
        for i in range(len(claim_set.claims)):
            claim_key = claims_keys.claim_keys[i]
            print('- {}'.format(json.dumps(
                claim_set.access_claim(i, claim_key), indent=2)))
    else:
        claim_key = claims_keys.claim_keys[index]
        print('Claim index {}:'.format(index))
        print(json.dumps(claim_set.access_claim(index, claim_key), indent=2))


def access_device_attested_claims(attestation_file: str,
                                  attester_sig_key_fd: io.TextIOBase,
                                  subject_sig_key_fd: io.TextIOBase,
                                  index: int,
                                  to_list: bool):
    """
    Access an unencrypted device claim set in a file.

    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use to verify the subject commitment
        (public).
    :param index: Index of the attribute to access (-1 for all).
    :param to_list: List the attribute types of the attestation.
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    my_attestation = _load_device_attestation(
        attestation_file, attester_sig_key, subject_sig_key)
    claim_set = my_attestation.claim_set_keys.claim_set
    if to_list:
        print('Claim set contains claims with the following types:')
        for i in range(len(claim_set.claims)):
            claim_data = claim_set.access_claim(i, None)
            print('- {}'.format(claims.get_claim_type_hint(claim_data)))
    elif index == -1:
        print('All claims:')
        for i in range(len(claim_set.claims)):
            claim_data = claim_set.access_claim(i, None)
            print('- {}'.format(json.dumps(claim_data, indent=2)))
    else:
        print('Claim index {}:'.format(index))
        claim_data = claim_set.access_claim(index, None)
        print(json.dumps(claim_data, indent=2))


def _indent_content(content: str, indent_by: int) -> str:
    """
    Indent the given content by the desired number of spaces.

    :content: String (line block) to indent.
    :indent_by: Amount of characters to indent each line by.
    :return: Block indented string representation.
    """
    lines = content.split('\n')
    indentation = ' ' * indent_by
    return '\n'.join('{}{}'.format(indentation, line)
                     for line in lines)


def dump_attestation_content(claimsetkeys_file: str,
                             attestation_file: str,
                             attester_sig_key_fd: io.TextIOBase,
                             subject_sig_key_fd: io.TextIOBase):
    """
    Access a claim set in a file using the given claim set keys.

    :param claimsetkeys_file: File to read the claim set keys from.
    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use to verify the subject commitment
        (public).
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    my_attestation = _load_attestation(attestation_file, claimsetkeys_file,
                                       attester_sig_key, subject_sig_key)
    claims_keys = my_attestation.claim_set_keys
    claim_set = claims_keys.claim_set
    print('Claim set:')
    print('  - sub: {}'.format(claim_set.sub))
    if claim_set.commitment is None:
        print('  - foreign claim set')
    else:
        print('  - self claim set')
    print('  - number of claims: {}'.format(len(claim_set.claims)))
    iat = claim_set.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    exp = claim_set.exp
    print('  - expires at: {} ({})'
          .format(exp, attestations.make_utc_datetime(exp).isoformat()))
    print('Claims:')
    for i in range(len(claim_set.claims)):
        claim_key = claims_keys.claim_keys[i]
        claim_data = json.dumps(claim_set.access_claim(i, claim_key), indent=2)
        print('  - claim {}:\n{}'
              .format(i, _indent_content(claim_data, 6)))
    print('Attestation data:')
    print('  - issuer/attester: {}'.format(my_attestation.attester_data.iss))
    iat = my_attestation.attestation_data.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    print('  - PROV-N trail:\n{}'
          .format(_indent_content(my_attestation.provenance, 6)))
    print('  - attestation statements:')
    for item in my_attestation.attestation_data.statements:
        exp = item['exp']
        metadata = item['metadata']
        print('    - expires at: {} ({})'
              .format(exp, attestations.make_utc_datetime(exp).isoformat()))
        print('      metadata:\n{}'
              .format(_indent_content(json.dumps(metadata, indent=2), 8)))
    print('  - ancestors:')
    for ancestor in my_attestation.attestation_data.ancestors:
        print('    - reference: {}'.format(ancestor['id']))
        print('      - object key:\n{}'
              .format(_indent_content(
                  json.dumps(ancestor['object_key'], indent=2), 8)))
        print('      - trace key:\n{}'
              .format(_indent_content(json.dumps(
                  ancestor['trace_key'], indent=2), 8)))
    print('Commitments:')
    for _, commitment in my_attestation.commitment_payloads.items():
        print('  - subject: {}'.format(commitment['sub']))
        print('  - committer role: {}'.format(commitment['role']))
        print('  - committer ID: {}'.format(commitment['iss']))
        print('  - elements:')
        parts = commitment['commitment'].split('.')
        for i in range(int(len(parts) / 2)):
            print('    - salt {}: {}'.format(i, parts[2 * i]))
            print('    - salted hash {}: {}'.format(i, parts[2 * i + 1]))


def dump_device_attestation_content(attestation_file: str,
                                    attester_sig_key_fd: io.TextIOBase,
                                    subject_sig_key_fd: io.TextIOBase):
    """
    Access a claim set in a file using the given claim set keys.

    :param attestation_file: File of the attestation to read and update.
    :param attester_sig_key_fd: Key to use to verify the attestation (public).
    :param subject_sig_key_fd: Key to use to verify the subject commitment
        (public).
    """
    attester_sig_key = Jwk.get_instance(from_json=attester_sig_key_fd.read())
    subject_sig_key = (Jwk.get_instance(from_json=subject_sig_key_fd.read())
                       if subject_sig_key_fd else None)
    my_attestation = _load_device_attestation(
        attestation_file, attester_sig_key, subject_sig_key)
    claim_set = my_attestation.claim_set_keys.claim_set
    print('Claim set:')
    print('  - sub: {}'.format(claim_set.sub))
    if claim_set.commitment is None:
        print('  - foreign claim set')
    else:
        print('  - self claim set')
    print('  - number of claims: {}'.format(len(claim_set.claims)))
    iat = claim_set.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    exp = claim_set.exp
    print('  - expires at: {} ({})'
          .format(exp, attestations.make_utc_datetime(exp).isoformat()))
    print('Claims:')
    for i in range(len(claim_set.claims)):
        claim_data = json.dumps(claim_set.access_claim(i, None), indent=2)
        print('  - claim {}:\n{}'
              .format(i, _indent_content(claim_data, 6)))
    print('Attestation data:')
    print('  - issuer/attester: {}'.format(my_attestation.attester_data.iss))
    iat = my_attestation.attestation_data.iat
    print('  - time stamp: {} ({})'
          .format(iat, attestations.make_utc_datetime(iat).isoformat()))
    print('  - PROV-N trail:\n{}'
          .format(_indent_content(my_attestation.provenance, 6)))
    print('  - attestation statements:')
    for item in my_attestation.attestation_data.statements:
        exp = item['exp']
        metadata = item['metadata']
        print('    - expires at: {} ({})'
              .format(exp, attestations.make_utc_datetime(exp).isoformat()))
        print('      metadata:\n{}'
              .format(_indent_content(json.dumps(metadata, indent=2), 8)))
    print('  - ancestors:')
    for ancestor in my_attestation.attestation_data.ancestors:
        print('    - reference: {}'.format(ancestor['id']))
        print('      - object key:\n{}'
              .format(_indent_content(
                  json.dumps(ancestor['object_key'], indent=2), 8)))
        print('      - trace key:\n{}'
              .format(_indent_content(json.dumps(
                  ancestor['trace_key'], indent=2), 8)))
    print('Commitments:')
    for _, commitment in my_attestation.commitment_payloads.items():
        print('  - subject: {}'.format(commitment['sub']))
        print('  - committer role: {}'.format(commitment['role']))
        print('  - committer ID: {}'.format(commitment['iss']))
        print('  - elements:')
        parts = commitment['commitment'].split('.')
        for i in range(int(len(parts) / 2)):
            print('    - salt {}: {}'.format(i, parts[2 * i]))
            print('    - salted hash {}: {}'.format(i, parts[2 * i + 1]))


def main(args: argparse.Namespace):
    """
    Delegate to the right functions from given (command line) arguments.

    :param args: Command line arguments provided:

        - args.operation - type: str
        - args.attestation - type: str
        - args.attester_data - type: io.TextIOBase
        - args.attestation_data - type: io.TextIOBase
        - args.subject_sig_key - type: io.TextIOBase
        - args.attester_sig_key - type: io.TextIOBase
        - args.claimsetkeys - type: str
        - args.claimset - type: str
        - args.index - type: int
        - args.list - type: bool
        - args.dump - type: bool
    """
    if args.operation == 'attest':
        if args.device:
            attest_device_claim_set(
                args.claimset, args.attester_data, args.attestation_data,
                args.attestation, args.attester_sig_key, args.subject_sig_key)
        else:
            attest_claim_set(
                args.claimsetkeys, args.attester_data, args.attestation_data,
                args.attestation, args.attester_sig_key, args.subject_sig_key)
    elif args.operation == 'accept':
        if args.device:
            accept_device_attestation(args.attestation, args.attester_sig_key,
                                      args.subject_sig_key)
        else:
            accept_attestation(args.claimsetkeys, args.attestation,
                               args.attester_sig_key, args.subject_sig_key)
    elif args.operation == 'access':
        if args.device:
            if args.dump:
                dump_device_attestation_content(
                    args.attestation, args.attester_sig_key,
                    args.subject_sig_key)
            else:
                access_device_attested_claims(
                    args.attestation, args.attester_sig_key,
                    args.subject_sig_key, args.index, args.list)
        else:
            if args.dump:
                dump_attestation_content(
                    args.claimsetkeys, args.attestation,
                    args.attester_sig_key, args.subject_sig_key)
            else:
                access_attested_claims(
                    args.claimsetkeys, args.attestation, args.attester_sig_key,
                    args.subject_sig_key, args.index, args.list)
    else:
        raise ValueError('Unsupported operation "{}" for attestations.'
                         .format(args.operation))

    logger.info('Operation "{}" finished.'.format(args.operation))
