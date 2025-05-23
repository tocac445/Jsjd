import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import os
from telegraph import Telegraph, upload_file
from datetime import datetime
import time
import requests

from save_user_data import save_user_performance, save_user_performance_l4,save_user_performance_daily, save_user_performance_l4_daily

def load_data(user_id, key):
  try:
      with open(f"{user_id}_data.json", 'r') as file:
          data = json.load(file)
          return data.get(key)
  except (FileNotFoundError, json.JSONDecodeError):
      return None
group_id = -1002222382775

async def send_pre_graph_to_user(update, context, chat_id, user_id, server_name, summary_message, nation, asn, source, allowed):
    from_user = update.callback_query.from_user
    full_name = from_user.full_name or "Unknown"
    user_name = from_user.username or "unknown"
    uid = from_user.id

    # Lấy ảnh đại diện của người dùng (nếu có)
    try:
        photos = await context.bot.get_user_profile_photos(uid, limit=1)
        if photos.total_count > 0:
            avatar_file = await context.bot.get_file(photos.photos[0][0].file_id)
            avatar = avatar_file.file_path
        else:
            avatar = "https://i.ibb.co/6RVR24Zp/telegram.png"
    except Exception as e:
        print(f"Error fetching user photo: {e}")
        avatar = "https://i.ibb.co/6RVR24Zp/telegram.png"

    try:
        def format_list_as_str(data_list):
            return "[" + ",".join(data_list) + "]"

        base_url = "https://skibiditoilet23432.github.io/gy/haha.html"
        query_params = {
            "sv": str(server_name),
            "date": datetime.now(timezone.utc).strftime("%d/%m/%Y"),
            "ovr": format_list_as_str(source),
            "nation": format_list_as_str(nation),
            "asn": format_list_as_str(asn),
            "username": full_name,
            "handle": user_name,
            "uid": str(uid),
            "avatar": avatar
        }

        full_url = base_url + "?" + urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1024x900")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--incognito")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_window_size(1024, 900)
        driver.get(full_url)

        time.sleep(5)  # đợi biểu đồ và DOM load

        driver.execute_script("document.body.style.overflow = 'hidden';")

        img_path = f"{uid}_graphclfpre.png"
        driver.get_screenshot_as_file(img_path)
        driver.quit()

        with open(img_path, 'rb') as photo:
            await context.bot.send_photo(chat_id=chat_id, photo=photo)
        await context.bot.send_message(chat_id=chat_id, text=summary_message, parse_mode='HTML')

        os.remove(img_path)

    except Exception as e:
        print(f"Error generating or sending graph to user: {e}")
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Error sending graph.")
        await context.bot.send_message(chat_id=5145402317, text=f"Error sending graph\n{e}")
