import os

from onepanel.utilities.cloud_storage_utility import CloudStorageUtility
from onepanel.utilities.creds_utility import CredsUtility

from onepanel.models.job import Job

from onepanel.commands.jobs import JobViewController
from onepanel.utilities.git_utility import CheckGitLfsInstalled
from onepanel.utilities.original_connection import Connection

class Jobs():
    def __init__(self, account_uid=None, project_uid=None):
        conn = Connection()
        conn.load_credentials()
        utility = CheckGitLfsInstalled()
        utility.figure_out_git_installed()
        if utility.git_installed is False:
            print('Error. Cannot detect git, please verify git is installed.')
            exit(-1)
        self.job_view_controller = JobViewController(conn)
        if account_uid is None or project_uid is None:
            self.job_view_controller.init_credentials_retrieval()
        else:
            self.job_view_controller.project_account_uid = account_uid
            self.job_view_controller.project_uid = project_uid
        self.job_view_controller.init_endpoint()

    def list(self, all=False):
        items = self.job_view_controller.list(params='?running=true' if not all else '')

        if items is None or len(items) == 0:
            msg = ['No jobs found.']
            if not all:
                msg.append('Set "all" to "true" to retrieve completed jobs.')
            print(''.join(msg))
            return

        items = [Job.from_json(item).simple_view() for item in items['data']]
        self.job_view_controller.print_items(items, fields=['uid', 'state', 'command'],
                                             field_names=['ID', 'STATE', 'COMMAND'])

    def create(self, job):
        if not job:
            print("Error: Need a job object to create a job.")
        if not job.machine_type.uid:
            print("Error: Machine Type must be set.")
        if not job.instance_template.uid:
            print("Error: Environment must be set.")
        if not job.volume_type.uid:
            print("Error: A volume must be set.")

        response = self.job_view_controller.create(job)

        if response['status_code'] == 200:
            print('New job created: {}'.format(response['data']['uid']))
        else:
            print("An error occurred: {}".format(response['data']))

    def status(self, job):
        if not job:
            print("Error: Need a job object to get status of.")
        if not job.uid:
            print("Error: Job UID cannot be blank to look up status.")
        response = self.job_view_controller.get('/'+str(job.uid))
        job_with_data = job.from_json(response['data'])
        print(job_with_data.state())

    def stop(self, job):
        if not job:
            print("Error: Need a job object to stop the job.")
        if not job.uid:
            print("Error: Job UID cannot be blank.")
        response = self.job_view_controller.delete_v2('/' + str(job.uid) + '/active')
        job_with_data = job.from_json(response['data'])
        print(job_with_data.state())

    def delete(self, job):
        if not job:
            print("Error: Need a job object to delete the job.")
        if not job.uid:
            print("Error: Job UID cannot be blank.")
        self.job_view_controller.delete(job.uid, message_on_success='Job deleted', message_on_failure='Job not found')

    def get(self, job):
        if not job:
            print("Error: Need a job object to get.")
        if not job.uid:
            print("Error: Job UID cannot be blank.")
        response = self.job_view_controller.get('/' + str(job.uid))
        return job.from_json(response['data'])

    def download_output(self, job, archive_flag=False):
        if not job:
            print("Error: Need a job object to download the output.")
        if not job.uid:
            print("Error: Job UID cannot be blank.")
        job_retrieved = self.get(job)
        if not job_retrieved:
            print("Job not found.")
            return False

        home = os.getcwd()
        jvc = self.job_view_controller
        creds = CredsUtility.get_credentials(self.job_view_controller.conn, jvc.project_account_uid, 'projects',
                                             jvc.project_uid)
        util = CloudStorageUtility.get_utility(creds)
        cloud_provider_download_to_path = home
        if archive_flag is True:
            print("Attempting to download the compressed output file to {home} directory.".format(
                home=cloud_provider_download_to_path))
            cloud_provider_path_to_download_from = jvc.get_cloud_provider_compressed_file_for_job_output_path(
                jvc.conn.account_uid, jvc.project_uid, job.uid)
            full_path = util.build_full_cloud_specific_url(cloud_provider_path_to_download_from)
            investigation_results = util.check_cloud_path_for_files(full_path, False)
            if investigation_results['code'] == -1:
                print("Error encountered.")
                print(investigation_results['msg'])
                return
            if investigation_results['code'] == 0 and investigation_results['data'] == 0:
                print("This job did not create any output or output was not saved. \n" +
                      "If you want to save and version control your output, modify your script to "
                      "save all output to the '/onepanel/output' directory.\n")
                return
            exit_code = util.download(cloud_provider_download_to_path, cloud_provider_path_to_download_from)
            if exit_code != 0:
                print("Error encountered.")
                return
        else:
            print("Attempting to download output to {home} directory.".format(home=cloud_provider_download_to_path))
            cloud_provider_path_to_download_from = jvc.get_cloud_provider_root_for_job_output(
                jvc.conn.account_uid, jvc.project_uid, job.uid)
            full_path = util.build_full_cloud_specific_url(cloud_provider_path_to_download_from)
            investigation_results = util.check_cloud_path_for_files(full_path)
            print(investigation_results)

            if investigation_results['code'] == -1:
                print("Error encountered.")
                print(investigation_results['msg'])
                return
            if investigation_results['code'] == 0 and investigation_results['data'] == 0:
                print("This job did not create any output or output was not saved. \n" +
                      "If you want to save and version control your output, modify your script to "
                      "save all output to the '/onepanel/output' directory.\n")
                return
            # Check if there any actual files to download from the output
            exit_code = util.download_all(cloud_provider_download_to_path, cloud_provider_path_to_download_from)
            if exit_code != 0:
                print("Error encountered.")
                return
        print("Finished downloading.")
        return True
