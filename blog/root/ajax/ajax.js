let basic_url = '/api/articles'
function ajax_load(url=basic_url){

    $.ajax({
        type:'GET',
        url: url,
        success: function load_page(data){
            let container = $('.alert:first').clone();
            let tag = $('.tag_link:first').clone();
            container.find('.tagsdiv').empty();
            $('.articlelist').empty();

            if (data.next != null){
                $('.next').attr('href', data.next).css('display', '')
            }else{
                $('.next').css('display', 'none')
            };

            if (data.previous != null){
                $('.prev').attr('href', data.previous).css('display', '')
            }else{
                $('.prev').css('display', 'none')
            };

            for (idx in data.results) {
                current_data = data.results[idx];
                let clone = container.clone().css('display', '');
                clone.find('.title').text(current_data.title);

                for (idx in current_data.tags){
                    item = current_data.tags[idx];
                    let new_tag = tag.clone();
                    new_tag.find('.badge').text(item.name);
                    tag_url= basic_url + '?tags=' + item.name;
                    new_tag.attr('href', tag_url);
                    new_tag.appendTo(clone.find('.tagsdiv'));
                };

                clone.find('.content').text(current_data.content);
                author_url = basic_url + '?author=' + current_data.author.username;
                clone.find('.author').text(current_data.author.username);
                clone.find('.author').attr('href', author_url)
                clone.find('.postdate').text(current_data.post_date);
                clone.appendTo('.articlelist');
            }

        }

    })

}

$('#listbutton').click(function(){
    ajax_load()
});
$(document).on('click','.next, .prev, .author, .tag_link', function(event){
    event.preventDefault();
    let page_url = $(this).attr('href');
    ajax_load(page_url);
});