async def send_graph_custom_to_user(update, context, chat_id, user_id, server_name,
  summary_message, max_difference, total_difference,bypassed_list, blocked_list):
  user_id = update.callback_query.from_user.id
  chat_id = update.callback_query.message.chat_id
  full_name = update.callback_query.from_user.full_name
  user_name = update.callback_query.from_user.username

  try:
      base_url = "https://connguoihaha.github.io/V2/"
      query_params = {
          "data": str(bypassed_list),
          "blocked": str(blocked_list)
      }
      encoded_query_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
      full_url = base_url + "?" + encoded_query_params

      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("window-size=1024x768")  
      chrome_options.add_argument("--no-sandbox")
      chrome_options.add_argument("--disable-dev-shm-usage") 
      chrome_options.add_argument("--disable-gpu")
      chrome_options.add_argument("--disable-extensions")
      chrome_options.add_argument("--disable-infobars")
      chrome_options.add_argument("--disable-blink-features=AutomationControlled")
      chrome_options.add_argument("--log-level=3")  
      chrome_options.add_argument("--single-process") 
      chrome_options.add_argument("--incognito")

      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

      driver.set_window_size(1024, 768)

      driver.get(full_url)

      driver.execute_script("document.body.style.overflow = 'hidden';")
      driver.implicitly_wait(2)

      img_path = f"{user_id}_graph.png"
      driver.get_screenshot_as_file(img_path)

      driver.close()


      await context.bot.send_photo(chat_id=chat_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')

      group_message = await context.bot.send_photo(chat_id=group_id,photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')
      group_message_link = f"https://t.me/{group_message.chat.username}/{group_message.message_id}"      

      save_user_performance(user_name, full_name, max_difference, total_difference, server_name,group_message_link)
      save_user_performance_daily(user_name, full_name, max_difference, total_difference, server_name,group_message_link)

  except Exception as e:
      print(f"Error generating or sending graph to user: {e}")
      await context.bot.send_message(chat_id=4543535352656565626, text="Error sending graph")
      await context.bot.send_message(chat_id=514540231646547, text=f"Error sending graph\n{e}")

async def send_graph_to_user(update, context, chat_id, user_id, server_name, summary_message):
    log_file = f"{user_id}_logs.json"
    user_id = update.callback_query.from_user.id
    chat_id = update.callback_query.message.chat_id
    full_name = update.callback_query.from_user.full_name
    user_name = update.callback_query.from_user.username or f"tg://user?id={user_id}"
    differences = load_data(user_id, 'differences') or []
    max_difference = max(differences) if differences else 0
    total_difference = sum(differences)

    try:
        # Ð?c file log
        with open(log_file, 'r') as file:
            logs = json.load(file)
            rps_list = [log['rps'] for log in logs]

        # T?o URL v?i query params
        base_url = "https://skibiditoilet23432.github.io/gy/gay"  # Ð?m b?o URL chính xác
        avatar_url = f"https://t.me/i/userpic/320/{user_id}.jpg"
        peak_requests = max(rps_list)
        total_requests = sum(rps_list)
        query_params = {
            "user": user_name,
            "uid": str(user_id),
            "avatar": avatar_url,
            "data": json.dumps(rps_list),
            "peak": peak_requests,
            "total": total_requests
        }
        encoded_query = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
        full_url = f"{base_url}?{encoded_query}"

        # Thi?t l?p Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--single-process")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1280,800")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(full_url)
        driver.execute_script("document.body.style.overflow = 'hidden';")
        time.sleep(2)

        img_path = f"{user_id}_graph.png"
        driver.save_screenshot(img_path)
        driver.quit()

        # G?i ?nh cho ngu?i dùng
        await context.bot.send_photo(chat_id=chat_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')

        # G?i ?nh d?n nhóm
        group_message = await context.bot.send_photo(chat_id=group_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')
        group_message_link = f"https://t.me/{group_message.chat.username}/{group_message.message_id}"

        # Luu hi?u su?t ngu?i dùng
        save_user_performance(user_name, full_name, max_difference, total_difference, server_name, group_message_link)
        save_user_performance_daily(user_name, full_name, max_difference, total_difference, server_name, group_message_link)

        os.remove(img_path)

    except Exception as e:
        print(f"Error generating or sending graph to user: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Error graph.")
        await context.bot.send_message(chat_id=5145402317, text=f"[ERROR] send_graph_to_user\n{e}")

async def send_graphl4_to_user(update, context, chat_id, user_id, server_name, summary_message):
  log_file = f"{user_id}_data_l4.json"
  user_id = update.callback_query.from_user.id
  chat_id = update.callback_query.message.chat_id
  try:
      with open(log_file, 'r') as file:
          logs = json.load(file)
          net_received_logs = logs['net_received']
          rps_list = [log['api_value'] for log in net_received_logs]
          pps_list = [log['packet_value'] for log in net_received_logs]


      base_url = "https://skibiditoilet23432.github.io/gy/"
      query_params = {
          "data": str(rps_list),
          "pps": str(pps_list)
      }
      encoded_query_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
      full_url = base_url + "?" + encoded_query_params

      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("window-size=1024x768")  
      chrome_options.add_argument("--no-sandbox")
      chrome_options.add_argument("--disable-dev-shm-usage") 
      chrome_options.add_argument("--disable-gpu")
      chrome_options.add_argument("--disable-extensions")
      chrome_options.add_argument("--disable-infobars")
      chrome_options.add_argument("--disable-blink-features=AutomationControlled")
      chrome_options.add_argument("--log-level=3")  
      chrome_options.add_argument("--single-process") 
      chrome_options.add_argument("--incognito")
      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

      driver.set_window_size(1024, 768)

      driver.get(full_url)

      # ?n thanh cu?n b?ng JavaScript
      driver.execute_script("document.body.style.overflow = 'hidden';")
      driver.implicitly_wait(2)

      img_path = f"{user_id}_graph_l4.png"
      driver.get_screenshot_as_file(img_path)

      driver.close()

      try:
          with open(f"{user_id}_data_l4.json", 'r') as file:
              data = json.load(file)
              net_received = [entry['api_value'] for entry in data['net_received']]
              packet_received = [entry['packet_value'] for entry in data['net_received']]
      except (FileNotFoundError, KeyError):
          net_received = []
          packet_received = []

      if net_received and packet_received:
          max_received = max(net_received)
          total_received = sum(net_received)
          average_received = round(total_received / len(net_received), 2) if net_received else 0

          max_packet = max(packet_received)
          total_packet = sum(packet_received)
          average_packet = round(total_packet / len(packet_received), 2) if packet_received else 0
          user_name = update.callback_query.from_user.username
          full_name = update.callback_query.from_user.full_name

          await context.bot.send_photo(chat_id=chat_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')

          group_message = await context.bot.send_photo(chat_id=group_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')
          group_message_link = f"https://t.me/{group_message.chat.username}/{group_message.message_id}"

          save_user_performance_l4(user_name, full_name, max_received, total_received, max_packet, total_packet, server_name, group_message_link)
          save_user_performance_l4_daily(user_name, full_name, max_received, total_received, max_packet, total_packet, server_name, group_message_link)
      
      
  except Exception as e:
      print(f"Error generating or sending graph to user: {e}")
      await context.bot.send_message(chat_id=chat_id, text="Error sending graph")
      await context.bot.send_message(chat_id=5145402317, text=f"Error sending graph\n{e}")


async def send_graph_aurologic_to_user(update, context, chat_id, user_id, server_name, summary_message, gb_list,pps_list):
  try:
      base_url = "https://skibiditoilet23432.github.io/gy/"
      query_params = {
          "data": str(gb_list),
          "pps": str(pps_list)
      }
      encoded_query_params = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
      full_url = base_url + "?" + encoded_query_params

      

      chrome_options = Options()
      chrome_options.add_argument("--headless")
      chrome_options.add_argument("window-size=1024x768")  
      chrome_options.add_argument("--no-sandbox")
      chrome_options.add_argument("--disable-dev-shm-usage") 
      chrome_options.add_argument("--disable-gpu")
      chrome_options.add_argument("--disable-extensions")
      chrome_options.add_argument("--disable-infobars")
      chrome_options.add_argument("--disable-blink-features=AutomationControlled")
      chrome_options.add_argument("--log-level=3")  
      chrome_options.add_argument("--single-process") 
      chrome_options.add_argument("--incognito")
      driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

      driver.set_window_size(1024, 768)

      driver.get(full_url)

      # ?n thanh cu?n b?ng JavaScript
      driver.execute_script("document.body.style.overflow = 'hidden';")
      driver.implicitly_wait(2)

      img_path = f"{user_id}_graph_l4.png"
      driver.get_screenshot_as_file(img_path)

      driver.close()
          
      user_name = update.callback_query.from_user.username
      full_name = update.callback_query.from_user.full_name

      await context.bot.send_photo(chat_id=chat_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')

      group_message = await context.bot.send_photo(chat_id=group_id, photo=open(img_path, 'rb'), caption=summary_message, parse_mode='HTML')
      group_message_link = f"https://t.me/{group_message.chat.username}/{group_message.message_id}"

      peak_gb = max(gb_list)
      peak_pps = max(pps_list)

      save_user_performance_l4(user_name, full_name, peak_gb, peak_gb, peak_pps, peak_pps, "Aurologic-3TB", group_message_link)
      save_user_performance_l4_daily(user_name, full_name, peak_gb, peak_gb, peak_pps, peak_pps, "Aurologic-3TB", group_message_link)
  except Exception as e:
          print(f"Error generating or sending graph to user: {e}")
          await context.bot.send_message(chat_id=chat_id, text="Error sending graph.")


