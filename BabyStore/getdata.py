import csv
from bs4 import BeautifulSoup
import requests
import re
from tkinter import W

list_ten_sp = []
list_chi_tiet_sp = []
list_ten_hinh = []
list_gia = []

# for i in range(1,5):
page_link = "https://bibomart.com.vn/be-mac.html"
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.content, 'html.parser')


#Tên sản phẩm
ds_ten_sp = page_content.find_all('a', attrs={'class': 'product-item-link'})
for ten_sp in ds_ten_sp:
    list_ten_sp.append(ten_sp.text.strip('\n').strip())

    page_link_chi_tiet_sp = ten_sp['href']
    page_response_chi_tiet_sp = requests.get(page_link_chi_tiet_sp)
    page_content_chi_tiet_sp = BeautifulSoup(page_response_chi_tiet_sp.content, 'html.parser')
    content_chi_tiet_sp = page_content_chi_tiet_sp.find_all('div', attrs={'class': 'product attribute description'})
    list_chi_tiet_sp.append(content_chi_tiet_sp)


#Tên hình 
ds_ten_hinh = page_content.find_all('img', attrs={'class': 'product-image-photo'})
for ten_hinh in ds_ten_hinh:
    # print(ten_hinh)
    list_ten_hinh.append(ten_hinh['src'].split('/')[-1])





ds_gia = page_content.find_all('span', attrs={'class': 'price-wrapper'})
for gia in ds_gia:
    list_gia.append(gia['data-price-amount'])



#Download hình ảnh
img_tags = page_content.find_all('img', attrs={'class': 'product-image-photo'})
urls = [img['src'] for img in img_tags]
for url in urls:
    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)    
    if filename:
        with open("media/store/images" + filename.group(0), 'wb') as f:        
            if 'http' not in url:                
                url = '{}'.format(url)           
                print(url)   
            response = requests.get(url)
            f.write(response.content)


#Lưu vào file csv 
dict_products = {
    'product_name': list_ten_sp,
    'image': list_ten_hinh,
    'price': list_gia,
    'description': list_chi_tiet_sp
}
with open('BabyStore/du_lieu/bibo-baby-clothes.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(dict_products.keys())
    writer.writerows(zip(*dict_products.values()))