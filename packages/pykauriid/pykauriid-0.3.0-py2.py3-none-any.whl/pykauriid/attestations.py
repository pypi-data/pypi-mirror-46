# -*- coding: utf-8 -*-
"""Attestations of claim sets."""

# Created: 2018-09-11 Guy K. Kloss <guy@mysinglesource.io>
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

import datetime
import time
from typing import List, Dict, Union, Iterable, Optional
import uuid

import prov.model
from sspyjose.jwe import Jwe
from sspyjose.jwk import Jwk
from sspyjose.jws import Jws

from pykauriid.claims import (ClaimSet,
                              ClaimSetKeys,
                              validate_commitment)
from pykauriid.config import config

PROTOCOL_VERSION = '0'
PROV_NAMESPACES = {
    # KauriID system (present by default)
    'kauriid': 'http://kauriid.nz/ns/prov#',
    # Dublin Core Terms (present by default)
    'dcterms': 'http://purl.org/dc/terms/',
    # DID URI scheme (present by default)
    'did': 'did:'
}


class _SimpleUTC(datetime.tzinfo):
    """
    Class to augment a Python datetime object object for a UTC time offset.
    """

    def tzname(self, **kwargs) -> str:  # @UnusedVariable
        return 'UTC'

    def utcoffset(self, dt: datetime.datetime  # @UnusedVariable
                  ) -> datetime.timedelta:
        return datetime.timedelta(0)


def make_utc_datetime(ts: Optional[int] = None) -> datetime.datetime:
    """
    Make a datetime object of the current time with UTC time offset.

    :param iat: UN*X epoch time stamp to obtain a datetime object for. If
        `None`, use the current time (default: None).
    :return: UTC datetime object.
    """
    ts = int(time.time()) if ts is None else ts
    result = datetime.datetime.utcfromtimestamp(ts)
    return result.replace(tzinfo=_SimpleUTC())


def _delegation_exists(prov_document: prov.model.ProvDocument,
                       delegate: Union[prov.model.ProvAgent, str],
                       responsible: Union[prov.model.ProvAgent, str]) -> bool:
    """
    Check whether a given delegation exists in the given document or not.

    :param prov_document: Provenance document to check within.
    :param delegate: Delegate to check for (object or identifier).
    :param responsible: Responsible to check for (object or identifier).
    :return: Outcome of check.
    """
    if isinstance(delegate, prov.model.ProvAgent):
        delegate = str(delegate.identifier)
    if isinstance(responsible, prov.model.ProvAgent):
        responsible = str(responsible.identifier)
    delegations = [item.attributes
                   for item in prov_document.records
                   if type(item) is prov.model.ProvDelegation]
    for delegation in delegations:
        party1, party2 = delegation
        if party1[0].localpart == 'delegate':
            recorded_delegate = str(party1[1])
            recorded_responsible = str(party2[1])
        else:
            # Just in case they're in reverse order.
            recorded_delegate = str(party2[1])
            recorded_responsible = str(party1[1])
        if (recorded_delegate == delegate
                and recorded_responsible == responsible):
            return True
    return False


class AttestationStatement:
    """Attestation statement container object with meta-data."""

    metadata = None  # type: Optional[dict]
    """Meta-data for the attestation statement."""
    exp = None  # type: Optional[int]
    """Time to live (last time valid as UNIX epoch time stamp in seconds)."""
    ttl = config.default_ttl  # type: Optional[int]
    """Time span for the time to live (in seconds)."""

    def __init__(self, *,
                 exp: Optional[int] = None,
                 ttl: Optional[int] = None,
                 metadata: Optional[dict] = None):
        """
        Constructor.

        :param exp: Time of expiry for the attestation statement
            (default: None).
        :param ttl: Time to live from time of attestation. Will be used to
            compute the expiry time (if not given) from the current point in
            time (default: `config.default_ttl`).
        :param metadata: Meta-data for this specific attestation statement.
        """
        self.exp = exp
        if not self.exp:
            self.ttl = ttl or config.default_ttl
        else:
            self.ttl = None
        if metadata:
            self.metadata = metadata

    def finalise(self, iat: int) -> dict:
        """
        Finalise the statement. Computes the TTL from the given time stamp.

        :param iat: Time stamp of attestation (as UNIX epoch time stamp in
            seconds).
        :return: Dictionary with attestation statement data.
        """
        if not self.exp:
            self.exp = int(iat + self.ttl)
            self.ttl = None
        return {
            'exp': self.exp,
            'metadata': self.metadata
        }


