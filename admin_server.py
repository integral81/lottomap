import http.server
import socketserver
import json
import os
import io

PORT = 8000
DB_FILE = 'lotto_data.json'

class MobileAdminHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/update_pov':
            self.handle_update_pov()
        elif self.path == '/api/delete_shop':
            self.handle_delete_shop()
        elif self.path == '/api/hide_shop':
            self.handle_hide_shop()
        else:
            self.send_error(404)

    def handle_update_pov(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
            shop_name = payload.get('name')
            new_pov = payload.get('pov')
            
            print(f"[Mobile Admin] UPDATE: {shop_name}")
            
            self.update_database(shop_name, new_pov)
            
            self.send_json_response({"success": True, "message": f"Updated {shop_name}"})
            
        except Exception as e:
            print(f"[Error] {e}")
            self.send_json_response({"success": False, "message": str(e)}, 500)

    def handle_hide_shop(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
            shop_name = payload.get('name')
            
            print(f"[Mobile Admin] HIDE: {shop_name}")
            
            self.hide_in_database(shop_name)
            
            self.send_json_response({"success": True, "message": f"Hidden {shop_name}"})
            
        except Exception as e:
            print(f"[Error] {e}")
            self.send_json_response({"success": False, "message": str(e)}, 500)

    def handle_delete_shop(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            payload = json.loads(post_data.decode('utf-8'))
            shop_name = payload.get('name')
            
            print(f"[Mobile Admin] DELETE: {shop_name}")
            
            self.delete_from_database(shop_name)
            
            self.send_json_response({"success": True, "message": f"Deleted {shop_name}"})
            
        except Exception as e:
            print(f"[Error] {e}")
            self.send_json_response({"success": False, "message": str(e)}, 500)

    def update_database(self, name, pov):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for shop in data:
             if shop.get('n') == name:
                 shop['pov'] = pov
                 updated_count += 1
        
        if updated_count > 0:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            print(f"[DB] Updated POV for {name} ({updated_count} entries).")
            self.generate_js_file(data)
        else:
            raise Exception("Shop not found")

    def delete_from_database(self, name):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        original_len = len(data)
        data = [s for s in data if s.get('n') != name]
        new_len = len(data)
        
        if new_len < original_len:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            print(f"[DB] Deleted {name}. Count: {original_len} -> {new_len}")
            self.generate_js_file(data)
        else:
            raise Exception("Shop not found for deletion")

    def hide_in_database(self, name):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        updated_count = 0
        for shop in data:
             if shop.get('n') == name:
                 shop['hidden'] = True
                 updated_count += 1
        
        if updated_count > 0:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
            print(f"[DB] Hid {name} ({updated_count} entries).")
            self.generate_js_file(data)
        else:
            raise Exception("Shop not found")

    def generate_js_file(self, data):
        try:
            # 1. Update lotto_data.js
            js_content = f"const lottoData = {json.dumps(data, ensure_ascii=False)};"
            with open('lotto_data.js', 'w', encoding='utf-8') as f:
                f.write(js_content)
            print(f"[Sync] lotto_data.js updated with {len(data)} records.")
            
            # 2. Daily Rolling Backup (To catch mobile mishaps)
            import shutil
            import time
            timestamp = time.strftime("%Y%m%d_%H") # Hourly backup should suffice to limit file count
            backup_path = f"lotto_data_backup_mobile_{timestamp}.json"
            if not os.path.exists(backup_path):
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                print(f"[Backup] Saved to {backup_path}")
                
        except Exception as e:
            print(f"[Sync Error] Failed to update JS/Backup: {e}")

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*') 
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MobileAdminHandler) as httpd:
        print(f"[Mobile Admin Server] running at port {PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()

if __name__ == '__main__':
    run()
