import os
import random
import requests
import string
import tempfile
import time
import django

from django.core.management import BaseCommand, call_command, CommandError
from requests_toolbelt.multipart.encoder import MultipartEncoder

CASSETTE_API_URL = os.getenv("CASSETTE_API")

def to_url(*parts):
    return "{}/{}".format(CASSETTE_API_URL, "/".join(map(str, parts)))

session = requests.Session()

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--command',
            dest='command',
            help='Command to run tests containing integration tests',
            required=True,
        )

        parser.add_argument(
            '--project-access-token',
            dest='project_access_token',
            help='Project access token',
            required=True,
        )

        parser.add_argument(
            '--project-id',
            dest='project_id',
            help='Project id',
            required=True,
        )

        parser.add_argument(
            '--branch',
            dest='branch',
            help='Branch to put the results in',
            required=True,
        )

    def write(self, text):
        self.stdout.write(text)

    def create_new_revision(self, project_id, branch_name):
        branch_id = None
        revision_id = None

        project_response = session.get(to_url("projects", project_id))
        if project_response.status_code not in [200, 201]:
            raise CommandError("[cassette] Failed to get project with id '{}'".format(project_id))

        branch_response = session.put(to_url("projects", project_id, "branches"), json={ "name": branch_name })
        if branch_response.status_code not in [200, 201]:
            raise CommandError("[cassette] Failed to get or create branch '{}'".format(branch_name))
        branch_id = branch_response.json()["branch"]["id"]

        revision_response = session.post(
            to_url("projects", project_id, "branches", branch_id, "revisions"),
            json={
                "framework_name": "django",
                "framework_version": django.get_version(),
                "framework_build_version": ".".join([str(v) for v in django.VERSION]),
            }
        )
        if revision_response.status_code not in [201]:
            raise CommandError("[cassette] Failed to create new revision in branch '{}'".format(branch_name))
        revision_id = revision_response.json()["revision"]["id"]

        return (branch_id, revision_id)

    def setup(self, options):
        session.headers.update({'authorization': f"Project {options['project_access_token']}"})
        project_id = options['project_id']
        branch_name = options['branch']

        branch_id, revision_id = self.create_new_revision(project_id, branch_name)
        self.project_id = project_id
        self.branch_id = branch_id
        self.revision_id = revision_id

        _, path = tempfile.mkstemp()
        os.environ["CASSETTE_BULK_FILE_PATH"] = path
        os.environ["CASSETTE_BULK_FILE_SEPARATOR"] = 'separator--' + ''.join(random.choices(string.ascii_letters + string.digits, k=64))


    def handle(self, *args, **options):
        self.pre_run(options)
        command_parts = filter(lambda x: len(x) > 0, options['command'].split(' '))
        call_command(*command_parts)
        self.post_run(options)
        self.finish_up(options)

    def pre_run(self, options):
        self.setup(options)
        os.environ["CASSETTE_RECORDING"] = "1"
        self.write(f"[cassette] Created new revision of {options['branch']} and started test run")

    def assert_has_episodes(self):
        bulk_file_size = os.stat(os.environ["CASSETTE_BULK_FILE_PATH"]).st_size
        if bulk_file_size == 0:
            raise CommandError("[cassette] Couldn't find any episodes after test run. Make sure you have selected a test suite with integration tests.")

    def post_run(self, options):
        os.environ["CASSETTE_RECORDING"] = "0"
        self.assert_has_episodes()

        start_time = time.time()
        bodies = [
            ("episodes", ("episodes.txt", open(os.getenv("CASSETTE_BULK_FILE_PATH"), "rb"), "text/plain"))
        ]
        episode_import_url = to_url("projects", self.project_id, "branches", self.branch_id, "revisions", self.revision_id, "episodes")
        mp = MultipartEncoder(fields=bodies)
        episode_import_response = session.post(episode_import_url, data=mp, headers={'content-type': mp.content_type})
        if episode_import_response.status_code not in [200]:
            self.write(episode_import_response.text)
            raise CommandError("[cassette] Failed to import episodes to revision '{}' on branch '{}'".format(self.revision_id, options['branch']))
            
        self.write("[cassette] Uploaded recorded requests to cassette in {} ms".format(
            round((time.time() - start_time) * 1000)
        ))

    def finish_up(self, options):
        complete_url = to_url("projects", self.project_id, "branches", self.branch_id, "revisions", self.revision_id, "complete")
        complete_response = session.post(complete_url)
        if complete_response.status_code not in [202]:
            raise CommandError("[cassette] Failed to complete to revision '{}' on branch '{}'".format(self.revision_id, options['branch']))

        if complete_response.json()["created_new_revision"]:
            self.write("[cassette] Completed new revision for '{}' (cassette://project/{}/branch/{}/revision/{})".format(
                options['branch'],
                self.project_id,
                self.branch_id,
                self.revision_id,
            ))
        else:
            self.write("[cassette] No changes made. Did not create a new revision for '{}'".format(
                options['branch']
            ))


