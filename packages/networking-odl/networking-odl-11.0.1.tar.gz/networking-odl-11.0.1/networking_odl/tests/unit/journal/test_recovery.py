#
# Copyright (C) 2016 Red Hat, Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
#

from oslo_config import cfg

import mock

from neutron_lib import exceptions as nexc
from neutron_lib.plugins import constants as plugin_constants
from neutron_lib.plugins import directory

from networking_odl.common import constants as odl_const
from networking_odl.db import db
from networking_odl.journal import full_sync
from networking_odl.journal import recovery
from networking_odl.l3 import l3_odl_v2
from networking_odl.ml2 import mech_driver_v2
from networking_odl.tests import base
from networking_odl.tests.unit import test_base_db


class RecoveryTestCase(test_base_db.ODLBaseDbTestCase):
    def setUp(self):
        self.useFixture(
            base.OpenDaylightRestClientGlobalFixture(recovery._CLIENT))
        super(RecoveryTestCase, self).setUp()
        self._CLIENT = recovery._CLIENT.get_client()
        self.addCleanup(self.clean_registered_resources)

    @staticmethod
    def clean_registered_resources():
        full_sync.ALL_RESOURCES = {}

    def _mock_resource(self, plugin, resource_type):
        mock_resource = mock.MagicMock()
        get_func = getattr(plugin, 'get_{}'.format(resource_type))
        get_func.return_value = mock_resource
        return mock_resource

    def _mock_row(self, resource_type):
        return mock.MagicMock(object_type=resource_type)

    def _test__get_latest_resource(self, plugin, resource_type):
        l2 = mech_driver_v2.L2_RESOURCES
        full_sync.ALL_RESOURCES[plugin_constants.CORE] = l2
        mock_resource = self._mock_resource(plugin, resource_type)
        mock_row = self._mock_row(resource_type)

        resource = recovery._get_latest_resource(self.db_context.session,
                                                 mock_row)
        self.assertEqual(mock_resource, resource)

    @mock.patch.object(directory, 'get_plugin')
    def test__get_latest_resource_l2(self, plugin_mock):
        for resource_type in mech_driver_v2.L2_RESOURCES:
            plugin = plugin_mock.return_value
            self._test__get_latest_resource(plugin, resource_type)

    @mock.patch.object(directory, 'get_plugin')
    def test__get_latest_resource_l3(self, plugin_mock):
        full_sync.ALL_RESOURCES[plugin_constants.L3] = l3_odl_v2.L3_RESOURCES
        for resource_type in l3_odl_v2.L3_RESOURCES:
            plugin = plugin_mock.return_value
            self._test__get_latest_resource(plugin, resource_type)

    def test__get_latest_resource_unsupported(self):
        mock_row = self._mock_row('aaa')
        self.assertRaises(
            recovery.UnsupportedResourceType, recovery._get_latest_resource,
            self.db_context.session, mock_row)

    @mock.patch.object(directory, 'get_plugin')
    def test__get_latest_resource_none(self, plugin_mock):
        plugin_mock.return_value.get_network.side_effect = nexc.NotFound()
        l2 = mech_driver_v2.L2_RESOURCES
        full_sync.ALL_RESOURCES[plugin_constants.CORE] = l2

        mock_row = self._mock_row(odl_const.ODL_NETWORK)
        self.assertRaises(
            nexc.NotFound, recovery._get_latest_resource,
            self.db_context.session, mock_row)

    def test_journal_recovery_retries_exceptions(self):
        db.create_pending_row(self.db_context.session, odl_const.ODL_NETWORK,
                              'id', odl_const.ODL_DELETE, {})
        created_row = db.get_all_db_rows(self.db_context.session)[0]
        db.update_db_row_state(self.db_context.session, created_row,
                               odl_const.FAILED)
        with mock.patch.object(db, 'update_db_row_state') as m:
            self._test_retry_exceptions(recovery.journal_recovery, m, True)

    def test_journal_recovery_no_rows(self):
        recovery.journal_recovery(self.db_context)
        self.assertFalse(self._CLIENT.get_resource.called)

    def _test_recovery(self, operation, odl_resource, expected_state):
        db.create_pending_row(self.db_context.session, odl_const.ODL_NETWORK,
                              'id', operation, {})
        created_row = db.get_all_db_rows(self.db_context.session)[0]
        db.update_db_row_state(self.db_context.session, created_row,
                               odl_const.FAILED)

        self._CLIENT.get_resource.return_value = odl_resource

        recovery.journal_recovery(self.db_context)

        if expected_state is None:
            completed_rows = db.get_all_db_rows_by_state(
                self.db_context.session, odl_const.COMPLETED)
            self.assertEqual([], completed_rows)
        else:
            row = db.get_all_db_rows_by_state(self.db_context.session,
                                              expected_state)[0]
            self.assertEqual(created_row['seqnum'], row['seqnum'])

        return created_row

    def _disable_retention(self):
        cfg.CONF.set_override('completed_rows_retention', 0, 'ml2_odl')

    def test_journal_recovery_handles_failure_quietly(self):
        class TestException(Exception):
            pass

        self._CLIENT.get_resource.side_effect = TestException('')
        self._test_recovery(
            odl_const.ODL_DELETE, None, odl_const.FAILED)

    def test_journal_recovery_deleted_row_not_in_odl(self):
        self._test_recovery(odl_const.ODL_DELETE, None, odl_const.COMPLETED)

    def test_journal_recovery_deleted_row_not_in_odl_purged(self):
        self._disable_retention()
        self._test_recovery(odl_const.ODL_DELETE, None, None)

    def test_journal_recovery_created_row_exists_in_odl(self):
        self._test_recovery(odl_const.ODL_CREATE, {}, odl_const.COMPLETED)

    def test_journal_recovery_created_row_exists_in_odl_purged(self):
        self._disable_retention()
        self._test_recovery(odl_const.ODL_CREATE, {}, None)

    def test_journal_recovery_deleted_row_exists_in_odl(self):
        self._test_recovery(odl_const.ODL_DELETE, {}, odl_const.PENDING)

    @mock.patch.object(recovery, '_get_latest_resource')
    def _test_recovery_creates_operation(
            self, operation, resource, odl_resource, expected_operation,
            recovery_mock):
        if resource is not None:
            recovery_mock.return_value = resource
        else:
            recovery_mock.side_effect = nexc.NotFound
        original_row = self._test_recovery(
            operation, odl_resource, odl_const.COMPLETED)

        pending_row = db.get_all_db_rows_by_state(
            self.db_context.session, odl_const.PENDING)[0]
        self.assertEqual(expected_operation, pending_row['operation'])
        self.assertEqual(original_row['object_type'],
                         pending_row['object_type'])
        self.assertEqual(original_row['object_uuid'],
                         pending_row['object_uuid'])

    def test_recovery_created_row_not_in_odl(self):
        self._test_recovery_creates_operation(
            odl_const.ODL_CREATE, {}, None, odl_const.ODL_CREATE)

    def test_recovery_updated_row_not_in_odl(self):
        self._test_recovery_creates_operation(
            odl_const.ODL_UPDATE, {}, None, odl_const.ODL_CREATE)

    def test_recovery_updated_resource_missing_but_exists_in_odl(self):
        self._test_recovery_creates_operation(
            odl_const.ODL_UPDATE, None, {}, odl_const.ODL_DELETE)

    @mock.patch.object(recovery, '_get_latest_resource')
    def test_recovery_created_resource_missing_and_not_in_odl(self, rmock):
        rmock.side_effect = nexc.NotFound
        self._test_recovery(odl_const.ODL_CREATE, None, odl_const.COMPLETED)

    @mock.patch.object(recovery, '_get_latest_resource')
    def test_recovery_created_resource_missing_and_not_in_odl_purged(
            self, rmock):
        rmock.side_effect = nexc.NotFound
        self._disable_retention()
        self._test_recovery(odl_const.ODL_CREATE, None, None)

    @mock.patch.object(recovery, '_get_latest_resource')
    def test_recovery_updated_resource_missing_and_not_in_odl(self, rmock):
        rmock.side_effect = nexc.NotFound
        self._test_recovery(odl_const.ODL_UPDATE, None, odl_const.COMPLETED)

    @mock.patch.object(recovery, '_get_latest_resource')
    def test_recovery_updated_resource_missing_and_not_in_odl_purged(
            self, rmock):
        rmock.side_effect = nexc.NotFound
        self._disable_retention()
        self._test_recovery(odl_const.ODL_UPDATE, None, None)
