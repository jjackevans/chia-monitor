import aiohttp
from chia.cmds.farm_funcs import summary, get_blockchain_state, get_harvesters, is_farmer_running, get_wallets_stats, \
    get_average_block_time
from chia.cmds.units import units
from chia.consensus.block_record import BlockRecord
from chia.util.misc import format_bytes, format_minutes
from chia.util.network import is_localhost
from flask import Flask, jsonify

app = Flask(__name__)


class PlotStats:
    total_plot_size = 0
    total_plots = 0

@app.route('/status')
async def test():

    await summary(None, None, None, None)
    all_harvesters = await get_harvesters(None)
    blockchain_state = await get_blockchain_state(None)
    farmer_running = await is_farmer_running(None)

    status = {}
    if blockchain_state is None:
        status['state'] = "Not available"
    elif blockchain_state["sync"]["sync_mode"]:
        status['state'] = "Syncing"
        status['sync_height'] = blockchain_state["sync"]["sync_progress_height"]
    elif not blockchain_state["sync"]["synced"]:
        status['state'] = "Not synced or not connected to peers"
    elif not farmer_running:
        status['state'] = "Not running"
    else:
        status['state'] = "Farming"

    try:
        amounts = await get_wallets_stats(None)
    except Exception as e:
        if isinstance(e, aiohttp.ClientConnectorError):
            wallet_not_running = True
        else:
            wallet_not_ready = True
    if all_harvesters is not None:
        harvesters_local: dict = {}
        harvesters_remote: dict = {}
        for harvester in all_harvesters["harvesters"]:
            ip = harvester["connection"]["host"]
            if is_localhost(ip):
                harvesters_local[harvester["connection"]["node_id"]] = harvester
            else:
                if ip not in harvesters_remote:
                    harvesters_remote[ip] = {}
                harvesters_remote[ip][harvester["connection"]["node_id"]] = harvester

        def process_harvesters(harvester_peers_in: dict):
            for harvester_peer_id, plots in harvester_peers_in.items():
                total_plot_size_harvester = sum(map(lambda x: x["file_size"], plots["plots"]))
                PlotStats.total_plot_size += total_plot_size_harvester
                PlotStats.total_plots += len(plots["plots"])
                status['plots_count'] = len(plots['plots'])
                status['plots_size'] = format_bytes(total_plot_size_harvester)

        if len(harvesters_local) > 0:
            print(f"Local Harvester{'s' if len(harvesters_local) > 1 else ''}")
            process_harvesters(harvesters_local)
        # for harvester_ip, harvester_peers in harvesters_remote.items():
        #     print(f"Remote Harvester{'s' if len(harvester_peers) > 1 else ''} for IP: {harvester_ip}")
        #     process_harvesters(harvester_peers)

        # print(f"Plot count for all harvesters: {PlotStats.total_plots}")
        #
        # print("Total size of plots: ", end="")
        # print(format_bytes(PlotStats.total_plot_size))
    else:
        status['plots_count'] = "Unknown"
        status['plots_size'] = "Unknown"

    print(blockchain_state)
    if blockchain_state is not None:
        p: BlockRecord = blockchain_state['peak']
        status['block_height'] = p.height
        print("Estimated network space: ", end="")
        status['estimated_size'] = format_bytes(blockchain_state["space"])

    if amounts is not None:
        status['total_farmed'] = amounts['farmed_amount'] / units['chia']
        status['tx_fees'] = amounts['fee_amount'] / units['chia']
        status['block_rewards'] = (amounts['farmer_reward_amount'] + amounts['pool_reward_amount']) / units['chia']
        status['last_farm_height'] = amounts['last_height_farmed']

    minutes = -1
    if blockchain_state is not None and all_harvesters is not None:
        proportion = PlotStats.total_plot_size / blockchain_state["space"] if blockchain_state["space"] else -1
        minutes = int((await get_average_block_time(None) / 60) / proportion) if proportion else -1

    if all_harvesters is not None and PlotStats.total_plots == 0:
        status['time_to_win'] = "Never"
        status['time_to_win_days'] = "Never"
    else:
        status['time_to_win'] = format_minutes(minutes)
        status['time_to_win_days'] = minutes / (60 * 24)

    return jsonify(status)

@app.route('/status')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()