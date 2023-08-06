# -*- coding: utf-8 -*-
"""Messages exchanged between participating parties."""

# Created: 2019-04-04 Guy K. Kloss <guy@mysinglesource.io>
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
from typing import Dict, Union, List, Optional

from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk
from sspyjose.jws import Jws

from pykauriid.claims import ClaimSetKeys
from pykauriid.config import config


class Message:
    """Base class for messages to exchange between parties."""

    message_type = None  # type: Optional[str]
    """Type of message."""
    _message = None  # type: Optional[dict]
    """Plain text message content in raw."""

    def __init__(self, message_type: str, *, message: dict = None):
        """
        Constructor.

        :param message_type: Type of message.
        """
        self.message_type = message_type
        if message:
            self._message = message

    def serialise(self, recipient_dh_pk: Union[Jwk, str, dict]) -> str:
        """
        Serialise the message object.

        :param recipient_dh_pk: Public encryption key of the recipient.
        :return: JSON serialised data structure.
        """
        raise NotImplementedError('Needs to be implemented by child class.')

    @classmethod
    def deserialise(cls, message: Union[str, bytes],
                    recipient_dh_sk: Union[Jwk, str, dict]) -> 'Message':
        """
        Deserialise a message, and returns a `Message` (sub-) class object.

        :param message: The message to deserialise.
        :param recipient_dh_sk: Secret/private DH key of the recipient.
        :return: A plain text message object.
        """
        if isinstance(recipient_dh_sk, dict):
            recipient_dh_sk = Jwk.get_instance(from_dict=recipient_dh_sk)
        elif isinstance(recipient_dh_sk, str):
            recipient_dh_sk = Jwk.get_instance(from_json=recipient_dh_sk)
        decrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_sk)
        decrypter.load_compact(message)
        recovered = decrypter.decrypt()
        message_type = recovered['message_type']
        if message_type in MESSAGE_TYPES:
            klass = MESSAGE_TYPES[message_type]
            return klass(message=recovered)
        else:
            return cls(message_type, message=recovered)


class AttestationRequest(Message):
    """Request for attestation of a claim set."""

    claim_set_keys = None  # type: Optional[ClaimSetKeys]
    """
    Keys to the claim set to attest (includes claim set of a reference to it).
    """
    ancestors = None  # type: Optional[Dict[str, str]]
    """
    Ancestor entities in the attestation trail. The key of the dictionary
    is the IPFS references, and the value contains the internal attestation
    entity ID from the attestation PROV graph. The new attestation to be
    generated will link up with these entities.
    """

    def __init__(self, *,
                 claim_set_keys: Union[Dict, ClaimSetKeys] = None,
                 message: dict = None,
                 ancestors: Dict[str, str] = None):
        """
        Constructor.

        :param claim_set_keys: Cryptographic keys to the serialised/encrypted
            claim set for the attestation request.
        :param message: Plain text message to use for initialising the
            content.
        :param ancestors: Ancestor entities in the attestation trail. The
            key of the dictionary is the IPFS reference, and the value
            contains the internal attestation entity ID from the attestation
            PROV graph. The new attestation to be generated will link up
            with these entities.
        """
        super().__init__('attestation_request')
        if claim_set_keys:
            self.claim_set_keys = claim_set_keys
        if message:
            self.claim_set_keys = message['claim_set_keys']
        if ancestors:
            self.ancestors = ancestors

    def serialise(self, recipient_dh_pk: Union[Jwk, str, dict]) -> str:
        """
        Serialise the attestation request object.

        :param recipient_dh_pk: Public encryption key of the recipient.
        :return: JWE encrypted JSON serialised data structure.
        """
        content = {
            'message_type': self.message_type,
            'claim_set_keys': self.claim_set_keys
        }
        self._message = content
        if isinstance(recipient_dh_pk, dict):
            recipient_dh_pk = Jwk.get_instance(from_dict=recipient_dh_pk)
        elif isinstance(recipient_dh_pk, str):
            recipient_dh_pk = Jwk.get_instance(from_json=recipient_dh_pk)
        encrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_pk)
        encrypter.message = content
        encrypter.encrypt()
        return encrypter.serialise()


