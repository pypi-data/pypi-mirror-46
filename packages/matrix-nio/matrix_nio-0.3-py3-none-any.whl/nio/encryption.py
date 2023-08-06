# -*- coding: utf-8 -*-

# Copyright © 2018 Damir Jelić <poljar@termina.org.uk>
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted, provided that the
# above copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER
# RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF
# CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN
# CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import unicode_literals

import json
import os
# pylint: disable=redefined-builtin
from builtins import str
from collections import defaultdict
from functools import wraps
from typing import (Any, DefaultDict, Deque, Dict, Iterator, List, NamedTuple,
                    Optional, Set, Tuple, Union)

import olm
from jsonschema import SchemaError, ValidationError
from logbook import Logger
from olm import (OlmGroupSessionError, OlmMessage, OlmPreKeyMessage,
                 OlmSessionError)

from .api import Api
from .crypto import (DeviceStore, GroupSessionStore, InboundGroupSession,
                     InboundSession, OlmAccount, OlmDevice,
                     OutboundGroupSession, OutboundSession, Session,
                     SessionStore)
from .events import (BadEventType, EncryptedEvent, Event, MegolmEvent,
                     OlmEvent, RoomEncryptedEvent, RoomEncryptedMessage,
                     RoomKeyEvent, UnknownBadEvent, validate_or_badevent)
from .exceptions import (EncryptionError, GroupEncryptionError, OlmTrustError,
                         VerificationError)
from .log import logger_group
from .responses import (KeysClaimResponse, KeysQueryResponse,
                        KeysUploadResponse, ShareGroupSessionResponse)
from .schemas import Schemas, validate_json
from .store import DefaultStore

logger = Logger("nio.encryption")
logger_group.add_logger(logger)

try:
    from json.decoder import JSONDecodeError
except ImportError:  # pragma: no cover
    JSONDecodeError = ValueError  # type: ignore


