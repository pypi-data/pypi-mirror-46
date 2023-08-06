import click
import json
from ddsc.sdk.client import Client as DukeDSClient, KindType
from ddsc.core.upload import ProjectUpload
from ddsc.core.remotestore import RemoteStore, ProjectNameOrId
from ddsc.core.d4s2 import D4S2Project
from urllib.parse import urlparse


class Settings(object):
    def __init__(self, cmdfile):
        data = json.load(cmdfile)
        self.name = data['name']
        self.description = data['description']
        self.started_on = data['started_on']
        self.ended_on = data['ended_on']
        self.input_file_version_ids = data['input_file_ids']
        self.workflow_output_json_path = data['workflow_output_json_path']


class DukeDSActivity(object):
    def __init__(self, dds_client, settings, uploaded_files_info):
        self.dds_client = dds_client
        self.data_service = dds_client.dds_connection.data_service
        self.activity_settings = settings.activity_settings
        self.file_id_lookup = uploaded_files_info.file_id_lookup

    def create(self):
        click.echo("Creating activity {}.".format(self.activity_settings.name))
        activity_id = self._create_activity()

        click.echo("Attaching {} used relations.".format(len(self.activity_settings.input_file_version_ids)))
        for input_file_version_id in self.activity_settings.input_file_version_ids:
            self._create_activity_used_relation(activity_id, input_file_version_id)

        output_file_paths = self._get_output_file_paths()
        click.echo("Attaching {} generated relations.".format(len(output_file_paths)))
        for output_file_path in output_file_paths:
            output_file_version_id = self._get_file_version_id_for_path(output_file_path)
            self._create_activity_generated_relation(activity_id, output_file_version_id)

    def _create_activity(self):
        resp = self.data_service.create_activity(
            self.activity_settings.name,
            self.activity_settings.description,
            self.activity_settings.started_on,
            self.activity_settings.ended_on)
        return resp.json()["id"]

    def _create_activity_used_relation(self, activity_id, file_version_id):
        self.data_service.create_used_relation(activity_id, KindType.file_str, file_version_id)

    def _create_activity_generated_relation(self, activity_id, file_version_id):
        self.data_service.create_was_generated_by_relation(activity_id, KindType.file_str, file_version_id)

    def _get_file_version_id_for_path(self, output_file_path):
        file_id = self.file_id_lookup[output_file_path]
        duke_ds_file = self.dds_client.get_file_by_id(file_id)
        return duke_ds_file.current_version['id']

    def _get_output_file_paths(self):
        file_paths = []
        with open(self.activity_settings.workflow_output_json_path, 'r') as infile:
            data = json.load(infile)
            for value in data.values():
                DukeDSActivity._recursive_add_cwl_file_paths(value, file_paths)
            return file_paths

    @staticmethod
    def _recursive_add_cwl_file_paths(dict_or_array, file_paths):
        if isinstance(dict_or_array, dict):
            if dict_or_array.get('class') == "File":
                if 'location' in dict_or_array:
                    file_location = dict_or_array['location']
                    file_path = urlparse(file_location).path
                    file_paths.append(file_path)
                if 'secondaryFiles' in dict_or_array:
                    secondary_files = dict_or_array['secondaryFiles']
                    DukeDSActivity._recursive_add_cwl_file_paths(secondary_files, file_paths)
        else:
            for elem in dict_or_array:
                DukeDSActivity._recursive_add_cwl_file_paths(elem, file_paths)


class ActivityUtil(object):
    def __init__(self, cmdfile):
        self.settings = Settings(cmdfile)
        self.dds_client = DukeDSClient()
        self.dds_config = self.dds_client.dds_connection.config

    def get_project(self):
        """
        Find or create a project with the name self.settings.destination
        :return: ddsc.sdk.client.Project
        """
        project_name = self.settings.destination
        for project in self.dds_client.get_projects():
            if project.name == project_name:
                return project
        raise ValueError("No project found with name {}".format(project_name))

    def create_provenance_activity(self, uploaded_files_info):
        """
        Create a provenance activity in DukeDS API for our project.
        :param uploaded_files_info: UploadedFilesInfo: contains details about uploaded files
        """
        activity = DukeDSActivity(self.dds_client, self.settings, uploaded_files_info)
        activity.create()

    def share_project(self, project):
        """
        Share the specified project with some users.
        :param project: ddsc.sdk.client.Project: project to share
        """
        remote_store = RemoteStore(self.dds_config)
        remote_project = remote_store.fetch_remote_project_by_id(project.id)
        d4s2_project = D4S2Project(self.dds_config, remote_store, print_func=print)
        for dds_user_id in self.settings.share_dds_user_ids:
            d4s2_project.share(remote_project,
                               remote_store.fetch_user(dds_user_id),
                               force_send=True,
                               auth_role=self.settings.share_auth_role,
                               user_message=self.settings.share_user_message)

    def create_annotate_project_details_script(self, project, outfile):
        """
        Create a script to annotat a pod with details about the uploaded project
        :param project: ddsc.sdk.client.Project: project to share
        :param outfile: output file to write script into
        """
        readme_file = project.get_child_for_path(self.settings.readme_file_path)
        click.echo("Writing annotate project details script project_id:{} readme_file_id:{} to {}".format(
            project.id, readme_file.id, outfile.name))
        contents = "kubectl annotate pod $MY_POD_NAME " \
                   "project_id={} readme_file_id={}".format(project.id, readme_file.id)
        outfile.write(contents)
        outfile.close()


@click.command()
@click.argument('cmdfile', type=click.File('r'))
@click.argument('outfile', type=click.File('w'))
def main(cmdfile, outfile):
    util = ActivityUtil(cmdfile)
    project = util.get_project()
    util.create_provenance_activity(uploaded_files_info)
    util.share_project(project)
    util.create_annotate_project_details_script(project, outfile)


if __name__ == '__main__':
    main()
