import csv
from bs4 import BeautifulSoup
import requests
import re
from tkinter import W

list_ten_post = []
list_chi_tiet_post = []
list_ten_hinh = []

# for i in range(1,5):
page_link = "https://www.kidsplaza.vn/blog/"
page_repostonse = requests.get(page_link)
page_content = BeautifulSoup(page_repostonse.content, 'html.parser')


#Tên bài viết

ds_ten_post = page_content.find_all('h3', attrs={'class': 'entry-title td-module-title'})

for ten_post in ds_ten_post:

    list_ten_post.append(ten_post.text.strip())

    page_link_chi_tiet_post = ten_post.a['href']
    page_repostonse_chi_tiet_post = requests.get(page_link_chi_tiet_post)
    page_content_chi_tiet_post = BeautifulSoup(page_repostonse_chi_tiet_post.content, 'html.parser')
    content_chi_tiet_post = page_content_chi_tiet_post.find_all('div', attrs={'class': 'td-ss-main-content'})
    # print(content_chi_tiet_post)
    list_chi_tiet_post.append(content_chi_tiet_post)
# else:
#     print(list_ten_post)



#Tên hình 


ds_ten_hinh = page_content.find_all('div', attrs={'class': 'td-module-image'})
for hinh in ds_ten_hinh:
    list_ten_hinh.append(hinh.img['data-img-url'].split('/')[-1])



    #Down hình ảnh
    # img_tags = page_content.find_all('div', attrs={'class': 'td-module-image'})
    # urls = [img['data-img-url'] for img in img_tags]
    # for url in urls:
    #     filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)    
    #     if filename:
    #         with open("images" + filename.group(0), 'wb') as f:        
    #             if 'http' not in url:                
    #                 url = '{}'.format(url)           
    #                 print(url)   
    #             repostonse = requests.get(url)
    #             f.write(repostonse.content)


# # Kiếm tra số lượng của các giá trị chỉ định
# print(len(list_ten_hinh), len(list_gia), len(list_ten_post), len(list_chi_tiet_post))

#Lưu vào file csv 
dict_products = {
    'product_name': list_ten_post,
    'image': list_ten_hinh,
    'description': list_chi_tiet_post
}
with open('BabyStore/du_lieu/blog/post.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(dict_products.keys())
    writer.writerows(zip(*dict_products.values()))