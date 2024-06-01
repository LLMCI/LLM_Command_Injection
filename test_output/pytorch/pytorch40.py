import io
import glob
import subprocess

DASHBOARD_DEFAULTS = {
    "dashboard_image_uploader": "/fsx/users/anijain/bin/imgur.sh",
    "dashboard_archive_path": "/data/home/anijain/cluster/cron_logs",
    "dashboard_gh_cli_path": "/data/home/anijain/miniconda/bin/gh",
}


class RegressionTracker:
   def __init__(self, args):
        self.args = args

   def generate_comment(self):
        title = "## Metrics over time ##\n"
        str_io = io.StringIO()
        if not self.args.update_dashboard_test and not self.args.no_graphs:
            for name in glob.glob(self.args.output_dir + "/*over_time.png"):
                output = (
                    subprocess.check_output([self.args.dashboard_image_uploader, name])
                    .decode("ascii")
                    .rstrip()
                )
                str_io.write(f"\n{name} : ![]({output})\n")
        
