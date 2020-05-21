from django.shortcuts import render
from datetime import datetime
from .summarization import crawl_news as cn
from .summarization import lda_topic_model as ltm
from .summarization import drawable_summary as ds
# from .summarization import word_cloud

# HttpResponse Error 
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden, HttpResponseBadRequest

def page_not_found(request, *args, **kwargs):
    return HttpResponseNotFound(render_to_string('404.html', request=request))

def forbidden(request, *args, **kwargs):
    return HttpResponseForbidden(render_to_string('403.html', request=request))

def server_error(request, *args, **kwargs):
    return HttpResponseServerError(render_to_string('500.html', request=request))

def bad_request(request, *args, **kwargs):
    return HttpResponseBadRequest(render_to_string('400.html', request=request))

# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# def request_test(request):
#     response=HttpResponse()
#     try:
#         method=request.method
#         http_host=request.META['HTTP_HOST']
#         http_user_agent=request.META['HTTP_USER_AGENT']
#         remote_addr=request.META['REMOTE_ADDR']
#         response.write('[method]:%s<br>' % (method))
#         response.write('[http_host]:%s<br>' % (http_host))
#         response.write('[http_user_agent]:%s<br>' % (http_user_agent))
#         response.write('[remote_addr]:%s' % (remote_addr))
#         response['Cache-Control']='no-cache'
#         return response
#     except e:
#         return response.write('Error:%s' % e)
#
# def redirect(request):
#     return HttpResponseRedirect("/")


# 首頁
def index_view(request):
    now = datetime.now()
    return render(request, 'index.html', locals())

# 文本摘要實作一
def summary_1(request):
    # 取得輸入之關鍵字、頁數，開始爬蟲
    keyword = request.POST['keyword']
    num_of_news = request.POST['num_of_news']

    print("keyword: ", keyword, "\n""views: num_of_news: ", num_of_news)
    df_news = cn.Crawl_BBC(keyword, int(num_of_news)).make_dataframe()

    # 取得爬蟲資料後，做LDA模型分類
    lda = ltm.LDAclass(df_news, chinese_only=True)  # 只做 jieba 分詞
    lda.lda_class(n_topics=3, max_iter=100, evaluate_every=10, verbose=1)  # 做 LDA
    df_lda = lda.dataframe

    # 取得LDA結果，做抽取式摘要
    summary = ds.Drawable_summary(df_lda, 'text_rank', 50, '3', keyword).make_summary()

    return render(request, 'summarization.html', locals())