# -*- coding: utf-8 -*-
"""Attestation support."""

# Created: 2019-03-28 Guy K. Kloss <guy@mysinglesource.io>
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

import json
from typing import Optional, Iterable, Union, List, Dict

from pykauriid.attestations import (AttesterData,  # noqa: F401
                                    AttestationData,
                                    Attestation,
                                    AttestationStatement)
from pykauriid.claims import (ClaimSet,
                              ClaimSetKeys)
from sspyjose.jwk import Jwk

from singlesource import utils
from singlesource.config import config  # noqa: F401 # @UnusedImport


def load_attestation(attestation_content: Union[str, bytes],
                     claimsetkeys_content: Union[str, bytes],
                     attester_sig_key: Jwk,
                     subject_sig_key: Jwk) -> Attestation:
    """
    Load an attestation together with claim set keys from raw content.

    :param attestation_content: Content of the attestation to load.
    :param claimsetkeys_content: Content of the claim set keys and claim set.
    :param attester_sig_key: Key to use to verify the attestation (public).
    :param subject_sig_key: Key to use for co-signing (private).
    :return: New attestation object from data given.
    """
    an_attestation = Attestation(claimsetkeys_content,
                                 subject_signing_key=subject_sig_key,
                                 attester_signing_key=attester_sig_key)
    an_attestation.load(attestation_content)
    return an_attestation


def load_device_attestation(attestation_content: Union[str, bytes],
                            attester_sig_key: Jwk,
                            subject_sig_key: Jwk) -> Attestation:
    """
    Load an unencrypted device attestation from raw content.

    :param attestation_content: Content of the attestation to load.
    :param attester_sig_key: Key to use to verify the attestation (public).
    :param subject_sig_key: Key to use for co-signing (private).
    :return: New attestation object from data given.
    """
    an_attestation = Attestation(subject_signing_key=subject_sig_key,
                                 attester_signing_key=attester_sig_key,
                                 allow_unencrypted=True)
    an_attestation.load(attestation_content)
    return an_attestation


def make_foreign_claim_set(claims: Iterable[dict],
                           subject: str,
                           *,
                           device: bool = False) -> ClaimSetKeys:
    """
    Create a new foreign claim set on the provided claims.

    :param claims: Iterable containing JSON-LD styled claims.
    :param subject: DID of the subject of the claims.
    :param device: Set to True, if the claim set is for a device
        (default: False). Device claim sets are unencrypted.
    :return: Claim set keys object containing the foreign claim set.
    """
    claim_set = ClaimSet(sub=subject, unencrypted=device)
    claims_keys = ClaimSetKeys()
    claims_keys.claim_set = claim_set
    for claim in claims:
        claims_keys.add_claim(claim)
    claims_keys.finalise_claim_set(include_commitment=False)
    return claims_keys


def attest_claim_set(claim_set_keys: Optional[ClaimSetKeys],
                     attester_data: AttesterData,
                     attestation_data: AttestationData,
                     attester_sig_key: Union[Jwk, str, dict],
                     *,
                     claim_set: Optional[ClaimSet] = None,
                     device: bool = False) -> Dict[str, Union[str, dict]]:
    """
    Attest a (self or foreign) claim set.

    :param claim_set_keys: Claim set keys object (will be updated for the new
        trace key if required). Not required if an unencrypted (device)
        attestation is to be created.
    :param attester_data: Information on the attester.
    :param attestation_data: Data on the specific attestation to make.
    :param attester_sig_key: Key to use to attest (private).
    :param claim_set: Optional unencrypted claim set to use with devices
        (not requiring claim set keys).
    :param device: Set to True, if the attestation is for a device
        (default: False). Device attestations and claim sets are unencrypted.
    :return: Dictionary containing the attestation `id`, the serialised
        `attestation` object and updated `claim_set_keys` dictionary.
    """
    attester_sig_key = utils.jwk_from(attester_sig_key)
    my_attestation = Attestation(claim_set_keys=claim_set_keys,
                                 attester_signing_key=attester_sig_key,
                                 allow_unencrypted=device)
    if claim_set:
        my_attestation.claim_set_keys.claim_set = claim_set
    # Add attester data.
    my_attestation.attester_data = attester_data
    my_attestation.attestation_data = attestation_data
    # Attest the claim set.
    serialised_attestation = my_attestation.finalise(attester_sig_key)
    # Return attestation with updated key data (containing trace key).
    claim_set_keys_dict = (None if device else
                           my_attestation.claim_set_keys.to_dict(
                               claim_type_hints=True))
    return {
        'id': my_attestation.id,
        'attestation': serialised_attestation,
        'claim_set_keys': claim_set_keys_dict
    }


def api_request_kym_attestation(subject: str,
                                claims: dict,
                                attester_obo: str,
                                statements: List[dict]) -> Dict[str, str]:
    """
    Request a device attestation via the KYM API.

    This REST API attests a device identity *on behalf of* the requestor.

    :param subject: DID of the claim set subject.
    :param claims: Identity attribute claims to attest.
    :param attester_obo: DID of the organisation/identity on whose behalf
        the attestation will be requested.
    :param statements: List of attestation statements (JSON serialisable).
    :return: Dictionary containing the API's attestation result. It contains
        an `attestation_id` and the `attestation` itself.
    """
    request_body = {
        'subject': subject,
        'attesterObo': attester_obo,
        'claims': claims,
        'statements': statements
    }
    response = utils.request_api(base_url=config.kym_attestation_base_url,
                                 resource=config.kym_attestation_resource_path,
                                 body=json.dumps(request_body, indent=2),
                                 method='POST')
    if response.status_code != 201:
        raise RuntimeError('Error requesting a KYM attestation: {} {}'
                           .format(response.status_code, response.content))
    response_body = json.loads(response.content.decode())
    result = {
        'attestation_id': response_body['attestationId'],
        'attestation': response_body['attestation']
    }
    return result
