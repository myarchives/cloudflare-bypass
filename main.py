def bypass_cloudflare(url_w):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    req=requests.Session()
    content=req.get(url_w,headers=headers)
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
    s=re.findall('<input type="hidden" name="s" value="(.*?)"></input>',content)
    jschl_vc=re.findall('<input type="hidden" name="jschl_vc" value="(.*?)"/>',content)
    passs=re.findall('<input type="hidden" name="pass" value="(.*?)"/>',content)
    ws=round(ws,10)+len(url_w.split('/')[-1])
    ws=round(ws,10)
    time.sleep(5)
    response=req.get(url_w+'/cdn-cgi/l/chk_jschl?s={0}&jschl_vc={1}&pass={2}&jschl_answer={3}'.format(s[0],jschl_vc[0],passs[0],ws),headers=headers,allow_redirects=False)
    cooki=req.cookies.get_dict()
    ck=''
    for i in cooki:
        ck+=i+'='+cooki[i]+';'
    print(ck[:-1])
    return ck[:-1],cooki

if __name__=='__main__':
    cookie=bypass_cloudflare('http://example.com')
