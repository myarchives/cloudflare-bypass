import js2py,requests,re

def bypass_cloudflare(baseurl):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36','Host':'kcddos.com','Referer': baseurl}
    req=requests.Session()
    content=req.get(baseurl,headers=headers)
    cookiess=content.headers['Set-Cookie']
    content=content.text
    w=re.findall('a\.value = \+(.*?) \+ t\.length; ',content)
    data=w[0].split('.')
    ws=re.findall(data[0]+'={"'+data[1]+'":(.*?)};',content)
    we=re.findall(data[0]+'\.'+data[1]+'(.*?);',content)
    ws=js2py.eval_js(ws[0])
    for i in we[:-1]:
        if i[:2]=='*=':
            ws*=js2py.eval_js(i[2:])

        elif i[:2]=='-=':
            ws-=js2py.eval_js(i[2:])
        elif i[:2]=='+=':
            ws+=js2py.eval_js(i[2:])
        else:
            ws/=js2py.eval_js(i[2:])

    url=re.findall('<form id="challenge-form" action="(.*?)" method="get">',content)
    url=baseurl+url[0]
    s=re.findall('<input type="hidden" name="s" value="(.*?)"></input>',content)
    jschl_vc=re.findall('<input type="hidden" name="jschl_vc" value="(.*?)"/>',content)
    passs=re.findall('<input type="hidden" name="pass" value="(.*?)"/>',content)
    ws=round(ws,10)+len('kcddos.com')
    ws=round(ws,10)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36','Host':'kcddos.com','Referer': 'http://kcddos.com/','Upgrade-Insecure-Requests': '1','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8' ,'Accept-Encoding': 'gzip, deflate','Accept-Language': 'zh-CN,zh;q=0.9' ,'Connection': 'keep-alive','Cookie':cookiess}    time.sleep(5)
    response=req.get(baseurl+'/cdn-cgi/l/chk_jschl?s={0}&jschl_vc={1}&pass={2}&jschl_answer={3}'.format(s[0],jschl_vc[0],passs[0],ws),headers=headers,allow_redirects=False)
    cooki=req.cookies.get_dict()
    ck=''
    for i in cooki:
        ck+=i+'='+cooki[i]+';'
    print(ck[:-1])
    return ck[:-1],cooki
