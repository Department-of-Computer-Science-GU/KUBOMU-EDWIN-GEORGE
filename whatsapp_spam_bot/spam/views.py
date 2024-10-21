from django.shortcuts import render
from django.http import HttpResponse
from .forms import MessageForm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# Path to your chromedriver executable
driver_path = 'C:/WebDriver/chromedriver.exe'  # Ensure this is the correct path

def send_message(contact_name, message, num_messages):
    try:
        chrome_service = Service(executable_path=driver_path)
        chrome_options = Options()
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get("https://web.whatsapp.com")

        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'))
        )

        search_box = driver.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p')
        search_box.click()
        search_box.send_keys(contact_name)
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
        )
        
        for _ in range(num_messages):
            message_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
            )
            
            message_box.clear()
            message_box.send_keys(message)
            message_box.send_keys(Keys.RETURN)
            print(f"Message sent at {datetime.datetime.now()}")
            time.sleep(5)

        driver.quit()
        return f"Sent {num_messages} messages successfully!"
    except Exception as e:
        return f"An error occurred: {e}"

def index(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            contact_name = form.cleaned_data['contact_name']
            message = form.cleaned_data['message']
            num_messages = form.cleaned_data['num_messages']
            result = send_message(contact_name, message, num_messages)
            return HttpResponse(result)
    else:
        form = MessageForm()

    return render(request, 'spam/index.html', {'form': form})
