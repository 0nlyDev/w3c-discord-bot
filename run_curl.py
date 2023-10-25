import subprocess


def run_curl(url):
    try:
        # Construct the curl command
        cmd = ['curl', url]

        # Execute the command
        response = subprocess.check_output(cmd)

        return response.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Command `{e.cmd}` returned with error (code {e.returncode}): {e.output}")
        return None
