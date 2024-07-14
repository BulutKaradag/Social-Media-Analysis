from flask import Flask, render_template, request
import markdown
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import translators as ts
import requests

genai.configure(api_key='Gemini API Key')

app = Flask(__name__)

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def index():
    result1 = ""
    result2 = ""

    if request.method == 'POST':
        input_text = request.form['input_text']
        cService = webdriver.ChromeService(executable_path='chromedriver-win64\chromedriver.exe')
        driver = webdriver.Chrome(service = cService)

        # Logging into LinkedIn
        driver.get("https://linkedin.com/uas/login")
        time.sleep(5)
 
        username = driver.find_element(By.ID, "username")
        username.send_keys("bulutkaradag@yandex.com")  # Enter Your Email Address
 
        pword = driver.find_element(By.ID, "password")
        pword.send_keys("Bb321321")        # Enter Your Password
 
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
 
        # Opening Kunal's Profile
        # paste the URL of Kunal's profile here
        profile_url = "https://www.linkedin.com/in/" + input_text

        driver.get(profile_url)
 
        profile_name = driver.find_element(By.CSS_SELECTOR, "h1.text-heading-xlarge").get_attribute("innerText")
        profile_title = driver.find_element(By.CSS_SELECTOR, "div.text-body-medium").get_attribute("innerText")
        profile_location = driver.find_element(By.CSS_SELECTOR, "span.text-body-small.inline").get_attribute("innerText")
    
        person = "Profile Name: {}".format(profile_name)
        title = "Title: {}".format(profile_title)
        location = "Location: {}".format(profile_location)

        person_tr = person
        title_tr = ts.translate_text((title), to_language='tr')
        location_tr = ts.translate_text((location), to_language='tr')


        model = genai.GenerativeModel('gemini-pro')
        responseFirst = model.generate_content('Bilgiler:'  + person_tr + title_tr + location_tr + 'Elimde bir veri seti var. Bu veriyi Json olarak sana veriyorum. Bu verilerde mesleğe göre risk oranı bulunuyor. Bu verileri ve bir önceki adımdaki kişinin çalıştığı yer ve mesleğini kullanarak kredi alabilme durumunu yorumlayabilir misin? Json Veri Seti:{"Meslek":"Akademisyen/Ögretim Görevlisi","Az Riskli":"30.14%","Çok İyi":"34.04%","Çok Riskli":"1.06%","İyi":"33.33%","Orta Riskli":"1.42%"},{"Meslek":"Antikaci","Az Riskli":"0.00%","Çok İyi":"0.00%","Çok Riskli":"0.00%","İyi":"100.00%","Orta Riskli":"0.00%"},{"Meslek":"Asci","Az Riskli":"50.00%","Çok İyi":"7.14%","Çok Riskli":"11.43%","İyi":"21.43%","Orta Riskli":"10.00%"},{"Meslek":"Asker","Az Riskli":"44.17%","Çok İyi":"29.45%","Çok Riskli":"0.61%","İyi":"22.09%","Orta Riskli":"3.68%"},{"Meslek":"Avukat","Az Riskli":"36.98%","Çok İyi":"23.44%","Çok Riskli":"3.13%","İyi":"28.13%","Orta Riskli":"8.33%"},{"Meslek":"Bankaci","Az Riskli":"26.03%","Çok İyi":"32.96%","Çok Riskli":"1.40%","İyi":"37.92%","Orta Riskli":"1.69%"},{"Meslek":"Borsaci","Az Riskli":"16.67%","Çok İyi":"33.33%","Çok Riskli":"0.00%","İyi":"33.33%","Orta Riskli":"16.67%"},{"Meslek":"Çiftçi","Az Riskli":"42.59%","Çok İyi":"24.07%","Çok Riskli":"5.56%","İyi":"20.37%","Orta Riskli":"7.41%"},{"Meslek":"Danisman","Az Riskli":"31.92%","Çok İyi":"27.31%","Çok Riskli":"5.38%","İyi":"27.69%","Orta Riskli":"7.69%"},{"Meslek":"Denetçi","Az Riskli":"34.88%","Çok İyi":"32.56%","Çok Riskli":"0.00%","İyi":"27.91%","Orta Riskli":"4.65%"},{"Meslek":"Diger","Az Riskli":"20.00%","Çok İyi":"60.00%","Çok Riskli":"0.00%","İyi":"20.00%","Orta Riskli":"0.00%"},{"Meslek":"Din Görevlisi","Az Riskli":"36.31%","Çok İyi":"35.67%","Çok Riskli":"0.64%","İyi":"26.11%","Orta Riskli":"1.27%"},{"Meslek":"Diplomat/Bürokrat","Az Riskli":"20.00%","Çok İyi":"50.00%","Çok Riskli":"0.00%","İyi":"30.00%","Orta Riskli":"0.00%"},{"Meslek":"Dis Hekimi","Az Riskli":"34.15%","Çok İyi":"21.95%","Çok Riskli":"4.88%","İyi":"31.71%","Orta Riskli":"7.32%"},{"Meslek":"Doktor","Az Riskli":"28.48%","Çok İyi":"32.36%","Çok Riskli":"1.29%","İyi":"33.66%","Orta Riskli":"4.21%"},{"Meslek":"Eczaci","Az Riskli":"48.98%","Çok İyi":"26.53%","Çok Riskli":"0.00%","İyi":"20.41%","Orta Riskli":"4.08%"},{"Meslek":"Emlakçi","Az Riskli":"41.38%","Çok İyi":"17.24%","Çok Riskli":"10.34%","İyi":"24.14%","Orta Riskli":"6.90%"},{"Meslek":"Esnaf (Bakkal,Market,Berber, Kuaför)","Az Riskli":"38.47%","Çok İyi":"20.74%","Çok Riskli":"5.51%","İyi":"26.93%","Orta Riskli":"8.35%"},{"Meslek":"Ev Hanimi","Az Riskli":"37.35%","Çok İyi":"5.84%","Çok Riskli":"32.30%","İyi":"17.90%","Orta Riskli":"6.61%"},{"Meslek":"Galerici","Az Riskli":"38.10%","Çok İyi":"28.57%","Çok Riskli":"4.76%","İyi":"28.57%","Orta Riskli":"0.00%"},{"Meslek":"Gazeteci","Az Riskli":"39.13%","Çok İyi":"34.78%","Çok Riskli":"0.00%","İyi":"21.74%","Orta Riskli":"4.35%"},{"Meslek":"Güvenlik Görevlisi","Az Riskli":"34.76%","Çok İyi":"24.06%","Çok Riskli":"3.74%","İyi":"32.62%","Orta Riskli":"4.81%"},{"Meslek":"Hakim/Savci","Az Riskli":"33.72%","Çok İyi":"32.56%","Çok Riskli":"1.16%","İyi":"30.23%","Orta Riskli":"2.33%"},{"Meslek":"Hemsire","Az Riskli":"30.69%","Çok İyi":"24.87%","Çok Riskli":"3.17%","İyi":"37.57%","Orta Riskli":"3.70%"},{"Meslek":"Hizmetli (Garson,Servis Elemani,Temizlik Görevlisi)","Az Riskli":"36.84%","Çok İyi":"7.02%","Çok Riskli":"14.04%","İyi":"29.82%","Orta Riskli":"12.28%"},{"Meslek":"Host/Hostes","Az Riskli":"22.22%","Çok İyi":"22.22%","Çok Riskli":"0.00%","İyi":"44.44%","Orta Riskli":"11.11%"},{"Meslek":"Isçi","Az Riskli":"39.29%","Çok İyi":"18.52%","Çok Riskli":"8.43%","İyi":"24.17%","Orta Riskli":"9.59%"},{"Meslek":"Isletmeci/Sanayici","Az Riskli":"36.42%","Çok İyi":"25.87%","Çok Riskli":"3.58%","İyi":"27.25%","Orta Riskli":"6.88%"},{"Meslek":"Kaptan","Az Riskli":"50.00%","Çok İyi":"35.00%","Çok Riskli":"0.00%","İyi":"10.00%","Orta Riskli":"5.00%"},{"Meslek":"Kimyager/Laborant","Az Riskli":"34.78%","Çok İyi":"26.09%","Çok Riskli":"0.00%","İyi":"39.13%","Orta Riskli":"0.00%"},{"Meslek":"Komisyoncu","Az Riskli":"0.00%","Çok İyi":"0.00%","Çok Riskli":"0.00%","İyi":"50.00%","Orta Riskli":"50.00%"},{"Meslek":"Kurye","Az Riskli":"33.33%","Çok İyi":"16.67%","Çok Riskli":"33.33%","İyi":"0.00%","Orta Riskli":"16.67%"},{"Meslek":"Kuyumcu","Az Riskli":"46.15%","Çok İyi":"23.08%","Çok Riskli":"7.69%","İyi":"23.08%","Orta Riskli":"0.00%"},{"Meslek":"Mali Müsavir","Az Riskli":"30.26%","Çok İyi":"32.31%","Çok Riskli":"2.05%","İyi":"31.28%","Orta Riskli":"4.10%"},{"Meslek":"Memur","Az Riskli":"28.74%","Çok İyi":"35.86%","Çok Riskli":"1.60%","İyi":"31.05%","Orta Riskli":"2.76%"},{"Meslek":"Milletvekili","Az Riskli":"50.00%","Çok İyi":"10.00%","Çok Riskli":"0.00%","İyi":"20.00%","Orta Riskli":"20.00%"},{"Meslek":"Mimar","Az Riskli":"47.62%","Çok İyi":"12.70%","Çok Riskli":"4.76%","İyi":"30.16%","Orta Riskli":"4.76%"},{"Meslek":"Muhasebeci","Az Riskli":"33.46%","Çok İyi":"26.77%","Çok Riskli":"5.93%","İyi":"27.53%","Orta Riskli":"6.31%"},{"Meslek":"Mühendis","Az Riskli":"32.40%","Çok İyi":"29.61%","Çok Riskli":"1.94%","İyi":"32.89%","Orta Riskli":"3.16%"},{"Meslek":"Müstesar","Az Riskli":"0.00%","Çok İyi":"100.00%","Çok Riskli":"0.00%","İyi":"0.00%","Orta Riskli":"0.00%"},{"Meslek":"Müteahhit","Az Riskli":"27.78%","Çok İyi":"29.17%","Çok Riskli":"2.78%","İyi":"34.72%","Orta Riskli":"5.56%"},{"Meslek":"Nakliyeci","Az Riskli":"45.45%","Çok İyi":"45.45%","Çok Riskli":"0.00%","İyi":"9.09%","Orta Riskli":"0.00%"},{"Meslek":"Noter","Az Riskli":"28.57%","Çok İyi":"57.14%","Çok Riskli":"0.00%","İyi":"14.29%","Orta Riskli":"0.00%"},{"Meslek":"Ögrenci","Az Riskli":"50.00%","Çok İyi":"5.88%","Çok Riskli":"23.53%","İyi":"5.88%","Orta Riskli":"14.71%"},{"Meslek":"Ögretmen","Az Riskli":"32.09%","Çok İyi":"31.94%","Çok Riskli":"1.83%","İyi":"32.24%","Orta Riskli":"1.91%"},{"Meslek":"Pazarlamaci/Satis Elemani","Az Riskli":"38.36%","Çok İyi":"22.37%","Çok Riskli":"5.02%","İyi":"29.68%","Orta Riskli":"4.57%"},{"Meslek":"Pilot","Az Riskli":"46.15%","Çok İyi":"23.08%","Çok Riskli":"7.69%","İyi":"23.08%","Orta Riskli":"0.00%"},{"Meslek":"Polis","Az Riskli":"28.19%","Çok İyi":"32.66%","Çok Riskli":"0.89%","İyi":"36.24%","Orta Riskli":"2.01%"},{"Meslek":"Psikolog","Az Riskli":"35.71%","Çok İyi":"35.71%","Çok Riskli":"14.29%","İyi":"14.29%","Orta Riskli":"0.00%"},{"Meslek":"Reklam ve Halkla Iliskiler","Az Riskli":"40.30%","Çok İyi":"19.40%","Çok Riskli":"4.48%","İyi":"29.85%","Orta Riskli":"5.97%"},{"Meslek":"Sanatçi","Az Riskli":"33.33%","Çok İyi":"0.00%","Çok Riskli":"33.33%","İyi":"33.33%","Orta Riskli":"0.00%"},{"Meslek":"Sekreter","Az Riskli":"39.13%","Çok İyi":"13.04%","Çok Riskli":"8.70%","İyi":"26.09%","Orta Riskli":"13.04%"},{"Meslek":"Sigortaci","Az Riskli":"46.94%","Çok İyi":"32.65%","Çok Riskli":"0.00%","İyi":"12.24%","Orta Riskli":"8.16%"},{"Meslek":"Soför","Az Riskli":"37.10%","Çok İyi":"20.16%","Çok Riskli":"7.26%","İyi":"24.19%","Orta Riskli":"11.29%"},{"Meslek":"Sporcu","Az Riskli":"41.67%","Çok İyi":"41.67%","Çok Riskli":"0.00%","İyi":"16.67%","Orta Riskli":"0.00%"},{"Meslek":"Tarim Isçisi","Az Riskli":"25.00%","Çok İyi":"50.00%","Çok Riskli":"0.00%","İyi":"0.00%","Orta Riskli":"25.00%"},{"Meslek":"Teknisyen","Az Riskli":"36.09%","Çok İyi":"23.31%","Çok Riskli":"3.51%","İyi":"32.08%","Orta Riskli":"5.01%"},{"Meslek":"Tercüman/Rehber","Az Riskli":"50.00%","Çok İyi":"0.00%","Çok Riskli":"16.67%","İyi":"16.67%","Orta Riskli":"16.67%"},{"Meslek":"Terzi/Modaci","Az Riskli":"23.08%","Çok İyi":"38.46%","Çok Riskli":"15.38%","İyi":"23.08%","Orta Riskli":"0.00%"},{"Meslek":"Tibbi Mümessil","Az Riskli":"25.00%","Çok İyi":"31.25%","Çok Riskli":"6.25%","İyi":"37.50%","Orta Riskli":"0.00%"},{"Meslek":"Usta (Boyaci,Marangoz,Elektrikçi,Tesisatçi)","Az Riskli":"57.69%","Çok İyi":"3.85%","Çok Riskli":"0.00%","İyi":"30.77%","Orta Riskli":"7.69%"},{"Meslek":"Veteriner","Az Riskli":"28.57%","Çok İyi":"38.10%","Çok Riskli":"0.00%","İyi":"28.57%","Orta Riskli":"4.76%"}')
        return render_template('index.html', result1=markdown.markdown(responseFirst.text), resultperson=markdown.markdown(person_tr),resulttitle=markdown.markdown(title_tr),resultlocation=markdown.markdown(location_tr))

if __name__ == '__main__':
    app.run(debug=True)
