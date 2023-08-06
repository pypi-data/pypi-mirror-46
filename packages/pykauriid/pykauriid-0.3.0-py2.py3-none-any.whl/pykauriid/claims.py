# -*- coding: utf-8 -*-
"""Claims and claim sets."""

# Created: 2018-08-13 Guy K. Kloss <guy@mysinglesource.io>
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

import time
from typing import List, Tuple, Dict, Union, Iterable, Optional

import nacl.bindings
import nacl.utils
from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk
from sspyjose.jws import Jws

from pykauriid import utils
from pykauriid.config import config


COMMITMENT_SALT_BYTES = 16


def generate_salt():
    """Generate salt suitable for the commitment hashes."""
    return nacl.utils.random(COMMITMENT_SALT_BYTES)


def _nacl_shuffle(length: int) -> List[int]:
    """
    Shuffles the indexes of an array of ``length`` elements.

    Note: Uses cryptographically secure random number generation.

    :param length: Number of elements in the list (index starting from 0).
    :return:
    """
    l1 = [nacl.utils.random(8) for _ in range(length)]
    l2 = l1.copy()
    l2.sort()
    return [l1.index(item) for item in l2]


def _collect_claim_type_elements(data: dict) -> Tuple[str, List[str]]:
    """
    Return the type and first level field names within a schema data dict.
    """
    if '@type' not in data:
        raise ValueError('Expected `@type` not in schema data.')
    the_type = data['@type']
    fields = [item for item in data.keys() if not item.startswith('@')]
    fields.sort()
    return the_type, fields


def _get_claim_types(a_claim: dict) -> List[str]:
    """
    Return a list representation of the claim types contained in the data.
    """
    root_type, fields = _collect_claim_type_elements(a_claim)
    paths = []
    for field in fields:
        data = a_claim[field]
        path = '{}.{}'.format(root_type, field)
        if isinstance(data, dict):
            sub_paths = _get_claim_types(data)
            for item in sub_paths:
                paths.append('{}/{}'.format(path, item))
        else:
            paths.append(path)
    paths.sort()
    return paths


def get_claim_type_hint(a_claim: dict) -> str:
    """Return a string representation hinting at the claim type."""
    paths = _get_claim_types(a_claim)
    return ','.join(paths)


def validate_commitment(commitment: str, signing_key: Jwk) -> Jws:
    """
    Validate the commitment given.

    :param commitment: The commitment to be validated.
    :param signing_key: Key used to sign the commitment.
    :return: Verified JWS object.
    :raises: nacl.exceptions.BadSignatureError on failed validation.
    """
    if not signing_key:
        raise RuntimeError(
            'Insufficient information: Issuer signing key missing.')
    verifier = Jws.get_instance(from_compact=commitment,
                                jwk=signing_key)
    verifier.verify()
    return verifier


