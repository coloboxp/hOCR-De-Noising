import ConfigParser
import os

# TODO: Need sane defaults for all settings
defaults = {
    "scheduler": "slurm",
    "mem_per_cpu": "4000",
    "cpus_per_task": "1",
}


class EmopSettings(object):

    def __init__(self, config_path):
        self.config_path = config_path
        self.config = ConfigParser.ConfigParser(defaults=defaults)
        self.config.read(self.config_path)

        if os.getenv("EMOP_HOME"):
            self.emop_home = os.getenv("EMOP_HOME")
        else:
            self.emop_home = os.path.dirname(self.config_path)

        # Settings for communicating with dashboard
        self.api_version = self.get_value('dashboard', 'api_version')
        self.url_base = self.get_value('dashboard', 'url_base')
        self.auth_token = self.get_value('dashboard', 'auth_token')
        self.api_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/emop; version=%s' % self.api_version,
            'Authorization': 'Token token=%s' % self.auth_token,
        }

        # Settings used by controller
        self.payload_input_path = self.get_value('controller', 'payload_input_path')
        self.payload_output_path = self.get_value('controller', 'payload_output_path')
        self.payload_completed_path = os.path.join(self.payload_output_path, "completed")
        self.payload_uploaded_path = os.path.join(self.payload_output_path, "uploaded")
        self.ocr_root = self.get_value('controller', 'ocr_root')
        self.input_path_prefix = self.get_value('controller', 'input_path_prefix')
        self.output_path_prefix = self.get_value('controller', 'output_path_prefix')
        self.log_level = self.get_value('controller', 'log_level')
        self.scheduler = self.get_value('controller', 'scheduler')

        # Settings used to interact with the cluster scheduler
        self.max_jobs = int(self.get_value('scheduler', 'max_jobs'))
        self.scheduler_queue = self.get_value('scheduler', 'queue')
        self.scheduler_job_name = self.get_value('scheduler', 'name')
        self.min_job_runtime = int(self.get_value('scheduler', 'min_job_runtime'))
        self.max_job_runtime = int(self.get_value('scheduler', 'max_job_runtime'))
        self.avg_page_runtime = int(self.get_value('scheduler', 'avg_page_runtime'))
        self.scheduler_logdir = self.get_value('scheduler', 'logdir')
        self.scheduler_logfile = os.path.join(self.scheduler_logdir, "%s-%%j.out" % self.scheduler_job_name)
        self.scheduler_mem_per_cpu = self.get_value('scheduler', 'mem_per_cpu')
        self.scheduler_cpus_per_task = self.get_value('scheduler', 'cpus_per_task')

        # Settings used by Juxta-cl
        self.juxta_cl_jx_algorithm = self.get_value('juxta-cl', 'jx_algorithm')

    def get_value(self, section, option, default=None):
        interpolation_map = {
            "home": os.getenv("HOME"),
            "emop_home": self.emop_home,
        }
        raw_value = self.config.get(section, option, 0, interpolation_map)

        return raw_value