class AttestationResponse(Message):
    """Response with attestation of a claim set."""

    claim_set_keys = None  # type: Optional[ClaimSetKeys]
    """
    Keys to the claim set attested (includes claim set of a reference to it).
    """
    attestation = None  # type: Optional[str]
    """
    Issued serialised attestation of the claim set.
    """

    def __init__(self, *,
                 claim_set_keys: Dict = None,
                 message: Dict = None,
                 attestation: str = None):
        """
        Constructor.

        :param claim_set_keys: Cryptographic keys to the serialised/encrypted
            claim set attested.
        :param message: Plain text message to use for initialising the
            content.
        :param attestation: Encrypted/serialised attestation object to send.
        """
        super().__init__('attestation_response')
        if claim_set_keys:
            self.claim_set_keys = claim_set_keys
        if message:
            self.claim_set_keys = message['claim_set_keys']
        if attestation:
            self.attestation = attestation

    def serialise(self, recipient_dh_pk: Union[Jwk, str, dict]) -> str:
        """
        Serialise the attestation response object.

        :param recipient_dh_pk: Public encryption key of the recipient.
        :return: JWE encrypted JSON serialised data structure.
        """
        content = {
            'message_type': self.message_type,
            'claim_set_keys': self.claim_set_keys,
            'attestation': self.attestation
        }
        self._message = content
        if isinstance(recipient_dh_pk, dict):
            recipient_dh_pk = Jwk.get_instance(from_dict=recipient_dh_pk)
        elif isinstance(recipient_dh_pk, str):
            recipient_dh_pk = Jwk.get_instance(from_json=recipient_dh_pk)
        encrypter = Jwe.get_instance(alg='ECDH-ES', jwk=recipient_dh_pk)
        encrypter.message = content
        encrypter.encrypt()
        return encrypter.serialise()


class DisclosureRequest(Message):
    """Response with attestation of a claim set."""

    requested_claims = None  # type: Optional[List[str]]
    """The claims to be requested from our recipient."""
    sender_sig_sk = None  # type: Optional[Union[Jwk, str, dict]]
    """The senders signing key, to sign the message."""
    sender_dh_pk = None  # type: Optional[Union[Jwk, str, dict]]
    """
    The senders Diffie-Helman public key, to allow the recipient to derive an
    encryption key.
    """
    callback_url = None  # type: Optional[str]
    """
    The URL the recipient should send their selective disclosure response
    to this request.
    """
    iss = None  # type: Optional[str]
    """The sender's (aka issuer's) DID."""
    issc = None  # type: Optional[dict]
    """
    Dict containing the `name`, `profileImage` and `obo` of the sender (aka
    issuer).
    """

    def __init__(self, *,
                 requested_claims: List[str],
                 iss: str,
                 issc: dict,
                 sender_sig_sk: Union[Jwk, str, dict],
                 sender_dh_pk: Union[Jwk, str, dict],
                 callback_url: str):
        """
        Constructor.

        :param requested_claims: List of Attested Claim to be requested from
            from the recipient. Each claim should be a Schema.org LD path
            (where possible).
        :param iss: the senders DID.
        :param issc: Dict containing the name, profileImage and obo
            of the sender.
        :param sender_sig_sk: senders signing key.
        :param sender_dh_pk: senders public diffiehelman key, for sending to
            the recipient.
        :param callback_url: the url of the resource the recipient should send
            their response
        """
        super().__init__('shareReq')
        self.requested_claims = requested_claims
        self.iss = iss
        self.issc = issc
        self.sender_sig_sk = sender_sig_sk
        self.sender_dh_pk = sender_dh_pk
        self.callback_url = callback_url

    def serialise(self) -> str:
        """
        Serialise the disclosure request object.

        :return: JWE encrypted JSON serialised data structure.
        """
        if isinstance(self.sender_dh_pk, str):
            self.sender_dh_pk = Jwk.get_instance(from_json=self.sender_dh_pk)
        elif isinstance(self.sender_dh_pk, dict):
            self.sender_dh_pk = Jwk.get_instance(from_dict=self.sender_dh_pk)
        if isinstance(self.sender_sig_sk, dict):
            self.sender_sig_sk = Jwk.get_instance(from_dict=self.sender_sig_sk)
        elif isinstance(self.sender_sig_sk, str):
            self.sender_sig_sk = Jwk.get_instance(from_json=self.sender_sig_sk)

        content = {
            'type': self.message_type,
            'iss': self.iss,
            'issc': self.issc,
            'iat': int(time.time()),
            'exp': int(time.time()) + config.default_request_ttl,
            'ephem_pk': self.sender_dh_pk.to_dict(exclude_private=True),
            'callback': self.callback_url,
            'verified': self.requested_claims,
        }
        self._payload = content
        signer = Jws.get_instance(jwk=self.sender_sig_sk)
        signer.payload = content
        signer.sign()
        return signer.serialise()


MESSAGE_TYPES = {
    None: Message,
    'attestation_request': AttestationRequest,
    'attestation_response': AttestationResponse,
    'shareReq': DisclosureRequest,
}