class AttesterData:
    """Attester data container object."""

    provenance_namespaces = None  # type: Optional[Dict[str, str]]
    """
    Namespace short names and URIs that are used/referenced in the provenance
    trail.
    """
    iss = None  # type: Optional[prov.model.ProvAgent, str]
    """Attester (issuer) (as a namespaced PROV actor)."""
    delegation_chain = None  # type: Optional[List[str]]
    """
    Delegation chain from highest to lowest actor (excluding the attester
    to be appended by the attestation process.
    """

    def __init__(self, iss: Union[prov.model.ProvAgent, str], *,
                 provenance_namespaces: Optional[Dict[str, str]] = None,
                 delegation_chain: Optional[List[str]] = None):
        """
        Constructor.

        :param iss: Attester (issuer) (as a namespaced PROV actor).
        :param provenance_namespaces: Mapping of short namespaces to full
            namespace URIs (default: None). These are added to resolve the
            attester.
        :param delegation_chain: Delegation chain from highest to lowest
            actor (excluding the attester to be appended by the attestation
            process (default: None).
        """
        self.iss = iss
        self.provenance_namespaces = provenance_namespaces or {}
        self.delegation_chain = delegation_chain or []


class AttestationData:
    """Attestation data container object."""

    iat = None  # type: Optional[int]
    """Time stamp of creation (as UNIX epoch time stamp in seconds)."""
    provenance_namespaces = None  # type: Optional[Dict[str, str]]
    """
    Namespace short names and URIs that are used/referenced in the provenance
    trail.
    """
    evidence_elements = None  # type: Optional[Dict[str, str]]
    """
    Mapping of an evidence (PROV) URI (or shortened via name space keys) of
    all evidence elements used in this attestation to a short description of
    the evidence (e.g. 'original document').
    """
    evidence_verification = None  # type: Optional[str]
    """
    (PROV) URI (or shortened via name space key) of the verification
    procedure used for the evidence.
    """
    ancestors = None  # type: Optional[List[dict]]
    """
    List of objects, one per ancestor. Each ancestor object contains an `id`,
    `object_key` and `trace_key` element (the keys in JWK dictionary form).
    In case the ancestor is a 'wrapper' (IPFS storage object), the
    `wrapper_uri` will hold the reference of the enclosing storage object.
    """
    statements = None
    # type: Optional[List[Union[AttestationStatement, dict]]]
    """List of individual attestation statements."""
    content = ()  # type: Iterable[str]
    """Content of attested elements within the attestation."""

    def __init__(self, *,
                 provenance_namespaces: Optional[Dict[str, str]] = None,
                 evidence_elements: Optional[Dict[str, str]] = None,
                 evidence_verification: Optional[str] = None,
                 ancestors: Optional[List[dict]] = None,
                 statements: Optional[List[Union[AttestationStatement,
                                                 dict]]] = None,
                 content: Optional[Iterable[str]] = None):
        """
        Constructor.

        :param provenance_namespaces: Mapping of short namespaces to full
            namespace URIs (default: None). These are added to resolve the
            attester.
        :param evidence_elements: Mapping of an evidence (PROV) URI (or
            shortened via name space keys) of all evidence elements used in
            this attestation to a short description of the evidence (e.g.
            'original document').
        :param evidence_verification: (PROV) URI (or shortened via name space
            key) of the verification procedure used for the evidence.
        :param ancestors: List of objects, one per ancestor. Each ancestor
            object contains a `uri`, `object_key` and `trace_key` element
            (the keys in JWK dictionary form).
        :param statements: List of individual attestation statements.
        :param content: Content of attested elements within the attestation.
        """
        # Make the time stamp on when this all happens.
        self.iat = int(time.time())
        self.provenance_namespaces = provenance_namespaces or {}
        self.evidence_elements = evidence_elements or {}
        self.evidence_verification = evidence_verification
        self.ancestors = ancestors or []
        self.statements = statements or []
        self.content = content or ()

    def check(self) -> bool:
        """
        Check for completeness of the required data.

        :return: True if complete, False otherwise.
        """
        if (self.provenance_namespaces
                and self.evidence_elements
                and self.statements):
            # We may have no ancestors, that's OK.
            return True
        else:
            return False


