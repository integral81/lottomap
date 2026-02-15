import json
import argparse
import sys
from lotto_utils import load_data, save_data, search_shops, update_shop_pov, group_by_shop

# Force UTF-8 output for Windows terminals
sys.stdout.reconfigure(encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(description="Lotto Shop Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command: search
    parser_search = subparsers.add_parser("search", help="Search for shops")
    parser_search.add_argument("query", help="Search query (name or address)")

    # Command: register
    parser_reg = subparsers.add_parser("register", help="Register/Update POV for a shop")
    parser_reg.add_argument("--name", required=True, help="Shop Name (substring match)")
    parser_reg.add_argument("--addr", required=True, help="Address (substring match)")
    parser_reg.add_argument("--panoid", required=True, help="Kakao Pano ID")
    parser_reg.add_argument("--pan", type=float, default=0.0)
    parser_reg.add_argument("--tilt", type=float, default=0.0)
    parser_reg.add_argument("--zoom", type=int, default=0)
    parser_reg.add_argument("--lat", type=float, help="Latitude (optional)")
    parser_reg.add_argument("--lng", type=float, help="Longitude (optional)")

    # Command: list_missing
    parser_missing = subparsers.add_parser("list_missing", help="List shops with 3+ wins missing POV")
    parser_missing.add_argument("--min_wins", type=int, default=3, help="Minimum wins")

    args = parser.parse_args()

    if args.command == "search":
        data = load_data()
        results = search_shops(args.query, data)
        print(f"Found {len(results)} records matching '{args.query}':")
        
        # Group by shop for display
        groups = group_by_shop(results)
        for key, items in groups.items():
            name, addr = key
            wins = len(items)
            has_pov = any(i.get('pov') for i in items)
            print(f"- [{name}] {addr} : {wins} wins {'(POV Registered)' if has_pov else '(No POV)'}")

    elif args.command == "register":
        data = load_data()
        pov_update = {
            "panoId": args.panoid,
            "pan": args.pan,
            "tilt": args.tilt,
            "zoom": args.zoom
        }
        if args.lat: pov_update["lat"] = args.lat
        if args.lng: pov_update["lng"] = args.lng

        count, updated_data = update_shop_pov(args.name, args.addr, pov_update, data)
        
        if count > 0:
            save_data(updated_data)
            print(f"Successfully updated {count} records for '{args.name}' at '{args.addr}'.")
        else:
            print(f"No records found matching Name='{args.name}' and Addr='{args.addr}'.")

    elif args.command == "list_missing":
        data = load_data()
        groups = group_by_shop(data)
        
        missing = []
        for key, items in groups.items():
            name, addr = key
            # Skip online
            if "동행복권" in name or "인터넷" in name: continue
            
            if len(items) >= args.min_wins:
                has_pov = any(i.get('pov') for i in items)
                if not has_pov:
                    missing.append((name, addr, len(items)))
        
        missing.sort(key=lambda x: x[2], reverse=True)
        print(f"Offline Shops with {args.min_wins}+ wins missing POV:")
        for m in missing:
            print(f"- {m[0]} ({m[2]} wins): {m[1]}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