class Olm(object):
    def __init__(
        self,
        user_id,  # type: str
        device_id,  # type: str
        session_path,  # type: str
    ):
        # type: (...) -> None
        self.user_id = user_id
        self.device_id = device_id
        self.session_path = session_path
        self.uploaded_key_count = None  # type: Optional[int]
        self.users_for_key_query = set()   # type: Set[str]

        # List of group session ids that we shared with people
        self.shared_sessions = []  # type: List[str]

        # Dict[user_id, Dict[device_id, OlmDevice]]
        self.device_store = DeviceStore()
        # Dict[curve25519_key, List[Session]]
        self.session_store = SessionStore()
        # Dict[RoomId, Dict[curve25519_key, Dict[session id, Session]]]
        self.inbound_group_store = GroupSessionStore()

        # Dict of outbound Megolm sessions Dict[room_id]
        self.outbound_group_sessions = {} \
            # type: Dict[str, OutboundGroupSession]

        self.store = DefaultStore(user_id, device_id, session_path)

        self.account = self.store.load_account()

        if not self.account:
            logger.info("Creating new Olm account for {} on device {}".format(
                        self.user_id, self.device_id))
            self.account = OlmAccount()
            self.save_account()
        else:
            self.load()

    def update_tracked_users(self, room):
        already_tracked = set(self.device_store.users)
        room_users = set(room.users.keys())

        missing = room_users - already_tracked

        if missing:
            self.users_for_key_query.update(missing)

    @property
    def should_query_keys(self):
        if self.users_for_key_query:
            return True
        return False

    @property
    def should_upload_keys(self):
        if self.uploaded_key_count is None:
            return False

        max_keys = self.account.max_one_time_keys
        key_count = (max_keys // 2) - self.uploaded_key_count
        return key_count > 0

    def user_fully_verified(self, user_id):
        # type: (str) -> bool
        devices = self.device_store.active_user_devices(user_id)
        for device in devices:
            if (not self.is_device_verified(device)
                    and not self.is_device_blacklisted(device)):
                return False

        return True

    def share_keys(self):
        # type: () -> Dict[str, Any]
        def generate_one_time_keys(current_key_count):
            # type: (int) -> None
            max_keys = self.account.max_one_time_keys

            key_count = (max_keys // 2) - current_key_count

            if key_count <= 0:
                raise ValueError("Can't share any keys, too many keys already "
                                 "shared")

            self.account.generate_one_time_keys(key_count)

        def device_keys():
            device_keys = {
                "algorithms": [
                    "m.olm.v1.curve25519-aes-sha2",
                    "m.megolm.v1.aes-sha2"
                ],
                "device_id": self.device_id,
                "user_id": self.user_id,
                "keys": {
                    "curve25519:" + self.device_id:
                        self.account.identity_keys["curve25519"],
                    "ed25519:" + self.device_id:
                        self.account.identity_keys["ed25519"]
                }
            }

            signature = self.sign_json(device_keys)

            device_keys["signatures"] = {
                self.user_id: {
                    "ed25519:" + self.device_id: signature
                }
            }
            return device_keys

        def one_time_keys():
            one_time_key_dict = {}

            keys = self.account.one_time_keys["curve25519"]

            for key_id, key in keys.items():
                key_dict = {"key": key}
                signature = self.sign_json(key_dict)

                one_time_key_dict["signed_curve25519:" + key_id] = {
                    "key": key_dict.pop("key"),
                    "signatures": {
                        self.user_id: {
                            "ed25519:" + self.device_id: signature
                        }
                    }
                }

            return one_time_key_dict

        content = {}  # type: Dict[Any, Any]

        # We're sharing our account for the first time, upload the identity
        # keys and one-time keys as well.
        if not self.account.shared:
            content["device_keys"] = device_keys()
            generate_one_time_keys(0)
            content["one_time_keys"] = one_time_keys()

        # Just upload one-time keys.
        else:
            if self.uploaded_key_count is None:
                raise EncryptionError("The uploaded key count is not known")

            generate_one_time_keys(self.uploaded_key_count)
            content["one_time_keys"] = one_time_keys()

        return content

    def _handle_key_claiming(self, response):
        keys = response.one_time_keys

        for user_id, user_devices in keys.items():
            for device_id, one_time_key in user_devices.items():
                # We need to find the device curve key for the wanted
                # user and his device.
                try:
                    device = self.device_store[user_id][device_id]
                except KeyError:
                    logger.warn("Curve key for user {} and device {} not "
                                "found, failed to start Olm session".format(
                                    user_id,
                                    device_id))
                    continue

                logger.info("Found curve key for user {} and device {}".format(
                    user_id,
                    device_id))

                key_object = next(iter(one_time_key.values()))

                verified = self.verify_json(key_object,
                                            device.ed25519,
                                            user_id,
                                            device_id)
                if verified:
                    logger.info("Succesfully verified signature for one-time "
                                "key of device {} of user {}.".format(
                                    device_id, user_id))
                    logger.info("Creating Outbound Session for device {} of "
                                "user {}".format(device_id, user_id))
                    self.create_session(key_object["key"], device.curve25519)
                else:
                    logger.warn("Signature verification for one-time key of "
                                "device {} of user {} failed, could not start "
                                "Olm session.".format(device_id, user_id))

    # This function is copyrighted under the Apache 2.0 license Zil0
    def _handle_key_query(self, response):
        # type: (KeysQueryResponse) -> None
        changed = defaultdict(dict)  \
            # type: DefaultDict[str, Dict[str, OlmDevice]]

        for user_id, device_dict in response.device_keys.items():
            try:
                self.users_for_key_query.remove(user_id)
            except KeyError:
                pass

            for device_id, payload in device_dict.items():
                if device_id == self.device_id:
                    continue

                if (payload['user_id'] != user_id
                        or payload['device_id'] != device_id):
                    logger.warn(
                        "Mismatch in keys payload of device %s "
                        "(%s) of user %s (%s).",
                        payload['device_id'],
                        device_id,
                        payload['user_id'],
                        user_id
                    )
                    continue

                try:
                    key_dict = payload["keys"]
                    signing_key = key_dict["ed25519:{}".format(device_id)]
                    curve_key = key_dict["curve25519:{}".format(device_id)]
                except KeyError as e:
                    logger.warning(
                        "Invalid identity keys payload from device %s of"
                        " user %s: %s.",
                        device_id,
                        user_id,
                        e
                    )
                    continue

                verified = self.verify_json(
                    payload,
                    signing_key,
                    user_id,
                    device_id
                )

                if not verified:
                    logger.warning(
                        "Signature verification failed for device %s of "
                        "user %s.",
                        device_id,
                        user_id
                    )
                    continue

                user_devices = self.device_store[user_id]
                try:
                    device = user_devices[device_id]
                except KeyError:
                    logger.info("Adding new device to the device store for "
                                "user {} with device id {}".format(
                                    user_id,
                                    device_id
                                ))
                    self.device_store.add(OlmDevice(
                        user_id,
                        device_id,
                        ed25519_key=signing_key,
                        curve25519_key=curve_key,
                    ))
                else:
                    if device.ed25519 != signing_key:
                        logger.warning("Ed25519 key has changed for device %s "
                                       "of user %s.", device_id, user_id)
                        continue
                    if device.curve25519 == curve_key:
                        continue
                    device.curve25519 = curve_key
                    logger.info("Updating curve key in the device store for "
                                "user {} with device id {}".format(
                                    user_id,
                                    device_id
                                ))

                changed[user_id][device_id] = user_devices[device_id]

            current_devices = set(device_dict.keys())
            stored_devices = set(
                device.id for device in
                self.device_store.active_user_devices(user_id)
            )
            deleted_devices = stored_devices - current_devices

            for device_id in deleted_devices:
                device = self.device_store[user_id][device_id]
                device.deleted = True
                logger.info("Marking device {} of user {} as deleted".format(
                    user_id, device_id))
                changed[user_id][device_id] = device

        self.store.save_device_keys(changed)
        response.changed = changed

    def handle_response(self, response):
        if isinstance(response, KeysUploadResponse):
            self.account.shared = True
            self.uploaded_key_count = response.signed_curve25519_count
            self.mark_keys_as_published()
            self.save_account()

        elif isinstance(response, KeysQueryResponse):
            self._handle_key_query(response)

        elif isinstance(response, KeysClaimResponse):
            self._handle_key_claiming(response)

        elif isinstance(response, ShareGroupSessionResponse):
            room_id = response.room_id
            session = self.outbound_group_sessions[room_id]
            logger.info("Marking outbound group session for room {} "
                        "as shared".format(room_id))
            session.shared = True

    def _create_inbound_session(
        self,
        sender,  # type: str
        sender_key,  # type: str
        message,  # type: Union[OlmPreKeyMessage, OlmMessage]
    ):
        # type: (...) -> InboundSession
        logger.info("Creating Inbound session for {}".format(sender))
        # Let's create a new inbound session.
        session = InboundSession(self.account, message, sender_key)
        logger.info("Created Inbound session for {}".format(sender))
        # Remove the one time keys the session used so it can't be reused
        # anymore.
        self.account.remove_one_time_keys(session)
        # Save the account now that we removed the one time key.
        self.save_account()

        return session

    def blacklist_device(self, device):
        # type: (OlmDevice) -> bool
        return self.store.blacklist_device(device)

    def unblacklist_device(self, device):
        # type: (OlmDevice) -> bool
        return self.store.unblacklist_device(device)

    def verify_device(self, device):
        # type: (OlmDevice) -> bool
        return self.store.verify_device(device)

    def is_device_verified(self, device):
        # type: (OlmDevice) -> bool
        return self.store.is_device_verified(device)

    def is_device_blacklisted(self, device):
        # type: (OlmDevice) -> bool
        return self.store.is_device_blacklisted(device)

    def unverify_device(self, device):
        # type: (OlmDevice) -> bool
        return self.store.unverify_device(device)

    def create_session(self, one_time_key, curve_key):
        # type: (str, str) -> None
        # TODO this can fail
        session = OutboundSession(self.account, curve_key, one_time_key)
        # Save the account, add the session to the store and save it to the
        # database.
        self.save_account()
        self.session_store.add(curve_key, session)
        self.save_session(curve_key, session)

    def create_group_session(
        self, sender_key, sender_fp_key, room_id, session_id, session_key
    ):
        # type: (str, str, str, str, str) -> None
        logger.info(
            "Creating inbound group session for {} from {}".format(
                room_id, sender_key
            )
        )

        try:
            session = InboundGroupSession(session_key, sender_fp_key)
            if session.id != session_id:
                raise OlmSessionError(
                    "Mismatched session id while creating "
                    "inbound group session"
                )

        except OlmSessionError as e:
            logger.warn(e)
            return

        self.inbound_group_store.add(session, room_id, sender_key)
        self.save_inbound_group_session(room_id, sender_key, session)

    def create_outbound_group_session(self, room_id):
        # type: (str) -> None
        logger.info("Creating outbound group session for {}".format(room_id))
        session = OutboundGroupSession()
        self.outbound_group_sessions[room_id] = session

        id_key = self.account.identity_keys["curve25519"]
        fp_key = self.account.identity_keys["ed25519"]

        self.create_group_session(
            id_key, fp_key, room_id, session.id, session.session_key
        )
        logger.info("Created outbound group session for {}".format(room_id))

    def get_missing_sessions(self, users):
        # type: (List[str]) -> Dict[str, List[str]]
        missing = defaultdict(list)  # type: DefaultDict[str, List[str]]

        for user_id in users:
            for device in self.device_store.active_user_devices(user_id):
                # we don't need a session for our own device, skip it
                if device.id == self.device_id:
                    continue

                if not self.session_store.get(device.curve25519):
                    logger.warn(
                        "Missing session for device {}".format(device.id)
                    )
                    missing[user_id].append(device.id)

        return missing

    def _try_decrypt(
        self,
        sender,  # type: str
        sender_key,  # type: str
        message,  # type: Union[OlmPreKeyMessage, OlmMessage]
    ):
        # type: (...) -> Optional[str]
        plaintext = None

        # Let's try to decrypt with each known session for the sender.
        # for a specific device?
        for session in self.session_store[sender_key]:
            matches = False
            try:
                if isinstance(message, OlmPreKeyMessage):
                    # It's a prekey message, check if the session matches
                    # if it doesn't no need to try to decrypt.
                    matches = session.matches(message)
                    if not matches:
                        continue

                logger.info(
                    "Trying to decrypt olm message using existing "
                    "session for {} and sender_key {}".format(
                        sender, sender_key
                    )
                )

                plaintext = session.decrypt(message)
                self.save_session(sender_key, session)

                logger.info(
                    "Succesfully decrypted olm message "
                    "using existing session"
                )
                return plaintext

            except OlmSessionError as e:
                # Decryption failed using a matching session, we don't want
                # to create a new session using this prekey message so
                # raise an exception and log the error.
                if matches:
                    logger.error(
                        "Found matching session yet decryption "
                        "failed for sender {} and "
                        "sender key {}".format(sender, sender_key)
                    )
                    raise EncryptionError(
                        "Decryption failed for matching " "session"
                    )

                # Decryption failed, we'll try another session in the next
                # iteration.
                logger.info(
                    "Error decrypting olm message from {} "
                    "and sender key {}: {}".format(
                        sender, sender_key, str(e)
                    )
                )
                pass

        return None

    def _verify_olm_payload(self, sender, payload):
        # type: (str, Dict[Any, Any]) -> bool
        # Verify that the sender in the payload matches the sender of the event
        if sender != payload["sender"]:
            raise VerificationError("Missmatched sender in Olm payload")

        # Verify that we're the recipient of the payload.
        if self.user_id != payload["recipient"]:
            raise VerificationError("Missmatched recipient in Olm " "payload")

        # Verify that the recipient fingerprint key matches our own
        if (
            self.account.identity_keys["ed25519"]
            != payload["recipient_keys"]["ed25519"]
        ):
            raise VerificationError(
                "Missmatched recipient key in " "Olm payload"
            )

        return True

    def _handle_olm_event(self, sender, sender_key, payload):
        # type: (str, str, Dict[Any, Any]) -> Optional[RoomKeyEvent]
        logger.info("Recieved Olm event of type: {}".format(payload["type"]))

        if payload["type"] != "m.room_key":
            logger.warn(
                "Received unsuported Olm event of type {}".format(
                    payload["type"]
                )
            )
            return None

        event = RoomKeyEvent.from_dict(payload, sender, sender_key)
        content = payload["content"]

        if event.algorithm != "m.megolm.v1.aes-sha2":
            logger.error(
                "Error: unsuported room key of type {}".format(
                    event.algorithm
                )
            )
            return event

        logger.info(
            "Recieved new group session key for room {} "
            "from {}".format(event.room_id, sender)
        )

        self.create_group_session(
            sender_key,
            payload["keys"]["ed25519"],
            content["room_id"],
            content["session_id"],
            content["session_key"],
        )

        return event

    def decrypt_megolm_event(self, event):
        # type (MegolmEvent) -> Union[Event, BadEvent]
        if not event.room_id:
            raise EncryptionError("Event doens't contain a room id")

        verified = False

        session = self.inbound_group_store.get(
            event.room_id,
            event.sender_key,
            event.session_id
        )

        if not session:
            message = (
                "Error decrypting megolm event, no session found "
                "with session id {} for room {}".format(
                    event.session_id,
                    event.room_id
                )
            )
            logger.warn(message)
            raise EncryptionError(message)

        try:
            plaintext, message_index = session.decrypt(event.ciphertext)
        except OlmGroupSessionError as e:
            message = "Error decrypting megolm event: {}".format(str(e))
            logger.warn(message)
            raise EncryptionError(message)

        # TODO check the message index for replay attacks

        # If the message is from our own session mark it as verified
        if (event.sender == self.user_id
                and event.device_id == self.device_id
                and session.ed25519
                == self.account.identity_keys["ed25519"]
                and event.sender_key
                == self.account.identity_keys["curve25519"]):
            verified = True
        # Else check that the message is from a verified device
        else:
            try:
                device = self.device_store[event.sender][event.device_id]
            except KeyError:
                # We don't have the device keys for this device, add them
                # to our quey set so we fetch in the next key query.
                self.users_for_key_query.add(event.sender)
                pass
            else:
                # Do not mark events decrypted using a forwarded key as
                # verified
                if (self.is_device_verified(device)
                        and not session.forwarding_chain):
                    if (device.ed25519 != session.ed25519
                            or device.curve25519 != event.sender_key):
                        message = ("Device keys mismatch in event sent "
                                   "by device {}.".format(device.id))
                        logger.warn(message)
                        raise EncryptionError(message)

                    logger.info("Event {} succesfully verified".format(
                        event.event_id))
                    verified = True

        try:
            parsed_dict = json.loads(plaintext, encoding="utf-8") \
                # type: Dict[Any, Any]
        except JSONDecodeError as e:
            raise EncryptionError("Error parsing payload: {}".format(str(e)))

        bad = validate_or_badevent(
            parsed_dict,
            Schemas.room_megolm_decrypted
        )

        if bad:
            return bad

        parsed_dict["event_id"] = event.event_id
        parsed_dict["sender"] = event.sender
        parsed_dict["origin_server_ts"] = event.server_timestamp

        if event.transaction_id:
            parsed_dict["unsigned"] = {
                "transaction_id": event.transaction_id
            }

        new_event = EncryptedEvent.parse_event(parsed_dict)

        if isinstance(new_event, UnknownBadEvent):
            return new_event

        new_event.decrypted = True
        new_event.verified = verified
        new_event.sender_key = event.sender_key
        new_event.session_id = event.session_id

        return new_event

    def decrypt_event(
        self,
        event  # type: RoomEncryptedEvent
    ):
        # type: (...) -> Union[Event, BadEventType, RoomKeyEvent, None]
        logger.debug("Decrypting event of type {}".format(
            type(event).__name__
        ))
        if isinstance(event, OlmEvent):
            try:
                own_key = self.account.identity_keys["curve25519"]
                own_ciphertext = event.ciphertext[own_key]
            except KeyError:
                logger.warn("Olm event doesn't contain ciphertext for our key")
                return None

            if own_ciphertext["type"] == 0:
                message = OlmPreKeyMessage(own_ciphertext["body"])
            elif own_ciphertext["type"] == 1:
                message = OlmMessage(own_ciphertext["body"])
            else:
                logger.warn("Unsuported olm message type: {}".format(
                    own_ciphertext["type"]))
                return None

            return self.decrypt(event.sender, event.sender_key, message)

        elif isinstance(event, MegolmEvent):
            try:
                return self.decrypt_megolm_event(event)
            except EncryptionError:
                return None

        return None

    def decrypt(
        self,
        sender,  # type: str
        sender_key,  # type: str
        message,  # type: Union[OlmPreKeyMessage, OlmMessage]
    ):
        # type: (...) -> Optional[RoomKeyEvent]

        try:
            # First try to decrypt using an existing session.
            plaintext = self._try_decrypt(sender, sender_key, message)
        except EncryptionError:
            # We found a matching session for a prekey message but decryption
            # failed, don't try to decrypt any further.
            return None

        # Decryption failed with every known session or no known sessions,
        # let's try to create a new session.
        if not plaintext:
            # New sessions can only be created if it's a prekey message, we
            # can't decrypt the message if it isn't one at this point in time
            # anymore, so return early
            if not isinstance(message, OlmPreKeyMessage):
                return None

            try:
                # Let's create a new session.
                s = self._create_inbound_session(sender, sender_key, message)
                # Now let's decrypt the message using the new session.
                plaintext = s.decrypt(message)
                # Store the new session
                self.session_store.add(sender_key, s)
                self.save_session(sender_key, s)
            except OlmSessionError as e:
                logger.error(
                    "Failed to create new session from prekey"
                    "message: {}".format(str(e))
                )
                return None

        # Mypy complains that the plaintext can still be empty here,
        # realistically this can't happen but let's make mypy happy
        if not plaintext:
            logger.error("Failed to decrypt Olm message: unknown error")
            return None

        # The plaintext should be valid json, let's parse it and verify it.
        try:
            parsed_payload = json.loads(plaintext, encoding="utf-8")
        except JSONDecodeError as e:
            # Failed parsing the payload, return early.
            logger.error(
                "Failed to parse Olm message payload: {}".format(str(e))
            )
            return None

        # Validate the payload, check that it contains all required keys as
        # well that the types of the values are the one we expect.
        # Note: The keys of the content object aren't checked here, the caller
        # should check the content depending on the type of the event
        try:
            validate_json(parsed_payload, Schemas.olm_event)
        except (ValidationError, SchemaError) as e:
            # Something is wrong with the payload log an error and return
            # early.
            logger.error(
                "Error validating decrypted Olm event from {}"
                ": {}".format(sender, str(e.message))
            )
            return None

        # Verify that the payload properties contain correct values:
        # sender/recipient/keys/recipient_keys and check if the sender device
        # is alread verified by us
        try:
            self._verify_olm_payload(sender, parsed_payload)

        except VerificationError as e:
            # We found a missmatched property don't process the event any
            # further
            logger.error(e)
            return None

        else:
            # Verification succeded, handle the event
            return self._handle_olm_event(sender, sender_key, parsed_payload)

    def rotate_outbound_group_session(self, room_id):
        logger.info("Rotating outbound group session for room {}".format(
            room_id))
        self.create_outbound_group_session(room_id)

    def group_encrypt(
        self,
        room_id,  # type: str
        plaintext_dict,  # type: Dict[str, str]
    ):
        # type: (...) -> Dict[str, str]
        if room_id not in self.outbound_group_sessions:
            self.create_outbound_group_session(room_id)

        session = self.outbound_group_sessions[room_id]

        if session.expired:
            self.rotate_outbound_group_session(room_id)
            session = self.outbound_group_sessions[room_id]

        if not session.shared:
            raise GroupEncryptionError("Group session for room {} not "
                                       "shared.".format(room_id))

        plaintext_dict["room_id"] = room_id
        ciphertext = session.encrypt(Api.to_json(plaintext_dict))

        payload_dict = {
            "algorithm": "m.megolm.v1.aes-sha2",
            "sender_key": self.account.identity_keys["curve25519"],
            "ciphertext": ciphertext,
            "session_id": session.id,
            "device_id": self.device_id,
        }

        return payload_dict

    def _group_decrypt(
        self,
        session,    # type: InboundGroupSession
        ciphertext  # type: str
    ):
        # type: (...) -> Tuple[Optional[str], Optional[int]]

        try:
            plaintext, message_index = session.decrypt(ciphertext)
            return plaintext, message_index
        except OlmGroupSessionError as e:
            logger.error("Error decrypting megolm event: {}".format(str(e)))
            return None, None

    def share_group_session(
        self,
        room_id,  # type: str
        users,    # type: List[str]
        ignore_missing_sessions=False  # type: bool
    ):
        # type: (...) -> Dict[str, Any]
        logger.info("Sharing group session for room {}".format(room_id))
        group_session = self.outbound_group_sessions[room_id]

        key_content = {
            "algorithm": "m.megolm.v1.aes-sha2",
            "room_id": room_id,
            "session_id": group_session.id,
            "session_key": group_session.session_key,
            "chain_index": group_session.message_index,
        }

        payload_dict = {
            "type": "m.room_key",
            "content": key_content,
            "sender": self.user_id,
            "sender_device": self.device_id,
            "keys": {"ed25519": self.account.identity_keys["ed25519"]},
        }

        to_device_dict = {"messages": {}}  # type: Dict[str, Any]

        for user_id in users:
            for device in self.device_store.active_user_devices(user_id):
                # No need to share the session with our own device
                if device.id == self.device_id:
                    continue

                if self.is_device_blacklisted(device):
                    continue

                session = self.session_store.get(device.curve25519)

                if not session:
                    if ignore_missing_sessions:
                        continue
                    else:
                        raise EncryptionError("Missing Olm session for user {}"
                                              " and device {}".format(
                                                  user_id,
                                                  device.id))

                if not self.is_device_verified(device):
                    raise OlmTrustError("Device {} for user {} is not "
                                        "verified or blacklisted.".format(
                                            device.id,
                                            device.user_id
                                        ))

                device_payload_dict = payload_dict.copy()
                device_payload_dict["recipient"] = user_id
                device_payload_dict["recipient_keys"] = {
                    "ed25519": device.ed25519
                }

                olm_message = session.encrypt(
                    Api.to_json(device_payload_dict)
                )
                self.store.save_session(device.curve25519, session)

                olm_dict = {
                    "algorithm": "m.olm.v1.curve25519-aes-sha2",
                    "sender_key": self.account.identity_keys["curve25519"],
                    "ciphertext": {
                        device.curve25519: {
                            "type": olm_message.message_type,
                            "body": olm_message.ciphertext,
                        }
                    },
                }

                if user_id not in to_device_dict["messages"]:
                    to_device_dict["messages"][user_id] = {}

                to_device_dict["messages"][user_id][device.id] = olm_dict

        return to_device_dict

    def load(self):
        # type: () -> None
        self.session_store = self.store.load_sessions()
        self.inbound_group_store = self.store.load_inbound_group_sessions()
        self.device_store = self.store.load_device_keys()

    def save(self):
        # type: () -> None
        self.save_account()

        for curve_key, session_list in self.session_store.items():
            for session in session_list:
                self.save_session(curve_key, session)

    def save_session(self, curve_key, session):
        # type: (str, Session) -> None
        self.store.save_session(curve_key, session)

    def save_inbound_group_session(self, room_id, sender_key, session):
        # type: (str, str, InboundGroupSession) -> None
        self.store.save_inbound_group_session(room_id, sender_key, session)

    def save_account(self):
        # type: () -> None
        logger.debug("Saving account")
        self.store.save_account(self.account)

    def sign_json(self, json_dict):
        # type: (Dict[Any, Any]) -> str
        signature = self.account.sign(Api.to_canonical_json(json_dict))
        return signature

    # This function is copyrighted under the Apache 2.0 license Zil0
    def verify_json(self, json, user_key, user_id, device_id):
        """Verifies a signed key object's signature.
        The object must have a 'signatures' key associated with an object of
        the form `user_id: {key_id: signature}`.
        Args:
            json (dict): The JSON object to verify.
            user_key (str): The public ed25519 key which was used to sign
                the object.
            user_id (str): The user who owns the device.
            device_id (str): The device who owns the key.
        Returns:
            True if the verification was successful, False if not.
        """
        try:
            signatures = json.pop('signatures')
        except KeyError:
            return False

        key_id = 'ed25519:{}'.format(device_id)
        try:
            signature_base64 = signatures[user_id][key_id]
        except KeyError:
            json['signatures'] = signatures
            return False

        unsigned = json.pop('unsigned', None)

        try:
            olm.ed25519_verify(
                user_key,
                Api.to_canonical_json(json),
                signature_base64
            )
            success = True
        except olm.utility.OlmVerifyError:
            success = False

        json['signatures'] = signatures
        if unsigned:
            json['unsigned'] = unsigned

        return success

    def mark_keys_as_published(self):
        # type: () -> None
        self.account.mark_keys_as_published()