class ClaimSet:
    """Claim set management container object."""

    claims = None  # type: Optional[List[Jwe]]
    """Claims in the set."""
    commitment_hashes = None  # type: Optional[List[bytes]]
    """Hashes of salted claims for the commitment."""
    commitment_salts = None  # type: Optional[List[bytes]]
    """Salts for the claims within the claim set for the commitment."""
    sub = None  # type: Optional[str]
    """Subject for whom the claims are."""
    commitment = None  # type: Optional[Jws]
    """JWS signature of the subject's claim set commitment."""
    iat = None  # type: Optional[int]
    """Time stamp of creation (as UNIX epoch time stamp in seconds)."""
    exp = None  # type: Optional[int]
    """Expiry (last time valid as UNIX epoch time stamp in seconds)."""
    ttl = config.default_ttl  # type: Optional[int]
    """Time to live (in seconds). Will be used to compute `exp`."""
    signing_key = None  # type: Optional[Jwk]
    """Signing key for the claim set."""
    unencrypted = False
    """Encryption status of the claim set."""

    def __init__(self,
                 sub: Optional[str] = None,
                 signing_key: Optional[Jwk] = None,
                 *,
                 from_binary: Union[bytes, str, None] = None,
                 object_key: Optional[Jwk] = None,
                 unencrypted: bool = False):
        """
        Constructor.

        :param sub: Subject identifier.
        :param signing_key: Subject's signing key.
        :param from_binary: Serialised binary representation of a claim set
            to load (as produced by ``finalise()``. If this option is used
            also the ``object_key`` parameter must be passed.
        :param object_key: Object key to deserialise the content of the
            ``from_binary`` parameter.
        :param unencrypted: Set to `True` to create a plaintext/unencrypted
            claim set. This uses a non-standard JWE algorithm type `unsecured`.
        """
        self.sub = sub
        self.signing_key = signing_key
        self.claims = []
        self.commitment_hashes = []
        self.commitment_salts = []
        self.unencrypted = unencrypted
        if from_binary:
            if not unencrypted and not object_key:
                raise ValueError(
                    'Object key parameter missing for deserialisation.')
            self.load(from_binary, object_key, allow_unencrypted=unencrypted)

    def make_salty_hash(self, claim_bytes: bytes) -> (bytes, bytes):
        """
        Make a salted hash of a claim payload.

        :param claim_bytes: Binary representation of the claim.
        :return: Tuple of the commitment salt and its hash.
        """
        commitment_salt = generate_salt()
        commitment_hash = nacl.hash.sha256(commitment_salt + claim_bytes,
                                           encoder=nacl.encoding.RawEncoder)
        return commitment_salt, commitment_hash

    def add_claim(self, a_claim: dict) -> Jwk:
        """
        Add a claim to the claim set, and return the claim key.

        Note: The claims (dictionaries) added are mutable. Therefore you
              *must not* change the dictionary after adding them top the
              claim set.

        :param a_claim: A JSON-LD compatible claim.
        :return: The key used for the claim encryption.
        """
        if self.unencrypted:
            claim_key = None
            claim_encrypter = Jwe.get_instance(alg='unsecured')
        else:
            claim_key = Jwk.get_instance(generate=True)
            claim_encrypter = Jwe.get_instance(jwk=claim_key)
        claim_encrypter.message = a_claim
        claim_encrypter.encrypt()
        commitment_salt, commitment_hash = self.make_salty_hash(
            claim_encrypter.get_message_bytes())
        self.claims.append(claim_encrypter.serialise())
        self.commitment_salts.append(commitment_salt)
        self.commitment_hashes.append(commitment_hash)
        return claim_key

    def access_claim(self, index: int, claim_key: Jwk,
                     *, raw_bytes: bool = False) -> Union[dict, bytes]:
        """
        Access and validates an (encrypted) claim from the claim set.

        :param index: The index of the claim within the claim set.
        :param claim_key: The key used for this claims encryption.
        :param raw_bytes: Returns the claim data in the binary serialised
            form, rather than a dictionary representation (default: False).
        :return: The plain text claim provided in the claim set. In case of
            `raw_bytes` as bytes, otherwise normally as a dictionary.
        """
        if self.unencrypted and claim_key is None:
            decrypter = Jwe.get_instance(alg='unsecured')
            decrypter.load_compact(self.claims[index])
            recovered = decrypter.decrypt(allow_unsecured=True)
        else:
            decrypter = Jwe.get_instance(jwk=claim_key)
            decrypter.load_compact(self.claims[index])
            recovered = decrypter.decrypt()
        if index < len(self.commitment_hashes):
            commitment_content = (self.commitment_salts[index]
                                  + decrypter.get_message_bytes())
            commitment_hash = nacl.hash.sha256(
                commitment_content, encoder=nacl.encoding.RawEncoder)
            # Constant time hash comparison (do not use `!=` or `==`).
            if not nacl.bindings.sodium_memcmp(commitment_hash,
                                               self.commitment_hashes[index]):
                raise RuntimeError('Commitment hash mismatch on claim {}.'
                                   .format(index))
        if raw_bytes:
            return decrypter.get_message_bytes()
        else:
            return recovered

    def _get_commitment_elements(self) -> List[str]:
        """
        Get the commitment elements that are to be signed/validated.
        """
        commitment_elements = []
        for the_salt, the_hash in zip(self.commitment_salts,
                                      self.commitment_hashes):
            commitment_elements.extend([utils.bytes_to_string(the_salt),
                                        utils.bytes_to_string(the_hash)])
        return commitment_elements

    def unpack_commitment_elements(self, commitment_payload: dict):
        """
        Recover the commitment elements contained within a commitment.

        :param commitment_payload: Signed commitment payload.
        """
        elements = commitment_payload['commitment'].split('.')
        self.commitment_salts = []
        self.commitment_hashes = []
        if len(elements) != 2 * len(self.claims):
            raise RuntimeError('Number of commitment elements incompatible'
                               ' with number of claims.')
        for i in range(len(self.claims)):
            self.commitment_salts.append(
                utils.string_to_bytes(elements[2 * i]))
            self.commitment_hashes.append(
                utils.string_to_bytes(elements[2 * i + 1]))

    def get_commitment(self, *,
                       iss: Optional[str] = None,
                       iss_key: Optional[Jwk] = None) -> Optional[str]:
        """
        Compute and return a commitment for the given claims.

        :param iss: Issuer/committer identifier. If none is given, the the
            subject (`sub`) will be used (default: None). This is to be used
            for an attester commitment, in which case the attester's signing
            key is provided. In that case the commitment label to be signed
            is adapted to reflect this.
        :param iss_key: Signing key for the issuer/committer of the
            attestation. If none is given, the the object's `signing_key`
            member will be used (default: None). This is mandatory to be used
            together with the `iss` parameter.
        :return: Commitment as compact JWS signature serialisation, `None` if
            no (private) signing key is available.
        """
        role = 'attester' if iss_key else 'subject'
        iss = iss or self.sub
        iss_key = iss_key or self.signing_key
        if not iss or not iss_key:
            raise RuntimeError('Insufficient information: Issuer or issuer'
                               ' signing key missing.')
        if iss_key and iss_key.d:
            signer = Jws.get_instance(jwk=iss_key)
            commitment = '.'.join(self._get_commitment_elements())
            signer.payload = {
                'commitment': commitment,
                'sub': self.sub,
                'iss': iss,
                'role': role}
            signer.sign()
            return signer.serialise(try_compact=True)
        else:
            return None

    def validate_commitment(self) -> dict:
        """
        Validate the commitment stored.

        :return: Dictionary of the signed commitment payload.
        :raises: nacl.exceptions.BadSignatureError on failed validation.
        """
        verifier = validate_commitment(self.commitment, self.signing_key)
        if verifier.payload['sub'] != self.sub:
            raise RuntimeError('Subject in commitment mismatches the'
                               ' claim set subject.')
        if (verifier.payload['role'] == 'subject'
                and verifier.payload['iss'] != self.sub):
            raise RuntimeError('Expected signature of commitment does not'
                               ' match claim set owner.')
        return verifier.payload

    def serialise(self, *,
                  object_key: Optional[Jwk] = None) -> (Jwk, str):
        """
        Serialise a claim set.

        :param object_key: Optional object key to encrypt the claim set. If
            not given, a new one will be generated.
        :return: Object key, encrypted string serialisation.
        """
        # Create final JSON data object.
        data_object = {
            'sub': self.sub,
            'iat': self.iat,
            'exp': self.exp,
            'claims': self.claims
        }
        if self.commitment:
            data_object['commitment'] = self.commitment
        # Encrypt JSON data object.
        if self.unencrypted:
            object_key = None
            object_encrypter = Jwe.get_instance(alg='unsecured')
        else:
            object_key = (object_key if object_key
                          else Jwk.get_instance(generate=True))
            object_encrypter = Jwe.get_instance(jwk=object_key)
        object_encrypter.message = data_object
        object_encrypter.encrypt()

        return object_key, object_encrypter.serialise()

    def finalise(self, *,
                 include_commitment: bool = True,
                 object_key: Optional[Jwk] = None) -> (Jwk, str):
        """
        Finalises a claim set, and returns the serialised representation.

        Also the commitment will be computed.

        :param include_commitment: Include a subject commitment
            (default: True).
        :param object_key: Optional object key to encrypt the claim set. If
            not given, a new one will be generated.
        :return: Object key, encrypted string serialisation.
        """
        commitment = self.get_commitment() if include_commitment else None
        self.commitment = commitment
        self.iat = int(time.time())
        self.exp = self.iat + self.ttl
        return self.serialise(object_key=object_key)

    def load(self, binary_data: Union[bytes, str], object_key: Jwk,
             signing_key: Optional[Jwk] = None,
             *,
             allow_unencrypted: bool = False):
        """
        Load a serialised, encrypted claim set.

        :param binary_data: Serialised binary representation of a claim set
            to load (as produced by ``finalise()``.
        :param signing_key: Key used to sign the commitment (default: None).
            If not given, uses the object's signing key property.
        :param object_key: Object key to deserialise the content of the
            ``binary_data`` parameter.
        :param allow_unencrypted: Allow for unencrypted (non-standard) JWEs
            for the claim set data (default: False).
        """
        self.signing_key = signing_key or self.signing_key
        if allow_unencrypted and object_key is None:
            self.unencrypted = True
            decrypter = Jwe.get_instance(alg='unsecured')
            decrypter.load_compact(binary_data)
            recovered = decrypter.decrypt(allow_unsecured=True)
        else:
            decrypter = Jwe.get_instance(jwk=object_key)
            decrypter.load_compact(binary_data)
            recovered = decrypter.decrypt()
        self.sub = recovered['sub']
        self.iat = recovered['iat']
        self.exp = recovered['exp']
        self.claims = [item for item in recovered['claims']]
        self.commitment = recovered.get('commitment')
        if self.commitment is not None:
            commitment_payload = self.validate_commitment()
            self.unpack_commitment_elements(commitment_payload)


