function ajax_load(url='/api/articles'){

    $.ajax({
        type:'GET',
        url: url,
        success: function load_page(data){
            let container = $('.alert:first').clone();
            let tag = $('.tag_link:first').clone();
            container.find('.tagsdiv').empty();
            $('.articlelist').empty();

            if (data.next != false){
                $('.next').attr('href', data.next).css('display', '')
            };
            if (data.previous != false){
                $('.prev').attr('href', data.previous).css('display', '')
            };

            for (idx in data.results) {
                current_data = data.results[idx];
                let clone = container.clone().css('display', '');
                clone.find('.title').text(current_data.title);

                for (idx in current_data.tags){
                    item = current_data.tags[idx];
                    let new_tag = tag.clone();
                    new_tag.find('.badge').text(item.name);
                    tag_url='posts/tags/' + item.name;
                    new_tag.attr('href', tag_url);
                    new_tag.appendTo(clone.find('.tagsdiv'));
                };

                clone.find('.content').text(current_data.content);
                author_url = '/posts/' + current_data.author.username;
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
})

$('.next, .prev').click(function(event){
    event.preventDefault();
    let page_url = $(this).attr('href');
    ajax_load(page_url);
})