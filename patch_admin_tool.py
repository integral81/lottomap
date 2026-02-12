
import json
import re

def update_admin_tool():
    try:
        with open('top_shops_4wins.json', 'r', encoding='utf-8') as f:
            shops_data = json.load(f)
        
        with open('admin_roadview.html', 'r', encoding='utf-8') as f:
            html = f.read()
    except Exception as e:
        print(f"Error: {e}")
        return

    # Create the JS block with embedded data
    embedded_data = json.dumps(shops_data, ensure_ascii=False)
    
    js_code = f"""
        let roadview, rvClient;
        let shops = {embedded_data};
        let currentShop = null;
        let currentBatch = 0;
        const BATCH_SIZE = 10;

        window.onload = async () => {{
            const rvContainer = document.getElementById('roadview');
            roadview = new kakao.maps.Roadview(rvContainer);
            rvClient = new kakao.maps.RoadviewClient();
            renderBatch();
            document.getElementById('loading').style.display = 'none';
        }};

        function changeBatch(delta) {{
            const maxBatch = Math.floor((shops.length - 1) / BATCH_SIZE);
            currentBatch += delta;
            if (currentBatch < 0) currentBatch = 0;
            if (currentBatch > maxBatch) currentBatch = maxBatch;
            renderBatch();
        }}

        function renderBatch() {{
            const start = currentBatch * BATCH_SIZE;
            const end = Math.min(start + BATCH_SIZE, shops.length);
            const batchShops = shops.slice(start, end);
            
            document.getElementById('batch-info').textContent = (start + 1) + " - " + end + " / " + shops.length;
            renderList(batchShops);
        }}
    """

    # Update logic and cleanup formatting
    # Target the script section - from the first "let roadview" to the end of window.onload
    # Based on previous view_file, it looks like:
    # let roadview, rvClient;
    # ...
    # window.onload = async () => { ... };
    
    # We'll replace the entire block more safely
    pattern = r'let roadview, rvClient;.*?}\s*;\s*\n'
    # Actually, let's use a simpler marker if possible, but the view showed that structure.
    
    # Let's try replacing from the first let roadview... to the start of renderList
    pattern = r'let roadview, rvClient;.*?function renderList\(list\)'
    replacement = js_code + "\n\n        function renderList(list)"
    
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open('admin_roadview.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"Successfully embedded {len(shops_data)} entries with batching logic.")

if __name__ == "__main__":
    update_admin_tool()
