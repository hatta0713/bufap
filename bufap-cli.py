import argparse
import logging
import pprint
import sys

import bufap


def main() -> None:
    output: str = ""

    logging.basicConfig(
        level=logging.WARN,
        format="%(asctime)s [%(levelname)s] %(message)s",
        stream=sys.stderr,
    )

    parser = argparse.ArgumentParser(
        description="WAPMシリーズコンフィグツール",  # 引数のヘルプの前に表示
        add_help=True,  # -h/–help オプションの追加
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--get-conf",
        help="設定を取得",
        action="store_const",
        const="get-conf",
        dest="action",
    )
    group.add_argument(
        "--read-conf",
        help="設定を読み込み",
        action="store_const",
        const="read-conf",
        dest="action",
    )
    group.add_argument(
        "--wireless-monitor",
        help="無線環境モニター",
        action="store_const",
        const="wireless-monitor",
        dest="action",
    )
    group.add_argument(
        "--client-monitor",
        help="クライアントモニター",
        action="store_const",
        const="client-monitor",
        dest="action",
    )

    parser.add_argument("--host", help="ホストアドレス(IP)")
    parser.add_argument("--username", default="admin", help="ユーザー名")
    parser.add_argument("--password", default="password", help="パスワード")

    parser.add_argument("--infile", help="設定ファイルのパス")
    parser.add_argument("--outfile", help="出力先ファイルのパス")

    parser.add_argument(
        "--summarize", help="ユーザーが変更した部分のみ表示する", choices=["yes", "no"], default="yes"
    )

    parser.add_argument("--column", choices=["user", "default"], default="user")

    parser.add_argument(
        "--format", choices=["raw", "text", "dict", "csv"], default="text"
    )
    args = parser.parse_args()

    summarize = True if args.summarize == "yes" else False

    logging.debug(args)
    if args.action == "get-conf":
        conf = bufap.BUFAPconf(
            hostname=args.host,
            username=args.username,
            password=args.password,
        )
    elif args.action == "read-conf":
        conf = bufap.BUFAPconf(conf_file=args.infile)
    elif args.action == "wireless-monitor":
        tool = bufap.BUFAPtool(args.host, args.username, args.password)
        output = tool.get_wireless_monitor(args.format)
    elif args.action == "client-monitor":
        tool = bufap.BUFAPtool(args.host, args.username, args.password)
        output = tool.get_client_monitor(args.format)

    if args.action in ["get-conf", "read-conf"]:
        if args.format == "raw":
            output = conf.as_raw()
        elif args.format == "text":
            conf.parse_as_table(summarize)
            output = conf.as_text(args.column, summarize)
        elif args.format == "dict":
            conf.as_dict(args.column, summarize)
            output = pprint.pformat(conf.conf_dict)

    if args.outfile:
        with open(args.outfile, "w") as f:
            f.write(output)
    else:
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
