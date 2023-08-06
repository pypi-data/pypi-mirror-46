# -*- coding: utf-8 -*-
"""
Module providing an entry point to attestation operations via a CLI.
"""

# Created: 2019-05-09 Guy K. Kloss <guy@mysinglesource.io>
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
from typing import Optional

from singlesource import utils
from singlesource.attestations import (api_request_kym_attestation,
                                       get_raw_subject_commitment,
                                       merge_subject_commitment)
from singlesource.config import config


logger = logging.getLogger(__name__)


def attest_kym_claim_set(subject: str,
                         claims_fd: io.TextIOBase,
                         attestation_file: str,
                         attester_obo: Optional[str] = None,
                         statements_fd: Optional[io.TextIOBase] = None):
    """
    Attest a claim set for a device using the KYM API.

    :param subject: DID of the claim set subject.
    :param claims_fd: File for the claims.
    :param attestation_file: File name to store the attestation in.
    :param attester_obo: DID of the organisation/identity on whose behalf
        the attestation will be requested.
    :param statements_fd: Name of JSON file containing attestation statements.
    """
    plain_claims = json.load(claims_fd)
    statements = config.kym_default_statements
    if statements_fd:
        statements = json.load(statements_fd)
    attester_obo = attester_obo or config.kym_default_attester_obo
    result = api_request_kym_attestation(subject, plain_claims,
                                         attester_obo=attester_obo,
                                         statements=statements,
                                         device=True)
    with open(attestation_file, 'wt') as fd:
        json.dump(result, fd, indent=2)


def extract_raw_subject_commitment(attestation_file: str,
                                   attester_sig_key_fd: io.TextIOBase,
                                   commitment_file: str):
    """
    Extract raw (unsigned) subject commitment data from an attestation.

    :param attestation_file: File of the attestation to read.
    :param attester_sig_key_fd: Key to use (public) for verification of the
        attester signature.
    :param commitment_file: Name of the file to write the subject commitment
        to.
    """
    raw_attestation = open(attestation_file, 'rt').read()
    attester_sig_key = utils.jwk_from(attester_sig_key_fd.read())
    raw_subject_commitment = get_raw_subject_commitment(raw_attestation,
                                                        attester_sig_key)
    with open(commitment_file, 'tw') as fd:
        fd.write(raw_subject_commitment)


def merge_cosigned_commitment(attestation_file: str,
                              attester_sig_key_fd: io.TextIOBase,
                              subject_sig_key_fd: io.TextIOBase,
                              commitment_file: str,
                              commitment_signature_file: str):
    """
    Extract raw (unsigned) subject commitment data from an attestation.

    :param attestation_file: File for attestation to read from/write to.
    :param attester_sig_key_fd: Key to use (public) for verification of the
        attester signature.
    :param subject_sig_key_fd: Key to use (public) for verification of the
        subject signature.
    :param commitment_file: Name of the file to read the subject commitment
        from.
    :param commitment_signature_file: Name of the file to read the subject
        commitment signature from.
    """
    raw_attestation = open(attestation_file, 'rt').read()
    attester_sig_key = utils.jwk_from(attester_sig_key_fd.read())
    subject_sig_key = utils.jwk_from(subject_sig_key_fd.read())
    raw_subject_commitment = open(commitment_file, 'tr').read()
    subject_commitment_signature = open(commitment_signature_file, 'br').read()
    accepted_attestation = merge_subject_commitment(
        raw_attestation, attester_sig_key, subject_sig_key,
        raw_subject_commitment, subject_commitment_signature)

    with open(attestation_file, 'tw') as fd:
        fd.write(accepted_attestation)


def main(args: argparse.Namespace):
    """
    Delegate to the right functions from given (command line) arguments.

    :param args: Command line arguments provided:

        - args.subject - type: str
        - args.claims - type: io.TextIOBase
        - args.attester_obo - type: str
        - args.statements - type: io.TextIOBase
        - args.attestation - type: str
        - args.attester_sig_key - type: io.TextIOBase
        - args.subject_sig_key - type: io.TextIOBase
        - args.commitment_file - type: str
        - args.commitment_signature_file - type: str
    """
    if args.operation == 'attest':
        attest_kym_claim_set(args.subject, args.claims, args.attestation,
                             args.attester_obo, args.statements)
    elif args.operation == 'extract-subj-commitment':
        extract_raw_subject_commitment(args.attestation, args.attester_sig_key,
                                       args.commitment_file)
    elif args.operation == 'merge-subj-commitment':
        merge_cosigned_commitment(args.attestation, args.attester_sig_key,
                                  args.subject_sig_key, args.commitment_file,
                                  args.commitment_signature_file)
    else:
        raise ValueError('Unsupported operation "{}" for attestations.'
                         .format(args.operation))

    logger.info('Operation "{}" finished.'.format(args.operation))
