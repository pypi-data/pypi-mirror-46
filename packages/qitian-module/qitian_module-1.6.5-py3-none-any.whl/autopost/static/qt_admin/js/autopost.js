(function ($) {
    let list_div = $('<div id="list_div" style="display: none"><div class="col-sm-1"></div><div class="col-sm-10"> <ul id="list_div_ul"></ul></div></div>');
    let detail_div = $('<div id="detail_div" style="display: none"><h1 id="preview_title" style="text-align: center;"></h1><div class="row"><div class="col-lg-1"></div><div class="col-lg-10" id="preview_content"></div> </div></div>');

    // 添加文章详情预览
    let detail_url_input = $('<div class="form-row grp-row grp-cells-1 detail_preview_url ">' +
        '<div class="field-box l-2c-fluid l-d-4">' +
        '<div class="c-1"><label for="id_content_selector">测试URL</label></div>' +
        '<div class="c-2"><input type="text" name="detail_preview_url" value="" class="vTextField" id="id_detail_preview_url"></div></div></div>');
    // 添加文档参考
    let css_referer = $('<a href="http://www.runoob.com/cssref/css-selectors.html" target=_blank>CSS选择器</a>');
    $(document).ready(function () {
        $('.preview_title_btn').after(list_div);
        $('.preview_detail_btn').before(detail_url_input);
        $('.preview_detail_btn').after(detail_div);
        $('#id_list_selector').after(css_referer);
    });
})(django.jQuery);


function title_preview() {
    let list_pattern = $('#id_list_selector').val();
    let url = $('#id_url').val();
    if (list_pattern == '' || url == '') {
        alert('请输入采集URL和采集规则.');
        return false;
    }
    $.get('/autopost/preview_list/?page_url=' + encodeURIComponent(url) + '&pattern=' + list_pattern, function (data) {
        if (data['code'] != 200) {
            return alert('数据错误,请检查代码.');
        }
        $('#list_div_ul').empty();
        $.each(data['data'], function (key, item) {
            let link_item = $('<li><a href="' + item.url + '" target="_blank">' + item.title + '</a> </li>');
            $('#list_div_ul').append(link_item);
        });
        $('#list_div').show('slow');
    });
}

function detail_preview() {
    let detail_url = $('#id_detail_preview_url').val();
    let title_pattern = $('#id_title_selector').val();
    let content_pattern = $('#id_content_selector').val();
    let exclude_pattern = $('#id_content_except').val();
    let title_replace = $('#id_title_replace').val();
    let content_replace = $('#id_content_replace').val();
    let lazy_photo = $('#id_lazy_photo').val();
    $.get('/autopost/preview_detail/', {
        'detail_url': encodeURIComponent(detail_url),
        'title_pattern': encodeURIComponent(title_pattern),
        'content_pattern': encodeURIComponent(content_pattern),
        'exclude_pattern': encodeURIComponent(exclude_pattern),
        'title_replace': encodeURIComponent(title_replace),
        'content_replace': encodeURIComponent(content_replace),
        'lazy_photo': encodeURIComponent(lazy_photo),
    }, function (data) {
        if(data.code!=200){
            return alert('数据错误,请检查代码.');
        }
        $('#preview_title').text(data['data'].title);
        $('#preview_content').html(data['data'].content);
        $('#detail_div').show('slow');
    });
}

function crawl_news(task_id) {
    (function ($) {
        $.get('/autopost/craw_news/' + task_id + '/', function (data) {
            alert(data.message);
        });
    })(django.jQuery);
}

function copy_task(task_id) {
    (function ($) {
        $.get('/autopost/copy_task/' + task_id + '/', function (data) {
            window.location.href = '/admin/autopost/autotask/'+data['data']['id']+'/change/'
        });
    })(django.jQuery);
}