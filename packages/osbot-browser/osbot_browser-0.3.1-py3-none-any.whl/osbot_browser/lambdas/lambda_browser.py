from pbx_gs_python_utils.utils.Files import Files
from pbx_gs_python_utils.utils.Process import Process

def cleanup_chrome_processes_and_tmp_files():               # remote temp files
    for file in Files.find('/tmp/core.headless_shell.*'):
        pid = file.split('.')[-1]
        Process.run('pkill',['-TERM','-P',str(pid)])             # this doesn't seem to be working since the  "headless_shell <defunct>" is still there
        Files.delete(file)


def run(event, context):
    from osbot_browser.browser.Browser_Commands import Browser_Commands
    from pbx_gs_python_utils.utils.slack.Slack_Commands_Helper import Slack_Commands_Helper
    params  = event.get('params')
    data    = event.get('data')
    channel = None
    team_id = None
    if data:
        channel = data.get('channel')
        team_id = data.get('team_id')
    data,_ = Slack_Commands_Helper(Browser_Commands).invoke(team_id, channel, params)

    cleanup_chrome_processes_and_tmp_files()

    return data