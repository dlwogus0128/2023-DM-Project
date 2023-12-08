import scrapy

from patent.items import PatentItem

from urllib import parse
import json

class PatentItemSpider(scrapy.Spider):
    name = 'patent'
    custom_settings ={
        'ITEM_PIPELINES':{
            'patent.pipelines.PatentPipeline':300
        }
    }

    def start_requests(self):
        target_patent_list=["AD=[20000101~20231129]"]
        datalist=[]
        base_url = "http://kpat.kipris.or.kr/kpat/resulta.do"
        request_headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; \
                           Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
                        'Referer':'http://kpat.kipris.or.kr/kpat/searchLogina.do?next=MainSearch',
                        'Origin':'http://kpat.kipris.or.kr'}
        request_type = "POST"
        for keyword in target_patent_list:
            # encoded_keyword = parse.quote(keyword.encode('utf-8'))
            encoded_keyword = keyword
            for i in range(1,500):
                request_body_dict=dict()
                # request_body_dict['remoconExpression']=''
                # request_body_dict['remoconDocsFound']=''
                # request_body_dict['remoconSelectedArticles']=''
                request_body_dict['queryText']= encoded_keyword
                # request_body_dict['searchInResultCk']=''
                # request_body_dict['next']='Mainlist'
                # request_body_dict['passwd']=''
                # request_body_dict['userId']=''
                request_body_dict['config']='G1111111111111111111111S111111111000000000'
                request_body_dict['sortField']='RANK'
                request_body_dict['sortState']='DESC'
                request_body_dict['sortField1']='AD'
                request_body_dict['sortState1']='DESC'
                # request_body_dict['sortField2']=''
                # request_body_dict['sortState2']=''
                request_body_dict['configChange']='Y'
                request_body_dict['expression']= encoded_keyword
                # request_body_dict['historyQuery']= encoded_keyword
                request_body_dict['numPerPage']=str(1000)
                request_body_dict['numPageLinks']=str(500)
                request_body_dict['currentPage']=str(i)
                # request_body_dict['FROM']=''
                # request_body_dict['BOOKMARK']=''
                # request_body_dict['NWBOOKMARK']=''
                # request_body_dict['REBOOKMARK']=''
                # request_body_dict['natlCD']=''
                request_body_dict['beforeExpression']=''
                request_body_dict['prefixExpression']=''
                # request_body_dict['userInput']=''
                # request_body_dict['searchKeyword']=''
                # request_body_dict['searchInTrans']='N'
                # request_body_dict['searchInResult']=''
                # request_body_dict['logFlag']='Y'
                # request_body_dict['searchSaveCnt']='0'
                # request_body_dict['piField']=''
                # request_body_dict['piValue']=''
                request_body_dict['piSearchYN']='N'
                # request_body_dict['leftGubnChk']=''
                # request_body_dict['leftHangjungChk']=''
                request_body_dict['SEL_PAT']='KPAT'
                # request_body_dict['merchandiseString']=''
                # request_body_dict['measureString']=''
                # request_body_dict['patternString']=''
                # request_body_dict['collectionValues']=''
                # request_body_dict['selectedLang']=''
                # request_body_dict['lang']=''
                request_body_dict['strstat']='TOP%7CKW'
                # request_body_dict['highlightKeyword']=''
                request_body_dict['searchInTransCk']='undefined'
                # url_params = "?"+"&".join(f'{key}={value}'for key, value in request_body_dict.items())
                datalist.append((keyword,request_body_dict))
                print(request_body_dict)
        return [scrapy.FormRequest(url=base_url,headers=request_headers ,callback=self.parse,method='POST',formdata=data,cb_kwargs=dict(keyword=keyword)) for keyword,data in datalist]

    def parse(self, response,keyword):
        patent_item = PatentItem()
        response_content = response.body.decode('utf-8')
        selector = scrapy.Selector(text=response_content)

        patent_item['patent_search_cat']=keyword
        search_section_title_list_selector=selector.css("div.search_section_title")
        patent_list=[]
        search_basic_info_list_selector=selector.css("div.search_basic_info")
        for index, section in enumerate(search_section_title_list_selector):
            patent=dict()
            patent['patent_name']=section.css("input").attrib['title']
            mainsearch_info_list = search_basic_info_list_selector[index].css("ul").css("li")
            
            ipc_section = mainsearch_info_list[0].css("span.point01")
            ipc_list=[]
            for ipc_item in ipc_section:
                text_data = ipc_item.css("a::text").get()
                ipc_list.append(text_data)
            patent['ipc']=ipc_list
            temp_application_info = mainsearch_info_list[1].css("a::text").get().split(" ")
            patent['application_number']=temp_application_info[0]
            patent['application_date']=temp_application_info[1]
            patent['applicant']=mainsearch_info_list[2].css("font::text").get()

            patent_list.append(patent)
        
        patent_item['patents']=patent_list
        # patent_item['patents']=response_content
        return patent_item