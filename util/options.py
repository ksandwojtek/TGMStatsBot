import argparse
import json

from structs.globals import GlobalVariables


def parse_arguments():
    parser = argparse.ArgumentParser(description="Runs an instance of the PVP Arcade Stat Bot")
    parser.add_argument("-t", "--token", nargs=1, type=str, help="Discord bot token")
    parser.add_argument("-c", "--channels", nargs="+", type=int, help="Channel ID(s) where the Discord Bot will respond"
                                                                      " to queries")
    parser.add_argument("-g", "--guilds", nargs="+", type=int, help="ID of the Guilds/Servers that the bot should "
                                                                    "respond in. "
                                                                    "The bot must be in those servers for it to work.")
    parser.add_argument("-p", "--proxy", nargs=1, type=str, help="URL of the proxy to send requests through. "
                                                                 "Supports HTTP, and SOCKS4/5 proxies. Pass in "
                                                                 "protocol://user:password@IP:Port format. Both the "
                                                                 "user and password parts are optional. For example "
                                                                 "to proxy the bot through TOR use "
                                                                 "socks5://127.0.0.1:9050 as the proxy")
    rdns_feature = parser.add_mutually_exclusive_group(required=False)
    rdns_feature.add_argument('--redirect-dns', dest='rdns', action='store_true', help="Redirects DNS requests through "
                                                                                       "the proxy, highly recommend "
                                                                                       "for when using TOR. Default"
                                                                                       "action is to use system DNS.")
    rdns_feature.add_argument('--use-system-dns', dest='rdns', action='store_false', help="Uses system DNS to resolve"
                                                                                          "DNS requests. Default action"
                                                                                          "is to do this.")
    parser.set_defaults(rdns=False)

    args = parser.parse_args()

    with open("./config.json", mode="r") as fl:
        config = json.loads(fl.read())

    # args_to_check = ["token", "channel", "guild"]
    if args.token is not None:
        # The documentation for argparse is incorrect, nargs=1 passes in data as a list even if it limits the list to
        # a size of 1 entry, as a result, we must cast the list to an int for the token
        # While it would be easier to just set config['bot']['token'] = args.token[0]
        # I would like to attempt to fix this in argparse itself or at least find a different nargs value to make a more
        # elegant workaround, this code will work if that change happens and if it does, I will delete this
        if type(args.token) == list and len(args.token) == 1:
            args.token = args.token[0]
        else:
            print("Argparse behaviour broken again, debug variable values to find the issue")
        config["bot"]["token"] = args.token
    if args.channels is not None:
        config["bot"]["channels"] = args.channels
    if args.guilds is not None:
        config['bot']['guilds'] = args.guilds
    if args.proxy is not None:
        # Same situation with the token applies to the proxy as well
        if type(args.proxy) == list and len(args.proxy) == 1:
            args.proxy = args.proxy[0]
        else:
            print("Argparse behaviour broken again, debug variable values to find the issue")
        config['connection']['proxy'] = args.proxy
        config['connection']['rdns'] = args.rdns

    if isinstance(config['bot']['channels'], int):
        config['bot']['channels'] = [config['bot']['channels']]
    if isinstance(config['bot']['guilds'], int):
        config['bot']['guilds'] = [config['bot']['guilds']]

    global_variables = GlobalVariables()
    global_variables.set_config(config)