class ClaimSetKeys:
    """
    Private storage container for holding the claim set keys and secret data.
    """

    # Or use the IPFS reference for the `claim_set`:
    claim_set = None  # type: Optional[ClaimSet]
    """Claim set these keys belong to."""
    claim_keys = None  # type: Optional[List[Jwk]]
    """Keys for the claims within the claim set."""
    claim_type_hints = None  # type: Optional[List[str]]
    """Type hints for the claims within the claim set."""
    object_key = None  # type: Optional[Jwk]
    """Symmetric encryption key for the claim set object."""
    encrypted_claim_set = None  # type: Optional[str]
    """Encrypted, serialised claim set."""
    trace_key = None  # type: Optional[Jwk]
    """Symmetric encryption key for recursively unlocking ancestors."""
    attestation_id = None  # type: Optional[str]
    """Attestation identifier this claim set keys refers to."""

    def __init__(self, *,
                 data: Union[bytes, str, dict, None] = None,
                 signing_key: Optional[Jwk] = None):
        """
        Constructor.

        :param data: Dictionary or serialised JSON representation of claim
            set keys to load (e.g. as produced by ``serialise()``.
        :param signing_key: Key used to sign the commitment (default: None).
        """
        self.claim_keys = []
        self.claim_type_hints = []
        if data:
            self.load(data, signing_key)

    def add_claim(self, a_claim: dict):
        """
        Add a claim to the claim set.

        This also stores the private management data to the claim set keys.

        Note: The claims (dictionaries) added are mutable. Therefore you
              *must not* change the dictionary after adding them top the
              claim set.

        :param a_claim: A JSON-LD compatible claim.
        """
        self.claim_keys.append(self.claim_set.add_claim(a_claim))
        claim_type_hint = get_claim_type_hint(a_claim)
        self.claim_type_hints.append(claim_type_hint)

    def finalise_claim_set(self, *,
                           include_commitment: bool = True,
                           retain_order: bool = False) -> str:
        """
        Finalises the claim set.

        Outcome:
        - Order of elements within the claim set is shuffled.
        - Commitment of the claim set is signed.
        - Encrypted serialisation of the claim set is returned.

        :param include_commitment: Include a subject commitment
            (default: True).
        :param retain_order: Retains the order of the claims within the
            claim set (default: False). This is useful for computing an
            attester commitment on an *existing* claim set.
        :return: Serialised version of encrypted claim set object.
        """
        if retain_order is False:
            # Shuffle the order of claims.
            order = _nacl_shuffle(len(self.claim_set.claims))
            self.claim_set.claims = [self.claim_set.claims[i] for i in order]
            self.claim_set.commitment_salts = [
                self.claim_set.commitment_salts[i] for i in order]
            self.claim_set.commitment_hashes = [
                self.claim_set.commitment_hashes[i] for i in order]
            self.claim_keys = [self.claim_keys[i] for i in order]
            self.claim_type_hints = [self.claim_type_hints[i] for i in order]
        if self.claim_set.iat:
            # We've got a finalised claim set already.
            object_key, encrypted_claim_set = self.claim_set.serialise(
                object_key=self.object_key)
        else:
            # Still needs to be finalised.
            object_key, encrypted_claim_set = self.claim_set.finalise(
                include_commitment=include_commitment)
        # Put the elements in order of the claim set.
        self.object_key = object_key
        self.encrypted_claim_set = encrypted_claim_set
        return encrypted_claim_set

    def to_dict(self, *,
                claim_type_hints: bool = False,
                to_export: Optional[Iterable] = None) -> Dict:
        """
        Represent the claim set keys object as a dictionary.

        :param claim_type_hints: True, if the claim type hints are to be
            serialised as well.
        :param to_export: List of claim keys to export.
        :return: Dictionary containing the data structure.
        """
        # TODO: `to_export` ... seq of integers or type hints?
        claim_set = self.finalise_claim_set(retain_order=True)
        result_object = {
            'claim_set': claim_set,
            'object_key': self.object_key.to_dict(),
            'claim_keys': {str(i): key.to_dict()
                           for i, key in enumerate(self.claim_keys)},
            'trace_key': self.trace_key.to_dict() if self.trace_key else None,
            'attestation_id': self.attestation_id
        }
        if claim_type_hints:
            result_object['claim_type_hints'] = {
                str(i): hint
                for i, hint in enumerate(self.claim_type_hints)}
        return result_object

    def serialise(self, *,
                  claim_type_hints: bool = False,
                  to_export: Optional[Iterable] = None) -> str:
        """
        Serialise the claim set keys object.

        :param claim_type_hints: True, if the claim type hints are to be
            serialised as well.
        :param to_export: List of claim keys to export.
        :return: JSON serialised data structure.
        """
        return utils.dict_to_json(self.to_dict(
            claim_type_hints=claim_type_hints, to_export=to_export))

    def load(self, data: Union[bytes, str, dict], signing_key: Jwk):
        """
        Load a serialised claim set keys JSON structure.

        :param data: Dictionary or serialised JSON representation of claim
            set keys to load (e.g. as produced by ``serialise()``.
        :param signing_key: Key used to sign the commitment.
        """
        content = data if isinstance(data, dict) else utils.json_to_dict(data)
        self.object_key = Jwk.get_instance(from_dict=content['object_key'])
        if 'trace_key' in content and content['trace_key']:
            self.trace_key = Jwk.get_instance(from_dict=content['trace_key'])
        self.attestation_id = content.get('attestation_id')
        self.encrypted_claim_set = content['claim_set']
        self.claim_set = ClaimSet(from_binary=content['claim_set'],
                                  object_key=self.object_key,
                                  signing_key=signing_key)
        for i, key_data in content['claim_keys'].items():
            i = int(i)
            claim_key = Jwk.get_instance(from_dict=key_data)
            self.claim_keys.append(claim_key)
            plain_claim = self.claim_set.access_claim(i, claim_key)
            claim_type = get_claim_type_hint(plain_claim)
            self.claim_type_hints.append(claim_type)