class Attestation:
    """Attestation management container object."""

    version = PROTOCOL_VERSION  # type: str
    """Protocol version of the attestation."""
    provenance = None  # type: Optional[str]
    """Provenance trace for this attestation (in PROV-N format)."""
    commitments = None  # type: Optional[[str]]
    """Cryptographic commitments to the claim set."""
    commitment_payloads = None  # type: Optional[Dict[str, dict]]
    """Unpacked commitments to the claim set."""
    content = None  # type: Optional[str]
    """Signed attestation content by issuer."""
    content_payload = None  # type: Optional[dict]
    """Unpacked attestation content."""
    claim_set_keys = None  # type: Optional[ClaimSetKeys]
    """Object containing all keys for the claim set."""
    attester_data = None  # type: Optional[AttesterData]
    """Data about the attester (for the PROV meta-data)."""
    attestation_data = None  # type: Optional[AttestationData]
    """Data about the attestation (for the PROV meta-data)."""
    subject_signing_key = None  # type: Optional[Jwk]
    """Subject's signing key."""
    attester_signing_key = None  # type: Optional[Jwk]
    """Attester's signing key."""
    id = None  # type: Optional[str]
    """Attestation identifier (generated in PROV trail during finalisation)."""
    _prov_document = None  # type: Optional[prov.model.ProvDocument]
    """The PROV document (as created with the Python PROV module)."""
    unencrypted = False
    """Encryption status of the attestation and claim set."""

    def __init__(self, *,
                 claim_set_keys: Union[ClaimSetKeys, str,
                                       bytes, dict, None] = None,
                 subject_signing_key: Optional[Jwk] = None,
                 attester_signing_key: Optional[Jwk] = None,
                 from_binary: Union[str, bytes, None] = None,
                 allow_unencrypted: bool = False):
        """
        Constructor.

        :param claim_set_keys: Claim set keys object, either as JSON or
            dictionary.
        :param subject_signing_key: Key used to sign the subject commitment
            (default: None). If a claim set or claim set keys object is given,
            this parameter needs to be used as well.
        :param from_binary: An attestation to load/access.
        :param allow_unencrypted: Allow for unencrypted (non-standard) JWEs
            for the claim set data (default: False).
        """
        self.subject_signing_key = subject_signing_key
        self.attester_signing_key = attester_signing_key
        self.unencrypted = allow_unencrypted
        if claim_set_keys:
            if isinstance(claim_set_keys, ClaimSetKeys):
                self.claim_set_keys = claim_set_keys
            else:
                self.claim_set_keys = ClaimSetKeys(
                    data=claim_set_keys, signing_key=subject_signing_key)
        claim_set = (self.claim_set_keys.encrypted_claim_set
                     if self.claim_set_keys else None)
        if claim_set:
            # This is (should be) a claim set in verbatim. Let's parse it!
            self.claim_set_keys.claim_set = ClaimSet(
                from_binary=claim_set,
                object_key=self.claim_set_keys.object_key,
                signing_key=subject_signing_key)
        self.commitments = {}
        self.commitment_payloads = {}
        self._prov_document = prov.model.ProvDocument()
        # Add base namespaces we always need.
        for short, full in PROV_NAMESPACES.items():
            self._prov_document.add_namespace(short, full)
        if from_binary:
            if not claim_set_keys:
                raise ValueError(
                    'Claim set key parameter missing for deserialisation.')
            self.load(from_binary)
        if self.unencrypted and not self.claim_set_keys:
            # Make a (dummy) claim set keys object. It won't be used.
            self.claim_set_keys = ClaimSetKeys()

    def _add_attestation_prov(self) -> str:
        """
        Add the attestation provenance to the attestation meta-data.

        :return: Target entity object identifier.
        """
        # Add the required name spaces.
        for ns_collection in [PROV_NAMESPACES,
                              self.attester_data.provenance_namespaces,
                              self.attestation_data.provenance_namespaces]:
            for ns, uri in ns_collection.items():
                self._prov_document.add_namespace(ns, uri)
        # Make target entity.
        target_id = uuid.uuid4()
        target_name = 'kauriid:attestations/{}'.format(target_id)
        other_attributes = {'prov:content': self.attestation_data.content}
        target = self._prov_document.entity(
            target_name, other_attributes=other_attributes)
        # Make activities.
        evidence_verification = self._prov_document.activity(
            'kauriid:evidenceVerification/{}'.format(target_id))
        attestation = self._prov_document.activity(
            'kauriid:identityAttestation/{}'.format(target_id),
            other_attributes={
                'dcterms:hasPart': evidence_verification})
        attestation.wasInformedBy(evidence_verification)
        # Add delegations.
        if len(self.attester_data.delegation_chain) > 0:
            previous_delegator = self.attester_data.delegation_chain[0]
            full_chain = (self.attester_data.delegation_chain[1:]
                          + [self.attester_data.iss])
            for actor_id in full_chain:
                if not _delegation_exists(self._prov_document,
                                          actor_id, previous_delegator):
                    self._prov_document.actedOnBehalfOf(actor_id,
                                                        previous_delegator)
                previous_delegator = actor_id
        # Add associations.
        attestation.wasAssociatedWith(
            self.attester_data.iss,
            attributes={'prov:hadRole': 'kauriid:attester'})
        evidence_verification.wasAssociatedWith(
            self.attester_data.iss,
            self.attestation_data.evidence_verification,
            attributes={'prov:hadRole': 'kauriid:verifier'})
        # Add generation.
        target.wasGeneratedBy(
            attestation, attributes={
                'prov:generatedAtTime':
                    make_utc_datetime(self.attestation_data.iat)
            })
        # Add derivations and usages.
        for ancestor in self.attestation_data.ancestors:
            if 'wrapper_uri' in ancestor:
                target_ipfs = self._prov_document.entity(
                    ancestor['wrapper_uri'],
                    other_attributes={'prov:type': 'prov:Collection'})
                target_ipfs.hadMember(ancestor['id'])
                attestation.used(target_ipfs)
                target.wasDerivedFrom(target_ipfs)
            else:
                attestation.used(ancestor['id'])
                target.wasDerivedFrom(ancestor['id'])
        for evidence_uri, description in (
                self.attestation_data.evidence_elements.items()):
            entity_id = 'kauriid:evidence/{}'.format(uuid.uuid4())
            evidence_entity = self._prov_document.entity(
                entity_id, other_attributes={
                    'dcterms:source': evidence_uri,
                    'dcterms:description': description
                }
            )
            attestation.used(evidence_entity)
            evidence_verification.used(evidence_entity)
            target.wasDerivedFrom(evidence_entity)
        self.provenance = self._prov_document.get_provn()
        return str(target.identifier)

    def _make_salty_hashes(self):
        """
        Make the commitment salts and hashes on the claim set.

        This is required if (some) commitment salts or hashes are missing,
        and no commitment exists, yet.
        """
        self.claim_set_keys.claim_set.commitment_salts = []
        self.claim_set_keys.claim_set.commitment_hashes = []
        for i in range(len(self.claim_set_keys.claim_set.claims)):
            claim_key = (self.claim_set_keys.claim_keys[i]
                         if not self.unencrypted else None)
            claim_bytes = self.claim_set_keys.claim_set.access_claim(
                i, claim_key, raw_bytes=True)
            commitment_salt, commitment_hash = (
                self.claim_set_keys.claim_set.make_salty_hash(claim_bytes))
            self.claim_set_keys.claim_set.commitment_salts.append(
                commitment_salt)
            self.claim_set_keys.claim_set.commitment_hashes.append(
                commitment_hash)

    def finalise(self, signing_key: Optional[Jwk] = None) -> str:
        """
        Finalise the attestation to return a completed attestation object.

        :param signing_key: Signing key of the attester/issuer (default: None).
            If not present, the object's `attester_signing_key` will be used.
        :return: JWE encrypted attestation object.
        """
        self.attester_signing_key = signing_key or self.attester_signing_key
        # Add the attestation provenance.
        self.id = self._add_attestation_prov()
        self.claim_set_keys.attestation_id = self.id
        # Finalise/serialise attestation statements with current time.
        self.attestation_data.statements = [
            item if isinstance(item, dict) else item.finalise(time.time())
            for item in self.attestation_data.statements]
        # Make the missing commitment salts and hashes.
        claim_set = self.claim_set_keys.claim_set
        if (len(claim_set.commitment_hashes) < len(claim_set.claims)):
            self._make_salty_hashes()
        # Get attester commitment.
        self.commitments['attester'] = claim_set.get_commitment(
            iss=self.attester_data.iss, iss_key=signing_key)
        # Migrate subject commitment (if present).
        if claim_set.commitment:
            self.commitments['subject'] = claim_set.commitment
            self.commitment_payloads['subject'] = (
                claim_set.validate_commitment())
            claim_set.commitment = None
            self.claim_set_keys.finalise_claim_set(retain_order=True,
                                                   include_commitment=False)
        # Encrypt ancestor keys.
        trace_key = None
        if not self.unencrypted:
            trace_key = Jwk.get_instance(generate=True)
            self.claim_set_keys.trace_key = trace_key
        ancestor_keys = {}
        for ancestor in self.attestation_data.ancestors:
            identifier = ancestor['id']
            ancestor_keys[identifier] = {}
            object_jwk = ancestor['object_key']
            trace_jwk = ancestor['trace_key']
            if self.unencrypted:
                encrypter = Jwe.get_instance(alg='unsecured')
            else:
                encrypter = Jwe.get_instance(jwk=trace_key)
            encrypter.message = (object_jwk if isinstance(object_jwk, dict)
                                 else object_jwk.to_dict())
            encrypter.encrypt()
            ancestor_keys[identifier]['object_key'] = encrypter.serialise()
            encrypter.message = (trace_jwk if isinstance(trace_jwk, dict)
                                 else trace_jwk.to_dict())
            encrypter.encrypt()
            ancestor_keys[identifier]['trace_key'] = encrypter.serialise()
        # Sign attestation payload.
        self.content_payload = {
            'iss': self.attester_data.iss,
            'iat': self.attestation_data.iat,
            'provenance': self.provenance,
            'statements': self.attestation_data.statements,
            'ancestor_keys': ancestor_keys
        }
        signer = Jws.get_instance(jwk=signing_key)
        signer.payload = self.content_payload
        signer.sign()
        self.content = signer.serialise(try_compact=True)

        return self.serialise()

    def load(self, attestation_data: Union[str, bytes],  # noqa: C901
             subject_signing_key: Optional[Jwk] = None,
             attester_signing_key: Optional[Jwk] = None):
        """
        Load attestation data into the object.

        Decrypt and validates the objects's consistency.

        :param attestation_data: Attestation data JWE encrypted to the
            recipient.
        :param subject_signing_key: Key used to sign the subject commitment
            (default: None).
        :param attester_signing_key: Key used to sign the attester commitment
            (default: None).
        """
        self.subject_signing_key = (subject_signing_key
                                    or self.subject_signing_key)
        self.attester_signing_key = (attester_signing_key
                                     or self.attester_signing_key)
        # Decrypt attestation object.
        decrypter = Jwe.get_instance(from_compact=attestation_data,
                                     jwk=self.claim_set_keys.object_key)
        decrypted_attestation_object = decrypter.decrypt(
            allow_unsecured=self.unencrypted)
        # Unpack the content.
        self.version = decrypted_attestation_object.get('v', PROTOCOL_VERSION)
        # TODO: Make a more capable check for the protocl version.
        assert self.version == PROTOCOL_VERSION
        self.id = decrypted_attestation_object.get('id')
        self.commitments = decrypted_attestation_object['commitments']
        self.content = decrypted_attestation_object['content']
        claim_set = ClaimSet(
            from_binary=decrypted_attestation_object['claim_set'],
            object_key=self.claim_set_keys.object_key,
            signing_key=self.subject_signing_key,
            unencrypted=self.unencrypted)
        self.claim_set_keys.claim_set = claim_set
        # Verify commitments.
        _lasts = None
        for role, commitment in self.commitments.items():
            signing_key = None
            if role == 'attester':
                signing_key = self.attester_signing_key
            elif role == 'subject':
                signing_key = self.subject_signing_key
            else:
                raise RuntimeError('Unknown role in commitment: {}!'
                                   .format(role))
            commitment_verifier = validate_commitment(commitment,
                                                      signing_key=signing_key)
            payload = commitment_verifier.payload
            claim_set.unpack_commitment_elements(payload)
            # Do some sanity checks.
            if payload['role'] != role:
                raise RuntimeError('Mismatch of role in commitment!')
            salts = tuple(claim_set.commitment_salts)
            if _lasts:
                if salts != _lasts['salts']:
                    raise RuntimeError(
                        "Mismatch of salts in attestation's commitments!")
                if payload['sub'] != _lasts['sub']:
                    raise RuntimeError(
                        'Mismatching subjects in attestation and commitment.')
                if payload['commitment'] != _lasts['commitment']:
                    raise RuntimeError(
                        'Mismatch of commitment data in commitments.')
            _lasts = {'salts': salts,
                      'sub': payload['sub'],
                      'commitment': payload['commitment']}
            # Now store the commitment.
            self.commitment_payloads[role] = payload

        content_verifier = Jws.get_instance(jwk=self.attester_signing_key,
                                            from_compact=self.content)
        content_verifier.verify()
        self.content_payload = content_verifier.payload
        if self.attester_data:
            self.attester_data.iss = self.content_payload['iss']
        else:
            self.attester_data = AttesterData(self.content_payload['iss'])
        self.attester_data.iss = self.content_payload['iss']
        self.attestation_data = self.attestation_data or AttestationData()
        self.attestation_data.iat = self.content_payload['iat']
        self.provenance = self.content_payload['provenance']
        self.attestation_data.statements = self.content_payload['statements']
        ancestor_keys = self.content_payload['ancestor_keys']
        # Unpick the ancestor keys.
        trace_key = self.claim_set_keys.trace_key
        for identifier, keys in ancestor_keys.items():
            decrypter = Jwe.get_instance(jwk=trace_key)
            decrypter.load_compact(keys['object_key'])
            object_key = decrypter.decrypt()
            decrypter.load_compact(keys['trace_key'])
            trace_key = decrypter.decrypt()
            ancestor = {'id': identifier,
                        'object_key': object_key,
                        'trace_key': trace_key}
            self.attestation_data.ancestors.append(ancestor)

    def serialise(self):
        """
        Serialise the attestation object.

        :return: JWE encrypted attestation object.
        """
        # Create encrypted attestation data structure.
        if not self.claim_set_keys.encrypted_claim_set:
            self.claim_set_keys.finalise_claim_set(include_commitment=False,
                                                   retain_order=True)
        attestation_data = {
            'v': self.version,
            'id': self.id,
            'claim_set': self.claim_set_keys.encrypted_claim_set,
            'commitments': self.commitments,
            'content': self.content
        }
        if self.unencrypted:
            object_encrypter = Jwe.get_instance(alg='unsecured')
        else:
            object_encrypter = Jwe.get_instance(
                jwk=self.claim_set_keys.object_key)
        object_encrypter.message = attestation_data
        object_encrypter.encrypt()

        return object_encrypter.serialise()

    def cosign(self, signing_key: Jwk):
        """
        Counter sign a commitment by the subject.

        Creates a subject commitment in the meta-data of the claim set object.

        :param subject_signing_key: The subject's (private) signing key.
        """
        self.claim_set_keys.claim_set.signing_key = signing_key
        commitment = self.claim_set_keys.claim_set.get_commitment()
        self.commitments['subject'] = commitment
