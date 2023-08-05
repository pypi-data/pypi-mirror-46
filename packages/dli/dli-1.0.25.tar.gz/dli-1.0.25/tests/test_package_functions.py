import logging
import datetime
from functools import partial
from unittest import skip
from tests.common import SdkIntegrationTestCase
from dli.client.exceptions import (
    CatalogueEntityNotFoundException,
    MissingMandatoryArgumentException,
    NoAccountSpecified,
)


logger = logging.getLogger(__name__)


class PackageFunctionsTestCase(SdkIntegrationTestCase):

    def test_get_unknown_package_raises_package_not_found(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_package("unknown")

    def test_can_get_package_by_id_or_name(self):
        package_id = self.create_package(
            name="test_get_package_returns_non_siren_response"
        )
        package = self.client.get_package(package_id)
        self.assertEqual(package.package_id, package_id)

        package_by_name = self.client.get_package(name=package.name)
        self.assertEqual(package_by_name.package_id, package_id)

    def test_cannot_get_package_without_package_id_or_name(self):
        with self.assertRaises(ValueError):
            self.client.get_package(None)

    def test_get_datasets_in_package(self):
        client = self.client
        package_id = self.create_package("test_get_datasets_in_package")
        builder = self.dataset_builder(package_id, "test_package_functions").with_external_storage("somewhere")
        self.client.register_dataset(builder)

        datasets = client.get_package_datasets(package_id)

        self.assertEqual(len(datasets), 1)

    def test_get_datasets_in_package_with_None_should_be_handled_gracefully(self):
        with self.assertRaises(MissingMandatoryArgumentException):
            self.client.get_package_datasets(None)

    def test_can_delete_package(self):
        package_id = self.create_package(
            "test_can_delete_package"
        )
        self.client.delete_package(package_id)
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.get_package(package_id)

    def test_delete_unknown_package_raises_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.delete_package("unknown")


class RegisterPackageTestCase(SdkIntegrationTestCase):

    def setUp(self):
        super(RegisterPackageTestCase, self).setUp()

        self.create = partial(
            self.client.register_package,
            name="RegisterPackageTestCase" + str(datetime.datetime.now()),
            description="my package description",
            topic="Automotive",
            access="Restricted",
            internal_data="Yes",
            data_sensitivity="Public",
            terms_and_conditions="Terms",
            publisher="Bloomberg",
            access_manager_id="datalake-mgmt",
            tech_data_ops_id="datalake-mgmt",
            manager_id="datalake-mgmt"
        )

    def test_edit_unknown_package_raises_unknown_package_exception(self):
        with self.assertRaises(CatalogueEntityNotFoundException):
            self.client.edit_package(package_id="unknown")

    def test_edit_package_should_ignore_extra_keys_and_succeed_when_unknown_key_passed_with_kwargs(self):
        package = self.create()
        updated_package = self.client.edit_package(package.package_id, i_do_not_exist='sabotage')
        self.assertTrue('i_do_not_exist' not in updated_package._fields)

    def test_edit_package_should_unset_field_when_passed_none(self):
        package = self.create(
            intended_purpose="Intended purpose",
            documentation="Documentation",
            internal_usage_rights="Yes",
            internal_usage_notes="internal usage notes",
            distribution_rights="Yes",
            distribution_notes="distribution notes",
            derived_data_rights="Yes",
            derived_data_notes="derived data notes"
        )

        updated_package = self.client.edit_package(
            package.package_id,
            intended_purpose=None,
            documentation=None,
            internal_usage_rights=None,
            internal_usage_notes=None,
            distribution_rights=None,
            distribution_notes=None,
            derived_data_rights=None,
            derived_data_notes=None
        )
        self.assertTrue('intended_purpose' not in updated_package._fields)
        self.assertTrue('documentation' not in updated_package._fields)
        self.assertTrue('internal_usage_rights' not in updated_package._fields)
        self.assertTrue('internal_usage_notes' not in updated_package._fields)
        self.assertTrue('distribution_rights' not in updated_package._fields)
        self.assertTrue('distribution_notes' not in updated_package._fields)
        self.assertTrue('derived_data_rights' not in updated_package._fields)
        self.assertTrue('derived_data_notes' not in updated_package._fields)

    def test_edit_package_allows_changing_single_field(self):
        package = self.create(intended_purpose="Testing")
        self.assertEqual(package.intended_purpose, "Testing")
        
        edited = self.client.edit_package(
            package.package_id, description="enhanced description"
        )
        self.assertEqual(edited.package_id, package.package_id)
        self.assertEqual(edited.description, "enhanced description")

        # accounts were not changed
        self.assertEqual(edited.manager_id, package.manager_id)
        self.assertEqual(edited.tech_data_ops_id, package.tech_data_ops_id)
        self.assertEqual(edited.publisher, package.publisher)
        self.assertEqual(edited.access_manager_id, package.access_manager_id)

        # name is still the same
        self.assertEqual(edited.name, package.name)

        self.assertEqual(edited.intended_purpose, package.intended_purpose)

    def test_edit_can_change_account_ids(self):
        package = self.create()

        edited = self.client.edit_package(
            package.package_id,
            tech_data_ops_id="iboxx"
        )

        self.assertEqual(edited.package_id, package.package_id)
        self.assertEqual(edited.tech_data_ops_id, "iboxx")

