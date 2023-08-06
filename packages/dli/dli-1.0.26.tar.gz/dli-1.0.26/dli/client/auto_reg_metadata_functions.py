import logging

from dli.client.exceptions import (
    CatalogueEntityNotFoundException,
    DownloadFailed,
    MissingMandatoryArgumentException,
)

from dli.siren import siren_to_entity, siren_to_dict


logger = logging.getLogger(__name__)


class AutoRegMetadataFunctions:

    @property
    def __root(self):
        return self.ctx.memoized(
            self.get_root_siren().auto_reg_metadatas_root,
            "auto_reg_metadatas_root"
        )

    def set_auto_registration_metadata(
        self,
        dataset_id,
        path_template,
        name_template,
        as_of_date_template,
        active,
        sns_topic_for_s3_events,
        handle_files=False
    ):
        """
        Submit a request to set up the auto registration metadata for a dataset.

        See description for each parameter, and whether they are optional or mandatory.

        :param str dataset_id: Mandatory. Dataset ID for which the auto registration metadata is being set up.
        :param str path_template: Mandatory. Path template for the files stored under the dataset.
        :param str name_template: Mandatory. Name template for the datafiles registered under the dataset.
        :param str as_of_date_template: Mandatory. As of date template for the datafiles registered under the dataset.
        :param bool active: Mandatory. Boolean flag to indicate the auto registration status of the dataset 
                            i.e. True => Active, False => Inactive or disabled
        :param str sns_topic_for_s3_events: Mandatory. Name of SNS topic where the S3 notification events are published when
                            files are added, updated or deleted from the S3 bucket for this dataset.
        :param bool handle_files: Optional. Boolean flag to indicate whether the individual files (for e.g. parquet part files
                                    in case of a parquet dataset) are to be registered under the datafile for the dataset.
        :returns: The created auto registration metadata object.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # For example if the files for dataset id `xyz` are stored in the s3 bucket along
                `region=US/as_of_date=2019-02-18`

                auto_reg_metadata = client.set_auto_registration_metadata(
                    dataset_id="xyz",
                    path_template="region={{ region }}/as_of_date={{ year }}-{{ month }}-{{ day }}",
                    name_template="Datafile_name_{{ region }}_{{ year }}-{{ month }}-{{ day }}",
                    as_of_date_template="{{ year }}-{{ month }}-{{ day }}",
                    active=True,
                    sns_topic_for_s3_events='s3-notifications-sns-topic'
                )
        """
        
        if not dataset_id:
            raise MissingMandatoryArgumentException('dataset_id')

        dataset = self.get_dataset(id=dataset_id)

        fields = {
            'datasetId': dataset.dataset_id,
            'pathTemplate': path_template,
            'nameTemplate': name_template,
            'asOfDateTemplate': as_of_date_template,
            'active': active,
            'snsTopicForS3Events': sns_topic_for_s3_events,
            'handlePartFiles': handle_files
        }

        payload = {k: v for k, v in fields.items() if v is not None}
        return siren_to_entity(self.__root.create_auto_reg_metadata(__json=payload))

    def get_auto_registration_metadata(self, dataset_id=None, auto_reg_metadata_id=None):
        """
        Fetches the auto registration metadata for a dataset.

        :param str dataset_id: The dataset id for which auto registration metadata is being fetched.
                            Either this or auto_reg_metadata_id is required for the look up
        :param str auto_reg_metadata_id: The id of the auto registration metadata.
                            Either this or dataset_id is required for the look up
        :returns: The auto registration metadata object.
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # Look up by dataset id
                auto_reg_metadata = client.get_auto_registration_metadata('my_dataset_id')
                # or equivalent
                auto_reg_metadata = client.auto_reg_metadata(dataset_id='my_dataset_id')


                # If auto reg metadata id is known
                auto_reg_metadata = client.auto_reg_metadata(auto_reg_metadata_id='my_auto_reg_id')
        """

        if dataset_id and auto_reg_metadata_id:
            return siren_to_entity(
                self._get_auto_reg_metadata(
                    auto_reg_metadata_id=auto_reg_metadata_id,
                    dataset_id=dataset_id
                )
            )
        elif auto_reg_metadata_id:
            return siren_to_entity(
                self._get_auto_reg_metadata(
                    auto_reg_metadata_id=auto_reg_metadata_id
                )
            )
        elif dataset_id:
            return siren_to_entity(
                self._get_auto_reg_metadata(
                    dataset_id=dataset_id
                )
            )

        raise ValueError("Either dataset id or auto reg metadata id must be specified to look up auto registration details for the dataset")

    def _get_auto_reg_metadata(self, **kwargs):

        auto_reg_metadata = self.__root.get_auto_reg_metadata(**kwargs)

        if not auto_reg_metadata:
            raise CatalogueEntityNotFoundException('AutoRegMetadata', params=kwargs)

        return auto_reg_metadata

    def edit_auto_registration_metadata(
        self,
        auto_reg_metadata_id,
        path_template=None,
        name_template=None,
        as_of_date_template=None,
        active=None,
        sns_topic_for_s3_events=None,
        handle_files=None
    ):
        """
        Edits existing auto registration metadata for a dataset.
        Fields passed as ``None`` will retain their original value.

        :param str auto_reg_metadata_id: Mandatory. The id of the auto registration metadata we want to modify.
        :param str path_template: Path template for the files stored under the dataset.
        :param str name_template: Name template for the datafiles registered under the dataset.
        :param str as_of_date_template: As of date template for the datafiles registered under the dataset.
        :param bool active: Boolean flag to indicate the auto registration status of the dataset 
                            i.e. True => Active, False => Inactive or disabled
        :param str sns_topic_for_s3_events: Name of SNS topic where the S3 notification events are published when
                            files are added, updated or deleted from the S3 bucket for this dataset.
        :param bool handle_files: Boolean flag to indicate whether the individual files (for e.g. parquet part files
                                    in case of a parquet dataset) are to be registered under the datafile for the dataset.

        :returns: The updated auto registration metadata object
        :rtype: collections.namedtuple

        - **Sample**

        .. code-block:: python

                # For example edit metadata to make it inactive

                updated_auto_reg_metadata = client.edit_auto_registration_metadata(
                    auto_reg_metadata_id="test-auto-reg-metadata-id",
                    active=False
                )
        """

        if not auto_reg_metadata_id:
            raise MissingMandatoryArgumentException('auto_reg_metadata_id')

        auto_reg_metadata = self._get_auto_reg_metadata(auto_reg_metadata_id=auto_reg_metadata_id)

        fields = {
            'datasetId': auto_reg_metadata.datasetId,
            'pathTemplate': path_template,
            'nameTemplate': name_template,
            'asOfDateTemplate': as_of_date_template,
            'active': active,
            'snsTopicForS3Events': sns_topic_for_s3_events,
            'handlePartFiles': handle_files,
        }

        # clean up any unknown fields, and update the entity
        auto_reg_metadata_dict = siren_to_dict(auto_reg_metadata)
        for key in list(auto_reg_metadata_dict.keys()):
            if key not in fields:
                del auto_reg_metadata_dict[key]

        payload = {k: v for k, v in fields.items() if v is not None}
        auto_reg_metadata_dict.update(payload)

        # perform the update and return the resulting entity
        return siren_to_entity(auto_reg_metadata.edit_auto_reg_metadata(__json=auto_reg_metadata_dict))

    def delete_auto_registration_metadata(self, auto_reg_metadata_id):
        """
        Marks auto registration metadata as deleted.

        :param str auto_reg_metadata_id: the id for the metadata we want to delete.

        :returns:

        - **Sample**

        .. code-block:: python

                client.delete_auto_registration_metadata(auto_reg_metadata_id)
        """

        if not auto_reg_metadata_id:
            raise MissingMandatoryArgumentException('auto_reg_metadata_id')

        auto_reg_metadata = self._get_auto_reg_metadata(auto_reg_metadata_id=auto_reg_metadata_id)
        if not auto_reg_metadata:
            raise CatalogueEntityNotFoundException('AutoRegMetadata', params=auto_reg_metadata_id)

        auto_reg_metadata.delete_auto_reg_metadata(auto_reg_metadata_id=auto_reg_metadata_id)